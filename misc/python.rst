
python
==========

.. code-block:: text

  installpath (UNIX)
  /usr/local/lib/pythonX.Y/site-packages

Basic
--------

format

.. code-block:: python

  print("{<10}".format())

class

.. code-block:: python

  class Spam:
    hoge = 10
    def __init__(self,ham,egg):
      self.ham = ham
      self.egg = egg
    def output(self):
      sum = self.ham + self.egg
      print("{0}".format(sum))

  class Base:
      basevalue = "base"
      def spam(self):
          print("Base.spam()")

      def ham(self):
          print("ham")

  class Derived(Base):
      def spam(self):
          print ("Derived.spam()")
          self.ham()

  derived = Derived()
  print("{0}".format(derived.basevalue))
  derived.ham()

  class Spam:
      __attr = 100 #private
      def __init__(self): #private
          self.__attr = 999
      def __method(self): #private
          print(self.__attr)
      def method(self): #public
          self.__method()

  spam =Spam()
  spam.method()   #OK
  spam.__method() #NG
  spam.__attr     #NG

  span.hoge             #10
  span.__dict__['hoge'] #10

dictional

.. code-block:: python

  d['slank'] = 'slank_context'
  d['tennis'] = 'tennis_context'
  print(d['slank']) #slank_context
  print(d['soccer']) #KeyError: 'soccer'
  print(d.get('soccer')) #None
  print(d.keys())   # ['slank','tennis']

set

.. code-block:: python

  s = set()
  s.add(1) #{1}
  s.add(3) #{1,3}

array

.. code-block:: python

  array = []
  array.append(1) #[1]
  array.append(3) #[1,3]

  array = [ 1,2,3,4,4,5,3,5,1,1,1, ]
  unique_array = list(set(array)) #[ 1,2,3,4,5 ]

  a1 = [1,2,3]
  a2 = [4,5,6]
  a3 = a1 + a2   #[1,2,3,4,5,6]
  a4 = a1 + 23   #Error
  a4 = a1 + [23] #[1,2,3,23]

string

.. code-block:: python

   s = 'ip link set vrf0 up'
   a = s.split(' ') #['ip', 'link', 'set', 'vrf0', 'up']
   a.join('_') #'ip_link_set_vrf0_up'

requests
---------

.. code-block:: python

  import requests
  response = requests.get(
        'http://127.0.0.1:5000/get',
        params={'foo': 'bar'})
  dict_data = response.json()

.. code-block:: python

  import requests
  os_token = "hoge"

  credential = {
    'auth': {
      'identity': {
        'methods': ['password'],
        'password': {
          'user': {
            'name': username,
            'domain': {'name': 'default'},
            'password': password,
          }
        }
      },
      'scope': {
        'project': {
          'name': project_name,
          'domain': { 'name': 'default' }
        }
      }
    }
  }

  response = requests.post(
        'http://127.0.0.1:5000/v1/auth/tokens',
        headers={
          'Content-Type': 'application/json',
          'X-Auth-Token': os_token,
        },
        data=json.dumps(credential))
  dict_data = response.json()


json
-----

.. code-block:: python

   import json
   json_str = '{"name":"slankdev", "age":24}'
   json_obj = json.loads(json_str)
   print(json_obj['name']) #slankdev

yaml
----

.. code-block:: python

   #pip3 install pyyaml
   import yaml
   yaml_file = 'main.yaml'
   with open(yaml_file) as f:
     yaml_obj = yaml.load(f, Loader=yaml.SafeLoader)
     print(yaml_obj['name']) #slankdev


subprocess
----------

.. code-block:: python

   import subprocess
   cmd = ['ip', 'link', 'set', 'dum0', 'up']
   subprocess.call(cmd)
   res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE) #redirect stdout,stderr to res
   print(res.stdout)

http
------

