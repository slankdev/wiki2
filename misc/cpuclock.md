
# CPUクロック速度の設定

事前に以下を編集.
これでintel pstateを無効化する。これはユーザに動作周波数を変えさせないようにする

```
$ sudo vim /etc/default/grub
GRUB_CMDLINE_LINUX="intel_pstate=disable"
$ sudo grub-update
```


```
# cpupower frequency-set -g performance
# cpupower frequency-set -g powersave
# cpupower frequency-set -g userspace
# cpupower frequency-set -f 800000
```


