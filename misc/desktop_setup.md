# Xmonadの環境構築

タイル型WMであるxmonadとステータスバーであるxmobarの環境構築を行う

# sshでの作業


## 必要なパッケージをインストール

日本語入力を行うには日本語のフォントがインストールされている必要がある。
まずotf-ipafontをpacmanからインストールする。（otf-ipaexfontではだめだった。）

```
# pacman -S vim  エディタ
# pacman -S zsh  シェル
# pacman -S git  バージョン管理
# pacman -S tmux ターミナルマルチプレクサ

# pacman -S ttf-hack   フォント
# pacman -S gvim       vimのクリップボードのため
# pacman -S lua        使います
# pacman -S python     使います
# pacman -S ctags      ご存知タグ

# pacman -S otf-ipafont      日本語フォント
# pacman -S ibus-anthy       日本語対応IM
# pacman -S nitrogen         壁紙管理
# pacman -S networkmanager   ネットワーク管理
# pacman -S xscreensaver     スクリーンセーバ

# pacman -S xorg-server xorg-server-utils xorg-xinit
# pacman -S xf86-video-intel
# pacman -S xf86-input-synaptics
# pacman -S xmonad xmonad-contrib  タイル型WM
# pacman -S xmobar                 便利なステータスバー
# pacman -S dmenu                  ショートカットでプログラムを実行するやつ

# pacman -S firefox        ブラウザ
# pacman -S nautilus       ファイルブラウザ
# pacman -S eog            画像ビューア(Eye of GNOME)
# pacman -S totem          メディアプレーヤ(GNOME Videos)
# pacman -S rxvt-unicode   ターミナルソフト

まとめたコマンド
# pacman -S vim zsh git tmux
# pacman -S ttf-hack gvim lua python ctags
# pacman -S otf-ipafont ibus-anthy nitrogen networkmanager xscreensaver
# pacman -S xorg-server xorg-server-utils xorg-xinit  xf86-video-intel
# pacman -S xmonad xmonad-contrib xmobar dmenu
# pacman -S firefox nautilus eog totem rxvt-unicode chromium
# yaourt -S urxvt-resize-font-git global
```




## ユーザ作成

useraddコマンドでユーザを作成する。
```
# useradd -m -g users -d /home/slank -G wheel -s /usr/bin/zsh slank
# passwd slank
```
作成したユーザをsudoersに追加する。
```
# visudo
%wheel ALL=(ALL) ALL　がある行のコメントアウトを解除
```
これで作成したユーザがsudoを使える様になる。


## LibPGENをインストール


```
$ cd ~/
$ mkdir git && cd git
$ git clone http://github.com/slankdev/libpgen.git && cd libpgen
$ make && sudo make install
```


## Dotfilesを準備

```
$ git clone https://github.com/slankdev/dotfiles.git ~/dotfiles
$ cd dotfiles
$ sh setup.sh all
```

### zplug, neobundle, gitの設定

~/dotfilesに移動して``zplug install``を実行
neobundleはvimを起動するだけ。

gitはユーザ名とメールアドレス、デフォルトのエディタを指定する
```
$ git config --global user.name  "slank"
$ git config --global user.email "slank.dev@gmail.com"
$ git config --global core.editor vim
```



## ネットワークインターフェースの名前を変更する

/etc/default/grub を編集する。
先頭のほうにGRUB_CMDLINE_LINUXがあるので、そこに
``biosdevname=0 net.ifnames=0``を追記する。

変更後は反映する為に以下のコマンドを実行する
```
# grub-mkconfig -o /boot/grub/grub.cfg
```



## NetworkManager

ネットワークの設定などはNetworkManagerを使用する

有効化する

```
$ sudo systemctl start NetworkManager.service
$ sudo systemctl enable NetworkManager.service
```




## Yaourtの設定

Yaourtコマンドを使える様にする。
/etc/pacman.confの末尾に以下を追加する。


```
# vim /etc/pacman.conf
```

以下を追記する

```
[archlinuxfr]
SigLevel = Never
Server = http://repo.archlinux.fr/$arch
```

pacmanを更新

```
# pacman --sync --refresh yaourt
# pacman -Syu
```







## Xmonadの有効化


Window Managerは /usr/share/xsessions/以下に\*.desktop として保存されているため、
インストール確認はそこを参照

/etc/X11/xinit/xinitrcを~/にコピーして最後の``exec ...``を``exec xmonad``に変更する。




## タッチパッドの設定

synapticsのドライバが素晴らしいのでそれにたよる
Xorgサーバの設定ファイルを使って設定を行う。
/usr/share/X11/xorg.conf.d/50-synaptics.confがデフォルトの設定ファイルな
ため、/etc/X11/xorg.conf.d/以下にコピーして編集することでここの設定を
反映させることができる。

自己環境では以下のような設定になっている。

