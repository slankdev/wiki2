
# OpenStack

## Setup w/ DevStack

bash completion / bash\_completion
```
openstack complete | sudo tee /etc/bash_completion.d/osc.bash_completion > /dev/null
soure /etc/bash_completion
```

```
$ git clone https://git.openstack.org/openstack-dev/devstack
$ sudo devstack/tools/create-stack-user.sh
$ sudo su - stack
stack$ git clone https://git.openstack.org/openstack-dev/devstack
stack$ cd devstack
stack$ vi local.conf
stack$ ./stack.sh
```

local.conf (1)
```
[[local|localrc]]
HOST_IP=192.168.99.152
MYSQL_PASSWORD=mysql
RABBIT_PASSWORD=rabbitmq
ADMIN_PASSWORD=secret
SERVICE_PASSWORD=secret
```

local.conf (2)
```
[[local|localrc]]
HOST_IP=192.168.99.38
SERVICE_HOST=192.168.99.38
MYSQL_HOST=192.168.99.38
RABBIT_HOST=192.168.99.38
GLANCE_HOSTPORT=192.168.99.38:9292
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=secret
RABBIT_PASSWORD=secret
SERVICE_PASSWORD=secret

## Neutron options
Q_USE_SECGROUP=True
FLOATING_RANGE="192.168.99.0/24"
IPV4_ADDRS_SAFE_TO_USE="10.0.0.0/22"
Q_FLOATING_ALLOCATION_POOL=start=192.168.99.200,end=192.168.99.210
PUBLIC_NETWORK_GATEWAY="192.168.99.1"
PUBLIC_INTERFACE=eno2

# Open vSwitch provider networking configuration
Q_USE_PROVIDERNET_FOR_PUBLIC=True
OVS_PHYSICAL_BRIDGE=br-ex
PUBLIC_BRIDGE=br-ex
OVS_BRIDGE_MAPPINGS=public:br-ex
```

```
#cloud-config
password: ubuntu
chpasswd: { expire: False }
ssh_pwauth: True
```

## Openstack CLI / openstack command

about image
```
$ source /devstack/openrc admin admin
$ openstack image create --disk-format qcow2 --container-format bare --public --file ./xenial-server-cloudimg-amd64-disk1.img  xenial
$ openstack image delete xenial

$ openstack image list
+--------------------------------------+---------------------------------+--------+
| ID                                   | Name                            | Status |
+--------------------------------------+---------------------------------+--------+
| efe71be1-b0f0-4a87-a556-88843a8ebbc5 | xenial                          | active |
| fc7a7195-c212-4eca-adb1-db101b8b0b8a | cirros-0.3.4-x86_64-uec         | active |
+--------------------------------------+---------------------------------+--------+

$ openstack image show xenial
+------------------+------------------------------------------------------+
| Field            | Value                                                |
+------------------+------------------------------------------------------+
| checksum         | 876b3ba41a84033fddf2743dcb025c00                     |
| container_format | bare                                                 |
| created_at       | 2019-10-01T03:41:32Z                                 |
| disk_format      | qcow2                                                |
| file             | /v2/images/efe71be1-b0f0-4a87-a556-88843a8ebbc5/file |
| id               | efe71be1-b0f0-4a87-a556-88843a8ebbc5                 |
| min_disk         | 0                                                    |
| min_ram          | 0                                                    |
| name             | xenial                                               |
| owner            | 5d871b2148f14f90b58c5cd4a2a5485f                     |
| protected        | False                                                |
| schema           | /v2/schemas/image                                    |
| size             | 296812544                                            |
| status           | active                                               |
| tags             |                                                      |
| updated_at       | 2019-10-01T03:41:33Z                                 |
| virtual_size     | None                                                 |
| visibility       | public                                               |
+------------------+------------------------------------------------------+
```

