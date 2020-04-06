

# Systemtap導入方法


カーネルをビルドする方法でやった。



## 下準備

apt-get sourceとかを使えるようにしないといけないので、
``/etc/apt/sources.list``を編集する。

```
$ sudo vim /etc/apt/sources.list

// 以下みたいなのをコメントを解除する
# deb-src http://archive.canonical.com/ubuntu xenial partner
```

あとは以下のとおりにやっていく。(解説省略)
最後のコマンドの時はtab補完がきかないことに注意する。
一回できていたのに、補完されなかったからもう一回ビルドしたことがあった。。。涙


```
$ cd $HOME
$ sudo apt-get install dpkg-dev debhelper gawk
$ mkdir tmp
$ cd tmp
$ sudo apt-get build-dep --no-install-recommends linux-image-$(uname -r)
$ apt-get source linux-image-$(uname -r)
$ cd linux-2.6.31 (this is currently the kernel version of 9.10)
$ fakeroot debian/rules clean
$ AUTOBUILD=1 fakeroot debian/rules binary-generic skipdbg=false
$ sudo dpkg -i ../linux-image-debug-2.6.31-19-generic_2.6.31-19.56_amd64.ddeb
```



## 実行方方

```
$ vim main.cc
$ g++ -g main.cc 
$ vim trace.stp
$ sudo stap trace.stp -c "./a.out" | c++filt | less
```

c++filtでデマングリングしてくれる。






## 参考文献

 - official https://wiki.ubuntu.com/Kernel/Systemtap
 - samples https://sourceware.org/systemtap/examples/keyword-index.html
 - 神サイト https://sourceware.org/systemtap/examples/keyword-index.html







## SystemTap Cheatsheet


### Event

 - event {} -> event handle
 - event.return{} -> event ret handle


#### Synchronism Event

 - syscall.SYSCALLNAME
 - kernel.function("KERNFUNCNAME")
 - kernel.trace("TRACEPOINT")
 - module("MODNAME").function("FUNCNAME")

#### Asynchronism Event
 
 - begin()
 - end()
 - timer
	 - timer.s(N)
	 - timer.ms(N)
	 - timer.us(N)
	 - timer.ns(N)
	 - timer.hz(N)
	 - timer.jiffies(N)

### Handler/Body

 - printf()
 - systemtap functions
	 - tid()
	 - uid()
	 - cpu()
	 - gettimeofday_s()
	 - ctime()
	 - pp()
	 - thread_indent(N)


#### Define Function

```
function FUNCNAME:RETTYPE() {
	printf("my func \n");
	...
}
```




