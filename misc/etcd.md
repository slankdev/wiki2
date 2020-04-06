
# etcd

```
yum install -y etcd

etcdctl set os linux
etcdctl get os
etcdctl --endpoints http://10.0.0.2:9999 ls
```

```
ETCDCTL_API=3 ./etcdctl get /ports --prefix  #ls
ETCDCTL_API=3 ./etcdctl get /ports/test
```
