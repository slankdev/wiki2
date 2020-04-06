
# QEMU

## QemuコマンドでVMを立てる時にシンプルにNICを生やす方法

### part1 超素朴に全部手作業でやる

最初にこの方法でやれば全て理解できるしこれが一番理解しやすい.

```
#!/bin/sh

sudo qemu-system-x86_64 \
        -enable-kvm \
        -m 16000 \
        -boot order=d \
        -cdrom ./cdrom.iso \
        ./disk.qcow2 \
        -vnc :20,password -monitor stdio
```

ホスト側からVM起動
```
HOST$ sudo qemu-system-x86_64     \
		-m 2048 -hda vm0.img          \
		-net nic -net tap,ifname=vtap0 \
		-vnc :5 -monitor stdio
(qemu)
```

ホスト側に新たに``vtap0``が増えるのを確認する
```
HOST$ ip a
...
67: vtap0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 1000
    link/ether 5a:95:ad:15:13:99 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::5895:adff:fe15:1399/64 scope link
       valid_lft forever preferred_lft forever
...
```

VM側ではこうなった
```
VM$
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens3: <BROADCAST,MULTICAST,PROMISC,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 52:54:00:12:34:56 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::5054:ff:fe12:3456/64 scope link
       valid_lft forever preferred_lft forever
```

VM側とHOST側にIPアドレスを割り当てる

```
VM$ sudo ip addr add 10.10.0.1/24 dev ens3
HOST$ sudo ip addr add 10.10.0.2/24 dev vtap0
```

するとpingが通るようになる

```
HOST$ ping 10.10.0.1
PING 10.10.0.1 (10.10.0.1) 56(84) bytes of data.
64 bytes from 10.10.0.1: icmp_seq=1 ttl=64 time=10.8 ms
64 bytes from 10.10.0.1: icmp_seq=2 ttl=64 time=0.277 ms
...

VM$ ping 10.10.0.2
PING 10.10.0.2 (10.10.0.2) 56(84) bytes of data.
64 bytes from 10.10.0.2: icmp_seq=1 ttl=64 time=1.37 ms
64 bytes from 10.10.0.2: icmp_seq=2 ttl=64 time=0.267 ms
...
```

変に紛らわしいことして浪費するよりこれの方がいいかもしれない.

### port2 ifupスクリプトを指定する

ググると``script=ifup.sh``みたいなのを指定する方法があって, 理解しにくい.
しかしpart1を理解した人からするととてもシンプルである.

**scriptオプションで指定したスクリプトはvmを起動したあとにifnameで指定した
内容を引数として渡して実行されるだけ**なので, 今回はtap0にipアドレスを
設定するスクリプトを書いた. 以下のようにすると, ホスト側のアドレス設定も
自動でやってくれる.


```
HOST$ cat ifup.sh
#!/bin/sh
/sbin/ip addr add 10.10.0.2/24 dev $1
/sbin/ip link set $1 up

HOST$ chmod -x ifup.sh
HOST$ sudo qemu-system-x86_64 \
		-m 2048 -hda vm0.img      \
		-net nic -net tap,ifname=vtap0,script=ifup.sh \
		-vnc :5 -monitor stdio
(qemu)
```

## DPDK

```
#!/bin/sh

sudo qemu-system-x86_64 \
  -cpu host -enable-kvm -m 1024M -hda vm0.img \
  \
  -net nic -net tap,ifname=vtap0,script=/etc/qemu-ifup-add-bridge.sh \
  -chardev socket,id=chr0,path=/tmp/sock0 \
  -netdev vhost-user,id=net0,chardev=chr0,vhostforce,queues=1 \
  -device virtio-net-pci,netdev=net0 \
  -chardev socket,id=chr1,path=/tmp/sock1 \
  -netdev vhost-user,id=net1,chardev=chr1,vhostforce,queues=1 \
  -device virtio-net-pci,netdev=net1 \
  \
  -vnc :5,password -monitor stdio
```