.. code-block:: python

  #!/usr/bin/env python3
  import sys, http
  from http.server import BaseHTTPRequestHandler
  port_range = { 'min':None, 'max':0 }

  class StubHttpRequestHandler(BaseHTTPRequestHandler):
      def __init__(self, *args, **kwargs):
          super().__init__(*args, **kwargs)

      def log_request(self, code='-', size='-'):
          addr = str(self.client_address[0])
          port = int(self.client_address[1])
          if port_range['min'] is None:
              port_range['min'] = port
          port_range['min'] = min(port_range['min'], port)
          port_range['max'] = max(port_range['max'], port)
          print("{}:{} ( min={}, max={}, diff={} )".format(addr, port,
              port_range['min'], port_range['max'],
              port_range['max'] - port_range['min']))

      def do_GET(self):
          r = [ "{}:{}\n".format(self.client_address[0], self.client_address[1]) ]
          encoded = '\n'.join(r).encode(sys.getfilesystemencoding())
          self.send_response(http.HTTPStatus.OK)
          self.end_headers()
          self.wfile.write(encoded)

  httpd = http.server.HTTPServer(('',9999), StubHttpRequestHandler)
  httpd.serve_forever()

socket
-------

.. code-block:: python

  import socket
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.connect(('vpn.slank.dev', 9999))
      s.sendall(b'hello')
      data = s.recv(1024)
      print(repr(data))

syslog
--------

.. code-block:: python

  import syslog
  syslog.syslog('message') #LOG_INFO
  syslog.syslog(syslog.LOG_ERR, 'Processing started')
  syslog.syslog(syslog.LOG_, 'Processing started')

  #     <-- higher   [LOG_priority]    lower -->
  # EMERG,ALERT,CRIT,ERR,WARNING,NOTICE,INFO,DEBUG

seaborn
--------

- https://seaborn.pydata.org/examples/color_palettes.html


matplotlib
-----------


tqdm / progress bar
--------------------

.. code-block:: text

  pip3 install tqdm

.. code-block:: python

  #!/usr/bin/env python3
  import time
  from tqdm import tqdm
  for _ in tqdm(range(100)):
    time.sleep(0.1)

sys.argv
---------

.. code-block:: python

  import sys
  for i in range(len(sys.argv)):
    print('sys.argv[{}]: {}'.format(i, sys.argv[i]))

argparse
---------

.. code-block:: python

  parser = argparse.ArgumentParser()
  parser.add_argument('-t', '--title', required=True)
  parser.add_argument('-x', '--xlabel', required=True)
  parser.add_argument('-i', '--input', action='append', required=True)
  parser.add_argument('-l', '--loc', default='lower right')
  parser.add_argument('-L', '--legend-font-size', default=16)
  args = parser.parse_args() ## nothing

  print(args.loc) #--> 'lower right'
  for input_one in args.input:
    print(input_one)

pyroute2
---------

