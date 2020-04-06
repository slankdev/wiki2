
# Cumulus Linux

## NCLU / Network Command Line Utility

```
net add hostname sn2700
net add vrf vrf0
net add interface swp0 ip address 10.0.0.2/24
net add interface swp0 ip gateway 10.0.0.1
net add interface swp0 mtu 9000
net add interface swp0 vrf vrf0
```

```
net add bgp router-id 1.1.1.1/32
net add routing route 1.1.1.2/32 10.0.1.2
net del routing route 1.1.1.2/32 10.0.1.2
net add routing route 1.1.1.2/32 10.0.1.2 vrf vrf0
net add routing route 0.0.0.0/0 10.0.1.2
```

```
net pending
net commit
net abort
net show configuration
```

## switchd

```
cat /etc/cumulus/switchd.conf
systemctl restart switchd
```

## References

- https://docs.cumulusnetworks.com/version/cumulus-linux-35/Layer-3/Virtual-Routing-and-Forwarding-VRF/
- https://docs.ansible.com/ansible/latest/modules/nclu_module.html
- https://www.apresiatac.jp/blog/20190329984/
