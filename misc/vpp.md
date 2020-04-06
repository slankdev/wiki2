
# VPP

## Contributing

- https://wiki.fd.io/view/VPP/Pulling,_Building,_Running,_Hacking_and_Pushing_VPP_Code#Pushing

pull and edit source
```
sudo apt install -y git-review
sudo yum install -y git-review
git clone https://gerrit.fd.io/r/vpp vpp && cd $_
git review -s
git config user.name "Hiroki Shirokura"
git config user.email slank.dev@gmail.com
git ls-remote | grep 21357
5e634596504e63b1b62a07191d13519290c937bb        refs/changes/57/21357/1
0a7d3dc977aa0717219290bd9d53e025ca45abf0        refs/changes/57/21357/2
2d64f780cc9a65800882fafa95838e5f02f25014        refs/changes/57/21357/3
47848805d40165d1d06149595d7951e2ceea26e8        refs/changes/57/21357/4
c68aeb981e5b616014d5c0f0a9bdbedea281918c        refs/changes/57/21357/5

git pull origin refs/changes/57/21357/5
git rebase
vim <...>
```

edit source and commit and push for review
```
vim <...>
git add .
git commit --amend
git review
```

## CLIs and Basic Configuration

check interface
```
lshw -class network -businfo
```

build and install on Ubuntu
```
git clone https://gerrit.fd.io/r/vpp vpp && cd $_
```

if you need to use Mlx-NIC.
```
vim build/external/packages/dpdk.mk
-  DPDK_MLX4_PMD                ?= n
-  DPDK_MLX5_PMD                ?= n
+  DPDK_MLX4_PMD                ?= y
+  DPDK_MLX5_PMD                ?= y
```

build procedure
```
make install-dep
make bootstrap
make build
make pkg-deb-debug
```

minimal config
```
unix {
        nodaemon
        interactive
        cli-listen /run/vpp/cli.sock
        cli-no-banner
        exec /etc/vpp/exec
}
```

```
unix {
  nodaemon
  log /var/log/vpp/vpp.log
  full-coredump
  cli-listen /run/vpp/cli.sock
  exec /etc/vpp/exec
  gid vpp
}

api-segment {
  gid vpp
}

dpdk {
        dev 0000:00:07.0
}
```

cli
```
set interface state GigabitEthernet0/7/0 up
set interface state GigabitEthernet0/7/1 up
set interface state GigabitEthernet0/7/2 up
set interface state GigabitEthernet0/7/3 up

create sub-interface GigabitEthernet0/7/0 100
create sub-interface GigabitEthernet0/7/1 101
create sub-interface GigabitEthernet0/7/2 102
create sub-interface GigabitEthernet0/7/3 103

set interface state GigabitEthernet0/7/0.100 up
set interface state GigabitEthernet0/7/1.101 up
set interface state GigabitEthernet0/7/2.102 up
set interface state GigabitEthernet0/7/3.103 up

set interface ip address GigabitEthernet0/7/0.100 10.100.0.1/24
set interface ip address GigabitEthernet0/7/1.101 10.101.0.1/24
set interface ip address GigabitEthernet0/7/2.102 10.102.0.1/24
set interface ip address GigabitEthernet0/7/3.103 10.103.0.1/24
```

