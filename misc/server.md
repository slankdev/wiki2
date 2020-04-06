
# 研究室サーバ SSH ユーザ追加手順

2018.4.17 Hiroki SHIROKURA (slank.dev@gmail.com)

## 手順

- サーバにSSHでログインする
- rootになる
- 必要な準備をする
- useraddコマンドでユーザを作成する
- 各ユーザからログインできるかを確認する



## 1ユーザに関しての具体的なコマンド操作

```
$ ssh USERNAME@ssh.ip.k.hosei.ac.jp
$ sudo su
$ mkdir -p /home/2018
$ useradd -m -g users -d /home/2018/shirokura -s /bin/bash shirokura
```



## サンプルのシェルスクリプト

```
#!/bin/sh

YEAR=2014
USER01=konoshin
USER02=chinko
USER03=gomi
USER04=manko

mkdir -p /home/$YEAR
useradd -m -g users -d /home/$YEAR/$USER01 -s /bin/bash $USER01
useradd -m -g users -d /home/$YEAR/$USER02 -s /bin/bash $USER02
useradd -m -g users -d /home/$YEAR/$USER03 -s /bin/bash $USER03
useradd -m -g users -d /home/$YEAR/$USER04 -s /bin/bash $USER04
```



## パスワードの設定方法

先ほどのユーザ作成だけでは、パスワードが設定されていない.
例として、以下のコマンドでkonoshinのパスワードを設定できる.

```
# passwd konoshin
New UNIX Password:
Retype New UNIX Password:
```

これを各ユーザに対して設定する





