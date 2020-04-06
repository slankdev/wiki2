
# Open vSwitch

install

```
$ sudo apt install openvswitch-switch openvswitch-common
```

basic operations

```
# ovs-vsctl show
# ovs-vsctl add-br <switch>
# ovs-vsctl add-port <switch> <port>
# ovs-vsctl del-port <switch> <port>
# ovs-vsctl set-manager ptcp:6632

# ovs-vsctl list port <switch>

# ovs-ofctl show <switch>
OFPT_FEATURES_REPLY (xid=0x2): dpid:0000a0369f391a68
n_tables:254, n_buffers:256
capabilities: FLOW_STATS TABLE_STATS PORT_STATS QUEUE_STATS ARP_MATCH_IP
actions: output enqueue set_vlan_vid set_vlan_pcp strip_vlan mod_dl_src mod_dl_dst mod_nw_src mod_nw_dst mod_nw_tos mod_tp_src mod_tp_dst
 1(eth2): addr:a0:36:9f:39:1a:68
     config:     0
     state:      0
     current:    10GB-FD COPPER AUTO_NEG
     advertised: 100MB-FD 1GB-FD 10GB-FD COPPER AUTO_NEG
     supported:  1GB-FD 10GB-FD COPPER AUTO_NEG
     speed: 10000 Mbps now, 10000 Mbps max
 2(eth3): addr:a0:36:9f:39:1a:6a
     config:     0
     state:      0
     current:    10GB-FD COPPER AUTO_NEG
     advertised: 100MB-FD 1GB-FD 10GB-FD COPPER AUTO_NEG
     supported:  1GB-FD 10GB-FD COPPER AUTO_NEG
     speed: 10000 Mbps now, 10000 Mbps max
 LOCAL(ovs0): addr:a0:36:9f:39:1a:68
     config:     PORT_DOWN
     state:      LINK_DOWN
     speed: 0 Mbps now, 0 Mbps max
OFPT_GET_CONFIG_REPLY (xid=0x4): frags=normal miss_send_len=0

# ovs-ofctl dump-flows <switch>
# ovs-ofctl add-flow <switch> in_port=1,actions=output:2
# ovs-ofctl add-flow <switch> arp,actions=all
# ovs-ofctl add-flow br100 \
	dl_src=aa:aa:aa:bb:bb:bb, \
	actions=mod_dl_src=11:11:11:22:22:22,output:all
```

## ovs-ofctl

```
in_port,
dl_vlan, dl_vlan_pcp, dl_src, dl_dst, dl_type,
nw_src, nw_dst, nw_proto, nw_tos, nw_ecn, nw_ttl,
tp_src, tp_dst,
icmp_type, icmp_code,
ipv6_src, ipv6_dst, ipv6_label,
arp_sha, arp_tha,
table, vlan_tci, ip_frag,
nd_target, nd_sll,
nd_tll, tun_id, regX
```
```
#!/bin/sh
BR=ovs0

ovs-ofctl del-flows $BR
ovs-ofctl add-flow $BR dl_type=0x0806,actions=drop
ovs-ofctl add-flow $BR in_port=1,actions=output:2
ovs-ofctl add-flow $BR in_port=2,actions=output:1
ovs-ofctl add-flow $BR actions=drop
ovs-ofctl dump-flows $BR
```

## Add VM's NIC to OVS

VMのconfigに追加
```
# virsh edit vm0
+   <interface type='bridge'>
+     <source bridge='ovs0'/>
+     <virtualport type='openvswitch'/>
+   </interface>
```

## VXLAN

```
# ovs-vsctl add-br ovs0
# ovs-vsctl add-port ovs0 eth0 tag=100
# ovs-vsctl add-port ovs0 vxlan0 tag=100 \
	-- set interface vxlan0 type=vxlan     \
	options:key=100                        \
	options:remote_ip=172.16.100.1
# ovs-vsctl list interface vxlan0
```

if up/down
```
auto-ovs ovs0
iface ovs0 inet static
  ovs_type OVSBridge
	ovs_ports eth0 vxlan0

auto vxlan0
iface vxlan0 inet manual
  ovs_bridge ovs0
	ovs_type OVSTunnel
	ovs_options tag=100
	ovs_tunnel_type vxlan
	ovs_tunnel_options options:key=100 options:remote_ip=133.25.196.23

auto eth0
iface eth0 inet manual
	ovs_bridge ovs0
	ovs_type OVSPort
	ovs_options tag=100
```

- http://komeiy.hatenablog.com/entry/2014/10/26/225654


# OVS-dpdk

Using OVS builed ourselves is better than apt-installed ovs, I think.
Because apt-installed DPDK is not stable and not-usefull than original-DPDK.
Building and Installing OVS from source code is easy and simple,
so you should choice it.

```
$ git clone http://github.com/openvswitch/ovs
$ cd ovs
...
```

Start OVS Shell Script

