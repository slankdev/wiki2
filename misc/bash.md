
# Bash Cheatsheet

function
```
#!/bin/bash
function f1 () {
    echo f1
}
```

check file
```
#!/bin/sh

if [ -e ~/.ssh/config ]; then
  mv ~/.ssh/config ~/.ssh/config.bak
  echo Already ~/.ssh/config was exist. rename
fi

ln -sf `pwd`/config ~/.ssh/config
```

引数チェック例
```
#!/bin/sh

if [ $# -ne 2 ]; then
	echo "invalid command syntax" 1>&2
	echo "Usage: $0 <arg0> <arg1>" 1>&2
	exit 1
fi

echo success
```

実行結果
```
$ /tmp/sh.sh slank test
success
$ /tmp/sh.sh slank test tet
invalid command syntax
Usage: /tmp/sh.sh <arg0> <arg1>
```

## 参考情報

```
#!/bin/sh
echo $#
while [ "$1" ]
do
    echo "$1"
    shift
done
```
実行結果
```
$ /tmp/sh.sh asf adf
2
asf
adf
$ /tmp/sh.sh asf adf sdfdf
3
asf
adf
sdfdf
```

```
count=1
count=$(expr $count + 1) # => 2

count=1
count=$((++count))    # => 2
count=$((count++))    # => 2
count=$((count += 1)) # => 3
```

switch
```
case "$var" in
  "test" ) echo "testという文字列" ;;
  a* ) echo "aで始まる文字列" ;;
  ?b* ) echo "2文字目がbの文字列" ;;
  [A-Z]* ) echo "大文字で始まる文字列" ;;
  [!xX]* ) echo "先頭がxではない文字列" ;;
  * ) echo "上記のいずれでもない文字列" ;;
esac
```