```
Section "InputClass"
    Identifier "touchpad catchall"
    Driver "synaptics"
    MatchIsTouchpad "on"
    Option "TapButton1" "1"
    Option "TapButton2" "3"
	Option "TouchpadOff" "2"S # これでタップがoffになり、クリックのみ有効
    Option "VertScrollDelta"  "-111" # OSXのようなナチュラルスクロール
    Option "HorizScrollDelta" "-111" # OSXのようなナチュラルスクロール
    Option "FingerHigh" "40"  # vaioではコメントアウトする
    Option "FingerLow"  "31"  # vaioではコメントアウトする
    Option "PalmDetect" "1"
	Option "PalmMinWidth" "10"
	Option "PalmMinZ"     "200"
    MatchDevicePath "/dev/input/event*"
EndSection
```

Ubuntuのときのnatural scrollingのhelp
https://askubuntu.com/questions/91426/reverse-two-finger-scroll-direction-natural-scrolling

## フォントを綺麗に表示する方法

/etc/font/conf.avail/71-no-embedded-bitmaps.confを作成し、以下を記入
(詳細な設定方法とこうなる理由はまだわからん。。)

```
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
  <match target="font">
    <edit mode="assign" name="embeddedbitmap">
      <bool>false</bool>
    </edit>
    <edit mode="assign" name="hintstyle">
       <const>hintnone</const>
    </edit>
  </match>
</fontconfig>
```
/etc/fonts/conf.d/にリンクをはる
```
$ sudo ln -s /etc/fonts/conf.avail/71-no-embedded-bitmaps.conf /etc/fonts/conf.d/71-no-embedded-bitmaps.conf
```

直接ファイルを置いて設定すればよいのではないか、とかいろいろツッコミどころが
あるが、とりあえず現段階はこれでよしとしよう。



### レイアウト設定

CUIモードでは``$ sudo loadkeys [jp106|us]``で設定でき、
GUIモードではで``$ sudo setxkbmap -layout [jp|us]``設定できる。


Ctrlキーの設定は
/etc/X11/xorg.conf.d/00-keyboard.confに以下を書き込む

```
Section "InputClass"
	Identifier "system-keyboard"
	MatchIsKeyboard "on"
	Option "XkbLayout" "jp,us"
	Option "XkbOptions" "ctrl:nocaps" # このぶぶんが重要
EndSection
```

xmodmapは単純な作業意外で使うことは推奨されていないらしく、
なるべくxkbを使うのがよさそう。
gnomeなどに設定を上書きされることがあるので、その都度注意する。

### Xの外でもCaps<-Ctrlにする方法

dumpkeysで現在のレイアウトをファイルに出力してからそれを一部編集して、再度loadkeysすれば
Xの外でもキーレイアウトを自由に変更することができる。
デフォルトのファイル群は``/usr/share/kbd/keymaps/i386/qwerty/``にある.

```
$ sudo dumpkeys | sudo tee /path/to/file.map
$ sudo vim /path/to/file.map

# 末尾に以下を追加
keycode 58 = Control

$ sudo loadkeys /path/to/file.map
```

これで変更することが出来る。


### キーリピートの時間設定

xsetコマンドで簡単に設定ができる

```
$ xset r rate 195 62
```


## サウンドの設定

以下のパッケージを入れていくつかファイルを編集すればよい

```
$ sudo pacman -S alsamixer
$ sudo vim /etc/asound.conf

# 以下を追記
defaults.pcm.card 1
defaults.pcm.device 0

$ alsamixer
```

F6でデバイスを指定して、音の大きさを設定する。これで大丈夫なはず




## Xmonad, Xmobarの設定

私はdotfilesで管理しているのでその設定ファイルの展開されているので割愛。
詳しくはslankdev/dotfilesを参照







# 実機での作業


## デスクトップの壁紙の設定

nitrogenを使う。``$ nitrogen path-to-picture-dir``で設定でき、
``$ nitrogen --restore``で起動



## 日本語入力環境を整える

ibus-anthyの設定は以下のコマンドでできる
```
$ ibus-setup
```
InputMethodタブでJapanese(Anthy)を追加。
Advancedタブでuse system layoutにチェック











### xmonad.hsで設定済みの内容

#### X起動時に自動起動する内容

一部を紹介する
```
spawn "ibus-daemon --xim --replace &"  -- ibus起動
```

ibusをコマンドから起動させるには
```
$ ibus-daemon --xmin --replace &
```
で起動できる



# トラブルシューティング

## スリープ解除後などに設定どうり動かない

Mod-qで再コンパイルすればなおるで



# MBP用の設定

## 無線LANの認識
https://wiki.archlinuxjp.org/index.php/Broadcom_%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9#wl_.E3.82.AB.E3.83.BC.E3.83.8D.E3.83.AB.E3.83.A2.E3.82.B8.E3.83.A5.E3.83.BC.E3.83.AB.E3.81.AE.E3.83.AD.E3.83.BC.E3.83.89

を参考に行う。自分の場合はwlをmodprobeすることで無線Lanインターフェースが認識された。

```
$ yaourt -S broadcom-wl // これたぶんいらない
$ yaourt -S broadcom-wl-dkms
$ sudo rmmod b43
$ sudo rmmod ssb
$ sudo modprobe wl
$ sudo depmod -a
```

Ubuntuの場合以下のサイトにそって行う
https://wiki.ubuntulinux.jp/UbuntuTips/Hardware/HowToSetupBcm43xx

