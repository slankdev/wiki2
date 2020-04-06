
# GoBGP

```
$ cd /tmp
$ wget https://github.com/osrg/gobgp/releases/download/v1.33/gobgp_1.33_linux_amd64.tar.gz
$ tar xpf gobgp*
$ cp gobgp gobgpd $GOPATH/bin/
```

command line completion
```
$ sudo apt-get install bash-completion
$ echo source /etc/bash_completion >> ~/.bashrc
$ echo source $GOPATH/src/github.com/osrg/gobgp/tools/completion/gobgp-completion.bash >> ~/.bashrc
```
