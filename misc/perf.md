
# performance tools

## netperf

```
server# netserver -4
Starting netserver with host 'IN(6)ADDR_ANY' port '12865' and family AF_INET

client# netperf -H 10.1.0.2 -4
MIGRATED TCP STREAM TEST from 0.0.0.0 (0.0.0.0) port 0 AF_INET to 10.1.0.2 () port 0 AF_INET : demo
Recv   Send    Send
Socket Socket  Message  Elapsed
Size   Size    Size     Time     Throughput
bytes  bytes   bytes    secs.    10^6bits/sec

 87380  16384  16384    10.00    5331.54

## Option
client# netperf -H 10.1.0.2 -4
client# netperf -H 10.1.0.2 -4 -- -m 64  --> message-size

## with routing instance. usually, netperf send with ttl=1..?
client# netperf -H 10.1.0.2 -4 -- -m 64 -R 1
```

## iperf

iperf/iperf3の使用方法について軽くまとめる.
現段階ではTCPのパフォーマンス計測のみついてまとめてある

サーバ側
```
$ iperf -s
```

クライアント側
```
$ iperf -c SERVERIP
$ iperf -c SERVERIP -l 100M   // 100Mbyteのデータ送信
$ iperf -c SERVERIP -t 10     // 10s間データ送信
$ iperf -c SERVERIP -i 1      // 1sごとに計測
$ iperf -c SERVERIP

##output csv
## -y, --reportstlle C|c
$ iperf -c localhost -yC -i1
20190824143448,127.0.0.1,53705,127.0.0.1,5001,5,0.0-1.0,6294732800,50357862400
20190824143449,127.0.0.1,53705,127.0.0.1,5001,5,1.0-2.0,6210584576,49684676608
20190824143450,127.0.0.1,53705,127.0.0.1,5001,5,2.0-3.0,6216744960,49733959680
date,src-ip,sport,dst-ip,dport,n_sample,count,range,total-len,speed
...
```

format
```
if (is_tcp) {
	// TCP Reporting
	printf( reportCSV_bw_format,
			timestamp,
			(stats->reserved_delay == NULL ? ",,," : stats->reserved_delay),
			stats->transferID,
			stats->startTime,
			stats->endTime,
			stats->TotalLen,
			speed);
} else {
	// UDP Reporting
	printf( reportCSV_bw_jitter_loss_format,
			timestamp,
			(stats->reserved_delay == NULL ? ",,," : stats->reserved_delay),
			stats->transferID,
			stats->startTime,
			stats->endTime,
			stats->TotalLen,
			speed,
			stats->jitter*1000.0,
			stats->cntError,
			stats->cntDatagrams,
			(100.0 * stats->cntError)/stats->cntDatagrams, stats->cntOutofOrder );
}
```

## perf perf\_event

まずperf listで計測できるイベントを調べておく。
root権限があるとより多くのイベントが見れる


```
$ perf list
  msr:read_msr                                       [Tracepoint event]
  msr:write_msr                                      [Tracepoint event]
  napi:napi_poll                                     [Tracepoint event]
  net:napi_gro_frags_entry                           [Tracepoint event]
  net:napi_gro_receive_entry                         [Tracepoint event]
  net:net_dev_queue                                  [Tracepoint event]
  net:net_dev_start_xmit                             [Tracepoint event]
  net:net_dev_xmit                                   [Tracepoint event]
  ...
```

以下のコマンドで計測できる。

```
perf stat -e branch-load-misses ./build/a.out
perf stat -e net:net_dev_xmit,net:net_dev_queue ./a.out
```

perf record, perf reportを使う
```
$ perf record a.out
$ perf report

// コールグラフ付き
$ perf record -g a.out
$ perf report -g -G
```

## Stress
```
$ stress -c 1
$ stress -c 1 -q
$ pkillall stress
```

## Taskset / numactl

```
numactl -H // --hardware
numactl -s // --show
numactl --cpunodebind=2 ls
numactl --cpunodebind=0,1,2 ls
numactl --cpunodebind=0-2 ls
numactl --physcpubind=0-2 ls

taskset -c 0 -- stress -c 1
taskset -p -c 5-9 $pid
```

## IRQ

```
# cat /proc/interrupts
CPU   0      1      2      3      4      5
83:  51  34622  96195  69119  24106  94346   IR-PCI-MSI 1050624-edge  eth3-TxRx-0
84:   0  22949  93910  05260  97706  99878   IR-PCI-MSI 1050625-edge  eth3-TxRx-1
85:   0  71071  12560  15409  49654  01001   IR-PCI-MSI 1050626-edge  eth3-TxRx-2
86:   0  80183  29811  74681  91800  07452   IR-PCI-MSI 1050627-edge  eth3-TxRx-3
87:   0  78841  49126  18125  02089  23274   IR-PCI-MSI 1050628-edge  eth3-TxRx-4
# cat /proc/irq/83/smp_affinity
004
# echo 1 /proc/irq/83/smp_affinity
# cat /proc/irq/83/smp_affinity
001
```

