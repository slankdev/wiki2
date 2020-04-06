
# GDB

```
(gdb) p/t value    // 2進数
(gdb) p/x value    // 16進数
(gdb) x/20xb value // 20個 b:1個=byte, x:表示は16進数
	 x:hex, d:dec, u:u-decimal, o:oct,
	 a:address, c:char, f:float, s:string,
	 t:binary
(gdb) info b
(gdb) delete 1
(gdb) b printf
```

## コンパイルのときのこと

32bitでコンパイルしていろいろ簡単にコンパイルする必要があるので、
いくつかオプションを指定する

```
```

## コマンドについて

### 簡単なコマンド(独断と偏見)

 - info breakpoints ブレークポイントを確認
 - info registers [REGISTER] レジスタ情報を表示
 - run [ARGS..] プログラムを実効
 - quit gdbを終了


### next, step, nexti, stepi

 - next 次の命令を実効(callの中に入らない)
 - step 次の命令を実効(callの中に入る)
 - nexti nextのアセンブリ命令版
 - stepi stepのアセンブリ命令版
 - set $eax=100 eaxに100を代入


### x

シンタックス
```
 x/[Number][Format][Unit]
```

 - Number
 	- 1,2,3...
 - Format
	 - b 1byte
	 - h 2byte
	 - w 4byte
	 - g 8byte
 - Unit
	 - x hex
	 - d dec
	 - u unsigned dec
	 - o oct
	 - a address
	 - c char
	 - f float
	 - s string

