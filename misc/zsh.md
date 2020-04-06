
# Zshチートシート

```
$ command 2>&1      標準エラー出力を標準出力にリダイレクト
$ command 1>&2      上のやつの逆
$ command > /dev/null    出力をなくす
$ command > /dev/null 2>&1 標準{|エラー}出力をなくす
$ 
```

## 制御構文

### 条件文

```
3 -gt 2
3 -lt 2
3 -gt 2
3 -lt 2
3 -gt 2
3 -lt 2
```


### if文

```
if 条件文1
then
    命令1
elif 条件文2
    命令2
elif 条件文3
    命令3
else
    命令4
fi
```

### while文

```
while 条件文
do
	命令
done
```

### for文

```
for i in {1..10}
do
	print $i
	命令
done
```