show runtime statistics (node's info)
```
DBGvpp# sh run
Time 2666.4, average vectors/node 1.00, last 128 main loops 0.00 per node 0.00
  vector rates in 3.7504e-4, out 3.7504e-4, drop 3.7504e-4, punt 0.0000e0
             Name                 State         Calls          Vectors        Suspends         Clocks       Vectors/Call
GigabitEthernet0/7/0-output      active                  1               1               0          2.02e4            1.00
GigabitEthernet0/7/0-tx          active                  1               1               0          4.39e4            1.00
acl-plugin-fa-cleaner-process  event wait                0               0               1          1.59e4            0.00
admin-up-down-process          event wait                0               0               1          8.99e3            0.00
api-rx-from-ring                any wait                 0               0             135          1.40e5            0.00
arp-input                        active                  1               1               0          6.65e3            1.00
arp-reply                        active                  1               1               0          5.18e5            1.00
avf-process                    event wait                0               0               1          1.50e4            0.00
bond-process                   event wait                0               0               1          1.32e4            0.00
dpdk-input                       polling        5098857376               1               0         3.59e12            0.00
dpdk-ipsec-process                done                   1               0               0          1.61e5            0.00
dpdk-process                    any wait                 0               0             889          6.72e6            0.00
drop                             active                  1               1               0          1.14e4            1.00
error-drop                       active                  1               1               0          1.32e4            1.00
ethernet-input                   active                  1               1               0          2.04e4            1.00
fib-walk                        any wait                 0               0            1334          6.45e3            0.00
...

DBGvpp#
```

## vat

```
vat# help
…(snip)…
acl_add_replace
acl_add_replace_from_file
acl_del
acl_dump
acl_interface_add_del
acl_interface_etype_whitelist_dump
acl_interface_list_dump
acl_interface_set_acl_list
acl_interface_set_etype_whitelist
acl_plugin_get_conn_table_max_entries
acl_plugin_get_version
…(snip)…

vat# acl_add_replace 0 ipv4 permit src 10.100.0.0/24 dst 10.101.0.0/24, ipv4 permit src 10.101.0.0/24 dst 10.100.0.0/24, ipv4 deny
vl_api_acl_add_replace_reply_t_handler:108: ACL index: 0

vat# exec show acl-plugin acl
acl-index 0 count 1 tag {}
          0: ipv4 permit src 10.100.0.0/24 dst 10.101.0.0/24 proto 0 sport 0-65535 dport 0-65535
          1: ipv4 permit src 10.101.0.0/24 dst 10.100.0.0/24 proto 0 sport 0-65535 dport 0-65535
          2: ipv4 deny src 0.0.0.0/0 dst 0.0.0.0/0 proto 0 sport 0-65535 dport 0-65535

vat# acl_del 0
vat# exec show acl-plugin acl

vat# acl_interface_set_acl_list host-veth0-host input 0 output 0
vat# acl_interface_set_acl_list host-veth1-host input 0 output 0
vat# exec sh acl-plugin int
sw_if_index 0:
sw_if_index 1:
  input acl(s): 0
  output acl(s): 0
sw_if_index 2:
  input acl(s): 0
  output acl(s): 0

vat# acl_interface_add_del sw_if_index 1 del input acl 0
vat# acl_interface_add_del sw_if_index 1 del output acl 0
vat# exec sh acl-plugin int
sw_if_index 0:
sw_if_index 1:
sw_if_index 2:
  input acl(s): 0
  output acl(s): 0
```

## packet tracer

startup.conf
```
api-trace { on }
```

```
vpp# trace add dpdk-input 1
vpp# clear trace
```

```
vpp# show trace
------------------- Start of thread 0 vpp_main -------------------
Packet 1

00:48:23:581536: dpdk-input
  GigabitEthernet0/7/0 rx queue 0
  buffer 0x9b6b4: current data 0, length 98, buffer-pool 0, ref-count 1, totlen-nifb 0, trace 0x0
                  ext-hdr-valid
                  l4-cksum-computed l4-cksum-correct
  PKT MBUF: port 0, nb_segs 1, pkt_len 98
    buf_len 2176, data_len 98, ol_flags 0x0, data_off 128, phys_addr 0x87cdad80
    packet_type 0x0 l2_len 0 l3_len 0 outer_l2_len 0 outer_l3_len 0
    rss 0x0 fdir.hi 0x0 fdir.lo 0x0
  IP4: 9a:3e:4a:3c:6c:f4 -> 52:54:00:c4:2b:b1
  ICMP: 10.100.0.2 -> 10.100.0.1
    tos 0x00, ttl 64, length 84, checksum 0xa4d8
    fragment id 0x8106, flags DONT_FRAGMENT
  ICMP echo_request checksum 0xb7ab
00:48:23:581914: ethernet-input
  frame: flags 0x1, hw-if-index 1, sw-if-index 1
  IP4: 9a:3e:4a:3c:6c:f4 -> 52:54:00:c4:2b:b1
00:48:23:581968: ip4-input
  ICMP: 10.100.0.2 -> 10.100.0.1
    tos 0x00, ttl 64, length 84, checksum 0xa4d8
    fragment id 0x8106, flags DONT_FRAGMENT
  ICMP echo_request checksum 0xb7ab
00:48:23:582067: ip4-lookup
  fib 0 dpo-idx 5 flow hash: 0x00000000
  ICMP: 10.100.0.2 -> 10.100.0.1
    tos 0x00, ttl 64, length 84, checksum 0xa4d8
    fragment id 0x8106, flags DONT_FRAGMENT
  ICMP echo_request checksum 0xb7ab
00:48:23:582136: ip4-local
    ICMP: 10.100.0.2 -> 10.100.0.1
      tos 0x00, ttl 64, length 84, checksum 0xa4d8
      fragment id 0x8106, flags DONT_FRAGMENT
    ICMP echo_request checksum 0xb7ab
00:48:23:582148: ip4-icmp-input
  ICMP: 10.100.0.2 -> 10.100.0.1
    tos 0x00, ttl 64, length 84, checksum 0xa4d8
    fragment id 0x8106, flags DONT_FRAGMENT
  ICMP echo_request checksum 0xb7ab
00:48:23:582174: ip4-icmp-echo-request
  ICMP: 10.100.0.2 -> 10.100.0.1
    tos 0x00, ttl 64, length 84, checksum 0xa4d8
    fragment id 0x8106, flags DONT_FRAGMENT
  ICMP echo_request checksum 0xb7ab
00:48:23:582218: ip4-load-balance
  fib 0 dpo-idx 2 flow hash: 0x00000000
  ICMP: 10.100.0.1 -> 10.100.0.2
    tos 0x00, ttl 64, length 84, checksum 0xf625
    fragment id 0x2fb9, flags DONT_FRAGMENT
  ICMP echo_reply checksum 0xbfab
00:48:23:582225: ip4-rewrite
  tx_sw_if_index 1 dpo-idx 2 : ipv4 via 10.100.0.2 GigabitEthernet0/7/0: mtu:9000 9a3e4a3c6cf4525400c42bb10800 flow hash: 0x00000000
  00000000: 9a3e4a3c6cf4525400c42bb10800450000542fb940004001f6250a6400010a64
  00000020: 00020000bfab00640001a504195d00000000b6ba0c00000000001011
00:48:23:582244: GigabitEthernet0/7/0-output
  GigabitEthernet0/7/0 l4-cksum-computed l4-cksum-correct l2_hdr_offset_valid l3_hdr_offset_valid
  IP4: 52:54:00:c4:2b:b1 -> 9a:3e:4a:3c:6c:f4
  ICMP: 10.100.0.1 -> 10.100.0.2
    tos 0x00, ttl 64, length 84, checksum 0xf625
    fragment id 0x2fb9, flags DONT_FRAGMENT
  ICMP echo_reply checksum 0xbfab
00:48:23:582290: GigabitEthernet0/7/0-tx
  GigabitEthernet0/7/0 tx queue 0
  buffer 0x9b6b4: current data 0, length 98, buffer-pool 0, ref-count 1, totlen-nifb 0, trace 0x0
                  ext-hdr-valid
                  l4-cksum-computed l4-cksum-correct l2-hdr-offset 0 l3-hdr-offset 14
  PKT MBUF: port 0, nb_segs 1, pkt_len 98
    buf_len 2176, data_len 98, ol_flags 0x0, data_off 128, phys_addr 0x87cdad80
    packet_type 0x0 l2_len 0 l3_len 0 outer_l2_len 0 outer_l3_len 0
    rss 0x0 fdir.hi 0x0 fdir.lo 0x0
  IP4: 52:54:00:c4:2b:b1 -> 9a:3e:4a:3c:6c:f4
  ICMP: 10.100.0.1 -> 10.100.0.2
    tos 0x00, ttl 64, length 84, checksum 0xf625
    fragment id 0x2fb9, flags DONT_FRAGMENT
  ICMP echo_reply checksum 0xbfab
```

tap-interface
```
create tap \
  [id <if-id>] \
  [hw-addr <mac-address>] \
  [rx-ring-size <size>] [tx-ring-size <size>] \
  [host-ns <netns>] [host-bridge <bridge-name>] \
  [host-ip4-addr <ip4addr/mask>] [host-ip4-gw <ip4-addr>] \
  [host-ip6-addr <ip6-addr>] [host-ip6-gw <ip6-addr>] \
  [host-if-name <name>] \
  [no-gso|gso]

create tap id 102 hw-addr 52:54:00:11:11:11 host-ns ns0 host-if-name peer0
```

l2 bridge configuration
```
ip netns add ns1
ip netns add ns2
ip netns exec ns1 ip link set lo up
ip netns exec ns2 ip link set lo up
vppctl create tap id 101 hw-addr 52:54:00:00:00:01 host-ns ns1 host-if-name peer1 host-ip4-addr 20.0.0.10/24
vppctl create tap id 102 hw-addr 52:54:00:00:00:02 host-ns ns2 host-if-name peer2 host-ip4-addr 20.0.0.20/24
vppctl set interface state tap101 up
vppctl set interface state tap102 up
vppctl set interface l2 bridge tap101 1
vppctl set interface l2 bridge tap102 1
ip netns exec ns2 ping 20.0.0.10 -c2
```

BVI(bridge-group virtual interface)
```
create loopback interace
set interface state loop0 up
set interface l2 bridge loop0 1 bvi
set interface ip address 20.0.0.254/24
```

check fib memory
```
DBGvpp# show fib memory
FIB memory
  Tables:
             SAFI              Number     Bytes
         IPv4 unicast             1     33619968
         IPv6 unicast             1      1049216
             MPLS                 0         0
        IPv4 multicast            1       1167
        IPv6 multicast            1      525312
  Nodes:
             Name               Size  in-use /allocated   totals
             Entry               72     17   /    17      1224/1224
         Entry Source            40     17   /    17      680/680
     Entry Path-Extensions       76      2   /    2       152/152
        multicast-Entry         192      6   /    6       1152/1152
           Path-list             40     21   /    21      840/840
           uRPF-list             16     21   /    21      336/336
             Path                72     21   /    21      1512/1512
      Node-list elements         20     29   /    29      580/580
        Node-list heads          8      29   /    29      232/232
```

## VPP's Debian packages deep dive

Build system on VPP provide us some-set of distribution-package files. (ex. vpp_19.08-rc0_*.deb, vpp-dev*.deb)
THat includes some specific files on each package. Following shows the specification of Debian package.

- vpp_<version>.deb
	- vpp binary
	- vpp.service
- vpp-dbg_<version>.deb
- vpp-dev_<version>.deb
- vpp-api-python_<version>.deb
- vpp-plugin-core_<version>.deb
	- pppoe_plugin.so, api.json
	- igmp_plugin.so, api.json
	- ikev2_plugin.so, api.json
	- ila_plugin.so, api.json
	- ioam_plugin.so, api.json
	- ixge_plugin.so, api.json
	- l2e_plugin.so, api.json
	- l3xc_plugin.so, api.json
	- lacp_plugin.so, api.json
	- etc...
- vpp-plugin-dpdk_<version>.deb
	- dpdk_plugin.so, api.json
- python3-vpp-api_<version>.deb
- libvppinfra-dev_<version>.deb
- libvppinfra_<version>.deb

## Efficient Build

```
vm:~/git/vpp.gerrit.org [work] :) gd build-data src/CMakeLists.txt
diff --git a/build-data/packages/vpp.mk b/build-data/packages/vpp.mk
index ec6108345..77505de63 100644
--- a/build-data/packages/vpp.mk
+++ b/build-data/packages/vpp.mk
@@ -42,7 +42,7 @@ ifneq ($(wildcard /opt/rh/devtoolset-7/enable),)
 vpp_cmake_args += -DCMAKE_PROGRAM_PATH:PATH="/opt/rh/devtoolset-7/root/bin"
 endif

-vpp_configure_depend += external-install
+#vpp_configure_depend += external-install
 vpp_configure = \
   cd $(PACKAGE_BUILD_DIR) && \
   $(CMAKE) -G Ninja $(vpp_cmake_args) $(call find_source_fn,$(PACKAGE_SOURCE))
diff --git a/src/CMakeLists.txt b/src/CMakeLists.txt
index 248d7b8d3..e8b2ffcc5 100644
--- a/src/CMakeLists.txt
+++ b/src/CMakeLists.txt
@@ -96,7 +96,10 @@ include(cmake/plugin.cmake)
 if("${CMAKE_SYSTEM_NAME}" STREQUAL "Linux")
   find_package(OpenSSL REQUIRED)
   set(SUBDIRS
-    vppinfra svm vlib vlibmemory vlibapi vnet vpp vat vcl plugins
+               #vppinfra svm vlib vlibmemory vlibapi vnet vpp vat vcl plugins
+    #vpp-api tools/vppapigen tools/g2 tools/elftool tools/perftool cmake pkg
+    #tools/appimage
+    vppinfra svm vlib vlibmemory vlibapi vnet vpp vcl
     vpp-api tools/vppapigen tools/g2 tools/elftool tools/perftool cmake pkg
     tools/appimage
   )
```

## for VPP Developers

build
```
```

direct or gdb-execute
```
make run
make debug
```

```
vim build-data/platforms/vpp.mk
(snip)
    vpp_common_cflags = \ 
      -g \ 
      -DFORTIFY_SOURCE=2 \ 
      -fstack-protector \ 
-     -Wall \   <---- KORE JAMA while developing
-     -Werror \ <---- KORE JAMA while developing
      -fPIC \ 
      -fno-common
(snip)
```

how to make build speedy and partially

build without dpdk modules
```
root:~/vpp$ gd build/external/Makefile
diff --git a/build/external/Makefile b/build/external/Makefile
index d178f0d83..58a497179 100644
--- a/build/external/Makefile
+++ b/build/external/Makefile
@@ -34,21 +34,23 @@ CMAKE?=cmake
 endif

 include packages.mk
-include packages/nasm.mk
-include packages/ipsec-mb.mk
-include packages/quicly.mk
-include packages/dpdk.mk
-include packages/rdma-core.mk
+# include packages/nasm.mk
+# include packages/ipsec-mb.mk
+# include packages/quicly.mk
+# include packages/dpdk.mk
+# include packages/rdma-core.mk

 .PHONY: clean
 clean:
        @rm -rf $(B) $(I)

 .PHONY: install
-install: dpdk-install rdma-core-install quicly-install
+# install: dpdk-install rdma-core-install quicly-install
+install:

 .PHONY: config
-config: dpdk-config rdma-core-config
+# config: dpdk-config rdma-core-config
+config:

 ##############################################################################
 # .deb packaging
```

## build only my plugins

delete unnessesary plugins
```
cd vpp/src/plugins
rm <unnessesary-plugins>
ls
CMakeLists.txt  cplane_netdev@
```

```
git diff Makefile
diff --git a/Makefile b/Makefile
index 7f3c4295e..dbe036ddd 100644
--- a/Makefile
+++ b/Makefile
@@ -370,6 +370,11 @@ wipe: wipedist test-wipe $(BR)/.deps.ok
        $(call make,$(PLATFORM)_debug,$(addsuffix -wipe,$(TARGETS)))
        @find . -type f -name "*.api.json" ! -path "./test/*" -exec rm {} \;

+wipe_plugin_only: wipedist test-wipe $(BR)/.deps.ok
+       @find . -type f -name "*.api.json" ! -path "./test/*" -exec rm {} \;
+
+rebuild_plugin_only: wipe_plugin_only build
+
 rebuild: wipe build

```

## Running VPP on Docker container

using tinet
```
nodes:
  - name: R1
    image: slankdev/vpp:19.04
    interfaces:
      - { name: net0, type: direct, args: R2#net0 }
      - { name: net1, type: direct, args: R3#net0 }
  - name: R2
    image: slankdev/ubuntu:18.04
    interfaces:
      - { name: net0, type: direct, args: R1#net0 }
  - name: R3
    image: slankdev/ubuntu:18.04
    interfaces:
      - { name: net0, type: direct, args: R1#net1 }

node_configs:
  - name: R1
    cmds:
      - cmd: nohup vpp -c /etc/vpp/startup.conf &
      - cmd: vppctl create host-interface name net0
      - cmd: vppctl create host-interface name net1
      - cmd: vppctl set int state host-net0 up
      - cmd: vppctl set int state host-net1 up
      - cmd: vppctl set int ip addr host-net0 10.100.0.1/24
      - cmd: vppctl set int ip addr host-net1 10.101.0.1/24
  - name: R2
    cmds:
      - cmd: ip addr add 10.100.0.2/24 dev net0
      - cmd: ip route add default via 10.100.0.1
  - name: R3
    cmds:
      - cmd: ip addr add 10.101.0.2/24 dev net0
      - cmd: ip route add default via 10.101.0.1
```

## How to install plugin on remote-machine

```
- /usr/include/vpp_plugins/myplugin/myplugin.api.h    // for API
- /usr/include/vpp_plugins/myplugin/myplugin.api.json // for API
- /usr/lib/vpp_plugins/myplugin_plugin.so
```

## Performance Tuning

check threading
```
DBGvpp# show threads
ID     Name                Type        LWP     Sched Policy (Priority)  lcore  Core   Socket State
0      vpp_main                        26330   other (0)                1      0      0

DBGvpp# show int rx-placement
Thread 0 (vpp_main):
  node virtio-input:
    tap0 queue 0 (polling)
    tap1 queue 0 (polling)
```

```
dpdk {
  dev default {
    num-rx-queues 1
  }
}

cpu {
  main-core 1
  corelist-workers 3-4,20-21
}
```

## Vhost-user

```
create vhost-user socket /var/lib/libvirt/qemu/vhost1.sock feature-mask 0x40400000 server
set interface state VirtualEthernet0/0/0 up
set interface ip addr VirtualEthernet0/0/0 10.0.0.1/24

create vhost-user socket /var/lib/libvirt/qemu/vhost2.sock feature-mask 0x40400000 server
set interface state VirtualEthernet0/0/1 up
set interface ip addr VirtualEthernet0/0/1 10.1.0.1/24
```

## How to skip external package download

```
curl http://fast.dpdk.org/rel/dpdk-19.02.tar.xz -o $HOME/vpp/build/external/downloads/dpdk-19.02.tar.xz
curl http://github.com/01org/intel-ipsec-mb/archive/v0.49.tar.gz -o $HOME/vpp/build/external/downloads/v0.49.tar.gz
```

## Enable MLX5 on Centos

```
sudo yum install -y git cpp gcc rpm-build openssl-devel libmnl-devel numactl-devel epel-release net-tools rdma-core-devel nasm
git clone https://github.com/FDio/vpp.git -b stable/1904 && cd vpp
make install-dep
make install-ext-deps DPDK_MLX5_PMD=y DPDK_MLX5_PMD_DLOPEN_DEPS=y
sudo cp /opt/vpp/external/x86_64/lib/librte_pmd_mlx5_glue.so* /usr/lib64/
make build-release
make pkg-rpm vpp_uses_dpdk_mlx5_pmd=yes DPDK_MLX5_PMD_DLOPEN_DEPS=y
cd build-root
sudo yum localinstall -y vpp-selinux*.rpm vpp-lib*.rpm vpp-19*.rpm vpp-plug*.rpm
```

## VRF

```
create tap id 0
create tap id 1
ip table add 100
set int ip table tap1 100

set int state tap0 up
set int state tap1 up
set int ip address tap0 2001::1/64
set int ip address tap1 10.0.0.1/24

ip route add A::/128 table 0 via 2001::2
ip route add B::/128 table 0 via 2001::2

sr policy add bsid cafe::1 next A:: next B:: fib-table 0
sr steer l3 10.1.0.0/24 via bsid cafe::1 fib-table 100
```

```
show ip fib table 100
```
