
# Vagrant

## install and setup

install on centos
download-link: https://www.vagrantup.com/downloads.html
```
echo options kvm_intel nested=Y | sudo tee /etc/modprobe.d/kvm_intel.conf
yum install -y qemu-kvm libvirt libvirt-devel gcc patch
systemctl enable libvirtd
systemctl start libvirtd

cd /tmp
wget <link>
wget https://releases.hashicorp.com/vagrant/2.2.5/vagrant_2.2.5_x86_64.rpm (latest on 2019.09.27)
rpm -ivh /tmp/vagrant_*.rpm
```

install on ubuntu
```
write soon
```

setup
```
vagrant plugin install vagrant-libvirt
vagrant box add centos/7
vagrant box add ubuntu/bionic64
```

## sample manufests

### virtualbox backend
```
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic64"
  config.disksize.size = '20GB' # vagrant plugin install vagrant-disksize

  config.vm.provider "virtualbox" do |vb|
    vb.cpus = 2
    vb.memory = "4000"
  end

  config.vm.define "vm" do |vm|
    vm.vm.hostname = "vm"
    vm.vm.network "private_network", ip: "192.168.33.10"
  end
end
```

### libvirt backend

```
# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.define "hv00" do |node|
      node.vm.hostname = "hv00"
      node.vm.provider :libvirt do |v|
          v.cpus = 4
          v.cpu_mode = "host-passthrough"
          v.memory = 8000
      end
      node.vm.network :private_network,
        :ip => "192.168.99.10",
        :libvirt__guest_ipv6 => "yes"
  end
  config.vm.define "hv01" do |node|
      node.vm.hostname = "hv01"
      node.vm.provider :libvirt do |v|
          v.cpus = 4
          v.cpu_mode = "host-passthrough"
          v.memory = 8000
      end
      node.vm.network :private_network,
        :ip => "192.168.99.11",
        :libvirt__guest_ipv6 => "yes"
  end
end #|config|
```

### networking

- ref: https://github.com/vagrant-libvirt/vagrant-libvirt#private-network-options

private network (virtualbox)
```
Vagrant.configure("2") do |config|
  config.vm.define "tst" do |node|
		node.vm.network "private_network", ip: "192.168.99.10"
  end
  config.vm.define "dut" do |node|
		node.vm.network "private_network", ip: "192.168.99.11"
  end
end
```

private network (libvirt)
```
Vagrant.configure("2") do |config|
  config.vm.define "hv00" do |node|
      node.vm.network :private_network,
        :ip => "192.168.99.10",
        :libvirt__guest_ipv6 => "yes"
  end
  config.vm.define "hv01" do |node|
      node.vm.network :private_network,
        :ip => "192.168.99.11",
        :libvirt__guest_ipv6 => "yes"
  end
end
```

private network (`auto_config:false`)
```
host$ cat Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "centos/7"
  config.vm.define :node1 do |node|
    node.vm.network :private_network, ip:"192.168.33.11", auto_config:false
  end
end

host$ vagrant reload
host$ vagrant ssh
vm$ ip a
...(snip)...
3: enp0s8: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 08:00:27:c7:09:b0 brd ff:ff:ff:ff:ff:ff
    inet6 fe80::a00:27ff:fec7:9b0/64 scope link
       valid_lft forever preferred_lft forever
```

provision script from file
```
$ cat Vagrantfile
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/bionic"
  config.vm.provision :shell, path: "setup.sh"
end

$ cat setup.sh
apt update
apt install -y nginx

$ vagrant destroy -f && vagrant up
$ vagrant provision
```

provision script inline version
```
Vagrant.configure("2") do |config|
	config.vm.box = "ubuntu/bionic"
	config.vm.provision :shell, inline: $script
end

$script = <<END
apt update
apt install -y nginx
END
```

## Good references

- explanation how to use vagrant-libvirt simply by manji-san
  https://qiita.com/manji0/items/d1ab7a0c134ed0e32b3f
- specifications are listed.
  https://github.com/vagrant-libvirt/vagrant-libvirt#libvirt-configuration

