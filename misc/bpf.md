
# BPF (eBPF / bpftools / BCC)

very-very-very greate references
- [eBPF introduction (ja)](https://qiita.com/sg-matsumoto/items/8194320db32d4d8f7a16)
- [persistent eBPF map object with bcc (ja)](http://yunazuno.hatenablog.com/entry/2017/04/09/112939)

## Setup

install tool-cahin
```
sudo apt-get install -y \
    bpfcc-tools python3-bpfcc \
    linux-headers-`uname -r`
```

## BCC

hook clone
```
#!/usr/bin/python3
from bcc import BPF

text="""
int kprobe__sys_clone(void *ctx) {
  bpf_trace_printk("Hello, World!\\n");
  return 0;
}
"""
BPF(text=text).trace_print()
```

## bpftools

build and install bpftool (kernel-version: 4.18.0)
```
sudo apt install \
  linux-image-4.18.0-13-generic \
	linux-modules-4.18.0-13-generic \
	linux-modules-extra-4.18.0-13-generic \
	linux-tools-4.18.0-13-generic \
	build-essential binutils-dev libelf-dev

export WORK=~/Desktop/work
cp /usr/src/linux-source-4.18.0.tar.bz2 $WORK && cd $_
tar xpf linux-source-4.18.0.tar.bz2
make -C linux-source-4.18.0/tools/bpf/bpftool
sudo cp linux-source-4.18.0/tools/bpf/bpftool/bpftool /usr/local/bin

bpftool --version
```

check bpf program
```
sudo bpftool prog
...(snip)
14: kprobe  name sys_clone  tag c514db71faba4034  gpl
        loaded_at 2019-07-08T15:53:10+0000  uid 0
        xlated 120B  jited 115B  memlock 4096B
...(snip)

sudo bpftool prog dump xlated id 14
   0: (b7) r1 = 2593
   1: (6b) *(u16 *)(r10 -4) = r1
   2: (b7) r1 = 1684828783
   3: (63) *(u32 *)(r10 -8) = r1
   4: (18) r1 = 0x57202c6f6c6c6548
   6: (7b) *(u64 *)(r10 -16) = r1
   7: (b7) r1 = 0
   8: (73) *(u8 *)(r10 -2) = r1
   9: (bf) r1 = r10
  10: (07) r1 += -16
  11: (b7) r2 = 15
  12: (85) call bpf_trace_printk#-47744
  13: (b7) r0 = 0
  14: (95) exit

sudo bpftool map
2: lpm_trie  flags 0x1
        key 8B  value 8B  max_entries 1  memlock 4096B
3: lpm_trie  flags 0x1
        key 20B  value 8B  max_entries 1  memlock 4096B
4: lpm_trie  flags 0x1
        key 8B  value 8B  max_entries 1  memlock 4096B
5: lpm_trie  flags 0x1
        key 20B  value 8B  max_entries 1  memlock 4096B
6: lpm_trie  flags 0x1
        key 8B  value 8B  max_entries 1  memlock 4096B
7: lpm_trie  flags 0x1
        key 20B  value 8B  max_entries 1  memlock 4096B
```

## eBPF-MAP Array

monitoring user process's call info about malloc / free.

```
#!/usr/bin/python
import sys
from bcc import BPF
from time import sleep

if len(sys.argv) < 2:
  print("Usage: {} <PID>".format(sys.argv[0]))
  exit()

bpf_text="""
#include <uapi/linux/ptrace.h>
#define MALLOC 0
#define FREE 1
BPF_ARRAY(count, u64, 2);

void trace_malloc(struct pt_regs *ctx) {
  u32 pid = bpf_get_current_pid_tgid();
  if (pid != PID)
    return;
  bpf_trace_printk("good\\n");
  count.increment(MALLOC);
}

void trace_free(struct pt_regs *ctx) {
  u32 pid = bpf_get_current_pid_tgid();
  if (pid != PID)
    return;
  bpf_trace_printk("bad\\n");
  count.increment(FREE);
}
"""

bpf_text = bpf_text.replace("PID", sys.argv[1])
b = BPF(text=bpf_text)
print("comple ...done")
b.attach_uprobe(
    name = "c",
    sym="malloc",
    fn_name="trace_malloc")
b.attach_uprobe(
    name = "c",
    sym="free",
    fn_name="trace_free")

while True:
  malloc = b["count"][0].value
  free = b["count"][1].value
  print("{} / {}".format(malloc, free))
  sleep(1)
```

```
sudo ./main.py 9786
compile ...done
...(snip)
7 / 0
10 / 0
14 / 0
17 / 0
20 / 0
...(snip)
```

we can also check table w/ bpftool
```
sudo bpftool map
2: lpm_trie  flags 0x1
        key 8B  value 8B  max_entries 1  memlock 4096B
3: lpm_trie  flags 0x1
        key 20B  value 8B  max_entries 1  memlock 4096B
4: lpm_trie  flags 0x1
        key 8B  value 8B  max_entries 1  memlock 4096B
5: lpm_trie  flags 0x1
        key 20B  value 8B  max_entries 1  memlock 4096B
6: lpm_trie  flags 0x1
        key 8B  value 8B  max_entries 1  memlock 4096B
7: lpm_trie  flags 0x1
        key 20B  value 8B  max_entries 1  memlock 4096B
46: array  name count  flags 0x0
        key 4B  value 8B  max_entries 2  memlock 4096B

sudo bpftool map dump id 46
key: 00 00 00 00  value: 7d 00 00 00 00 00 00 00
key: 01 00 00 00  value: 00 00 00 00 00 00 00 00
Found 2 elements
```

we can also check table via another BCC script
```
#!/usr/bin/python
from bcc import libbcc, table
import ctypes
import sys

class PinnedArray(table.Array):
  def __init__(self, map_path, keytype, leaftype, max_entries):
    map_fd = libbcc.lib.bpf_obj_get(ctypes.c_char_p(map_path))
    if map_fd < 0:
      raise ValueError("Failed to open eBPF map")
    self.map_fd = map_fd
    self.Key = keytype
    self.Leaf = leaftype
    self.max_entries = max_entries

counter = PinnedArray(
    map_path = "/sys/fs/bpf/count",
    keytype = ctypes.c_uint32,
    leaftype = ctypes.c_long,
    max_entries = 1)
print(counter[0].value)
```

## TO-READ
 
- XDPのサンプルコードを含め, 基本的なHandsonを含んでいる
  https://rheb.hatenablog.com/entry/xdp1
  https://rheb.hatenablog.com/entry/xdp2
