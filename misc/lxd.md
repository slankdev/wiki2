
# LXD/LXC

install
```
$ sudo apt install lxd
$ sudo lxd init
$ sudo gpassword -a <user> lxd
```

basic commands
```
$ lxc list
$ lxc image list
$ lxc init <ubuntu:16.04>  // 取得のみ
$ lxc launch <ubuntu:16.04> [<container>]  // 取得&起動
$ lxc launch ubuntu:14.04 c1
$ lxc launch ubuntu:75182b1241be c3
$ lxc start <container>
$ lxc stop <container>
$ lxc stop <container> [--force]
$ lxc restart <container> [--force]
$ lxc pause <container>
$ lxc delete <container>
$ lxc exec <container> <command>
$ lxc copy <src-container> <dst-container>
$ lxc move <src-container> <dst-container> // renamable
```

Make original container image
```
$ lxc launch ubuntu:14.04 tmp
$ lxc exec tmp bash
container$ apt install -y quagga
container$ cp /usr/share/doc/quagga/bgpd.conf.sample /etc/quagga/bfgpd.conf
container$ cp /usr/share/doc/quagga/ospfd.conf.sample /etc/quagga/ospfd.conf
container$ exit
$ lxc stop tmp
$ lxc publish tmp --alias newimage
$ lxc delete tmp
```

