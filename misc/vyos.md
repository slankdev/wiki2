
# VyOS Setup

```
$ install image
```

1. システムの設定
1. インターフェースの設定

- set/delete
- show/compare/commit/save
	- commit 設定の反映 (再起動前まで反映)
	- save 起動時設定に反映

## NAPT Router

Basic system configuration

```
$ configure
# set system login user root
# set system login user vyos authentication plaintext-password <pass>
# set interfaces ethernet eth0 address 10.0.0.2/16
# set interfaces ethernet eth1 address 192.168.10.1/24
# set service ssh
# commit
# save
```

NAPT Router Configuration

```
> ssh vyos@10.0.0.2
$ configure
# set system time-zone Asia/Tokyo
# set interfaces ethernet eth0 address 10.0.0.2/16
# set interfaces ethernet eth0 description 'UpperSide'
# set system host-name <hostname>
# set system gateway-address 10.0.0.1
# set nat source rule 100 source address 192.168.10.0/24
# set nat source rule 100 translation address masquaerade
# set nat source rule 100 outbound-interface eth0
# commit
# save
```

```
# delete interfaces ethernet eth0 address
# delete interfaces ethernet eth0 description
```

## VXLAN

```
# set interfaces vxlan vxlan0
# set interfaces vxlan vxlan0 group 239.0.0.1
# set interfaces vxlan vxlan0 link eth0
# set interfaces vxlan vxlan0 vni 100

# set interfaces bridge br0
# set interfaces ethernet eth1 bridge-group bridge br0
# set interfaces vxlan vxlan0 bridge-group bridge br0
```

## Port Forwarding

to eth0:2222 from WAN -> 192.168.1.3:22

```
# set nat destination rule 20 inbound-interface eth0
# set nat destination rule 20 destination port 2222
# set nat destination rule 20 protocol tcp
# set nat destination rule 20 translation port 22
# set nat destination rule 20 translation address 192.168.10.3
```