.. code-block:: python

  import pyroute2
  ip = pyroute2.IPRoute()
  for link in ip.get_links():
      print(link.get_attr('IFLA_IFNAME'))

  {
    'family': 0, '__align': (), 'ifi_type': 772, 'index': 1, 'flags': 65609, 'change': 0,
    'state': 'up',
    'event': 'RTM_NEWLINK'
    'header': {'length': 1316, 'type': 16, 'flags': 2, 'sequence_number': 255,
               'pid': 107977, 'error': None, 'stats': Stats(qsize=0, delta=0, delay=0) },

    'attrs': [
       ('IFLA_IFNAME', 'lo'),
       ('IFLA_TXQLEN', 1000),
       ('IFLA_OPERSTATE', 'UNKNOWN'),
       ('IFLA_LINKMODE', 0),
       ('IFLA_MTU', 65536),
       ('UNKNOWN', {'header': {'length': 8, 'type': 50}}),
       ('UNKNOWN', {'header': {'length': 8, 'type': 51}}),
       ('IFLA_GROUP', 0),
       ('IFLA_PROMISCUITY', 0),
       ('IFLA_NUM_TX_QUEUES', 1),
       ('IFLA_GSO_MAX_SEGS', 65535),
       ('IFLA_GSO_MAX_SIZE', 65536),
       ('IFLA_NUM_RX_QUEUES', 1),
       ('IFLA_CARRIER', 1),
       ('IFLA_QDISC', 'noqueue'),
       ('IFLA_CARRIER_CHANGES', 0),
       ('IFLA_PROTO_DOWN', 0),
       ('IFLA_CARRIER_UP_COUNT', 0),
       ('IFLA_CARRIER_DOWN_COUNT', 0),
       ('IFLA_MAP', {'mem_start': 0, 'mem_end': 0, 'base_addr': 0, 'irq': 0, 'dma': 0, 'port': 0}),
       ('IFLA_ADDRESS', '00:00:00:00:00:00'),
       ('IFLA_BROADCAST', '00:00:00:00:00:00'),
       ('IFLA_STATS64', {'rx_packets': 0, 'tx_packets': 0, 'rx_bytes': 0, 'tx_bytes': 0, 'rx_errors': 0,
                        'tx_errors': 0, 'rx_dropped': 0, 'tx_dropped': 0, 'multicast': 0, 'collisions': 0,
                        'rx_length_errors': 0, 'rx_over_errors': 0, 'rx_crc_errors': 0, 'rx_frame_errors': 0,
                        'rx_fifo_errors': 0, 'rx_missed_errors': 0, 'tx_aborted_errors': 0, 'tx_carrier_errors': 0,
                        'tx_fifo_errors': 0, 'tx_heartbeat_errors': 0, 'tx_window_errors': 0, 'rx_compressed': 0,
                        'tx_compressed': 0}),
       ('IFLA_STATS', {'rx_packets': 0, 'tx_packets': 0, 'rx_bytes': 0, 'tx_bytes': 0, 'rx_errors': 0, 'tx_errors': 0,
                       'rx_dropped': 0, 'tx_dropped': 0, 'multicast': 0, 'collisions': 0, 'rx_length_errors': 0,
                       'rx_over_errors': 0, 'rx_crc_errors': 0, 'rx_frame_errors': 0, 'rx_fifo_errors': 0,
                       'rx_missed_errors': 0, 'tx_aborted_errors': 0, 'tx_carrier_errors': 0, 'tx_fifo_errors': 0,
                       'tx_heartbeat_errors': 0, 'tx_window_errors': 0, 'rx_compressed': 0, 'tx_compressed': 0}),
       ('IFLA_XDP', '05:00:02:00:00:00:00:00'),
       ('IFLA_AF_SPEC', {'attrs': [('AF_INET', {'dummy': 65668, 'forwarding': 1, 'mc_forwarding': 0, 'proxy_arp': 0,
                         'accept_redirects': 0, 'secure_redirects': 1, 'send_redirects': 0, 'shared_media': 1,
                         'rp_filter': 0, 'accept_source_route': 0, 'bootp_relay': 0, 'log_martians': 1,
                         'tag': 0, 'arpfilter': 0, 'medium_id': 0, 'noxfrm': 1, 'nopolicy': 1, 'force_igmp_version': 0,
                         'arp_announce': 0, 'arp_ignore': 1, 'promote_secondaries': 1, 'arp_accept': 0, 'arp_notify': 0,
                         'accept_local': 0, 'src_vmark': 0, 'proxy_arp_pvlan': 0, 'route_localnet': 0,
                         'igmpv2_unsolicited_report_interval': 10000, 'igmpv3_unsolicited_report_interval': 1000}),
                         ('AF_INET6', {'attrs': [('IFLA_INET6_FLAGS', 2147483648),
       ('IFLA_INET6_CACHEINFO', {'max_reasm_len': 65535, 'tstamp': 115418899, 'reachable_time': 27555, 'retrans_time': 1000}),
       ('IFLA_INET6_CONF', {'forwarding': 1, 'hop_limit': 64, 'mtu': 65536, 'accept_ra': 1, 'accept_redirects': 1, 'autoconf': 1,
                            'dad_transmits': 1, 'router_solicitations': 4294967295, 'router_solicitation_interval': 4000,
                            'router_solicitation_delay': 1000, 'use_tempaddr': 4294967295, 'temp_valid_lft': 604800,
                            'temp_preferred_lft': 86400, 'regen_max_retry': 3, 'max_desync_factor': 600, 'max_addresses': 16,
                            'force_mld_version': 0, 'accept_ra_defrtr': 1, 'accept_ra_pinfo': 1, 'accept_ra_rtr_pref': 1,
                            'router_probe_interval': 60000, 'accept_ra_rt_info_max_plen': 0, 'proxy_ndp': 0, 'optimistic_dad': 0,
                            'accept_source_route': 0, 'mc_forwarding': 0, 'disable_ipv6': 0, 'accept_dad': 4294967295,
                            'force_tllao': 0, 'ndisc_notify': 0}), ('IFLA_INET6_STATS', {'num': 37, 'inpkts': 0,
                            'inoctets': 0, 'indelivers': 0, 'outforwdatagrams': 0, 'outpkts': 0, 'outoctets': 0,
                            'inhdrerrors': 0, 'intoobigerrors': 0, 'innoroutes': 0, 'inaddrerrors': 0, 'inunknownprotos': 0,
                            'intruncatedpkts': 0, 'indiscards': 0, 'outdiscards': 0, 'outnoroutes': 0, 'reasmtimeout': 0,
                            'reasmreqds': 0, 'reasmoks': 0, 'reasmfails': 0, 'fragoks': 0, 'fragfails': 0, 'fragcreates': 0,
                            'inmcastpkts': 0, 'outmcastpkts': 0, 'inbcastpkts': 0, 'outbcastpkts': 0, 'inmcastoctets': 0,
                            'outmcastoctets': 0, 'inbcastoctets': 0, 'outbcastoctets': 0, 'csumerrors': 0, 'noectpkts': 0,
                            'ect1pkts': 0, 'ect0pkts': 0, 'cepkts': 0}),
       ('IFLA_INET6_ICMP6STATS', {'num': 6, 'inmsgs': 0, 'inerrors': 0, 'outmsgs': 0, 'outerrors': 0, 'csumerrors': 0}),
       ('IFLA_INET6_TOKEN', '::'),
       ('IFLA_INET6_ADDR_GEN_MODE', 0)]})]})],
  }

