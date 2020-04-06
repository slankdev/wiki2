
# Cisco IOS / IOS-XR / IOS-XE

```
show l2vpn bridge-domain bd-name CUSTOMER1
```

initial check
```
show version
admin
show platform [node-id]
exit
show redundancy
show environment
```

user
```
hostname asr99901
username slankdev
 group root-lr
 group cisco-support
 secret 0 password-text

interface MgmtEth0/RSP0/CPU0/0
 ipv4 address dhcp

ipv4 access-list PERMIT-SSH
 10 permit ipv4 192.168.99.1/24 any

ssh server v2
ssh server vrf default ipv4 access-list PERMIT-SSH
```

## VRF Route-Leak examle (thx yas-nyan)

blue -> red

```
vrf red
 rd 100:100
 address-family ipv4 unicast
  import route-target
   1:0
  !
 !
!
vrf blue
 rd 100:200
 address-family ipv4 unicast
  export route-target
   1:0
  !
 !
!

router bgp 65535
 bgp router-id 192.0.2.2

 address-family vpnv4 unicast
 !
 vrf red
  address-family ipv4 unicast
  !
 !
 vrf blue
  address-family ipv4 unicast
  redistribute static route-policy ACCEPT_ANY
  redistribute connected route-policy ACCEPT_ANY
  !
 !
!
route-policy ACCEPT_ANY
 pass
end-policy
!
```

