
# Docker

**Easiest Instralltion**
```
$ curl -fsSL get.docker.com | sudo sh
$ sudo usermod -aG docker $USER
```

**Instralltion**
```
$ sudo apt-get update && sudo apt-get install -y \
    apt-transport-https ca-certificates curl \
    software-properties-common
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) stable"
$ sudo apt-get update && sudo apt-get install -y docker-ce && sudo usermod -aG docker $USER
```

```
$ sudo curl -L "https://github.com/docker/compose/releases/download/1.12.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose && docker-compose -v
docker-compose version 1.12.0, build b31ff33
```


**Basic Operation**

```
$ docker pull ubuntu
$ docker pull ubuntu:latest # same as above
$ docker pull ubuntu:16.04
```

```
$ docker run -it ubuntu /bin/bash             # ubuntu:latest
$ docker run -it ubuntu:16.04 /bin/bash       # run: create + start
$ docker run -it --rm ubuntu /bin/sh          # remove after termination
$ docker run -it --name "Baka" ubuntu /bin/sh # naming
$ docker run -d centos /bin/ping dpdk.ninja   # -d: background-exe
$ docker rum --net='host' -it ubunt /bin/bash # use host's network stack (share)
$ docker run --rm ubuntu /bin/echo "Hello Docker"
```

```
$ docker rm `docker ps -aq`  # Stoped container only
$ docker rm -f `docker ps -aq` # All container forcibly
```

```
$ docker ps --all
$ docker run -it -d --rm --name tttest ubuntu:16.04
$ docker commit tttest slankdev/ubuntu:16.04
$ docker push slankdev/ubuntu:16.04
```

```
[machine]$ docker run -it --name baka ubuntu /bin/bash
[ubuntu]# apt update && apt install -y sl
[machine]$ docker commit baka ubunt:slankdev
```

status確認
```
host$ docker stats test --format "table {{.Container}}\t{{.MemUsage}}"
```


## その他

docker pull などでNetwork timed out が出た時は
docker-machineを再起動しなおせば直る。

	$ docker-machine restart MACHINENAME
	$ eval $(docker-machine env MACHINENAME)

- http://www.atmarkit.co.jp/ait/articles/1407/08/news031.html
- https://docs.docker.com/


## Dockerfileの書き方

{命令} {引数} という感じにスペース区切りで記述していく。
'#'から始まる行はコメントとして処理される。

Dockerfileでは以下の命令を指定できる

| 命令        | 用途                              |
|:------------|:----------------------------------|
| FROM        | 元となるDockerイメージを指定      |
| MAINTAINER  | 作成者情報                        |
| RUN         | コマンド実行                      |
| ADD         | ファイル/ディレクトリの追加       |
| CMD         | コンテナの実行コマンド1           |
| ENTRYPOINT  | コンテナの実行コマンド2           |
| WORKDIR     | 作業ディレクトリの指定            |
| ENV         | 環境変数の指定                    |
| USER        | 実行ユーザの指定                  |
| EXPOSE      | ポートのエクスポート              |
| VOLUME      | ボリュームのマウント              |

各それぞれの命令について記述していく。

**FROM**
コンテナの元となるDockerイメージを指定する。
イメージはdocker hubから持ってきてるっぽい。
指定方法は{イメージ名}:{タグ名}という感じに指定してやればいい。

```
	FROM [IMAGE]
	FROM [IMAGE]:[TAG]
	FROM [IMAGE]:[DIGEST]
```

```
	FROM ubuntu:14.04　　# DockerHubからubuntuの14.04を持ってくる
	FROM ubuntu          # DockerHubからubuntuのlatestを持ってくる
	FROM
```

**MAINTAINER**
Dockerfileの作成者情報を指定する。これはなくても大丈夫っぽい。
メールアドレスでも名前でもなんでも大丈夫なもよう。
Docker Hub でイメージ公開するなら必ず記述しとくこと

```
	MAINTAINER [AUTHOR_INFO]
```

```
	MAINTAINER slank.dev@gmail.com
	MAINTAINER Hiroki Shirokura slank
```


**RUN, CMD**
コマンドを実行する。RUNは外部パッケージとかのインストールをするために使う。
CMDはRUNなどで入れたパッケージとかの起動で使う。
sshdとかをコンテナで動作させる時はこれを使う。
Shell形式とExcel形式があるが、自分はShell形式しか使わないため、
Excel形式は省く。

```
	RUN [COMMAND]
	CMD [COMMAND]
```

```
	RUN apt-get -y install openssh-server  # sshdをインストールする
	RUN yum -y install httpd               # apacheをインストール
	CMD /usr/sbin/httpd -D FOREGROUND      # httpdをフォアグラウンドで実行
```

**ADD**
ファイル/ディレクトリの追加を追加する時に指定する。
ディレクトリなどを共有する時に指定するっぽい

```
	ADD Docker/tmp/ /tmp/
	ADD http://hoge.com/bashrc /root/.bashrc
```

**EXPOSE**
expose=晒す、のとおり、コンテナが外部に公開するポートを指定します。
WEBサーバなどなら80とかを指定する。

```
	EXPOSE 80
	EXPOSE 8080
```

## DPDK

```
# docker pull slankdev/ubuntu:16.04
# echo 4 > /sys/devices/system/node/node0/hugepages/hugepages-1048576kB/nr_hugepages
# echo 2048 > /sys/devices/system/node/node0/hugepages/hugepages-2048kB/nr_hugepages
# mount -t hugetlbfs -o pagesize=1G none /dev/hugepages
# mkdir -p /mnt/huge_c0
# mount -t hugetlbfs -o pagesize=1G none  /mnt/huge_c0
# docker run -it --rm --privileged -v /mnt/huge_c0/:/dev/hugepages/ --net='host' slankdev/ubuntu:16.04
```

- https://community.mellanox.com/docs/DOC-2978
- https://github.com/redhat-performance/docker-dpdk

## Docker netns mount script

```
#!/bin/sh

if [ $# -ne 2 ]; then
        echo "invalid command syntax" 1>&2
        echo "Usage: $0 <containername> <netnsname>" 1>&2
        exit 1
fi

PID=`docker inspect $1 -f "{{.State.Pid}}"`
mkdir -p /var/run/netns
ln -s /proc/$PID/ns/net /var/run/netns/$2
```

## Changen escape key

It doesn't need to restart docker daemon for apply new config. That's good.
```
$ mkdir -p ~/.docker
$ vim ~/.docker/config.json
$ cat ~/.docker/config.json
{
    "detachKeys": "ctrl-\\"
}
```

## Remote control

```
# vim /lib/systemd/system/docker.service
# systemctl daemon-reload
# systemctl stop docker
# systemctl start docker
# docker -H tcp://localhost:2376 info
```

```
- ExecStart=/usr/bin/dockerd -H fd://
+ ExecStart=/usr/bin/dockerd -H tcp://0.0.0.0:2376 -H fd://
```

```
client$ docker -H tcp://192.168.56.102:2376 info
client$ export DOCKER_HOST=tcp://192.168.99.36:2376
client$ docker info
```

