
# TestPMD

- http://dpdk.org/doc/guides/testpmd_app_ug/

Running command

```
# ./testpmd -- -i --rxq=2 --txq==2
```

Runtime command

```
> show port info (<pid>|all)
> show config (rxtx|cores|fwd|txpkts)
> set fwd (io|mac|macswap|flowgen|rxonly|txonly|csum|icmpecho) (""|retry)
> set coremask <mask>
> set promisc (<pid>|all) (on|off)
> set vf promisc (<pid>) (<vf_id>) (on|off)
> set link-up port <pid>
> set link-down port <pid>
> port (start|stop|close) <pid>
> port config all (rxq|txq|rxd|txd) <value>
```

```
# ./testpmd -- -i
> port stop all
> port config all rxq 4
> port config all txq 4
> set coremask 0x4
> show config fwd
> port start all
> start
```