project, users, and roles
```
$ openstack project list
+----------------------------------+--------------------+
| ID                               | Name               |
+----------------------------------+--------------------+
| 316a2dfda0e6488bbf84fb307bbd93e4 | service            |
| 6c8ea05b18794a178e299a5808d45536 | alt_demo           |
| 9f411a0bb5df481cb8c2835cfea8ee85 | invisible_to_admin |
| c0891801e0d342e5b4b477a0530db913 | admin              |
| e8bb1be18c7d404d84622c488d1e3cb5 | demo               |
+----------------------------------+--------------------+

$ openstack user list
+----------------------------------+-----------+
| ID                               | Name      |
+----------------------------------+-----------+
| 03cae59375a64d5e9fd95db63f3377cd | nova      |
| 05de6172c6e04e3a8d063293b41de7ee | demo      |
| 131964360fe24a85b3e617bc4fa41655 | alt_demo  |
| 76bcac54b2fc414184e8e9fe51ae296d | placement |
| a8c172db986344d9aa9f5b38a9dd12fc | neutron   |
| cfee5e791a7d479fb954f2ff022e0d69 | cinder    |
| de8f76956ad54eb7bb84ee098536666a | glance    |
| f695186a196b45738171b55ac966ce78 | admin     |
+----------------------------------+-----------+

$ openstack role list
+----------------------------------+---------------+
| ID                               | Name          |
+----------------------------------+---------------+
| 51554174cccf471aa70fc61e09186132 | member        |
| 516e61b65df8498884d281e26943fea1 | reader        |
| 8eeb6c23d18a4743a3e133e7774aa631 | service       |
| b8413cb7a0ad4a7f806eb598a8848998 | ResellerAdmin |
| c50cb69983c04e41b2d7a2c1cb7ef296 | admin         |
| f1f8ad1b023449be92da4aa3a96beb9f | anotherrole   |
+----------------------------------+---------------+
```

about image
```
$ openstack image list
+--------------------------------------+---------------------------------+--------+
| ID                                   | Name                            | Status |
+--------------------------------------+---------------------------------+--------+
| d35bb2f8-aa41-416d-a55f-2fe84d46517b | cirros-0.3.4-x86_64-uec         | active |
| fc8dc550-e71e-4229-80f3-ceabef4f8a0d | cirros-0.3.4-x86_64-uec-ramdisk | active |
| a31ca311-94fd-40b3-855e-d7f258b06549 | cirros-0.3.4-x86_64-uec-kernel  | active |
+--------------------------------------+---------------------------------+--------+
```

about flavor
```
$ openstack flavor list
+----+-----------+-------+------+-----------+-------+-----------+
| ID | Name      |   RAM | Disk | Ephemeral | VCPUs | Is Public |
+----+-----------+-------+------+-----------+-------+-----------+
| 1  | m1.tiny   |   512 |    1 |         0 |     1 | True      |
| 2  | m1.small  |  2048 |   20 |         0 |     1 | True      |
| 3  | m1.medium |  4096 |   40 |         0 |     2 | True      |
| 4  | m1.large  |  8192 |   80 |         0 |     4 | True      |
| 42 | m1.nano   |    64 |    0 |         0 |     1 | True      |
| 5  | m1.xlarge | 16384 |  160 |         0 |     8 | True      |
| 84 | m1.micro  |   128 |    0 |         0 |     1 | True      |
| c1 | cirros256 |   256 |    0 |         0 |     1 | True      |
| d1 | ds512M    |   512 |    5 |         0 |     1 | True      |
| d2 | ds1G      |  1024 |   10 |         0 |     1 | True      |
| d3 | ds2G      |  2048 |   10 |         0 |     2 | True      |
| d4 | ds4G      |  4096 |   20 |         0 |     4 | True      |
+----+-----------+-------+------+-----------+-------+-----------+
```

about network
```
$ openstack network list
+--------------------------------------+---------+----------------------------------------------------------------------------+
| ID                                   | Name    | Subnets                                                                    |
+--------------------------------------+---------+----------------------------------------------------------------------------+
| 1b3e7ee0-f2b8-45ea-b0e7-734e28e13dbd | private | 2875d465-4753-4351-b178-312f8ea61382, 4990a872-26b7-45a7-bea9-21285f838eca |
| 86ebd5bf-bff9-4aba-9ad8-65949e5be8b1 | public  | 34526c73-7699-40e3-9e9c-9d32d3040713, 917bd20d-99c4-4fcb-b9af-e593b8292d9e |
+--------------------------------------+---------+----------------------------------------------------------------------------+
```

