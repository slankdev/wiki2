
# Debian Package

```
sudo apt update && sudo apt install -y devscripts build-essential
```

```
dpkg -c build-root/vpp-plugin-core_19.08-rc0~439-g10522f266_amd64.deb
drwxr-xr-x root/root         0 2019-07-20 10:30 ./
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/lib/
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/lib/x86_64-linux-gnu/
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/lib/x86_64-linux-gnu/vpp_plugins/
-rw-r--r-- root/root     73136 2019-07-20 10:30 ./usr/lib/x86_64-linux-gnu/vpp_plugins/cplane_netdev_plugin.so
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/share/
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/share/doc/
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/share/doc/vpp-plugin-core/
-rw-r--r-- root/root       146 2019-07-20 10:30 ./usr/share/doc/vpp-plugin-core/changelog.Debian.gz
-rw-r--r-- root/root       263 2019-06-24 02:22 ./usr/share/doc/vpp-plugin-core/copyright
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/share/vpp/
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/share/vpp/api/
drwxr-xr-x root/root         0 2019-07-20 10:30 ./usr/share/vpp/api/plugins/
-rw-r--r-- root/root      2198 2019-07-20 10:30 ./usr/share/vpp/api/plugins/cplane_netdev.api.json

dpkg { -I | --info } build-root/vpp-plugin-core_19.08-rc0~439-g10522f266_amd64.deb
 new Debian package, version 2.0.
 size 20128 bytes: control archive=668 bytes.
     350 bytes,    11 lines      control
     336 bytes,     4 lines      md5sums
 Package: vpp-plugin-core
 Source: vpp
 Version: 19.08-rc0~439-g10522f266
 Architecture: amd64
 Maintainer: fd.io VPP Packaging Team <vpp-dev@fd.io>
 Installed-Size: 89
 Depends: vpp (= 19.08-rc0~439-g10522f266), libc6 (>= 2.4)
 Section: net
 Priority: extra
 Description: Vector Packet Processing--runtime core plugins
  This package contains VPP core plugins
```

```
apt update
apt install -y <hoge>
apt install -d ./package.deb # download depen
dpkg -i package.deb
dpkg -r package.deb
dpkg --purge package.deb
apt policy meson  # check version policy
apt-cache madison meson # check which version can be installed
```

```
clean_debian:
  rm -f  debian/routerd.substvars
  rm -f  debian/debhelper-build-stamp
  rm -rf debian/routerd
  rm -rf debian/output

debian_package:
  debuild -uc -us
  mkdir -p debian/output
  mv ../routerd-dbgsym_*.ddeb debian/output/
  mv ../routerd_*.dsc debian/output/
  mv ../routerd_*.tar.gz debian/output/
  mv ../routerd_*.build debian/output/
  mv ../routerd_*.buildinfo debian/output/
  mv ../routerd_*.changes debian/output/
  mv ../routerd_*.deb debian/output/
```

```
kernel-dev:~/git/routerd/debian:( cat changelog
routerd (0.0.0) Hiroki Shirokura; urgency=medium

  * Initial release. (Under the developing)

 --  <slankdev@coe.ad.jp>  Sun, 24 Feb 2019 11:20:00 +0900
```

```
kernel-dev:~/git/routerd/debian:) cat compat
10
```

```
kernel-dev:~/git/routerd/debian:) cat control
Source: routerd
Priority: optional
Maintainer: Hiroki Shirokura <slankdev@coe.ad.jp>
Build-Depends: debhelper (>=5), libjson-c-dev (>= 0.12.1-1.3)
Standards-Version: 0.0.0
Homepage: https://github.com/slankdev

Package: routerd
Architecture: any
Depends:
Description: netlink monitor for special d-plane
```

```
kernel-dev:~/git/routerd/debian:) cat copyright
This package was debianized by Hiroki Shirokura <slankdev@coe.ad.jp> on
Thu, 24 Feb 2019 11:40:00 +0900.

Upstream Author(s):

    Hiroki Shirokura <slankdev@coe.ad.jp>

Copyright:

    Copyright(C) 2019 Hiroki Shirokura

License:

                MIT License

                Permission is hereby granted, free of charge, to any person obtaining a copy
                of this software and associated documentation files (the "Software"), to deal
                in the Software without restriction, including without limitation the rights
                to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                copies of the Software, and to permit persons to whom the Software is
                furnished to do so, subject to the following conditions:

                The above copyright notice and this permission notice shall be included in all
                copies or substantial portions of the Software.

                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                SOFTWARE.


The Debian packaging is (C) 2019, Hiroki Shirokura <slankdev@coe.ad.jp> and
is licensed under the MIT, see `/usr/share/common-licenses/MIT'.
```

```
kernel-dev:~/git/routerd/debian:) cat files
routerd-dbgsym_0.0.0_amd64.ddeb debug optional
routerd_0.0.0_amd64.buildinfo - optional
routerd_0.0.0_amd64.deb - optional
```

```
kernel-dev:~/git/routerd/debian:) cat rules
#!/usr/bin/make -f
%:
        dh $@

# include /usr/share/cdbs/1/rules/debhelper.mk
# include /usr/share/cdbs/1/class/autotools.mk
#
# DEB_INSTALL_DIRS_groonga = /usr/bin
#
# install/srdump::
#       cp -ar debian/tmp/usr/bin/* debian/srdump/usr/bin/

override_dh_auto_install:
        mkdir -p `pwd`/debian/routerd/etc/routerd
        mkdir -p `pwd`/debian/routerd/etc/systemd/system
        install -D -m 0755 routerd.out `pwd`/debian/routerd/usr/local/bin/routerd
        cp -f root/etc/routerd/config.json `pwd`/debian/routerd/etc/routerd/config.json
        cp -f root/etc/systemd/system/routerd.service `pwd`/debian/routerd/etc/systemd/system/routerd.service
        # systemctl daemon-reload

# uninstall:
#       rm -f /usr/local/bin/routerd
#       rm -f /etc/routerd/config.json
#       rm -f /etc/systemd/system/routerd.service
#       systemctl daemon-reload

override_dh_usrlocal:
        install -D -m 0755 routerd.out `pwd`/debian/routerd/usr/local/bin/routerd
```
