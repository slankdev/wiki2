
# Docker Command

Dockerコマンドのよく使うものの備忘録的なやつ

	
## ps
コンテナの一覧を表示
	
	$ docker ps [OPTIONS] 

### OPTIONS

 - a 停止しているコンテナも表示
 - q IDのみを表示する

### EXAMPLE

	$ docker ps -aq  // 全てのコンテナのIDを表示する

## images
作成されているイメージを確認。

	$ docker images [OPTIONS] [REPOSITORY[:TAG]]

### OPTIONS

 - a 全てのイメージを表示
 - q IDのみを表示する
 - digest ダイジェストを表示

### EXAMPLE

	$ docker images // イメージを表示
	$ docker images -aq   // 全てのイメージのIDを表示する


## rm
コンテナを消去するときに使う。A
	
	$ docker rm [OPTIONS] CONTAINER [CONTAINER...]	

### OPTIONS

 - f 起動しているコンテナも消去する
 - l リンクを消去する。
 - v ボリューム関連のコンテナを消去する。

### EXAMPLE

	$ docker rm `docker ps -a -q`  //停止しているコンテナを全て消去


## rmi
イメージを消去
	
	$ docker rmi [OPTIONS] IMAGE [IMAGE...] 

### OPTIONS

 - f 強制的に消去

### EXAMPLE

	$ docker rmi nginx  // nginxイメージを消去
	$ docker rmi $(docker images -aq)  // 全てのイメージを消去する




## pull
	
	$ docker pull [OPTIONS] IMAGE[:TAG]

Docker Hubからイメージをダウンロードする。
タグ名を省略すると、最新版(latest)がダウンロードされる。
URLを指定してイメージをダウンロードすることもできる。

### OPTIONS

 - a 全てのタグをダウンロードする

### EXAMPLE
	
	$ docker pull ubuntu:latest // ubuntuイメージの最新版をダウンロード
	$ docker pull ubuntu        // ubuntuイメージの最新版をダウンロード
	$ docker pull -a ubuntu     // ubuntuイメージの全てのタグをダウンロード
	$ docker pull rgst.hub.com/centos:7 // https://rgst.hub.comからcentos:7をダウンロード



## build

	$ docker built [OPTIONS]  DOCKERFILEDIR

Dockerfileからイメージの作成を行う。tオプション以外ほとんど使わない気がする

### OPTIONS

 - t IMAGE[:TAG] イメージ名とタグ名を指定してビルド

### EXAMPLE

	$ docker build -t test:9.1 /tmp/    /tmp/以下にあるDockerfileからtest:9.1としてイメージを作成
	$ docker build -t slank  .    カレントディレクトリにあるDockerfileからslankとしてイメージ作成



## run

	$ docker run [OPTIONS] IMAGE[:TAG] [COMMAND]

イメージからコンテナを生成して実行。nameオプションを指定しないと、
適当に名前をつけられる。(たまに卑猥な名前になる気がする。)  
フォアグラウンドで動かす時に、itオプションは常に必要なのかまだ不明


### OPTIONS
 
 - 標準オプション
	 - name=NAME 名前をNAMEとしてつける
	 - t  TTYを確保して、端末デバイスを使用する
	 - i  コンテナ起動後STDOUTを開きっぱなしにする
	 - h  ホスト名を指定する
	 - d  デタッチ。コンテナを作成し、バックグラウンドで実行する
	 - rm コンテナ実行終了後にコンテナを自動的に消去する

 - ネットワーク関連
	 - add-host=HOSTNAME:IP コンテナの/etc/hostsにHOSTNAME=IPの名前解決レコードを登録
	 - dns=IP  コンテナのDNSサーバをIPに指定
	 - h HOSTNAME コンテナ自体のホストネームをHOSTNAMEに指定
	 - p HOST:CONTAINER ホストのポートHOSTをコンテナのポートCONTAINERに割り当てる
	 - link これはまだわからん

### EXAMPLE

	$ docker run -it centos   // centos:latestのコンテナを作成実行
	$ docker run -d httpd:1.0 // httpd:1.0のコンテナをバックグラウンドで作成実行





## commit

	$ docker commit [OPTIONS] CONTAINER [IMAGE[:TAG]]

コンテナの変更結果を新たにイメージとして保存する


### OPTIONS

 - a author情報を付加
 - m メッセージを付加
 - p コンテナを一時停止してコミットする

### EXAMPLE

	$ docker commit base new // baseというコンテナの変更点をnewとしてイメージを作成


 