about security group
```
$ openstack security group list
+--------------------------------------+---------+------------------------+----------------------------------+------+
| ID                                   | Name    | Description            | Project                          | Tags |
+--------------------------------------+---------+------------------------+----------------------------------+------+
| e2773c4c-b1dc-434d-af9a-68ace487bc56 | default | Default security group | 51d8801ed38540c1bbceb65258cb6ff1 | []   |
+--------------------------------------+---------+------------------------+----------------------------------+------+

$ openstack security group rule list GROUPNAME
+--------------------------------------+-------------+-----------+-----------------+-----------------------+
| ID                                   | IP Protocol | IP Range  | Port Range      | Remote Security Group |
+--------------------------------------+-------------+-----------+-----------------+-----------------------+
| 353d0611-3f67-4848-8222-a92adbdb5d3a | udp         | 0.0.0.0/0 | 1:65535         | None                  |
| 63536865-e5b6-4df1-bac5-ca6d97d8f54d | tcp         | 0.0.0.0/0 | 1:65535         | None                  |
+--------------------------------------+-------------+-----------+-----------------+-----------------------+

$ openstack security group rule create --protocol icmp default
$ openstack security group rule create --protocol tcp --dst-port 22:22 default
```

about server
```
$ IMAGEID=$(openstack image show cirros-HOGE -c id -f value)
$ NETID=$(openstack network show private -c id -f value)
$ openstack server create --image $IMAGEID --flavor 1 --nic net-id=$NETID test1

$ SECGROUPID=b2b4f049-75fb-48f0-8687-1110dca84444
$ openstack security group rule list $SECGROUPID
$ openstack security group rule create --proto icmp $SECGROUPID
$ openstack security group rule create --proto tcp --dst-port 22:22 $SECGROUPID

$ openstack server create --flavor m1.tiny --image cirros-0.3.5-x86_64-disk --security-group default test-instance
+-----------------------------+-----------------------------------------------------------------+
| Field                       | Value                                                           |
+-----------------------------+-----------------------------------------------------------------+
| OS-DCF:diskConfig           | MANUAL                                                          |
| OS-EXT-AZ:availability_zone |                                                                 |
| OS-EXT-STS:power_state      | NOSTATE                                                         |
| OS-EXT-STS:task_state       | scheduling                                                      |
| OS-EXT-STS:vm_state         | building                                                        |
| OS-SRV-USG:launched_at      | None                                                            |
| OS-SRV-USG:terminated_at    | None                                                            |
| accessIPv4                  |                                                                 |
| accessIPv6                  |                                                                 |
| addresses                   |                                                                 |
| adminPass                   | zcTFHjYoSa5s                                                    |
| config_drive                |                                                                 |
| created                     | 2018-10-28T17:56:55Z                                            |
| flavor                      | m1.tiny (1)                                                     |
| hostId                      |                                                                 |
| id                          | bb3216a7-21d6-4778-b673-ab2f2d02d1a7                            |
| image                       | cirros-0.3.5-x86_64-disk (26d49cbb-9abb-4d77-b374-a9c6a293afc9) |
| key_name                    | None                                                            |
| name                        | test-instance                                                   |
| progress                    | 0                                                               |
| project_id                  | 51d8801ed38540c1bbceb65258cb6ff1                                |
| properties                  |                                                                 |
| security_groups             | name='e2773c4c-b1dc-434d-af9a-68ace487bc56'                     |
| status                      | BUILD                                                           |
| updated                     | 2018-10-28T17:56:55Z                                            |
| user_id                     | bfec66c487ef43b6ba6ca0fe24e88e81                                |
| volumes_attached            |                                                                 |
+-----------------------------+-----------------------------------------------------------------+

$ openstack flavor create --public --vcpus 1 --disk 3 --ram 512 test
+----------------------------+--------------------------------------+
| Field                      | Value                                |
+----------------------------+--------------------------------------+
| OS-FLV-DISABLED:disabled   | False                                |
| OS-FLV-EXT-DATA:ephemeral  | 0                                    |
| disk                       | 3                                    |
| id                         | f2370399-7708-48ad-9687-bfd96a03b576 |
| name                       | test                                 |
| os-flavor-access:is_public | True                                 |
| ram                        | 512                                  |
| rxtx_factor                | 1.0                                  |
| swap                       |                                      |
| vcpus                      | 1                                    |
+----------------------------+--------------------------------------+
```

service host
```
$ openstack host list
+-----------+-----------+----------+
| Host Name | Service   | Zone     |
+-----------+-----------+----------+
| hv00      | conductor | internal |
| hv00      | scheduler | internal |
| hv00      | compute   | nova     |
| hv01      | compute   | nova     |
+-----------+-----------+----------+
```