```
#!/bin/sh

BR=ovs0

killall ovsdb-server ovs-vswitchd
rm   -rf /tmp/openvswitch
mkdir -p /tmp/openvswitch
rm -f /usr/local/var/run/openvswitch/conf.db

ovsdb-tool create \
    /usr/local/var/run/openvswitch/conf.db \
    /usr/local/share/openvswitch/vswitch.ovsschema

ovsdb-server \
    --remote=punix:/usr/local/var/run/openvswitch/db.sock \
    --remote=db:Open_vSwitch,Open_vSwitch,manager_options --pidfile --detach

ovs-vsctl --no-wait init
ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-lcore-mask=0x3f
ovs-vsctl --no-wait set Open_vSwitch . other_config:pmd-cpu-mask=0x30
ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-socket-mem=1024,0
ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true
ovs-vswitchd unix:/usr/local/var/run/openvswitch/db.sock --pidfile
```

Create OVS-dpdk instance Shell Script

```
#!/bin/sh

BR=ovs0
ovs-vsctl del-br $BR
ovs-vsctl add-br $BR -- set bridge $BR datapath_type=netdev
ovs-vsctl add-port $BR dpdk0 -- set Interface dpdk0 type=dpdk options:dpdk-devargs=0000:3b:00.0
ovs-vsctl add-port $BR dpdk1 -- set Interface dpdk1 type=dpdk options:dpdk-devargs=0000:3b:00.1
ovs-vsctl add-port $BR vhost_user0 -- set Interface vhost_user0 type=dpdkvhostuser
ovs-vsctl add-port $BR vhost_user1 -- set Interface vhost_user1 type=dpdkvhostuser
ip link set $BR up
```

## QEMU w/ vhost-user

```

#!/bin/sh

sudo qemu-system-x86_64 \
    -cpu host -enable-kvm -m 4000M -hda vm0.img \
    -object memory-backend-file,id=mem,size=4000M,mem-path=/dev/hugepages,share=on \
    -numa node,memdev=mem -mem-prealloc -smp sockets=1,cores=2 \
    -net nic -net tap,ifname=vtap0,script=./ifup.sh \
    -vnc :5,password -monitor stdio \
    \
    -chardev socket,id=chr0,path=/usr/local/var/run/openvswitch/vhost_user1  \
    -netdev type=vhost-user,id=net0,chardev=chr0,vhostforce,queues=1 \
    -device virtio-net-pci,netdev=net0,mrg_rxbuf=off \
    \
    -chardev socket,id=chr1,path=/usr/local/var/run/openvswitch/vhost_user2  \
    -netdev type=vhost-user,id=net1,chardev=chr1,vhostforce,queues=1 \
    -device virtio-net-pci,netdev=net1,mrg_rxbuf=off
```

## KVM w/ vhost-user

- vhost.sock should be placed on `/var/lib/libvirt/qemu/`..?
- vhost.sock should be set permission as `root:libvirt` ...? --> `root:root` was ok... :(

```
    <memory unit='KiB'>1048576</memory>
    <currentMemory unit='KiB'>1048576</currentMemory>

+   <memoryBacking><hugepages/></memoryBacking>

+   <cpu mode='host-passthrough'>
+     <numa>
+       <cell id='0' cpus='0' memory='1048576' unit='KiB' memAccess='shared'/>
+     </numa>
+   </cpu>

+ <interface type='vhostuser'>
+     <source type='unix' path='/var/lib/libvirt/qemu/vhost_user0.sock' mode='client'/>
+     <model type='virtio'/>
+ </interface>
```

## Vhost-user Trouble Shooting

- invalid socket-file path
```
error: internal error: process exited while connecting to monitor: 2019-08-05T07:36:56.146971Z qemu-system-x86_64: -chardev socket,id=charnet1,path=/tmp/vhost2.sock: Failed to connect socket /tmp/vhost2.sock: No such file or directory
```

- kvm and qemu's persmission setting is invalid.
- http://docs.openvswitch.org/en/latest/topics/dpdk/vhost-user/#adding-vhost-user-ports-to-the-guest-libvirt
```
error: internal error: process exited while connecting to monitor: 2019-08-05T07:36:28.579478Z qemu-system-x86_64: -chardev socket,id=charnet1,path=/tmp/vhost2.sock: Failed to connect socket /tmp/vhost2.sock: Permission denied
```

- add more hugepages when following case.
- if hugepages is few to create vm, kvm prints such error logs.
```
error: internal error: process exited while connecting to monitor: 2019-08-05T07:37:14.159699Z qemu-system-x86_64: -object memory-backend-file,id=ram-node0,prealloc=yes,mem-path=/dev/hugepages/libvirt/qemu/9-vm01,share=yes,size=8388608000: unable to map backing store for guest RAM: Cannot allocate memory
```

## Good references

- https://software.intel.com/en-us/articles/configure-vhost-user-multiqueue-for-ovs-with-dpdk
- https://www.redhat.com/ja/blog/ovs-dpdk-migrating-vhostuser-socket-mode-red-hat-openstack
- https://wiki.qemu.org/Features/VirtioVhostUser
- https://www.youtube.com/watch?v=OnTQRgUyiv8&t=3s --> describing how to configure ovs-dpdk w/ vhost-user
  "[2017] Configuring and Benchmarking Open vSwitch, DPDK and vhost-user by Pei Zhang"
- http://www.virtualopensystems.com/en/solutions/guides/snabbswitch-qemu/ --> describing the architecture of
  vhost-user and how they are performing low-cost packet delivery.