Daemonize
----------

.. code-block:: python

  import os,sys,time

  def main_routine():
    while True:
      print('hoge')
      time.sleep(1)

  def daemonize():
    pid = os.fork()
    if pid > 0:
      pid_file = open('daemon.pid','w')
      pid_file.write(str(pid)+"\n")
      pid_file.close()
      sys.exit()
    if pid == 0:
      main_routine()

scapy
-------

ip range flood.

.. code-block:: python

  from scapy.all import *
  iface='net0'
  for ip in range(0,10):
    packet = Ether()/IP(dst='10.0.0.'+str(ip), ttl=20)
    sendp(packet, iface=iface)

simple ip send

.. code-block:: python

  def ipsend(dst, iface):
    eh = Ether(dst='ff:ff:ff:ff:ff:ff')
    ih = IP(dst=dst, ttl=20)
    pk = eh/ih
    sendp(pk, iface=iface)

  def send_range(n):
    for i in range(n):
      dst = '10.0.0.{}'.format(i)
      print('sendto {}'.format(dst))
      ipsend(dst, 'net0')


openstack client
----------------

- https://www.ibm.com/developerworks/jp/cloud/library/cl-openstack-pythonapis/index.html
- https://docs.openstack.org/ocata/user-guide/sdk-neutron-apis.html
- https://docs.openstack.org/python-neutronclient/latest/reference/index.html

get credentials

.. code-block:: python

  # this is old version
  def get_keystone_creds():
      d = {}
      d['username'] = os.environ['OS_USERNAME']
      d['password'] = os.environ['OS_PASSWORD']
      d['auth_url'] = os.environ['OS_AUTH_URL']
      d['tenant_name'] = os.environ['OS_TENANT_NAME']
      return d

  # this is old version
  def get_nova_creds():
      d = {}
      d['username'] = os.environ['OS_USERNAME']
      d['api_key'] = os.environ['OS_PASSWORD']
      d['auth_url'] = os.environ['OS_AUTH_URL']
      d['project_id'] = os.environ['OS_TENANT_NAME']
      return d

  def get_keystone_password_creds():
    d = {}
    d['user_domain_name'] = "default"
    d['project_domain_name'] = "default"
    d['username'] = os.environ['OS_USERNAME']
    d['password'] = os.environ['OS_PASSWORD']
    d['auth_url'] = os.environ['OS_AUTH_URL']
    d['project_name'] = os.environ['OS_PROJECT_NAME']
    return d

  def get_nova_credentials_v2():
      d = {}
      d['version'] = '2.1'
      d['user_domain_name'] = "default"
      d['project_domain_name'] = "default"
      d['username'] = os.environ['OS_USERNAME']
      d['password'] = os.environ['OS_PASSWORD']
      d['auth_url'] = os.environ['OS_AUTH_URL']
      d['project_name'] = os.environ['OS_PROJECT_NAME']
      return d

