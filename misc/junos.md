
# JUNOS

initial
```
set system root-authentication plain-text-password
delete chassis auto-image-upgrade
commit check
commit
```

```
set system host-name CHIKUWA01
set system services ssh
set system login user slankdev class super-user
set system login user slankdev authentication plain-text-password
set system login user slankdev authentication ssh-rsa <public-key-str>
```

```
request system <power-off|reboot>
request vmhost <power-off|reboot>
request system license add terminal
show system license
```

load from terminal (copy-and-paste)
```
# load terminal
# load set terminal
[Type ^D at a new line to end input]
set interface lt-0/0/10 unit 0 family inet addr 1.1.1.1/24
^D

# load merge terminal
[Type ^D at a new line to end input]
interface {
  lt-0/0/10 {
		unit 0 {
			family inet {
				addr {
					1.1.1.1/24
				}
			}
		}
	}
}
^D
```

mgmt ethernet
```
set interfaces em0  unit 0 family inet dhcp  // qfx
set interfaces me0  unit 0 family inet dhcp  // ex
set interfaces fxp0 unit 0 family inet dhcp  // mx
```

l-sys
```
set chassis fpc 0 pic 0 tunnel-service bandwidth 1g
set logical-systems R1
set logical-systems R1 interface lt-0/0/0 unit 10 encapsulation ethernet
set logical-systems R1 interface lt-0/0/0 unit 10 peer-unit 11
set logical-systems R2
set logical-systems R2 interface lt-0/0/0 unit 11 encapsulation ethernet
set logical-systems R2 interface lt-0/0/0 unit 11 peer-unit 10

set cli logical-system R1
clear cli logical-system
```

Tips
```
show system users
rsh -JU __juniper_private4__ 192.168.1.1
```

insert config
```
// current
set firewall family inet filter FILTER01 term TERM10 from source-address 10.0.0.1/32
set firewall family inet filter FILTER01 term TERM10 from destination-address 192.168.1.0/24
set firewall family inet filter FILTER01 term TERM10 from tcp-established
set firewall family inet filter FILTER01 term TERM10 then accept
set firewall family inet filter FILTER01 term TERM20 then count COUNTER20
set firewall family inet filter FILTER01 term TERM20 then discard

// config
set firewall family inet filter FILTER01 term TERM15 from source-address 10.0.0.2/32
set firewall family inet filter FILTER01 term TERM15 from destination-address 192.168.1.0/24
set firewall family inet filter FILTER01 term TERM15 from protocol tcp
set firewall family inet filter FILTER01 term TERM15 from destination-port 20-21
set firewall family inet filter FILTER01 term TERM15 then accept
insert firewall family inet filter FILTER01 term TERM15 after TERM10

// result
set firewall family inet filter FILTER01 term TERM10 from source-address 10.0.0.1/32
set firewall family inet filter FILTER01 term TERM10 from destination-address 192.168.1.0/24
set firewall family inet filter FILTER01 term TERM10 from tcp-established
set firewall family inet filter FILTER01 term TERM10 then accept
set firewall family inet filter FILTER01 term TERM15 from source-address 10.0.0.2/32
set firewall family inet filter FILTER01 term TERM15 from destination-address 192.168.1.0/24
set firewall family inet filter FILTER01 term TERM15 from protocol tcp
set firewall family inet filter FILTER01 term TERM15 from destination-port 20-21
set firewall family inet filter FILTER01 term TERM15 then accept
set firewall family inet filter FILTER01 term TERM20 then count COUNTER20
set firewall family inet filter FILTER01 term TERM20 then discard
```

change working configuration-position
```
edit interface lt-0/0/10
set unit 10 description hoge
top
up
```

## reset factory-default

```
configure
load factory-default
commit
set system root-authentication plain-text-password
commit
```

