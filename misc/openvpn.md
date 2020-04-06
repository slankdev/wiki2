
# OpenVPN

## Required Package Install

```
# apt-get install -y openvpn easy-rsa
```

## Configuration & Environment

```
[CLIENT]$ tree .
.
├── ca.crt
├── client.crt
├── client.key
└── client.conf
[CLIENT]$ sudo openvpn --config client.conf
```

[SERVER] procedure
```
make-cadir ~/ca && cd $_
vi ./vars
source ./vars
./clean-all
./build-dh
./build-key server
./build-key client0
./build-key client1
openvpn --genkey --secret keys/ta.key

tree /etc/openvpn/east-rsa/keys
├── ca.crt
├── ca.key
├── dh2048.pem
├── server.crt
├── server.csr
├── server.key
├── client0.crt
├── client0.csr
├── client0.key
├── client1.crt
├── client1.csr
├── client1.key
└── ta.key
```

```
export EASY_RSA="`pwd`"
export OPENSSL="openssl"
export PKCS11TOOL="pkcs11-tool"
export GREP="grep"
#export KEY_CONFIG=`$EASY_RSA/whichopensslcnf $EASY_RSA`
export KEY_CONFIG="$EASY_RSA/openssl-1.0.0.cnf"
export KEY_DIR="$EASY_RSA/keys"
export PKCS11_MODULE_PATH="dummy"
export PKCS11_PIN="dummy"
export KEY_SIZE=2048
export CA_EXPIRE=3650
export KEY_EXPIRE=3650
export KEY_COUNTRY="JP"
export KEY_PROVINCE="TYO"
export KEY_CITY="Otemachi"
export KEY_ORG="slank.dev"
export KEY_EMAIL="slank.dev@gmail.com"
export KEY_OU="MyOrganizationalUnit"
export KEY_NAME="EasyRSA"<Paste>
```

```
#server.conf

port 1194
proto udp
dev tun

ca   ca.crt
dh   dh2048.pem
cert server.crt
key  server.key

server 10.8.0.0 255.255.255.0               # VPN接続時のネットワークセグメント．
ifconfig-pool-persist ipp.txt               # 再接続用のテーブル．
push "route 192.168.179.0 255.255.255.0"    # サーバ側のLANのセグメント．
keepalive 10 120                            # セッション継続頻度．
status openvpn-status.log                   # ステータスログ．
log         openvpn.log                     # ログファイル．
comp-lzo                                    # LZO圧縮を有効に
verver
persist-key
persist-tun
```

```
#client.conf

client                        # クライアントモードであることを宣言
dev tun                       # VPNプロトコル：ルーティング方式．
proto udp                     # 通信プロトコル: UDP．
remote vpn.slank.dev 1194     # グローバルIPアドレスを指定する．
resolv-retry infinite         # 接続の継続．
nobind                        # ポート番号をバインドしない．

ca   ca.crt
cert client.crt
key  client.key

persist-key
persist-tun
comp-lzo # LZO圧縮を有効に
verb 3   # ログレベル
```

## User ID/Pass Auth

```
#server.ovpn

port 1194
proto udp
dev tun
ca   server/ca.crt
cert server/server.crt
key  server/server.key
dh   server/dh2048.pem
server 10.8.0.0 255.255.255.0
cipher AES-256-CBC
persist-key
persist-tun
status /var/log/openvpn/openvpn-status.log
verb 3
explicit-exit-notify 1

ifconfig-pool-persist /var/log/openvpn/ipp.txt
;push "redirect-gateway def1"

## ADD
script-security 2
client-cert-not-required
username-as-common-name
auth-user-pass-verify /etc/openvpn/auth.py via-file
management localhost 7505

client-to-client
keepalive 10 120
```

```
# client_without_password.ovpn

client
dev tun
proto udp
remote vpn.slank.dev 1194
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
cipher AES-256-CBC
verb 3
auth-user-pass passwd.txt
<ca>
-----BEGIN CERTIFICATE-----
MIIFEDCCA/igAwIBAgIUZW8tVf5fU7RCnT7IXbeUH5Bw+ZIwDQYJKoZIhvcNAQEL
BQAwga4xCzAJBgNVBAYTAkpQMQwwCgYDVQQIEwNUWU8xETAPBgNVBAcTCE90ZW1h
Y2hpMRIwEAYDVQQKEwlzbGFuay5kZXYxHTAbBgNVBAsTFE15T3JnYW5pemF0aW9u
YWxVbml0MRUwEwYDVQQDEwxzbGFuay5kZXYgQ0ExEDAOBgNVBCkTB0Vhc3lSU0Ex
...(snip)...
4MsI1caMb2yyw/harIz06LwaewlR/AIzlNaQf/sdBK+EHXmAU3Se7sZYlw4k+/zm
IsGnLvHNRHbGFAFCeIsIdJ99yP6d34swAPd09Sj15NK49eKncQQfsRDdz+gJ+R5u
yaYV0LNKjRPgQIdytoCEXAW9WaVkr+wC/Gth+9ymj03Dz1Bmwtm3EfA7R+6BfA/9
jzCyGiiS14nPkXrldzgrzA2BsBCjcOXDdJJiD2TY3UBYh/EnPS/emTjVnmoSU6PF
tRUFWw==
-----END CERTIFICATE-----
</ca>
```

```
# client_without_password.ovpn

client
dev tun
proto udp
remote vpn.slank.dev 1194
resolv-retry infinite
nobind
persist-key
persist-tun
remote-cert-tls server
cipher AES-256-CBC
verb 3
auth-user-pass
<ca>
-----BEGIN CERTIFICATE-----
MIIFEDCCA/igAwIBAgIUZW8tVf5fU7RCnT7IXbeUH5Bw+ZIwDQYJKoZIhvcNAQEL
BQAwga4xCzAJBgNVBAYTAkpQMQwwCgYDVQQIEwNUWU8xETAPBgNVBAcTCE90ZW1h
Y2hpMRIwEAYDVQQKEwlzbGFuay5kZXYxHTAbBgNVBAsTFE15T3JnYW5pemF0aW9u
YWxVbml0MRUwEwYDVQQDEwxzbGFuay5kZXYgQ0ExEDAOBgNVBCkTB0Vhc3lSU0Ex
...(snip)...
4MsI1caMb2yyw/harIz06LwaewlR/AIzlNaQf/sdBK+EHXmAU3Se7sZYlw4k+/zm
IsGnLvHNRHbGFAFCeIsIdJ99yP6d34swAPd09Sj15NK49eKncQQfsRDdz+gJ+R5u
yaYV0LNKjRPgQIdytoCEXAW9WaVkr+wC/Gth+9ymj03Dz1Bmwtm3EfA7R+6BfA/9
jzCyGiiS14nPkXrldzgrzA2BsBCjcOXDdJJiD2TY3UBYh/EnPS/emTjVnmoSU6PF
tRUFWw==
-----END CERTIFICATE-----
</ca>
```

## Reference

- http://qiita.com/moutend/items/22984fc725ce84c66444
- http://qiita.com/hironobu_s/items/713539a47b998d987445
- http://felis-silvestris-catus.hatenablog.com/entry/2015/05/27/222434
- https://www.openvpn.jp/document/how-to/