### PCI-passthrough / SR-IOV

unbind ixgbe and bind to vfio
```
# vendor=`cat /sys/bus/pci/devices/0000:05:00.0/vendor`
# device=`cat /sys/bus/pci/devices/0000:05:00.0/device`
# echo 0000:05:00.0 > /sys/bus/pci/devices/0000:05:00.0/driver/unbind
# echo $vendor $device > /sys/bus/pci/drivers/vfio-pci/new_id

// 以下と同じだった
# dpdk_nic_bind -b vfio-pci 0000:05:00.0
```

create VF
```
# cat /sys/class/net/ens20f0/device/sriov_numvfs
0
# echo 3 > /sys/class/net/ens20f0/device/sriov_numvfs
# cat /sys/class/net/ens20f0/device/sriov_numvfs
3
```

```
$ cat ifdown.sh
#!/bin/sh
ovs-vsctl del-port br-ex $1
$ cat ifup.sh
#!/bin/sh
ip link set $1 up
ovs-vsctl add-port br-ex $1
$ cat start_pktgen.sh
#!/bin/sh
IMAGE=./pktgen.img
qemu-system-x86_64 \
	-cpu host -enable-kvm \
	-smp 4 -m 8000 -hda $IMAGE \
	-net nic,macaddr=52:54:00:22:22:22 \
	-net tap,script=ifup.sh,downscript=ifdown.sh \
	-vnc :1,password -monitor stdio \
  -device vfio-pci,host=85:00.0 \
  -device vfio-pci,host=85:00.1
$ cat start_testpmd.sh
#!/bin/sh
IMAGE=./testpmd.img
qemu-system-x86_64 \
	-cpu host -enable-kvm \
	-smp 8 -m 8000 -hda $IMAGE \
	-net nic,macaddr=52:54:00:11:11:11 \
	-net tap,script=ifup.sh,downscript=ifdown.sh \
	-vnc :0,password -monitor stdio \
  -device vfio-pci,host=05:10.0 \
  -device vfio-pci,host=05:10.1
```

```
#!/bin/sh

IMAGE=bionic-server-cloudimg-amd64.img

qemu-system-x86_64 \
  -cpu host -enable-kvm \
  -smp 4 -m 8000 -hda $IMAGE  \
  -net nic -net tap,ifname=vtap10 \
  -vnc :4,password -monitor stdio
```

```
broadwell1:~/new:) cat startvm_from_disk.sh
#!/bin/sh

IMAGE=./disk.qcow2

qemu-system-x86_64 \
  -cpu host -enable-kvm \
  -smp 8 -m 16000 -hda $IMAGE  \
  -net nic -net tap,ifname=vtap10 \
  -vnc :20,password -monitor stdio
broadwell1:~/new:) cat startvm_from_iso.sh
#!/bin/sh

sudo qemu-system-x86_64 \
	-enable-kvm \
	-m 16000 \
	-boot order=d \
	-cdrom ./kamuee.iso \
	./disk.qcow2 \
	-vnc :20,password -monitor stdio
	# -nographic
broadwell1:~/new:)
```

```
qemu-system-x86_64 \
-enable-kvm -m 8192 -smp cores=4,threads=0,sockets=1 -cpu host \
-drive file="ubuntu-16.04-server-cloudimg-amd64-disk1.img",if=virtio,aio=threads \
-drive file="seed.img",if=virtio,aio=threads \
-nographic -object memory-backend-file,id=mem,size=8192M,mem-path=/dev/hugepages,share=on \ -numa node,memdev=mem \
-mem-prealloc \
-chardev socket,id=char1,path=/var/run/vpp/sock1.sock \
-netdev type=vhost-user,id=net1,chardev=char1,vhostforce \
-device virtio-net-pci,netdev=net1,mac=00:00:00:00:00:01,csum=off,gso=off,guest_tso4=off,guest_tso6=off,guest_ecn=off,mrg_rxbuf=off
```

