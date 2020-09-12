
# Linux

## systemd

systemctl command (root)
```
systemctl -l
```

journalctl command (root)
```
journalctl -e          //check msg
journalctl -xe         //check msg detail
journalctl -f          //tail -f /var/log/syslog
journalctl -u <UNIT>   //specify unit
```

service file [ref](https://qiita.com/masami256/items/ef0f23125cf8255e4857)
```
[Unit]
Description=Load dump capture kernel
After=local-fs.target

[Service]
Type={ simple, forking, oneshot, notify, dbus }
ExecStart=/usr/lib/slankdev/start.sh
ExecStop=/usr/lib/slankdev/stop.sh
RemainAfterExit=yes  //oneshot.
Restart=always

[Install]
WantedBy=multi-user.target
```

## Live USB

zero clear

```
$ sudo dd if=/dev/zero of=/dev/sdb
```

macOS

```
$ diskutil list
$ diskutil unmountDisk /dev/disk1
$ sudo dd if=linux.iso of=/dev/disk1 bs=8192
$ sudo killall -INFO dd
$ diskutil eject /dev/disk1
```

Linux

```
$ ls /dev/sd*
$ sudo dd if=linux.iso of=/dev/sdb bs=512k
$ sudo killall -USR1 dd
```

## Disk Mount

```
mount -t ext4 /dev/sdc1 /mnt
umount /mnt
```

## File compression and decompression / tar.gz tgz

```
-z	--gzip
-c	--create
-x	--extract
-v	--verbose
-p  --preserve-permissions
-f	--file <filename>

tar -zcpf filename.tgz filename   #COMPRESS
tar -zxpf filename.tgz            #DECOMPRESS
```

## Date command

```
$ date "+%Y-%m-%d-%H-%M-%S"
2019-10-04-17-35-52
```

## Neovim Setup

```
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:neovim-ppa/unstable
$ sudo apt-get update
$ sudo apt-get install neovim
$ sudo apt install python3-dev python3-pip
$ pip3 install -U pip3
$ pip3 install neovim
```

クリップボード関係の必要パッケージをインストール

```
$ sudo apt install xclip xsel
```

## ACPI
電力関連などをまとめてくれるすごいやつ
c言語で叩く場合はlibacpiというのをインストールする必要がある。
libacpi.hをインクルードする。

## check keycode

Xorgの中の場合xevを使って調べる
コンソール画面上の場合showkeyを使って調べる.

```
$ xev | awk -F'[ )]+' '/^KeyPress/ { a[NR+2] } NR in a { printf "%-3s %s\n", $5, $8 }'
$ showkey
```

## /etc/profile

自分は以下のようなコマンドを記述している

 - wmname LG3D // タイル型WMでJAVAアプリケーションレイアウトが崩れないようにする


## Service Name (Port name)

```
# vi /etc/services

...
ssh       22/tcp    # The Secure Shell (SSH) Protocol
ssh       22/udp    # The Secure Shell (SSH) Protocol
...

# telnet localhost ssh
```

## Hostname

両方変更しないといけない

```
# vi /etc/hosts
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

# vi /etc/hostname
localhost.localdomain
```


## DNS

```
# vi /etc/resolf.conf
nameserver 192.168.0.1  # Primary
nameserver 8.8.8.8      # Secondary
```

## ifupdown

```
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
 address         192.168.11.101
 netmask         255.255.255.0
 broadcast       192.168.11.255
 gateway         192.168.11.1
 dns-nameservers 192.168.11.1

auto eth1
iface eth1 inet dhcp
```

```
auto eth0
iface eth0 inet manual
post-up ip route add 10.0.0.1/24 via 10.1.0.1
```

```
vi /etc/network/if-up.d/static-route
#!/bin/sh
/sbin/ip route add 1.1.1.1 via 10.0.0.1
chmod +x /etc/network/if-up.d/static-route
```

```
iface ens3 inet manual
up /sbin/ifconfig ens3 promisc up

auto ens4
iface ens4 inet manual
up /sbin/ifconfig ens4 promisc up

auto br0
iface br0 inet static
 address         192.168.11.101
 netmask         255.255.255.0
 broadcast       192.168.11.255
 gateway         192.168.11.1
 dns-nameservers 192.168.11.1
bridge_ports ens3 ens4
bridge_stp off
bridge_maxwait 1
```

## NetPlan Ubuntu18.04LTS

```
$ cat /etc/netplan/**.cfg
network:
  version: 2
  renderer: networkd
  ethernets:
    eno1:
      dhcp4: no
      dhcp6: no
      addresses: [ 172.18.1.6/24 ]
$ sudo netplan apply
```

```
network:
  version: 2
  renderer: networkd
  ethernets:
    eth0:
      dhcp4: no
      dhcp6: no
  vlans:
    eth0.10:
      link: eth0
      id: 10
      dhcp4: no
      dhcp6: no
      addresses: [ 10.0.0.1/30 ]
      gateway4: 10.0.0.2
      nameservers:
        addresses: [ 8.8.8.8 ]
    eth0.20:
      link: eth0
      id: 20
      dhcp4: no
      dhcp6: no
      addresses: [ 10.0.0.5/30 ]
```

## Network-script sysconfig / CentOS

```
# vi /etc/sysconfig/network-scripts/ifcfg-eth0

# Common Config
TYPE=Ethernet
ONBOOT=yes
NAME=eth0

# Static Config
BOOTPROTO=static
IPADDR=192.168.0.2
NETMASK=255.255.255.0
GATEWAY=192.168.0.1
DNS1=8.8.8.8

# DHCP Config
BOOTPROTO=dhcp
TYPE=Ethernet
```

```
$ cat /etc/sysconfig/network-scripts/ifcfg-eth0
DEVICE=eth0
TYPE=Ethernet
BOOTPROTO=none
ONBOOT=yes

$ cat /etc/sysconfig/network-scripts/ifcfg-eth0.10
DEVICE=eth0.192
BOOTPROTO=none
ONBOOT=yes
IPADDR=192.168.1.1
PREFIX=24
NETWORK=192.168.1.0
VLAN=yes

$ sudo systemctl restart network
```

## Wait Networkを設定する / raising network

`A start job is running for wait for network to be configured.`の場合
```
systemctl disable systemd-networkd-wait-online.service
systemctl mask systemd-networkd-wait-online.service
```

なんとかraising networkの場合.
```
$ sudo vim /etc/systemd/system/network-online.targets.wants/networking.service
...
- TimeoutStartSec = 5min
+ TimeoutStartSec = 1sec
...
$ sudo systemctl daemon-reload
```

- https://ubuntuforums.org/showthread.php?t=2323253

## User/Group

Create/Delete new user
```
ubuntu# useradd -m -G users,sudo -s /bin/bash slankdev
# passwd NAME
# userdel -r NAME
```

**ユーザ情報の変更**

```
# usermod -aG <group> <user>  # -aは追加という意味, これなくすと辛い
# usermod -l NEWNAME OLDNAME
# usermod -d /PATH/TO/NEW/HOME USERNAME
# mv /OLD/HOME /PATH/TO/NEW/HOME
```

**sudoersについて**

```
# visudo
%wheel ALL=(ALL) ALL　がある行のコメントアウトを解除
```

centos
```
useradd -s /bin/bash slankdev
echo "slankdev ALL=(ALL) NOPASSWD: ALL" | tee /etc/sudoers.d/slankdev
```

## Grub

```
$ ls /home/slankdev/image.iso
/home/slankdev/image.iso
$ sudo vim /etc/grub.d/40_custom
$ cat /etc/grub.d/40_custom
#!/bin/sh
exec tail -n +3 $0
# This file provides an easy way to add custom menu entries.  Simply type the
# menu entries you want to add after this comment.  Be careful not to change
# the 'exec tail' line above.

menuentry "test entry iso" {
        loopback loop (hd0,1)/home/slankdev/image.iso
        linux (loop)/install/vmlinuz boot=install \
                iso-scan/filename=/home/slankdev/image.iso \
                noprompt noeject quiet splash
        initrd (loop)/install/initrd.gz
}
$ sudo update-grub
$ sudo reboot
```

```
$ sudo grubby --info ALL
$ sudo grubby --default-kernel
$ sudo grubby --set-default `find /boot/vmlinuz-* | sort | tail -n1`
```

## Sudo without password

```
$ sudo visudo
...
+ slankdev ALL=NOPASSWD: ALL
...
```

## Hostname commit

```
sudo su
export VAL=vpp-template
echo $VAL > /etc/hostname
echo "127.0.1.1 $VAL" >> /etc/hosts
hostname $VAL
```

ubuntu 18.04
```
vim /etc/cloud/cloud.cfg
- preserve_hostname: false
+ preserve_hostname: true
hostnamectl set-hostname hogehoge
reboot
```

## Hugepages

```
vim /etc/default/grub
grub-mkconfig -o /boot/grub/grub.cfg
reboot
cat /proc/meminfo | grep -i huge
```
```
GRUB_CMDLINE_LINUX="default_hugepagesz=1G hugepagesz=1G hugepages=4"
```

without reboot
```
echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
echo 8    > /sys/kernel/mm/hugepages/hugepages-16384kB/nr_hugepages
echo 8    > /sys/kernel/mm/hugepages/hugepages-16384kB/nr_overcommit_hugepages
echo 1024 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
echo 1024 > /sys/devices/system/node/node1/hugepages/hugepages-2048kB/nr_hugepages
echo 8    > /sys/devices/system/node/node0/hugepages/hugepages-16384kB/nr_hugepages
echo 8    > /sys/devices/system/node/node1/hugepages/hugepages-16384kB/nr_hugepages
```

## netrc

```
$ vim ~/.netrc
$ chmod 600 ~/.netrc
```

```
machine github.com
login slankdev
password xxxxxxx
```

## udev

```
## /etc/udev/rules.d/slankdev.rules
SUBSYSTEM=="net", ACTION=="add", DEVPATH=="/devices/virtual/net/dum0", \
RUN+="/sbin/ip link set dev %E{INTERFACE} master red", \
RUN+="/sbin/ip link set dev %E{INTERFACE} up", \
RUN+="/sbin/ip addr add 10.0.0.1/24 dev %E{INTERFACE}", \
RUN+="/sbin/ip addr add cafe::1/64 dev %E{INTERFACE}"
```

```
$ sudo udevadm monitor -k
monitor will print the received events for:
KERNEL - the kernel uevent

KERNEL[114278.600213] remove   /devices/virtual/net/dum0/queues/rx-0 (queues)
KERNEL[114278.600261] remove   /devices/virtual/net/dum0/queues/tx-0 (queues)
KERNEL[114278.600281] remove   /devices/virtual/net/dum0 (net)
KERNEL[114282.117451] add      /devices/virtual/net/dum0 (net)
KERNEL[114282.117493] add      /devices/virtual/net/dum0/queues/rx-0 (queues)
KERNEL[114282.117501] add      /devices/virtual/net/dum0/queues/tx-0 (queues)
```

## serial console

after boot
```
sudo systemctl enable serial-getty@ttyS0.service
sudo systemctl start  serial-getty@ttyS0.service
```

on booting time
```
GRUB_DEFAULT=0
GRUB_TIMEOUT=1
GRUB_CMDLINE_LINUX_DEFAULT="text"
GRUB_CMDLINE_LINUX="console=tty1 console=ttyS0,115200"
GRUB_TERMINAL="console serial"
GRUB_SERIAL_COMMAND="serial --speed=115200"
```

## rc.local rc-local.service

```
sudo vi /etc/rc.local
sudo chmod u+x /etc/rc.local
sudo systemctl enable rc-local.service
```

## iproute2

add new link
```
// bridge
ip link add br0 type bridge
ip link set eth0 master br0
ip link set eth0 nomaster

// bonding
ip link add bond1 type bond miimon 100 mode active-backup
ip link set eth0 master bond1
ip link set eth1 master bond1

// team-dev
teamd -o -n -U -d -t team0 -c '{"runner": {"name": "activebackup"},"link_watch": {"name": "ethtool"}}'
ip link set eth0 down
ip link set eth1 down
teamdctl team0 port add eth0
teamdctl team0 port add eth1

// vlan
ip link add link eth0 name eth0.2 type vlan id 2
ip link add link eth0 name eth0.3 type vlan id 3

// vxlan
ip link add vx0 type vxlan id 100 dstport 4789 group 239.0.1.1 dev eth0
ip link add vx0 type vxlan id 100 dstport 4789 local 1.1.1.1 remote 2.2.2.2
ip link add vx0 type vxlan id 100 dstport 4789 local 1.1.1.1

// macvlan
ip link add macv1 link eth0 type macvlan mode bridge
ip link add macv2 link eth0 type macvlan mode bridge
ip netns add net1
ip netns add net2
ip link set macvlan1 netns net1
ip link set macvlan2 netns net2

// ipvlan
ip netns add ns0
ip link add name ipv1 link eth0 type ipvlan mode l2
ip link set dev ipvl0 netns ns0

// macvtap/ipvtap
ip link add link eth0 name macvtap0 type macvtap

// MACsec
ip link add macsec0 link eth1 type macsec

// veth
ip netns add net1
ip netns add net2
ip link add veth1 netns net1 type veth peer name veth2 netns net2

// vcan
ip link add dev vcan1 type vcan

// vxcan
ip netns add net1
ip netns add net2
ip link add vxcan1 netns net1 type vxcan peer name vxcan2 netns net2

// ipoib
ip link add ipoib0 type ipoib mode connected

// nlmon
ip link add nlmon0 type nlmon
ip link set nlmon0 up
tcpdump -i nlmon0 -w nlmsg.pcap

// dummy
ip link add dummy1 type dummy
ip addr add 1.1.1.1/24 dev dummy1
ip link set dummy1 up

// ifb
ip link add ifb0 type ifb
ip link set ifb0 up
tc qdisc add dev ifb0 root sfq
tc qdisc add dev eth0 handle ffff: ingress
tc filter add dev eth0 parent ffff: u32 match u32 0 0 action mirred egress redirect dev ifb0

echo 4 > /sys/class/net/eno1/device/sriov_numvfs
ip link set eno1 up
ip link set eno1 vf 0 vlan 10
ip link set eno1 vf 1 vlan 11
ip link set eno1 vf 2 vlan 12
ip link set eno1 vf 3 vlan 13
```

bridge utils
```
ip link set br100 type bridge vlan_filtering 1
ip link set br100 type bridge vlan_filtering 0
bridge fdb show dev br0
bridge vlan add vid 100 dev eth0
bridge vlan del vid 100 dev eth0
bridge vlan add vid 1 dev net1 pvid 1 untagged
```

netns veth magic
```
ip netns add C0
ip netns add C1
ip link add net0 netns C0 type veth peer name net0 netns C1
```

setting link
```
ip link set eth0 address 11:22:33:44:55:66
ip link set em1 up
ip link set em1 down
ip link set em1 promisc on
ip link set em1 promisc off
ip link set eth0 name em0 // rename eth0 -> em0 link-state-down needed
```

getting info from link
```
ip maddr show dev em1
ip -s link show dev em0
```

mcast / multicast
```
ip maddr
ip maddr show dev em1
ip maddr add 33:33:00:00:00:01 dev em1
ip maddr del 33:33:00:00:00:01 dev em1
```

nexthop
```
ip nexthop list
ip nexthop add id 1 encap seg6local action End dev net0
ip nexthop add id 2 via fe80::2 dev net0
ip nexthop add id 3 via fe80::3 dev net1
ip nexthop add id 4 via fe80::4 dev net2
ip nexthop add id 10 group 2/3/4            ##ECMP
ip nexthop add id 10 group 2,10/3,10/4,5    ##Weighted
```

route
```
ip route list vrf vrf0
ip route add 1.1.1.1/32 nhid 10
ip route add default via 192.168.1.1 dev em1
ip route add 192.168.1.0/24 via 192.168.1.1
ip route add 192.168.1.0/24 dev em1
ip route del 192.168.1.0/24 via 192.168.1.1
ip route replace 192.168.1.0/24 dev em1
ip route get 192.168.1.5

//seg6,seg6local
ip route add 2001:12::1/64 encap seg6 mode encap segs fc00:1::10 dev dum0
ip route del 2001:12::1/64 encap seg6 mode encap segs fc00:1::10 dev dum0
ip route add fc00:1::10/32 encap seg6local action End.DX4 nh4 10.0.0.1 dev dum0
ip route del fc00:1::10/32 encap seg6local action End.DX4 nh4 10.0.0.1 dev dum0

//ipip,ipip6
ip route add 1.1.1.1 encap ip src 10.0.0.1 dst 10.1.0.2 ttl 100 dev dum0
ip route add 1.1.1.1 encap ip6 src 2001::1 dst 2001:1::2 hoplimit 100 dev dum0

proto
  - kernel   --> from kernel (auto-generate-route), like-a connected-route
  - dhcp     --> from dhcp-client
	- bgp,ospf --> from routing software
  - boot     --> from iproute2 statically ...?

scope
  - link     --> unicast/broadcast, so connected-route
	- host     --> goto-ours to-my-local-interface
	- global   --> using gateway routing type

ip route add 1.1.1.1/32 encap mpls 100 via inet 10.0.0.2
ip route add 1.1.1.1/32 via mpls 100/200/300 dev net0
ip -f mpls route add 100 via mpls 100/200/300 dev net0
ip -f mpls route add 100 as 200 via inet 10.0.0.2
ip -f mpls route add 300 dev vrf0
ip -f mpls route show

ip route save 1.1.1.1 > out.bin
xxd out.bin
00000000: 2412 3145 7000 0000 1800 0200 a2b5 a55d  $.1Ep..........]
00000010: b816 0000 0220 0000 fe03 fd01 0000 0000  ..... ..........
00000020: 0800 0f00 fe00 0000 0800 0100 0101 0101  ................
00000030: 0800 0400 2a00 0000 3400 1600 3000 0100  ....*...4...0...
00000040: 0100 0000 0004 0401 0100 0000 0002 0000  ................
00000050: 0000 0000 0000 0000 0000 0000 0001 0000  ................
00000060: 0000 0000 0000 0000 0000 0000 0600 1500  ................
00000070: 0500 0000                                ....
```

neigh
```
$ ip neigh
$ ip neigh show dev em1
$ ip neigh add 192.168.1.1 lladdr 1:2:3:4:5:6 dev em1
$ ip neigh del 191.168.1.1 dev em1
$ ip neigh replace 192.168.1.1 lladdr 1:2:3:4:5:6 dev em1
```

socket
```
ss ソケットの統計情報表示
ss -a すべてのソケットを表示する
ss -e ソケットの詳細情報を表示する
ss -o タイマ情報を表示する
ss -n アドレス解決をしない
ss -p ソケットを使用しているすべてのプロセスを表示する
```

segment-routing-ipv6 / srv6
```
ip sr tunsrc set fc00:1::1
```

genl - generic netlink utility frontend
```
$ genl ctrl list
...(snip)...
Name: SEG6
        ID: 0x1a  Version: 0x1  header size: 0  max attribs: 7
        commands supported:
                #1:  ID-0x1
                #2:  ID-0x2
                #3:  ID-0x3
                #4:  ID-0x4
...(snip)...
```

tc (traffic control)
- pfifo: per-Packet FIFO
- bfifo: per-Byte FIFO
- sfq: Stochastic Fairness Queuing
- tbf: Token Bucket Filter
- netem: Network Emulator (Delay, Loss, etc.)
- fq: Fair Queue Packet Scheduling
```
tc qdisc show dev eth0
tc qdisc del  dev eth0 root
tc qdisc add  dev eth0 root tbf limit 1Mb buffer 200Kb rate 1Mbps
```

### tc でパケットフィルタを用意する.

- tc-u32 is universal 32bit traffic control filter
	- man: https://man7.org/linux/man-pages/man8/tc-u32.8.html
	- filterを定義して何かしらのactionを実施することができる
- `u32 match W A B at N` は ethernet headerの先頭からの `u32[N]` を意味する
- 以下三種類は基本的には同じだし, シンプルにするため, `u32 match u32` で統一した方がいい.
	- `u32 match u32 A B at N` のA,Bは 32bitで指定する
	- `u32 match u16 A B at N` のA,Bは 16bitで指定する
	- `u32 match u8  A B at N` のA,Bは  8bitで指定する
- FILTER EXAMPLE
	- ip.protocol==1 `u32 match ip protocol 0x01 0xff`
	- ip.protocol==1 `u32 match u32 0x00010000 0x00ff0000 at 8`
	- ip.protocol==1 `u32 match u16 0x0001     0x00ff     at 8`

## ethtool

```
# ethtool -g eth0 リングバッファを表示
# ethtool -i eth0 eth0のドライバ情報を表示する
# ethtool -p eth0 NWポートでLEDが点灯する
# ethtool -S eth0 eth0のドライバ統計を表示する
# ethtool -p eth0 // LED Blink
# ethtool -i eth0 ドライバ情報, PCIアドレスも見れる
# ethtool -k eth0 offloadの状態が見れる
# ethtool -K eth0 OFFLOADNAME on OFFLOADNAMEを有効に
# ethtool -K eth0 OFFLOADNAME off OFFLOADNAMEを無効に
# ethtool -g eth0 ringパラメータが見れる
# ethtool -G eth0 .. ringパラメータ設定
# ethtool -S eth0 統計情報
# ethtool -e eth0 eepromダンプ
# ethtool -E eth0 eeprom情報書き換え
```

Set/Get NIC Parameter
```
ethtool -l eth0               // get multiqueue info
ethtool -L ens2f0 combined 20 // set multiqueue=20

ethtool -k eth0         // get-param
ethtool -K eth0 sg off  // set-param

 display-name                  specify-name
-------------------------     ---------------
 scatter-gather                sg
 rx-checksumming               rx
 tx-checksumming               tx
 TCP-segumentation-offload     tso
                               ufo
															 gso
															 gro
															 lro
															 rxvlan
															 txvlan
															 ntuple
															 rxhash
```

## arping / ARPing

```
$ arping -I eth0 192.168.1.1
$ arping -D -I eth0 192.168.1.1
```

## conntrack

```
# conntrack -h
Command line interface for the connection tracking system. Version 1.4.4
Usage: conntrack [commands] [options]

Commands:
  -L [table] [options]          List conntrack or expectation table
  -G [table] parameters         Get conntrack or expectation
  -D [table] parameters         Delete conntrack or expectation
  -I [table] parameters         Create a conntrack or expectation
  -U [table] parameters         Update a conntrack
  -E [table] [options]          Show events
  -F [table]                    Flush table
  -C [table]                    Show counter
  -S                            Show statistics

Tables: conntrack, expect, dying, unconfirmed

Conntrack parameters and options:
  -n, --src-nat ip                      source NAT ip
  -g, --dst-nat ip                      destination NAT ip
  -j, --any-nat ip                      source or destination NAT ip
  -m, --mark mark                       Set mark
  -c, --secmark secmark                 Set selinux secmark
  -e, --event-mask eventmask            Event mask, eg. NEW,DESTROY
  -z, --zero                            Zero counters while listing
  -o, --output type[,...]               Output format, eg. xml
  -l, --label label[,...]               conntrack labels

Expectation parameters and options:
  --tuple-src ip        Source address in expect tuple
  --tuple-dst ip        Destination address in expect tuple

Updating parameters and options:
  --label-add label     Add label
  --label-del label     Delete label

Common parameters and options:
  -s, --src, --orig-src ip              Source address from original direction
  -d, --dst, --orig-dst ip              Destination address from original direction
  -r, --reply-src ip            Source addres from reply direction
  -q, --reply-dst ip            Destination address from reply direction
  -p, --protonum proto          Layer 4 Protocol, eg. 'tcp'
  -f, --family proto            Layer 3 Protocol, eg. 'ipv6'
  -t, --timeout timeout         Set timeout
  -u, --status status           Set status, eg. ASSURED
  -w, --zone value              Set conntrack zone
  --orig-zone value             Set zone for original direction
  --reply-zone value            Set zone for reply direction
  -b, --buffer-size             Netlink socket buffer size
  --mask-src ip                 Source mask address
  --mask-dst ip                 Destination mask address
```

```
conntrack -L    //display record
conntrack -E    //display update
conntrack -o xml //output as xml
conntrack -I -s 1.1.1.1 -d 2.2.2.2 -p tcp --sport 10 --dport 20 --state LISTEN -u SEEN_REPLY -t 50 --mark 42
conntrack -I -s 4.1.1.1 -d 2.2.2.2 -p tcp --sport 10 --dport 20 --state ESTABLISHED -u SEEN_REPLY -t 49999 --mark 0
conntrack -U -s 4.1.1.1 -d 2.2.2.2 -p tcp --sport 10 --dport 20 --state ESTABLISHED -u SEEN_REPLY -t 49999 --mark 0
conntrack -I --timeout 120000 --src 10.0.0.1 --dst 8.8.8.8 -p tcp --dport 9999 --state ESTABLISHED --status ASSURED \
  --mark 0 --reply-dst 20.0.0.1 --reply-src 8.8.8.8 --reply-port-src 9999 --reply-port-dst 10041 --sport 10101

                 private-nw                     public-nw
[client].10------10.0.0.0/24----.1[natbox].1----199.0.0.0/24-----.8[server]

client# curl --interface 10.0.0.10 --local-port 9999 http://199.0.0.8:80
natbox# conntrack -I --timeout 1200 --src 10.0.0.11 --dst 119.0.0.8 -p tcp --sport 9999 --dport 80 --state ESTABLISHED --status ASSURED --mark 0
```

## kernel development

```
sudo apt install -y \
	build-essential libncurses-dev fakeroot \
	kernel-package linux-source libssl-dev \
	bison flex
sudo apt build-dep linux
git clone https://github.com/slankdev/linux && cd linux
mkdir ../build
cp /boot/config-`uname -r` ../build/.config
make O=../build/ olddefconfig
make -j`nproc` O=../build/ LOCALVERSION=-slankdev
make -j`nproc` bindeb-pkg O=../build/ LOCALVERSION=-slankdev
dpkg -i ../linux-*.deb
```
```
GRUB_DISABLE_SUBMENU=y
```
```
awk -F\' '$1=="menuentry " {print i++ " : " $2}' /boot/grub/grub.cfg
grub-set-default 2
grub-editenv list
```

```
sudo apt install \
  linux-image-4.18.0-13-generic \
	linux-modules-4.18.0-13-generic \
	linux-modules-extra-4.18.0-13-generic \
	linux-tools-4.18.0-13-generic
```

## DMI(Desktop Management Interface) Info / dmidecode / SMBIOS

```
dmidecode -s system-product-name
dmidecode -t bios
dmidecode -t memory
```

```
## check RAM size and nb-ram-installed
dmidecode -t memory | grep -i size | grep -iv "no module installed"
	Size: 8192 MB
	Size: 8192 MB
	Size: 8192 MB
	Size: 8192 MB

## check RAM version
...(snip)...
Handle 0x0053, DMI type 17, 34 bytes
Memory Device
	Array Handle: 0x0045
	Error Information Handle: Not Provided
	Total Width: 72 bits
	Data Width: 64 bits
	Size: 8192 MB
	Form Factor: DIMM
	Set: None
	Locator: DIMM-1G
	Bank Locator: Not Specified
	Type: DDR3
	Type Detail: Registered (Buffered)
	Speed: 1600 MHz
	Manufacturer: Samsung
	Serial Number: 1766A609
	Asset Tag:
	Part Number: M393B1G70QH0-YK0
	Rank: 1
	Configured Clock Speed: Unknown
...(snip)...

## check M/B info
dmidecode -t system
...(snip)...
Handle 0x0001, DMI type 1, 27 bytes
System Information
	Manufacturer: FUJITSU
	Product Name: PRIMERGY RX200 S8
	Version: GS01
	Serial Number: MANS013297
	UUID: 77241FD6-2A1D-E411-B134-70E28409FF12
	Wake-up Type: Power Switch
	SKU Number: S26361-K1455-Vxxx
	Family: SERVER
...(snip)...
```

## RPM / yum

```
rpm -ivh file.rpm
yum install ./file.rpm
dnf install ./file.rpm

yum list installed
```

## tee

```
$ cat /tmp/file
hiroki

$ echo slank | tee /tmp/file
$ cat /tmp/file
slank
echo slank2 | tee /tmp/file

$ cat /tmp/file
slank
slank2
```

## iptables / ip6tables / ebtables

```
$ sudo sysctl -w net.ipv4.ip_forward=1
$ sudo iptables -t nat -A POSTROUTING -s 192.168.111.0/255.255.255.0 -j MASQUERADE
```

Routerのmgmt参照config
- `-P` is default policy
- `-A` specify chain (INPUT, OUTPUT, FORWARD, POSTROUTING, PREROUTING)
```
$ sudo apt install iptables-persistent
$ sudo iptables -P INPUT DROP    // white-list filter
$ sudo iptables -P INPUT ACCEPT  // black-list filter
$ sudo netfilter-psersistent save
$ sudo netfilter-psersistent reload
```

console log
```
iptables -t nat -L -n --line-number
iptables -t nat -D POSTROUTING 5     // delete rule from line5
iptables -t nat -I POSTROUTING 1 -s 172.16.3.0/24 -j MASQUERADE // add rule to line1

iptables -t raw -Z OUTPUT    // reset counter raw[OUTPUT]
iptables -t filter -Z OUTPUT    // reset counter filter[OUTPUT]
```

## nftables

```
yum install -y nftables
apt install -y nftables iptables-nttables-compat
```

```
nft add table nat
nft delete table nat
nft add chain nat postrouting
nft delete chain nat postrouting

nft list tables
nft list chains
nft list ruleset

nft create table ip nat
nft create chain ip nat prerouting { type nat hook prerouting priority 0 \;}
nft create chain ip nat postrouting { type nat hook postrouting priority 0 \;}
nft add rule nat postrouting ip saddr 10.0.0.0/24 oif net1 masquerade

nft create table ip nat
nft create chain ip nat prerouting { type nat hook prerouting priority 0 \;}
nft create chain ip nat postrouting { type nat hook postrouting priority 0 \;}
nft add rule nat postrouting ip protocol tcp snat to 20.0.0.1:100-200
```

## namespace / nsenter

```
ps aux | grep mininet | psawk_pid    #pid is 9999
nsenter -t 9999 -n bash

   -n enter NetworkNamespace
	 -t target pid (nsenter read the /proc/$PID/ns )
```
