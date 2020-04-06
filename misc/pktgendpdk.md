
# Pktgen-DPDK

## Option

```
-m “[1-8:9-10].[0-1:0-1]”
         Rx  Tx       Rx   Tx
           cpu            port
-f configfile
-T 色つきになる
-l logfilename
-b 03:00.0 // blacklist
-c 0xff
-P enablePromisc
```

## Command

```
$ page \*\*\* ページ
$ range all on
$ save OUTFILENAME
$ set all burst 16
```


## Sample

```
./app/app/xxxxx/pktgen -- -m “[1-6:7].[0-1:0-1]”   -T -P
./app/app/xxxxx/pktgen -- -m “[1-5:6-7].[0-1:0-1]” -T -P
./app/app/xxxxx/pktgen -- -m "[]"
```

```
> enable all range
> range all size start 64
> set fwd mac
> set 0 dst mac 52:54:00:11:11:11
```


