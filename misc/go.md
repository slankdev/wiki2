
# Go lang

```
$ sudo apt-get update && sudo apt-get install gcc make golang-1.10
$ echo export PATH=$PATH:/usr/lib/go-1.10/bin >> ~/.bashrc
$ source ~/.bashrc
$ echo "export GOPATH=$HOME/go"        >> ~/.bashrc
$ echo "export PATH=$PATH:$GOPATH/bin:" >> ~/.bashrc
```

install with apt on ubuntu16.04
```
$ sudo add-apt-repository ppa:longsleep/golang-backports
$ sudo apt-get update && sudo apt-get install -y golang-go
```

install with binary
```
// download go binary from ``https://golang.org/dl/``
$ tar -C /usr/local -xzf go$VERSION.$OS-$ARCH.tar.gz
```



