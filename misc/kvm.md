

# KVM


## Notice

It should be that depends file in following path because of file-permission.

```
 iso image    /var/lib/libvirt/images/
 vm  image    /var/lib/libvirt/images/
 xml file     /etc/libvirt/qemu/
```

## Install Package & start

```
sudo apt install libvirt-bin bridge-utils qemu-kvm virt-manager
```

```
yum install qemu-kvm libvirt libvirt-python libguestfs-tools virt-install
systemctl enable libvirtd
systemctl start libvirtd
```

Nested-VM
```
echo options kvm_intel nested=Y | sudo tee /etc/modprobe.d/kvm_intel.conf

vim /etc/modprobe.d/kvm_intel.conf
options kvm_intel nested=Y

modprobe -r kvm_intel
modprobe -r kvm
modprobe kvm_intel kvm_intel nested=Y
cat /sys/module/kvm_intel/parameters/nested
```

### Command Cheat

basic VM edit

```
$ virsh setmaxmem $dom 8G --config
$ virsh setmem $dom 8G --config
$ virsh set vcpus $dom 4 --config --maximum
$ virsh set vcpus $dom 4 --config
$ virsh dominfo $dom
```

Commands

```
# virsh autostart <domain>
# virsh autostart --disable <domain>
# virsh list
# virsh list --all
# virsh start <domain>
# virsh start <domname> --console
# virsh console <domname>
# virsh shutdown <domain>
# virsh destroy <domain>    //強制終了
# virsh reboot
# virsh suspend
# virsh resume
# virsh dominfo <domain>
# virsh vcpuinfo <domain>
# virsh vcpupin <domain> <guest_cid> <host_cid>
```

Delete VM
```
# virsh undefine <xml file>
```

Clone VM
```
# virt-clone --original <org-domain> --name <new-domain> --file <img-path>
# virt-clone --original vm0 --name vm1 --file /var/lib/libvirt/images/vm1.img
# virsh dumpxml <new-domain> | grep mac
# virsh start   <new-domain>
# virsh console <new-domain> // change hostname
```

```
#!/bin/sh

if [ "$#" -ne 2 ]; then
	echo "Usage: $0 <original> <target>"
	exit
fi
virt-clone --original $1 --name $2 --file /var/lib/libvirt/images/$2.img
virsh dumpxml $2 | grep mac
```

その他
```
# virsh uri
# virsh connect
# virsh connect qemu+ssh://192.168.0.1/system
# virsh connect qemu:///system --readonly
# virsh version
# virsh hostname
# virsh nodeinfo # hostspec
# virsh create  <xml file> # define and start
# virsh define  <xml file>
# virsh destroy <xml file> # stop
# virsh edit <domname>
# virsh vcpuinfo <domain>
# virsh schedinfo <domain>
# virsh iface-list
# virsh iface-dumpxml <interface>
# virsh net-list
# virsh net-list --all
# virsh net-edit <network>
# virsh net-start <network>
# virsh net-destroy <network>
# virsh net-define <domain>
# virsh net-undefine default
# virsh nodedev-list
# virsh nodedev-list --tree
```

Device attach/detach
```
# cat nic.xml
<interface type='network'>
  <mac address='52:54:00:ff:00:00'/>
  <source network='default'/>
  <model type='virtio'/>
  <address type='pci' domain='0x0000' bus='0x00' slot='0x03' function='0x0'/>
</interface>
# virsh attach-device --config vm0 nic.xml
# virsh detach-device --config vm0 nic.xml
```

## Create VM

VNC Install (using VNC)
```
#!/bin/sh

NAME=firm-builder
CDROM=./image.iso
VCPUS=16
DISKSZ=120 #GB
RAM=8000 #MB
DISKPATH=/var/lib/libvirt/images/$NAME.img

virt-install --connect=qemu:///system \
  --name=$NAME \
  --vcpus=$VCPUS \
  --ram=$RAM \
  --accelerate \
  --hvm \
  --disk path=$DISKPATH,size=$DISKSZ \
  --cdrom=$CDROM \
  --network network=default,model=virtio \
  --graphics vnc,port=5900,listen=0.0.0.0,keymap=us,password=hoge
```

Console Install (using Serial Only)
```
#!/bin/sh

NAME=slankdev01
CDROM=~/Downloads/ubuntu-16.04.2-server-amd64.iso
DISKSZ=16
DISKPATH=/var/lib/libvirt/images/$NAME

virt-install --connect=qemu:///system \
	--name $NAME \
	--vcpus 1 \
	--ram 512 \
	--accelerate \
	--hvm \
	--disk path=$DISKPATH,size=$DISKSZ \
	--cdrom $CDROM \
	--network network=default,model=virtio \
	--nographics --extra-args='console=tty0 console=ttyS0,115200n8'
```