key pair
```
$ openstack keypair create demo_key > demo_key

$ openstack keypair list
+---------+-------------------------------------------------+
| Name    | Fingerprint                                     |
+---------+-------------------------------------------------+
| testkey | c7:4b:54:e8:88:ed:46:eb:ec:63:f1:eb:95:08:61:03 |
+---------+-------------------------------------------------+

$ openstack keypair show testkey
+-------------+-------------------------------------------------+
| Field       | Value                                           |
+-------------+-------------------------------------------------+
| created_at  | 2019-10-01T03:40:44.000000                      |
| deleted     | False                                           |
| deleted_at  | None                                            |
| fingerprint | c7:4b:54:e8:88:ed:46:eb:ec:63:f1:eb:95:08:61:03 |
| id          | 1                                               |
| name        | testkey                                         |
| updated_at  | None                                            |
| user_id     | 7ee626a63c894c599d9439bb333c98e3                |
+-------------+-------------------------------------------------+
```

## Neutron CLI / neutron command

```
neutron net-create slankdev-net
neutron subnet-create --name slankdev-subnet slankdev-net --enable-dhcp 169.254.1.0/24

$ neutron net-list
+--------------------------------------+------------+-----------------------------------------------------+
| id                                   | name       | subnets                                             |
+--------------------------------------+------------+-----------------------------------------------------+
| 588783d9-dc32-428f-8930-6b877ff78c3b | public-net | 48530524-d7cb-41ac-82a1-3ff672c766c7 172.24.4.0/24  |
| 9fca4b86-8d13-4566-b364-6bc5e97a26e0 | admin-net  | 0c103d84-b62a-4e4b-b3d4-fb252142aa67 10.10.10.0/24  |
| 3f5347d1-cc68-43af-a206-961d3963ded9 | net        | ba9079eb-c283-4ecc-8b65-c6d1f243b168 10.0.0.0/24    |
+--------------------------------------+------------+-----------------------------------------------------+

$ neutron agent-list
+--------------------------------------+------------+------+-------------------+-------+----------------+--------------------+
| id                                   | agent_type | host | availability_zone | alive | admin_state_up | binary             |
+--------------------------------------+------------+------+-------------------+-------+----------------+--------------------+
| 30708798-3681-469c-b1a9-5fa006343cd8 | HG agent   | hv01 |                   | :-)   | True           | neutron-hoge-agent |
| aa018e44-8bd6-4ae5-97fc-c40507c1cdaa | HG agent   | hv00 |                   | :-)   | True           | neutron-hoge-agent |
+--------------------------------------+------------+------+-------------------+-------+----------------+--------------------+

$ neutron port-list
 +--------------------------------------+-----------------+-------------------+------------------------------------------------------------------------------------+
| id                                   | name            | mac_address       | fixed_ips                                                                          |
+--------------------------------------+-----------------+-------------------+------------------------------------------------------------------------------------+
| 1d823e29-ce58-40ab-9bfd-1a193812e758 |                 | fa:16:3e:de:73:82 | {"subnet_id": "00055fc6-1d29-4cc4-ac37-c584c7ae1ec0", "ip_address": "169.254.1.6"} |
| 1f4de83e-6d5c-4ef9-9570-af30e6c3fce8 |                 | fa:16:3e:d0:80:6c | {"subnet_id": "00055fc6-1d29-4cc4-ac37-c584c7ae1ec0", "ip_address": "169.254.1.2"} |
| 3195841e-8863-4c43-a5e7-84825b772bec |                 | fa:16:3e:2f:56:4a | {"subnet_id": "5404e9d4-c3e3-4ab7-b8af-a56d7d588e4f", "ip_address": "10.0.0.4"}    |
| 6e5300b7-4495-4f09-944c-1eded04761c3 |                 | fa:16:3e:e4:09:76 | {"subnet_id": "00055fc6-1d29-4cc4-ac37-c584c7ae1ec0", "ip_address": "169.254.1.4"} |
| 83ef836b-a445-4430-87a7-7237fe5b57d6 |                 | fa:16:3e:12:5b:ec | {"subnet_id": "00055fc6-1d29-4cc4-ac37-c584c7ae1ec0", "ip_address": "169.254.1.3"} |
| 9611fcac-9199-4db8-afb4-aea03616d2c4 |                 | fa:16:3e:8d:c4:64 | {"subnet_id": "00055fc6-1d29-4cc4-ac37-c584c7ae1ec0", "ip_address": "169.254.1.5"} |
| a3600a3e-aa12-4993-8223-2f389cd4b02f |                 | fa:16:3e:9c:d3:4c | {"subnet_id": "5404e9d4-c3e3-4ab7-b8af-a56d7d588e4f", "ip_address": "10.0.0.2"}    |
| b195162c-47ac-4498-93cb-cc7d58ad7da9 |                 | fa:16:3e:43:aa:65 | {"subnet_id": "5404e9d4-c3e3-4ab7-b8af-a56d7d588e4f", "ip_address": "10.0.0.3"}    |
+--------------------------------------+-----------------+-------------------+------------------------------------------------------------------------------------+

$ neutron net-create    --provider:network_type=<type-name> <net-name>
$ neutron subnet-create --name <subnet-name>                <net-name>
$ neutron port-create   --name <port-name>                  <subnet-name>
```

