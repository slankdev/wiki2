

# GCCチートシート

詳しい情報
http://www.asahi-net.or.jp/~wg5k-ickw/html/online/gcc-2.95.2/gcc_2.html#SEC13

## 前提知識

コンパイルとは以下の処理を行うことである
 1. 前処理
 2. 狭義コンパイル
 3. アセンブル
 4. リンク


## 一般的なオプション

 - -x language  どの言語でコンパイルするか指定
 - -c リンクはしない
 - -o name  出力ファイル名を指定
 - -v 実行されたコマンドを表示する
 - -Ipath インクルードパスにpathを追加
 - -Lpath ライブラリパスにpathを追加


## C言語
## C++
## Warning

ここでは-Wextraに含まれないオプションを列挙していく

 - -pedantic 独自拡張オプションを指定できる
 - -Wold-style-cast C++コード内でCスタイルなキャストを行っているとき警告
 - -error 警告はすべてエラーにする


## Debug

 - -g デバッグ情報を生成する
 - -Q コンパイルしている関数名を表示してその統計情報を表示


## Optimisation

 - -O -O1 -O2 -O3 最適化をする。数字が大きいほどたくさん最適化をする
 - -O0 最適化をしない。



## Preprocessing

 - include file 指定したファイルを入力として処理をする.(一番最初にfileがコンパイルされる)
 - g++ -fpreprocessed t.cpp -dD -E | sed -e'1d'
   でコメントを取り除き、先頭一行を取り除く


## Link

 - -Wl,option optionをリンカへのオプションとして渡します。gccが知らないオプションはこれで渡す
 - -whole-archive このあとにリンク指定するライブラリは順番に関わらず互いをリンクし合う。
 - -no-whole-archive whole-archiveを無効にする。 基本的に二つセットで使うっぽい？
 - -export-dynamic シンボルが生成されないやつでもシンボルを作ってくれる。(実行時リンク用)-Wl,--end-group
 - -as-needed -no-as-needed 前者はプログラム内で使用する最低限の場所にだけ、リンクをする。
   これだと生成物がスリムになってくれるかもしれないけど、関数ポインタとかで渡したりして、
   判断ができなくなったところでリンクし忘れが起きることがある。後者はこれを無効化するっぽい
 - -start-group -stop-group これらで挟んだやつはコンパイラが自動で省略したりしない。


## Asm
## Machine


