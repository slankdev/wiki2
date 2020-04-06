
# OpenSSL

encrypt
```
openssl aes-256-cbc -e -md sha256 -in iproute2.tgz -out iproute2.tgz.encrepted
enter aes-256-cbc encryption password: #hogehoge
Verifying - enter aes-256-cbc encryption password: #hogehoge
```

decrypt
```
openssl aes-256-cbc -d -md sha256 -in iproute2.tgz.encrepted -out iproute2.tgz
```

generate safe-password
```
pwgen -sy 16 1

-s
-y
-0
-A
```
