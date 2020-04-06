
# DPDK

## Very Easy Setup

- OS: ubuntu (recommended v16.04LTS)
	-	shell bash
- DPDK:
	- latest version (clone from dpdk.org)
	- install path: $HOME/dpdk

Prepare ENVs
```
$ echo "export RTE_SDK=$HOME/dpdk" >> $HOME/.bashrc
$ echo "export RTE_TARGET=x86_64-native-linuxapp-gcc" >> $HOMA/.bashrc
```

Install required package from apt.
```
$ sudo apt install -y \
	libpcap-dev python \
	linux-image-extra-`uname -r` \    #this is important for uio_pci_generic
	linux-headers-`uname -r` \
	build-essential git libnuma-dev \
	pkg-config
```

Download dpdk and build it.
```
$ git clone http://dpdk.org/git/dpdk $RTE_SDK
$ cd $RTE_SDK
$ make install T=$RTE_TARGET
```

Setup Hugepages
```
$ sudo vim /etc/default/grub
- GRUB_CMDLINE_LINUX=""
+ GRUB_CMDLINE_LINUX="hugepages=512" # This value (512) is important (*1)
$ sudo grub-mkconfig -o /boot/grub/grub.cfg
$ sudo mkdir -p /mnt/huge
$ sudo vim /etc/fstab
+ nodev /mnt/huge hugetlbfs defaults 0 0
$ reboot
```

***\*1***: If this value is too huge, maybe reboot will be fail.
because there are no such memory resouce... :(
You cannot fix this problem, please access me(@slankdev) via Twitter,
or email ( slank.dev [at] gmail.com )

Build Sample Application and Execute.
```
$ cd $RTE_SDK/examples/helloworld
$ make
$ sudo ./build/helloworld
```

## DPDKにNICをバインドする

NICをlinux-kernelの管理下から, DPDKの管理下に移動する.
dpdk/tools/dpdk-devbind.py を使用してバインドをする。これを実行すると``ip addr``や ``ifconfig``では
ネットワークインターフェースが見れなくなるが、アンバインドすれば見れるようになるので、怖がらなくて大丈夫

```
$ sudo modprobe uio_pci_generic
$ cd $RTE_SDK
$ tools/dpdk-devbind.py --status    # これでNICの状態が確認できる
$ sudo tools/dpdk-devbind.py --bind=uio_pci_generic 03:00.0 # バインドしたいPCIeデバイスアドレス
$ sudo tools/dpdk-devbind.py --bind=ixgbe  00:03:00.0 # アンバインドしたいPCIeデバイスアドレス
```


## DPDK開発用のVagrantfile

```
# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure(2) do |config|
  config.vm.define "master" do |master|
  	  master.vm.box = "dpdk-slank"
      master.vm.hostname = "master.vagrant"
	  master.vm.network "private_network", ip: "192.168.11.10", virtualbox__intnet: "in1"
      config.vm.provider "virtualbox" do |vb|
          vb.customize ["modifyvm", :id, "--memory", "2048", "--cpus", "3", "--ioapic", "on"]
      end
  end
  config.vm.define "host" do |host|
  	  host.vm.box = "dpdk-slank"
      host.vm.hostname = "host.vagrant"
	  host.vm.network "private_network", ip: "192.168.11.111", virtualbox__intnet: "in1"
  end
end
```

## その他

```
GRUB_CMDLINE_LINUX="default_hugepagesz=1G hugepagesz=1G hugepages=4"
nodev /mnt/huge hugetlbfs defaults 0 0
nodev /mnt/huge_1GB hugetlbfs pagesize=1GB 0 0
```
```
$ sudo mount -t hugetlbfs none /mnt/huge
# echo 1024 > /sys/kernel/mm/hugepages/hugepages-2048kB/nr_hugepages
# echo 1024 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
# echo 1024 > /sys/devices/system/node/node1/hugepages/hugepages-2048kB/nr_hugepages
# echo 128  > /sys/kernel/mm/hugepages/hugepages-16384kB/nr_hugepages
# echo 128  > /sys/kernel/mm/hugepages/hugepages-16384kB/nr_overcommit_hugepages
```


## 起動しなくなった場合

おそらくほとんどの場合でHugepagesのマウントで失敗している。
そんへんの設定を見直そう。わからなければ``@slankdev``までご連絡を.

Thank you all of DPDK developers and Users.