```
$ neutron port-list
+--------------------------------------+------+-------------------+-----------------------------------------------------------------------------------+
| id                                   | name | mac_address       | fixed_ips                                                                         |
+--------------------------------------+------+-------------------+-----------------------------------------------------------------------------------+
| 2398df4b-e119-4d16-b667-c13c9b8fa367 |      | fa:16:3e:de:ee:30 | {"subnet_id": "b5fe0a3e-1e3d-4e4b-867b-f59b5249647c", "ip_address": "10.0.0.2"}   |
| 29d5f7b8-642a-452a-9ff6-7dd8596407a9 |      | fa:16:3e:15:06:94 | {"subnet_id": "8efc30b0-40a0-47e7-abb8-cbec569bfca8", "ip_address": "172.24.4.2"} |
+--------------------------------------+------+-------------------+-----------------------------------------------------------------------------------+

$ nova interface-list testvm2
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+
| Port State | Port ID                              | Net ID                               | IP addresses | MAC Addr          |
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+
| ACTIVE     | 2398df4b-e119-4d16-b667-c13c9b8fa367 | 28e22622-df52-459d-a64e-3d493a46affb | 10.0.0.2     | fa:16:3e:de:ee:30 |
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+

$ neutron port-create public-net --name newslank
Created a new port:
+-----------------------+-----------------------------------------------------------------------------------+
| Field                 | Value                                                                             |
+-----------------------+-----------------------------------------------------------------------------------+
| admin_state_up        | True                                                                              |
| allowed_address_pairs |                                                                                   |
| binding:vnic_type     | normal                                                                            |
| created_at            | 2019-10-03T08:44:20                                                               |
| description           |                                                                                   |
| device_id             |                                                                                   |
| device_owner          |                                                                                   |
| extra_dhcp_opts       |                                                                                   |
| fixed_ips             | {"subnet_id": "8efc30b0-40a0-47e7-abb8-cbec569bfca8", "ip_address": "172.24.4.4"} |
| id                    | 55049e4d-6eb0-423c-9cb5-ab7d108d2872                                              |
| mac_address           | fa:16:3e:4a:66:68                                                                 |
| name                  | newslank                                                                          |
| network_id            | f821c017-0e3a-4d92-ae12-700a4e6d9f82                                              |
| port_security_enabled | True                                                                              |
| security_groups       | 74dd113b-585b-436a-aa13-ebef6b2dd03c                                              |
| status                | DOWN                                                                              |
| tenant_id             | 9c2fbd0d25d44ede8e06c94e32c971bd                                                  |
| updated_at            | 2019-10-03T08:44:20                                                               |
+-----------------------+-----------------------------------------------------------------------------------+

$ neutron port-list
+--------------------------------------+----------+-------------------+-----------------------------------------------------------------------------------+
| id                                   | name     | mac_address       | fixed_ips                                                                         |
+--------------------------------------+----------+-------------------+-----------------------------------------------------------------------------------+
| 2398df4b-e119-4d16-b667-c13c9b8fa367 |          | fa:16:3e:de:ee:30 | {"subnet_id": "b5fe0a3e-1e3d-4e4b-867b-f59b5249647c", "ip_address": "10.0.0.2"}   |
| 29d5f7b8-642a-452a-9ff6-7dd8596407a9 |          | fa:16:3e:15:06:94 | {"subnet_id": "8efc30b0-40a0-47e7-abb8-cbec569bfca8", "ip_address": "172.24.4.2"} |
| 55049e4d-6eb0-423c-9cb5-ab7d108d2872 | newslank | fa:16:3e:4a:66:68 | {"subnet_id": "8efc30b0-40a0-47e7-abb8-cbec569bfca8", "ip_address": "172.24.4.4"} |
+--------------------------------------+----------+-------------------+-----------------------------------------------------------------------------------+

$ nova interface-attach --port-id 55049e4d-6eb0-423c-9cb5-ab7d108d2872 testvm2
$ nova interface-list testvm2
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+
| Port State | Port ID                              | Net ID                               | IP addresses | MAC Addr          |
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+
| ACTIVE     | 2398df4b-e119-4d16-b667-c13c9b8fa367 | 28e22622-df52-459d-a64e-3d493a46affb | 10.0.0.2     | fa:16:3e:de:ee:30 |
| ACTIVE     | 55049e4d-6eb0-423c-9cb5-ab7d108d2872 | f821c017-0e3a-4d92-ae12-700a4e6d9f82 | 172.24.4.4   | fa:16:3e:4a:66:68 |
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+
```

