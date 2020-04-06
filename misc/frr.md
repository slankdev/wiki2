
# FRR / Quagga

```
$ sudo apt install quagga
$ cd /etc/quagga
$ sudo cp /usr/share/doc/quagga/examples/zebra.conf.sample  zebra.conf
$ sudo cp /usr/share/doc/quagga/examples/bgpd.conf.sample  bgpd.conf
$ sudo cp /usr/share/doc/quagga/examples/ospfd.conf.sample ospfd.conf
$ cat daemons
zebra=yes
bgpd=yes
ospfd=yes
ospf6d=no
ripd=no
ripngd=no
isisd=no
babeld=no
$ sudo systemctl restart quagga
$ telnet localhost 2601 // zebra
$ telnet localhost 2605 // bgpd
```

## BGPd

```
$ telnet localhost 2605
bgpd> en
bgpd# show ip bgp summary
bgpd# show ip bgp neighbor
```

```
$ cat /etc/quagga/bgpd.conf

...
router bgp 100
 bgp router-id 3.3.3.3
 neighbor 10.9.0.1 remote-as 500
 neighbor 10.4.0.2 remote-as 200
...

```

## VTYSH

```
$ export VTYSH_PAGER=more
vtysh# show yang operational-data /frr-ripd:ripd
```

## Good Examples

- https://gist.github.com/rwestphal
- frr-isis-sr-6r.yml https://gist.github.com/rwestphal/f10601e4a86ca2b00eb842d182559b17
- frr-isis-sr-grid-10x10.yml https://gist.github.com/rwestphal/faf01418f47c7c1dd33152b2a31327da
- frr-isis-sr-vpls.yml https://gist.github.com/rwestphal/532566e2ce004e3f397aa53cb68d17de
- frr-isis-sr-vpnv6.yml https://gist.github.com/rwestphal/6e921f204fd9ac3893a0d3277978e3a7
- frr-isis-sr.yml https://gist.github.com/rwestphal/08f6dd65db89ee68f15f770f3aa000d2
- frr-osif-sr-bfd.yml https://gist.github.com/rwestphal/414ce64e2c45fbf7482d128444bff40f
- frr-l3vpn-isis-ppr.yml https://gist.github.com/rwestphal/68f6e8962746566cdef35d6311f2b366
- ppr-dataplane-v6-native.yml https://gist.github.com/rwestphal/1f21d83324bed58c29c0e15167814fcf
- frr-ospf-sr.yml https://gist.github.com/rwestphal/9fc59b2bc055371f9814c84e9472e3f4
- frr-bgp-l3vpn-gre.yml https://gist.github.com/rwestphal/931f070240ffffebc2213f5d5fbefcb7
- show yang operational-data https://gist.github.com/rwestphal/a185eb52c8016fd3ccfea763d040db04

## Install

