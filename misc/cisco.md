
# Cisco 1812J

## Initial Connect

```
$ sudo screen /dev/ttyUSB0 9600
```

## password

enable
```
# configure terminal
(config)# enable password <pass>
(config)# exit
```

console
```
> enable
# configure terminal
(config)# line console 0
(config-line)# password <pass>
(config-line)# login
```

vty
```
> enable
# configure terminal
(config)# line vty 0 4
(config-line)# password <pass>
(config-line)# login
```

## WAN Port Config

```
R> enable
R# configure terminal
R(config)#

R(config)# hostname R
R(config)# no ip domain-lookup
R(config)# line console 0
R(config-line)# logging synchronous

R(config)# interface fastEthernet 0
R(config-if)# ip address 133.25.196.30 255.255.254.0
R(config-if)# no shutdown
R(config-if)# description WAN-Port
R(config-if)# exit
R(config)# ip route 0.0.0.0 0.0.0.0 133.25.196.1

R(config)# line vty 0 4
R(config-line)# password PASS0
R(config-line)# login
R(config)# enable password PASS1
```


## LAN Port Config

```
R(config)# interface vlan 1
R(config-if)# ip address 10.0.0.1 255.255.0.0

R(config)# interface fastEthernet 2
R(config-if)# switchport mode access
R(config-if)# switchport access vlan 1
R(config-if)# no shutdown

R(config)# interface fastEthernet 3
R(config-if)# switchport mode access
R(config-if)# switchport access vlan 1
R(config-if)# no shutdown

R(config)# interface fastEthernet 4
R(config-if)# switchport mode access
R(config-if)# switchport access vlan 1
R(config-if)# no shutdown

R(config)# interface fastEthernet 5
R(config-if)# switchport mode access
R(config-if)# switchport access vlan 1
R(config-if)# no shutdown
```


## DHCP Server Config

```
R(config)# service dhcp
R(config)# ip dhcp excluded-address 10.0.0.1 10.0.1.0
R(config)# ip dhcp pool CLIENT
R(dhcp-config)# network 10.0.0.0 255.255.0.0
R(dhcp-config)# import all
R(dhcp-config)# default-router 10.0.0.1
R(dhcp-config)# dns-server 133.25.243.11 133.25.251.10
R(dhcp-config)# lease 6
R(dhcp-config)# exit
```


## PAT Config

```
R(config)#ip nat pool TEST 133.25.196.30 133.25.196.30 netmask 255.255.254.0
R(config)#access-list 1 permit 10.0.0.0 0.0.255.255
R(config)#ip nat inside source list 1 pool TEST overload

R(config)#interface vlan 1
R(config-if)#ip nat inside

R(config)#interface fastEthernet 0
R(config-if)#ip nat out
```

Extra Port Forwarding
```
R(config)# ip nat inside source static tcp 10.0.0.2 22 133.25.196.30 22
```


## Save/Reset Configuration

- startup-config
- running-config

Save
```
R# copy running-config startup-config
R# show startup-config
```

Reset
```
R# erase startup-config
R# reload <- reboot router
```


## Show Stats

```
R# show ip interface fastEthernet 0
R# show ip route
R# show ip nat translations
R# show ip dhcp binding
```