others
```
$ neutron ext-list
+---------------------------+-----------------------------------------------+
| alias                     | name                                          |
+---------------------------+-----------------------------------------------+
| default-subnetpools       | Default Subnetpools                           |
| availability_zone         | Availability Zone                             |
| network_availability_zone | Network Availability Zone                     |
| auto-allocated-topology   | Auto Allocated Topology Services              |
| binding                   | Port Binding                                  |
| agent                     | agent                                         |
| subnet_allocation         | Subnet Allocation                             |
| tag                       | Tag support                                   |
| external-net              | Neutron external network                      |
| net-mtu                   | Network MTU                                   |
| network-ip-availability   | Network IP Availability                       |
| quotas                    | Quota management support                      |
| provider                  | Provider Network                              |
| multi-provider            | Multi Provider Network                        |
| address-scope             | Address scope                                 |
| timestamp_core            | Time Stamp Fields addition for core resources |
| extra_dhcp_opt            | Neutron Extra DHCP opts                       |
| security-group            | security-group                                |
| rbac-policies             | RBAC Policies                                 |
| standard-attr-description | standard-attr-description                     |
| port-security             | Port Security                                 |
| allowed-address-pairs     | Allowed Address Pairs                         |
+---------------------------+-----------------------------------------------+

$ neutron ext-show security-group
...
```

## Openstack REST API

```
#!/bin/sh
curl --silent -v \
	-H "Content-Type: application/json" \
	-X POST -d @- $OS_AUTH_URL/auth/tokens <<EOS
{
    "auth": {
        "identity": {
            "methods": [ "password" ],
            "password": {
                "user": {
                    "name": "$OS_USERNAME",
                    "domain": { "name": "Default" },
                    "password": "$OS_PASSWORD"
                }
            }
        }
    }
}
EOS
```

```
$ source openrc admin admin
$ OS_TOKEN=$(openstack token issue -c id -f value)

$ curl -s \
  -H "X-Auth-Token: b4febf0e5c15481dbcac2513aaf7aa81" \
  "http://localhost:5000/v3/domains"

$ curl -s \
  -H "X-Auth-Token: $OS_TOKEN" \
  http://localhost:9696/v2.0/networks

$ curl -s \
  -H "X-Auth-Token: $OS_TOKEN" \
  "http://localhost:5000/v3/users"

$ curl -s \
  -H "X-Auth-Token: $OS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"user": {"name": "newuser", "password": "changeme"}}' \
  "http://localhost:5000/v3/users"

$ curl -s \
  -H "X-Auth-Token: $OS_TOKEN" \
  http://localhost:9696/v2.0/srv6_encap_networks

$ TENANT_ID=9c2fbd0d25d44ede8e06c94e32c971bd
$ curl -s \
  -H "X-Auth-Token: $OS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '\
{ \
  "tenant_id":$TENANT_ID, \
  "project_id": $TENANT_ID, \
  "encap_rules": [ \
    { "nexthop":"fc00:17::a00:fa", "destination":"10.0.201.201" } \
  ] \
}' \
  http://localhost:9696/v2.0/srv6_encap_networks

curl -i \
  -H "Content-Type: application/json" \
  -d '
{ "auth": {
    "identity": {
      "methods": ["token"],
      "token": {
        "id": "'$OS_TOKEN'"
      }
    }
  }
}' \
  "http://localhost:5000/v3/auth/tokens" ; echo

```

