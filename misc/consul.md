
# Consul

## install and configuration

download and install dockerfile
```
FROM slankdev/frr:centos-7-stable-7.0
ADD https://releases.hashicorp.com/consul/1.7.1/consul_1.7.1_linux_amd64.zip /tmp
RUN yum -y install bind-utils unzip \
 && unzip /tmp/consul_1.7.1_linux_amd64.zip -d /usr/bin
```

manufests
```
nodes:
  - name: S1
    image: slankdev/consul
    interfaces: [ { name: net0, type: bridge, args: S1 } ]
  - name: S2
    image: slankdev/consul
    interfaces: [ { name: net0, type: bridge, args: S1 } ]
  - name: S3
    image: slankdev/consul
    interfaces: [ { name: net0, type: bridge, args: S1 } ]
  - name: C1
    image: slankdev/consul
    interfaces: [ { name: net0, type: bridge, args: S1 } ]
  - name: C2
    image: slankdev/consul
    interfaces: [ { name: net0, type: bridge, args: S1 } ]
  - name: C3
    image: slankdev/consul
    interfaces: [ { name: net0, type: bridge, args: S1 } ]
switches:
  - name: S1
    interfaces:
      - { name: net0, type: docker, args: S1 }
      - { name: net0, type: docker, args: S2 }
      - { name: net0, type: docker, args: S3 }
      - { name: net0, type: docker, args: C1 }
      - { name: net0, type: docker, args: C2 }
      - { name: net0, type: docker, args: C3 }

node_configs:
  - name=S1, cmds=[ cmd: ip addr add 10.0.0.1/24 dev net0 ]
  - name=S2, cmds=[ cmd: ip addr add 10.0.0.2/24 dev net0 ]
  - name=S3, cmds=[ cmd: ip addr add 10.0.0.3/24 dev net0 ]
  - name=C1, cmds=[ cmd: ip addr add 10.0.0.11/24 dev net0 ]
  - name=C2, cmds=[ cmd: ip addr add 10.0.0.12/24 dev net0 ]
  - name=C3, cmds=[ cmd: ip addr add 10.0.0.13/24 dev net0 ]
```

launch (1)
```
docker exec S1 -it consul agent -server -data-dir /tmp/consul
docker exec S2 -it consul agent -server -data-dir /tmp/consul -join 10.0.0.1
docker exec S3 -it consul agent -server -data-dir /tmp/consul -join 10.0.0.1
docker exec C1 -it consul agent -data-dir=/tmp/consul -join 10.0.0.1
```

launch (2)
```
consul agent -config-file=/etc/consul/consul.json -config-dir=/etc/consul/consul.d 
```

configuration
```
$ cat consul.server.json
{
        "bootstrap_expect": 3,
        "data_dir": "/tmp/consul",
        "log_level": "INFO",
        "server": true,
        "start_join": [ "10.0.0.1", "10.0.0.2", "10.0.0.3" ]
}

$ cat consul.client.json
{
        "data_dir": "/tmp/consul",
        "enable_script_checks": true,
        "start_join": [ "10.0.0.1", "10.0.0.2", "10.0.0.3" ]
}

$ cat web.json
{
        "service": {
                "name": "web",
                "port": 80,
                "check": {
                        "args": ["curl", "-s", "localhost"],
                        "interval": "1s"
                }
        }
}
```

## CLI

apply configuration changes
```
cd <conf-dir>
vim web.json
consul reload
```

check
```
consul members
consul catalog services
consul catalog nodes
```

watch (web is service name)
```
consul watch -type=service -service=web "jq . ; echo ----"
```

Environment Variable.
ref: https://www.consul.io/docs/commands/index.html
```
export CONSUL_HTTP_ADDR=http://localhost:30850
```

unregister / deregister / delete service
```
consul services deregister -id=web
```

## HTTP API

ref: https://www.consul.io/api/agent.html

```
export HOST=localhost:8500
$ curl $HOST/v1/catalog/nodes
$ curl $HOST/v1/agent/members
$ curl -X GET $HOST/v1/agent/services

$ curl -X PUT -H "Content-Type: application/json" $HOST/v1/agent/service/register -d '
{
  "name": "web",
  "port": 80,
  "check": {
    "args": ["curl", "-s", "localhost"],
    "interval": "1s"
  },
  "meta": {
    "meta": "dummy value"
  }
}'

$ curl -X PUT -H "Content-Type: application/json" $HOST/v1/agent/service/deregister/web

$ curl $HOST/v1/health/state/passing
$ curl $HOST/v1/health/state/critical
$ curl $HOST/v1/health/checks/:service
```

## DNS API

ref: https://www.consul.io/docs/agent/dns.html

dns api (web is service name)
```
$ dig @127.0.0.1 -p 8600 web.service.consul.
web.service.consul.     0       IN      A       10.0.0.11
web.service.consul.     0       IN      A       10.0.0.12
web.service.consul.     0       IN      A       10.0.0.13
```