get auth token

.. code-block:: python

  # this is old
  import keystoneclient.v2_0.client as ksclient
  creds = get_keystone_creds()
  keystone = ksclient.Client(**creds)
  print(keystone.auth_token) # u'fI9JnOBZJwuoma8je0a1AvLff6AcJ1zFkVZGb'

  # correct
  from keystoneclient.v3.client import Client as KC
  from keystoneauth1 import identity
  from keystoneauth1 import session
  creds = get_keystone_creds()
  auth = identity.v3.Password(**creds)
  sess = session.Session(auth=auth)
  keystone_client = KC(session=sess)
  data = auth.get_auth_ref(sess)
  print(data.__dict__['_auth_token'])

list servers

.. code-block:: python

  #old
  from novaclient import client as novaclient
  creds = get_nova_creds()
  nova = novaclient.Client("2.0", **creds)
  print(nova.servers.list()) # [<Server: test1>, <Server: test2>]
  sv = nova.servers.list()[0]
  sv.name # test1
  sv.__dict__['OS-EXT-SRV-ATTR:hypervisor_hostname'] # hv01

  # correct
  from novaclient.client import Client as NC
  creds = get_nova_credentials_v2()
  nova_client = NC(**creds)
  servers = nova_client.servers.list(search_opts={
          'all_tenants': 1,
          'tenant_id': "af2d74ba14fa40f8a607f383e13729d8", })
  for server in servers:
      info = server.to_dict()
      print('id={} name={} created={}'.format(info['id'], info['name'], info['created']))

  #lise-endpoints (name="test", type="test")
  services = client.services.list(name="test", type="test")
  if len(services) == 0:
  	raise Exception("service isn't found")
  endpoint = services[0].links['self']


example server monitor program

