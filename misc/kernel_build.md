
# Linuxカーネル構築の伝統的方法

Archのwikiを参考にまとめた。さらに詳しい情報は以下を参照する。
https://wiki.archlinuxjp.org/index.php/%E3%82%AB%E3%83%BC%E3%83%8D%E3%83%AB/%E3%82%B3%E3%83%B3%E3%83%91%E3%82%A4%E3%83%AB/%E4%BC%9D%E7%B5%B1%E7%9A%84%E3%81%AA%E6%96%B9%E6%B3%95

## 手順

 1. カーネルソースの入手、展開
 2. カーネルのコンフィグとビルド
 3. カーネルとカーネルモジュールのインストール
 4. Grubの設定


## 1. カーネルソースの入手、展開
``kernel.org``から入手したいカーネルのソースを持ってきてホームディレクトリ以下のどこかに
展開をする。``/usr/src``以下を使用するという考え方もあるが、僕は前者の方が好きです。

```
$ mkdir kernel_build && cd kernel_build
$ wget https://cdn.kernel.org/pub/linux/kernel/v4.x/linux-4.6.4.tar.xz
$ tar xvf linux-4.6.4
$ cd linux-4.6.4
```


## 2. カーネルのコンフィグとビルド
コンフィグをする前にカーネルがまっさらな状態がないか確認することをカーネルデベロッパは
推奨しているので、それをする。

```
$ make mrproper
```

特にどぎついことをしたいわけではないので既存のカーネルのコンフィグを持ってきて、
一部それを変更する方法をとっていく。

```
$ make localmodconfig
新たなコンフィグがある場合はここでどうするかを聞かれる。
デフォの設定にしたがってエンターをいくつか押していけば終わる。
```

その後にある程度細かく設定したい場合はmenuconfigで設定を行う。
カーネルの名前とかを変えたり、IPv6を無効にしたりするときはここでやろう。
menuconfigにはncursesパッケージが必要なのでない場合はインストールしておく.

```
$ make menuconfig
```

コンフィグが終わったらビルドをする。コマンドはmakeだけだが、マルチスレッドでやったりする
オプションがあるが、今回は使わない。

```
$ make
```


## 3. カーネルとカーネルモジュールのインストール
以下の作業を行う。

 - モジュールのインストール
 - カーネルを/bootにコピー
 - initrdの作成

```
$ sudo make modules_install
$ sudo cp -v arch/x86_64/bzImage /boot/vmlinuz-YourKernName
$ sudo mkinitcpio -k FullKernName -c /etc/mkinitcpio.conf -g /boot/initramfs-YourKernName.img
```


## 4. Grubの設定
最後にGrubのメニューに追加して終わり。以下を行う。

 - ``/etc/grub/40_custom``を編集する
 - grub-mkconfigをして変更を適用する

```
$ sudo vim /etc/grub/40_custom

以下を追記
menuentry 'Slankdev's Kernel from Linux-4.6.4' {
	set root='hd0,gpt1'
	echo	'Loading My-Kernel...'
	linux	/vmlinuz-YourKernName root=/dev/sda3
	echo	'Loading Initrd...'
	initrd	/intel-ucode.img /initramfs-slankdev.img
}

```
今回はOSを/dev/sda3にインストールしていたためこのように記述した。
HDDのUUIDを調べたい場合はroot権限で``blkid``コマンドをつかうと調べることができる。
必要に応じて調べとく。


以上