fedora:24 (http://docs.frrouting.org/projects/dev-guide/en/latest/building-frr-for-fedora.html)
build rpm package
```
dnf remove vim-minimal
dnf install -y wget vim git autoconf automake libtool make \
  readline-devel texinfo net-snmp-devel groff pkgconfig json-c-devel \
  pam-devel python3-pytest bison flex c-ares-devel python3-devel \
  python3-sphinx perl-core patch systemd-devel libcap-devel \
  python python-devel python-sphinx rpm-build

wget https://ci1.netdef.org/artifact/LIBYANG-YANGRELEASE/shared/build-10/Fedora-24-x86_64-Packages/libyang-0.16.111-0.x86_64.rpm
wget https://ci1.netdef.org/artifact/LIBYANG-YANGRELEASE/shared/build-10/Fedora-24-x86_64-Packages/libyang-debuginfo-0.16.111-0.x86_64.rpm
wget https://ci1.netdef.org/artifact/LIBYANG-YANGRELEASE/shared/build-10/Fedora-24-x86_64-Packages/libyang-devel-0.16.111-0.x86_64.rpm
dnf install *.rpm -y

git clone https://github.com/frrouting/frr.git frr && cd frr
./bootstrap.sh
./configure --with-pkg-extra-version=-slankdev
make dist

mkdir rpmbuild
mkdir rpmbuild/SOURCES
mkdir rpmbuild/SPECS
cp redhat/*.spec rpmbuild/SPECS/
cp frr*.tar.gz rpmbuild/SOURCES/

vim rpmbuild/SPECS/frr.spec
rpmbuild --define "_topdir `pwd`/rpmbuild" -ba rpmbuild/SPECS/frr.spec
```

my favorite frr.spec
```
#################### FRRouting (FRR) configure options #####################
# with-feature options
%{!?with_babeld:        %global  with_babeld        0 }
%{!?with_bfdd:          %global  with_bfdd          0 }
%{!?with_bgp_vnc:       %global  with_bgp_vnc       0 }
%{!?with_cumulus:       %global  with_cumulus       0 }
%{!?with_eigrpd:        %global  with_eigrpd        1 }
%{!?with_fpm:           %global  with_fpm           0 }
%{!?with_ldpd:          %global  with_ldpd          0 }
%{!?with_multipath:     %global  with_multipath     256 }
%{!?with_nhrpd:         %global  with_nhrpd         0 }
%{!?with_ospfapi:       %global  with_ospfapi       0 }
%{!?with_ospfclient:    %global  with_ospfclient    0 }
%{!?with_pam:           %global  with_pam           0 }
%{!?with_pbrd:          %global  with_pbrd          0 }
%{!?with_pimd:          %global  with_pimd          0 }
%{!?with_vrrpd:         %global  with_vrrpd         0 }
%{!?with_rpki:          %global  with_rpki          0 }
%{!?with_rtadv:         %global  with_rtadv         0 }
%{!?with_watchfrr:      %global  with_watchfrr      0 }

# user and group
%{!?frr_user:           %global  frr_user           frr }
%{!?vty_group:          %global  vty_group          frrvty }

# path defines
%define     configdir   %{_sysconfdir}/%{name}
%define     _sbindir    /usr/lib/frr
%define     zeb_src     %{_builddir}/%{name}-%{frrversion}
%define     zeb_rh_src  %{zeb_src}/redhat
%define     zeb_docs    %{zeb_src}/doc
%define     frr_tools   %{zeb_src}/tools

# defines for configure
%define     rundir  %{_localstatedir}/run/%{name}

############################################################################
```

my favorite configure options
```
./configure \
  --prefix=/usr \
  --includedir=\${prefix}/include \
  --enable-exampledir=\${prefix}/share/doc/frr/examples \
  --bindir=\${prefix}/bin \
  --sbindir=\${prefix}/lib/frr \
  --libdir=\${prefix}/lib/frr \
  --libexecdir=\${prefix}/lib/frr \
  --localstatedir=/var/run/frr \
  --sysconfdir=/etc/frr \
  --with-moduledir=\${prefix}/lib/frr/modules \
  --with-libyang-pluginsdir=\${prefix}/lib/frr/libyang_plugins \
  --enable-configfile-mask=0640 \
  --enable-logfile-mask=0640 \
  --enable-snmp=agentx \
  --enable-multipath=64 \
  --enable-user=frr \
  --enable-group=frr \
  --enable-vty-group=frrvty \
  --with-pkg-git-version \
  \
  --disable-ripd     \
  --disable-ripngd   \
  --disable-ospfd    \
  --disable-ospf6d   \
  --disable-ldpd     \
  --disable-nhrpd    \
  --disable-eigrpd   \
  --disable-babeld   \
  --disable-isisd    \
  --disable-pimd     \
  --disable-pbrd     \
  --disable-fabricd  \
  --disable-vrrpd
```

start frr
```
/usr/lib/frr/frr start           #(1) old
/usr/lib/frr/frrinit.sh start    #(2) new
```

configure options
```
## You can choose.
--disable-zebra
--disable-bgpd
--disable-ripd
--disable-ripngd
--disable-ospfd
--disable-ospf6d
--disable-ldpd
--disable-nhrpd
--disable-eigrpd
--disable-babeld
--disable-watchfrr
--disable-isisd
--disable-pimd
--disable-pbrd
--enable-sharpd
--disable-staticd
--disable-fabricd
--disable-vrrpd
--disable-bgp-announce
--disable-bgp-vnc
--disable-bgp-bmp
--enable-snmp
--enable-config-rollbacks
```

## Debugging

enable logging to file
```
vtysh -c 'conf term' -c 'log file /tmp/frr.log debugging'
tail -f /tmp/frr.log
```

