
# SSH Cheatsheet

## 基本書式

```
$ ssh HOSTNAME         // user名が同じな場合
$ ssh USER@HOSTNAME
$ ssh USER@HOSTNAME -p PORTNUM -i /PATH/TO/PRIVKEY
```

## Generate Key

クライアントで公開鍵と秘密鍵を作って, サーバにクライアントの秘密鍵を登録する.
それでクライアントからクライアント秘密鍵でサーバに接続する

```
[client]$ ssh-keygen -t rsa -C your_email@example.com
[client]$ ssh-keygen -t rsa -b 4096 -C your_email@example.com
[client]$ ssh-keygen -t rsa

Generating public/private rsa key pair.
Enter file in which to save the key (/home/vagrant/.ssh/id_rsa): CONOHAVPS
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in vps.
Your public key has been saved in vps.pub.
The key fingerprint is:
SHA256:t2Vyt2r8LkPGW+GcEePwr4R6R8uhIlI6Cf9ZD+EdeRA vagrant@vagrant
The key's randomart image is:
+---[RSA 2048]----+
|            E    |
|            ..o  |
|            .+ o |
|             o=  |
|        S +.*+o= |
|    .   .o O=+O..|
|     o +  ==.B.+ |
|      * .oooO.=  |
|       +o. +o*o  |
+----[SHA256]-----+

[client]$ ls
CONOHAVPS CONOHAVPS.pub
[client]$ scp CONOHAVPS.pub USER@HOSTNAME:~/

[client]$ ssh USER@HOSTNAME
[server]$ cat CONOHAVPS.pub >> ~/.ssh/authorized_keys
[server]$ chmod 600 ~/.ssh/authorized_keys
[server]$ rm CONOHAVPS.pub

[client]$ ssh -l USER -i ~/.ssh/CONOHAVPS HOSTNAME
```

``~/.ssh``以下に``CONOHAVPS``, ``CONOHAVPS.pub``が出来上がっていて、
それぞれ秘密鍵,公開鍵である。


## .ssh/config の書き方

```
Host           host0
Hostname       10.0.0.1
User           slankdev
IdentityFile   /PATH/TO/PRIVKEY

Host           fujikojump
HostName       163.138.238.18
User           slankdev
IdentityFile   ~/.ssh/privatekey
ProxyCommand   ssh -CW %h:%p host0
```

これにより以下が同じになる

```
ssh ALIASNAME
ssh USER@HOSTNAME -p PORTNUM -i /PATH/TO/PRIVKEY
```


## ServerAliveInterval

```
$ vi .ssh/config
ServerAliveInterval 60   # 60sec毎に生きている報告をする
```

## SSHトンネル

topology
```
client---------(internet)--------(1.1.1.1)jumper(.1)-----(10.0.0.0/24)-----(.2)target[http]
```

```
client$ ssh -L 8080:10.0.0.2:80 jumper 
client$ curl localhost:8080
This is taiget's http server
```

その時のconfig

```
Host *
User slankdev

Host           jumper
Hostname       1.1.1.1
User           slankdev
IdentityFile   ~/.ssh/id_rsa

Host           jumper-tunnel
Hostname       1.1.1.1
User           slankdev
IdentityFile   ~/.ssh/id_rsa
LocalForward   8080 10.0.0.2:80

Host testvm
User slankdev
Hostname dev001-testvm.example.local
ProxyCommand  ssh -W %h:%p igw1
```

## SSH Server Operation

- log: (Ubuntu: /var/log/auth.log)
- config:
	- /etc/ssh/ 以下にある
		- sshd_config: 基本config
	- $HOME/.ssh/ 以下にもおける
		- config: client config置いてる

一部だけ
```
Port 22
Protocol 2
PermitRootLogin yes
RSAAuthentication yes
PubkeyAuthentication yes
ChallengeResponseAuthentication yes
PasswordAuthentication no
```

## Check priv,pub-keys pair is valid

```
$ ssh-keygen -y -f <private_key>
% ssh-keygen -e -f <private_key> [-m <key_format>]
```

## ssh-agent

```
TBW
```