## Delete VM

```
# virsh snapshot-delete <domain> <snapshot>
# virsh snapshot-delete <domain> <snapshot> --metadata
# virsh autostart --disable <domain>
# virsh undefine  <domain>
# virsh vol-delete --pool <pool> <device>
# virsh pool-destroy <pool>
```

## Enable Serial Connection

```
$ sudo systemctl enable serial-getty@ttyS0.service
$ sudo systemctl start  serial-getty@ttyS0.service
```

## Add Network Interface

```
# virsh shutdown <domain>
# virsh edit <domain>
...
+ <interface type='network'>
+   <source network='default'/>
+ 	<model type='virtio'/>
+ </interface>
...
# virsh start <domain>
```

## Modify VM

```
# virsh edit <domain>

 <domain>
     ...
~    <vcpu placement='static' cpuset="1-4,^3,6" current="1">2</vcpu>
	   ...
~	   <memory unit='KiB'>2097152</memory>
~	   <currentMemory unit='KiB'>2097152</currentMemory>
	   ...
+    <interface type='bridge'>
+        <source bridge='br1'/>
+        <model type='virtio'/>
+    </interface>
+    <interface type='bridge'>
+        <source bridge='br2'/>
+        <model type='virtio'/>
+    </interface>
     ...
 </domain>

# virsh define /etc/libvirt/qemu/<domain>.img
```

## Snapshot

check snapshot
```
# virsh snapshot-list <domain>
# virsh snapshot-create-as <dom> <sshot>
# virsh snapshot-revert --force <dom> <sshot>
```

create snapshot
```
# virsh snapshot-create-as <domain> <snapshot> <comment> --disk-only --atomic // external snapshot
# virsh snapshot-create-as <domain> <snapshot> <comment>                      // external snapshot
```

detele snapshot
```
# virsh snapshot-delete <domain> <snapshot> --metadata // external snapshot
# virsh snapshot-delete <domain> <snapshot>            // internal snapshot
```

revert
```
# virsh snapshot-revert <domain> <snapshot>
```

## VCPU pinning

```
# virsh edit <domain>
...
<vcpu cpuset='0-7'>8</vcpu>
	<cputune>
		<vcpupin vcpu='0' cpuset='0'/>
		<vcpupin vcpu='1' cpuset='1'/>
		<vcpupin vcpu='2' cpuset='2'/>
		<vcpupin vcpu='3' cpuset='3'/>
		<vcpupin vcpu='4' cpuset='4'/>
		<vcpupin vcpu='5' cpuset='5'/>
		<vcpupin vcpu='6' cpuset='6'/>
		<vcpupin vcpu='7' cpuset='7'/>
	</cputune>
...
# virsh vcpuinfo <domain>
```

## NUMA Topology

virt-install時
```
	--vcpus=8,sockets=2,cores=2,thread=2
```

virsh edit時
```
# virsh edit <domain>
+ <cpu>
+   <topology sockets='2' cores='2' threads='2'/>
+ </cpu>
```

## Reference

- http://qiita.com/knqyf263/items/e47d77adad797eae98a0
- ipaddress Configuration
  http://momijiame.tumblr.com/post/84423976326/libvirtkvm-%E3%81%A7-vm-%E3%81%AB%E9%9D%99%E7%9A%84%E3%81%AA-ip-%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%82%92%E9%85%8D%E5%B8%83%E3%81%99%E3%82%8B

