# Arch Linux インストールバトル 2015/09/08

## UEFIで起動しているかを確認する
以下のコマンドを実行してBIOS起動かEFI起動かを確認する。
ここで、もしefiというディレクトリが存在していればEFIで起動している。

```
# ls /sys/firmware/
acpi/ efi memmap/
```

また、起動時のブートローダがカラーで起動している場合はBIOS起動をしているみたいです。(tahnks @aruneko)
EFI起動している場合はArchのアイコンなどは表示されません。


## SSH経由でインストールする

iosイメージにsshdが入っているので、それでssh-serverのデーモンを起動する。

```
# systemctl start sshd
# passwd
# wifi-menu

まとめたコマンド
# systemctl start sshd ; passwd ; wifi-menu
```


## ネットワーク接続の確認とキーボードレイアウトの設定
デフォルトのキーレイアウトはus配列になっているので、もしjp配列のキーボードを使っている場合は
jp106に設定する。

```
# loadkeys jp106
```

ネットワークの接続を確認する。
無線LANでの接続でインストールを行うこともできるが、めんどくさいので、今回は有線接続で行った。
googleにpingを打ってネットワークの接続確認をする。

```
# ping -c3 www.google.com
```


## ドライブのパーティショニング

以前使用してたドライブへインストールする場合は、以下のコマンドでドライブの既存のパーティションを消しておく

```
# sgdisk --zap-all /dev/sda
```


Archをインストールする記憶領域をパーティショニングしていく。今後の作業はBIOS起動とEFI起動で
作業工程が若干違うので注意する。だが作業する内容はBIOS起動でもEFI起動でも同じなので、その作業内容を
最初に説明する。


1. パーティションテーブルを作成する
2. パーティションを追加する
3. パーティションをフォーマットする

次にBIOS起動とEFI起動で作業内容が違うところを説明していきます。
-  パーティショニング方法が違う(UEFI System Partitionと)
-  ディスクのフォーマット方式が違う (これはおなじでもうまくいくかもしれない)

今回作成するパーティション構造は以下の様にします。homeディレクトリを別パーティションにはしません。

```
/dev/sda1: /boot	()
/dev/sda2: swap		(swapパーティション)
/dev/sda3: /		(ルートディレクトリ)
```

では以下ではBIOS起動時とEFI起動時でそれぞれ説明していきます。

### EFI起動でのパーティショニング
#### 既存のパーティションを消去

```
# dd if=/dev/zero of=/dev/sdX bs=1M count=4
```

####  GPTパーティションの作成

```
# gdisk /dev/sda
Command (? for help): o			(パーティションテーブルの作成)
Proceed? (Y/N): y

Command (? for help): n（新しいパーティションを作る）
Partition number : (空enter)
First sector: (空enter)
Last sector: +512M
Hex code or GUID: ef00 (UEFI System partition用のパーティションなのでef00にする)

Command (? for help): n
Partition number: (空enter)
First sector: （空enterl）
Last sector: +4G
Hex code or GUID: 8200 (linux-swap用は8200)


Command (? for help): n
Partition number: (空enter)
First sector: （空enter）
Last sector: （空enter）
Hex code or GUID: （空enter）

Command (? for help): w
Do you want to proceed?: Y
```





## 作成したパーティションをフォーマット
前項で作成したパーティションをフォーマットする。
bootパーティションはfat32,他はext4でフォーマットする。
スワップパーティションはmkswapで設定する。

```
# mkfs.fat -F32 /dev/sda1
# mkswap /dev/sda2
# swapon /dev/sda2
# mkfs.ext4 /dev/sda3

まとめたコマンド
# mkfs.fat -F32 /dev/sda1 ; mkswap /dev/sda2 ; swapon /dev/sda2 ; mkfs.ext4 /dev/sda3
```



## パーティションをマウント
フォーマットしたら/mnt以下にマウントしていきます。

```
# mount /dev/sda3 /mnt
# mkdir /mnt/boot
# mount /dev/sda1 /mnt/boot

まとめたコマンド
# mount /dev/sda3 /mnt ; mkdir /mnt/boot ; mount /dev/sda1 /mnt/boot
```