.. code-block:: python

  #!/usr/bin/env python2
  import os
  from novaclient import client as novaclient
  from neutronclient.v2_0 import client as neutronclient

  def get_credentials():
      d = {}
      d['username'] = os.environ['OS_USERNAME']
      d['password'] = os.environ['OS_PASSWORD']
      d['auth_url'] = os.environ['OS_AUTH_URL']
      d['tenant_name'] = os.environ['OS_TENANT_NAME']
      return d

  def get_nova_credentials():
      d = {}
      d['username'] = os.environ['OS_USERNAME']
      d['api_key'] = os.environ['OS_PASSWORD']
      d['auth_url'] = os.environ['OS_AUTH_URL']
      d['project_id'] = os.environ['OS_TENANT_NAME']
      return d

  def main():
    print('[SERVER]')
    print(' {0:<38} {1:<10} {2:<10} {3:<16} {4:<10}'.format(
      'id', 'name', 'status', 'network', 'compute'))
    print(' {0:<38} {1:<10} {2:<10} {3:<16} {4:<10}'.format(
      '-'*38, '-'*10, '-'*10, '-'*16, '-'*10))
    creds = get_nova_credentials()
    nova = novaclient.Client("2.0", **creds)
    for sv in nova.servers.list(search_opts={'all_tenants':1}):
      hv_hostname = sv.__dict__['OS-EXT-SRV-ATTR:hypervisor_hostname']
      for key in sv.addresses.keys():
        net = "{}={}".format(key, sv.addresses[key][0]['addr'])
        print(' {0:<38} {1:<10} {2:<10} {3:<16} {4:<10}'.format(
          sv.id, sv.name, sv.status, net, hv_hostname))

    print('\n[NETWORK]')
    print(' {0:<38} {1:<12} {2:<10}'.format('id', 'name', 'status'))
    print(' {0:<38} {1:<12} {2:<10}'.format('-'*38, '-'*12, '-'*10))
    creds = get_credentials()
    neutron = neutronclient.Client(**creds)
    networks = neutron.list_networks()['networks']
    for net in networks:
      subnets = net['subnets']
      print(' {0:<38} {1:<12} {2:<10}'.format(
        net['id'],
        net['name'],
        net['status']
        ))

    print('\n[PORT]')
    ports = neutron.list_ports()['ports']
    print(' {0:<38} {1:<20} {2:<16}'.format('id', 'name', 'ip_address'))
    print(' {0:<38} {1:<20} {2:<16}'.format('-'*38, '-'*20, '-'*16))
    for port in ports:
      name = port['name'] if port['name'] else '<n/a>'
      addr = port['fixed_ips'][0]['ip_address']
      print(' {0:<38} {1:<20} {2:<16}'.format(port['id'], name, addr))

  if __name__ == '__main__': main()
  ## [SERVER]
  ## id                                     name       status     network          compute
  ## -------------------------------------- ---------- ---------- ---------------- ----------
  ## da9651f1-5b40-468c-a0db-cbde53976d2d   net2test1  ACTIVE     net2=10.1.0.3    hv03
  ## ce9dd57d-fd31-49e2-aca7-cfcb8a6034c2   net2test   ACTIVE     net2=10.1.0.2    hv03
  ##
  ## [NETWORK]
  ## id                                     name         status
  ## -------------------------------------- ------------ ----------
  ## c4670868-f8f1-48c7-bc6c-14e5ef3e42ca   admin-net    ACTIVE
  ## 3df9474e-8cee-44ac-87f2-1e3740dbd553   vrf-net      ACTIVE
  ## 4a841f1f-e402-47a8-8333-dfbaeaf7f13c   public-net   ACTIVE
  ## 9a9151b6-bf04-45c6-98e0-aff93b8cd358   lb-net       ACTIVE
  ## b6ae95c8-4ad7-4e2a-a4f3-1d14a038b8f9   net          ACTIVE
  ## 94131b93-0fbc-43ee-94d6-4445204a35a8   net2         ACTIVE
  ##
  ## [PORT]
  ## id                                     name                 ip_address
  ## -------------------------------------- -------------------- ----------------
  ## 1e6e30c5-1ea3-4559-a2f0-f76e9d52dcfe   <n/a>                10.1.0.3
  ## 3b0b5865-47c2-4379-bc9e-cca416777691   vrf01a16c94131b      169.254.1.7
  ## 490d4e8b-b5a4-423b-bc04-44ae7142426c   vrfc021584a841f      169.254.1.3
  ## 4c791dbf-9776-4be3-8325-f657afe650bc   <n/a>                10.1.0.2
  ## 726c8994-110b-480a-8516-44db919b28ba   vrf01a16cb6ae95      169.254.1.5
  ## 7b4f66c6-e643-49b5-aef0-202feac3e384   lvrfc021589a915      169.254.1.6
  ## 83a8c835-4bd0-4158-b102-52968893b875   vrf01a16c4a841f      169.254.1.2
  ## d3f9fc75-ecc1-4144-9095-530b42e093dc   vrfc02158c46708      169.254.1.4


Ansible Custom Module
---------------------

.. code-block:: python

  def main():
      module = AnsibleModule(
          argument_spec = dict(
              os_auth_url     = dict(required=True),
              os_username     = dict(required=True),
              os_password     = dict(required=True),
              os_project_name = dict(required=True),
              object_name     = dict(requests=True),
              mode            = dict(default='a', choices=['a', 'b']),
          ),
          supports_check_mode = True
      )
      changed = False

      ## (0) Get OS_TOKEN
      os_token = get_token(
              module.params["os_username"],
              module.params["os_password"],
              module.params["os_project_name"],
              module.params["os_auth_url"])

      ## (1) Check Role Is Exist
      name = module.params["object_name"]
      obj = get_obj_by_name(namt, os_token)
      if obj is None:
          create_obj(name, os_token)
          changed = True
      module.exit_json(changed=changed)

  from ansible.module_utils.basic import AnsibleModule
  if __name__ == "__main__": main()