- [KVM Hugepages](http://30boys.ddo.jp/kvmwiki/)

- [Attach PCI device to VM](https://access.redhat.com/documentation/ja-JP/Red_Hat_Enterprise_Linux/6/html/Virtualization_Host_Configuration_and_Guest_Installation_Guide/chap-Virtualization_Host_Configuration_and_Guest_Installation_Guide-PCI_Device_Config.html)

- [Qemuを使う方法について](http://www.mztn.org/kvm/kvm2.html)


## SR-IOV/PCI-passthrough

```
# vim /boot/grub/grub.cfg
intel_iommu=on pci=assign-busses pci=realloc
# grub-mkconfig -o /boot/grub/grub.cfg
```

0000:3b:00:1をpci-passthroughする場合
```
<device>
	<hostdev mode='subsystem' type='pci' managed='yes'>
		<source>
			<address domain='0x0000' bus='0x3b' slot='0x00' function='0x1'/>
		</source>
	</hostdev>
</device>
```

0000:3b:00:1をsriovとする場合. (もしかしたら, pci-ptと同じ方法でもできるかもしれない)
```
<device>
  <interface type='hostdev' managed='yes'>
    <source>
      <address type='pci' domain='0x0000' bus='0x3c' slot='0x10' function='0x1'/>
    </source>
  </interface>
</device>
```

```
# vim /boot/grub/grub.cfg
intel_iommu=on pci=assign-busses pci=realloc
# grub-mkconfig -o /boot/grub/grub.cfg
```

VFの作成
```
# modprobe -r ixgbe
# modprobe ixgbe max_vfs=3
# lspci | grep X540
3b:00.1 Ethernet controller: Intel Corporation Ethernet Controller 10-Gigabit X540-AT2 (rev 01)
3c:10.1 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
3c:10.3 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
3c:10.5 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
5e:00.1 Ethernet controller: Intel Corporation Ethernet Controller 10-Gigabit X540-AT2 (rev 01)
5f:10.1 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
5f:10.3 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
5f:10.5 Ethernet controller: Intel Corporation X540 Ethernet Controller Virtual Function (rev 01)
```

デバイスの親子関係(VF,PF)を確認する方法
```
# virsh nodedev-dumpxml pci_0000_0b_00_0
<device>
   <name>pci_0000_0b_00_0</name>
   <parent>pci_0000_00_01_0</parent>
   <driver>
      <name>igb</name>
   </driver>
   <capability type='pci'>
      <domain>0</domain>
      <bus>11</bus>
      <slot>0</slot>
      <function>0</function>
      <product id='0x10c9'>82576 Gigabit Network Connection</product>
      <vendor id='0x8086'>Intel Corporation</vendor>
   </capability>
</device>
```

0000:3c:10.1をSR-IOVする場合
```
# virsh edit vm0
  <device>
+   <interface type='hostdev' managed='yes'>
+     <source>
+       <address type='pci' domain='0x0000' bus='0x3c' slot='0x10' function='0x1'/>
+     </source>
+   </interface>
  </device>
# ip link set enp94s0f1 up
# virsh start vm0
```

- https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/7/html/virtualization_deployment_and_administration_guide/sect-sr_iov-using_sr_iov

## CPU Hotplug

```
HV$ virsh edit vm0
-   <vcpu placement='static'>1</vcpu>
+   <vcpu placement='static' current='1'>4</vcpu>
HV$ virsh reboot vm0
```

```
HV$ virsh vcpucount vm0
maximum      config         4
maximum      live           4
current      config         1
current      live           1
HV$ virsh setvcpus vm0 2 --live
HV$ virsh vcpucount vm0
maximum      config         4
maximum      live           4
current      config         1
current      live           2

VM# echo 1 > /sys/devices/system/cpu/cpu1/inline
VM# lscpu
```

- http://blog.etsukata.com/2013/09/qemukvm-cpu-hotplug.html
- https://www.ibm.com/developerworks/library/l-vCPU-hotplug-using-libvirt-trs/index.html


## Virtual Network

KVM導入時に最初に作った仮想NWを編集する.
```
host$ virsh net-list
Name                 State      Autostart     Persistent
----------------------------------------------------------
default              active     yes           yes
host$ virsh net-edit default

<network>
  <name>default</name>
  <uuid>9fdf9e6c-7812-4285-8b44-0c9818e3b10b</uuid>
  <forward mode='nat'/>
  <bridge name='virbr0' stp='on' delay='0' />
  <mac address='52:54:00:45:AE:0C'/>
  <ip address='192.168.122.1' netmask='255.255.255.0'>
    <dhcp>
~     <range start='192.168.122.100' end='192.168.122.254' />
+     <host mac='52:54:00:ff:00:00' name='vm0.local' ip='192.168.122.100' />
+     <host mac='52:54:00:ff:00:01' name='vm1.local' ip='192.168.122.101' />
+     <host mac='52:54:00:ff:00:02' name='vm2.local' ip='192.168.122.102' />
    </dhcp>
  </ip>
</network>

host$ virsh net-destroy default
host$ virsh net-start default
cat /var/lib/libvirt/dnsmasq/default.hostsfile
52:54:00:ff:00:00,192.168.122.100,vm0.local
52:54:00:ff:00:01,192.168.122.101,vm1.local
52:54:00:ff:00:02,192.168.122.102,vm2.local
```

dnsmasqが使えるのでvm間も楽になる.
```
vm0$ ping vm1
PING vm1 (192.168.122.101): 56 data bytes
64 bytes from 192.168.122.101: icmp_seq=0 ttl=51 time=4.149 ms
64 bytes from 192.168.122.101: icmp_seq=1 ttl=51 time=4.870 ms
....
```

現在の割り当てアドレスの確認
```
$ cat /var/lib/libvirt/dnsmasq/default.leases
```

## Add VM's network interface to OVS

```
host$ ovs-vsctl add-br ovs0
host$ virsh edit <vmnmae>
...
<interface type='bridge'>
	<mac address='52:54:00:77:77:77'/>
	<source bridge='ovs0'/>
	<virtualport type='openvswitch'>
		<parameters interfaceid='0b060c88-7d7e-4ebb-b41b-22b85970186b'/>
	</virtualport>
	<target dev='vnet2'/>
	<model type='virtio'/>
	<driver name='vhost'/>
	<alias name='net2'/>
	<address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
</interface>
...
host$ virsh start <vmname>
```

```
<interface type='vhostuser'>
	<source type='unix' path='/var/lib/libvirt/qemu/vhost2.sock' mode='server'/>
	<model type='virtio'/>
	<driver name='vhost'/>
</interface>

<interface type='vhostuser'>
	<source type='unix' path='/var/lib/libvirt/qemu/vhost2.sock' mode='client'/>
	<model type='virtio'/>
	<driver name='vhost'/>
</interface>
```

**Add VM's network interface to OVS with VLAN**

```
<interface type='bridge'>
	<source bridge='ovs0'/>
	<virtualport type='openvswitch'/>
	<vlan> <tag id='10'/> </vlan>
	<address type='pci' domain='0x0000' bus='0x00' slot='0x07' function='0x0'/>
</interface>
```

```
<interface type='bridge'>
	<source bridge='ovs0'/>
	<virtualport type='openvswitch'/>
	<vlan trunk='yes'>
		<tag id='110'/>
		<tag id='111'/>
		<tag id='120'/>
		<tag id='121'/>
	</vlan>
	<model type='rtl8139'/>
	<address type='pci' domain='0x0000' bus='0x00' slot='0x08' function='0x0' multifunction='on'/>
</interface>
```

## Additional VM Configuration

Refs
- https://access.redhat.com/documentation/ja-jp/red_hat_enterprise_linux/7/html/virtualization_tuning_and_optimization_guide/sect-virtualization_tuning_optimization_guide-memory-tuning

### Host Specification
```
CPU Model name: Intel(R) Xeon(R) Platinum 8180 CPU @ 2.50GHz
Thread(s) per core:    1
Core(s) per socket:    28
Socket(s):             2
NUMA node(s):          2
Virtualization:        VT-x
node 0 cpus: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27
node 1 cpus: 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55
MemTotal:       196722648 kB
```

### Single Sockets VM
```
<vcpu placement='static'>40</vcpu>
<cpu mode='host-passthrough'>
    <topology sockets='1' cores='40' threads='1'/>
</cpu>
```
```
CPU Model name: Intel(R) Xeon(R) Platinum 8180 CPU @ 2.50GHz
Thread(s) per core:    1
Core(s) per socket:    40
Socket(s):             1
NUMA node(s):          1
```

### Multi Sockets VM
```
<currentMemory unit='KiB'>16384000</currentMemory>
<vcpu placement='static'>40</vcpu>
<cpu mode='host-passthrough'>
	<topology sockets='2' cores='20' threads='1'/>
	<numa>
		<cell id='0' cpus='0-19' memory='8192000' unit='KiB'/>
		<cell id='1' cpus='20-39' memory='8192000' unit='KiB'/>
	</numa>
</cpu>
```
```
CPU Model name: Intel(R) Xeon(R) Platinum 8180 CPU @ 2.50GHz
Thread(s) per core:    1
Core(s) per socket:    20
Socket(s):             2
NUMA node(s):          2
Virtualization:        VT-x
Hypervisor vendor:     KVM
Virtualization type:   full
node 0 cpus: 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19
node 1 cpus: 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39
MemTotal:       16038096 kB
```

### VMのメモリをHostのHugepagesから持ってくる
```
<memoryBacking>
  <hugepages/>
</memoryBacking>
```

### Vhost-net multi queue

```
<interface type='network'>
      <source network='default'/>
      <model type='virtio'/>
      <driver name='vhost' queues='N'/>
</interface>
```

## Mount Qcow Image on Hyperviwor

mount
```
modprobe nbd max_part=8
qemu-nbd -c /dev/nbd0 /var/lib/libvirt/images/vm01.img
fdisk -l /dev/nbd0
mount -o ro /dev/nbd0p2 /mnt
```

umount
```
umount /mnt
killall qemu-nbd
losetup -d /dev/nbd0
modprobe -r nbd
```