## Arch環境の構築
ここからは共通のやるだけ作業なんで簡単です。

#### pacmanのミラーサーバの設定とpacstrap
設定ファイルを編集して日本のサーバを先頭に持ってきます。

```
# vi /etc/pacman.d/mirrorlist
```

だいたいScore: 2.3 くらいに日本のサーバがあります。
日本のサーバを指定したらbase, base-develをインストール

```
# pacstrap /mnt base base-devel
```


#### fstabを生成
/etc/fstab ファイルはディスクパーティションや様々なブロックデバイス、
リモートファイルをどうやってファイルシステムにマウントするかを記述します。

```
# genfstab -U -p /mnt >> /mnt/etc/fstab
```


#### /mntにchrootする

```
# arch-chroot /mnt /bin/bash
```


#### ロケールの設定
locale を設定する。 /etc/locale.gen を編集して locale-genでlocaleを生成する。
次にlocale.conf を作成する。 /etc/locale.confにファイルを作成して、それをexportで大域変数追加する。

```
# vi /etc/locale.gen

en_US	(ここをコメントアウト)
ja_JP	(ここをコメントアウト)
```
localeファイルを生成して,
最後にLANG=ja_JP.UTF-8を付加する。

```
# locale-gen
# echo "LANG=en_US.UTF-8" >> /etc/locale.conf
# export LANG=en_US.UTF-8

まとめたコマンド
# locale-gen ; echo "LANG=en_US.UTF-8" >> /etc/locale.conf ; export LANG=en_US.UTF-8
```


#### タイムゾーンの設定
タイムゾーンのファイルがあるのでそのファイルのシンボリックリンクを貼る

```
# ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
# hwclock --systohc --utc

まとめたコマンド
# ln -s /usr/share/zoneinfo/Asia/Tokyo /etc/localtime ; hwclock --systohc --utc
```

#### ネットワーク接続の設定(DHCP), ホストネームの設定
IPアドレスの自動取得を有効かするためにDHCPクライアントのデーモンを有効化する。


```
# systemctl enable dhcpcd.service
# echo x250 > /etc/hostname

# systemctl enable dhcpcd.service && echo usb > /etc/hostname
```

#### rootパスワードの設定

```
# passwd
```

#### キー配列の設定(任意？？わからん)

```
# loadkeys jp106
# echo "FONT=Lat2-Terminus16" >> /etc/vconsole.conf
# echo KEYMAP=jp106 >> /etc/vconsole.conf

# loadkeys jp106 && echo "FONT=Lat2-Terminus16" >> /etc/vconsole.conf && echo KEYMAP=jp106 >> /etc/vconsole.conf
```
#### pacmanの設定

```
# vi /etc/pacman.conf

...
[multilib]
Include = /etc/pacman.d/mirrorlist  (ここをコメントアウトする)
...
```

変更を反映する

```
# pacman -Syu
```

#### Intel製のCPUを仕様している場合
Intel製のCPUを仕様している場合はIntelのマイクロコードのアップデートを有効にするためにintel-ucodeを
インストールする必要がある。

```
# pacman -S intel-ucode
```




## ブートローダのインストールと設定
まずgrubのパッケージをインストール


次にbrupを起動パーティションにインストールするのですが、ここもBIOS起動とEFI起動で手順が変わる。


### EFI起動の場合
#### EFI System Partitionを操作するためのパッケージ, Grubをインストール

```
# pacman -S dosfstools efibootmgr grub
# grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=arch_grub --recheck
```

さらに /boot/EFI/bootにもブータブルスタブを作成

```
# mkdir /boot/EFI/boot
# cp /boot/EFI/arch_grub/grubx64.efi /boot/EFI/boot/bootx64.efi
```

grub.cfgを作成

```
# grub-mkconfig -o /boot/grub/grub.cfg
```



## 設定は以上なので再起動
お疲れさまでした。設定は以上で終了なので、chrootしたところからexitで脱出して、
/mntをアンマウントして、再起動しましょう。

```
# exit
# umount -R /mnt
# reboot
```

これで次の起動時はインストールしたArchを起動するgrubが立ち上がるはずです。






