
# ISC-DHCP server

```
$ sudo apt install isc-dhcp-server
$ vim /etc/dhcp/dhcpd.conf
$ sudo systemctl enable isc-dhcp-server
$ sudo systemctl start isc-dhcp-server
```

config example
```
subnet 10.0.0.0 netmask 255.255.0.0 {
	range 10.0.1.0 10.0.1.255;
  option routers 10.0.0.1;
  option domain-name-servers 8.8.8.8, 8.8.4.4;

	host jk3 {
		hardware ethernet 52:54:00:e9:ee:38;
		fixed-address 10.0.0.4;
	}

	host jk5 {
		hardware ethernet
		fixed-address 10.0.0.5;
	}
}

```

## References

- http://maruchan-shiro123.hatenablog.com/entry/2015/04/05/112530


