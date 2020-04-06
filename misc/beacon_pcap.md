# すべてのパケットをキャプチャする
Security Mini Camp in Nigata 
2015.05.16-17
by Honma


## capture all packet using aircrack-ng
### service  stop 

	$ sudo service network-manager stop
	$ sudo service avahi-daemon stop
	$ sudo killall wpa_supplicant

### airmon-ng setting

	$ sudo airmon-ng stop wlan0
	$ sudo airmon-ng start wlan0 5882  ifconfig -a

### capture 

	$ sudo wireshark
	$ exit

### if channel change then
	
	$ sudo ip link set dev wlan0 down
	$ sudo iw dev wlan0 set channel 1
	$ sudo ip link set dev wlan0 up



