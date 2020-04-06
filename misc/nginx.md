
# nginx / NGINX

```
#/etc/nginx/nginx.conf

user www-data;
worker_processes auto;
pid /run/nginx.pid;
include /etc/nginx/modules-enabled/*.conf;
events { worker_connections 768; }

http {
        sendfile on;
        tcp_nopush on;
        tcp_nodelay on;
        keepalive_timeout 65;
        types_hash_max_size 2048;
        include /etc/nginx/mime.types;
        default_type application/octet-stream;

        ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
        ssl_prefer_server_ciphers on;
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;
        gzip on;

        server {
                listen 80;
                server_name drive.slank.dev;
                root /var/www/html;
                index index.html;
                proxy_set_header    Host    $host;
                proxy_set_header    X-Real-IP    $remote_addr;
                proxy_set_header    X-Forwarded-Host       $host;
                proxy_set_header    X-Forwarded-Server    $host;
                proxy_set_header    X-Forwarded-For    $proxy_add_x_forwarded_for;
                location / {
                        proxy_pass http://10.8.0.10
                        #try_files $uri $uri/ =404;
                }
        }
        server {
                listen 80;
                server_name vpn.slank.dev;
                root /var/www/html/vpn.slank.dev;
                index index.html;
                location / {
                        try_files $uri $uri/ =404;
                }
        }

        include /etc/nginx/conf.d/*.conf;
        include /etc/nginx/sites-enabled/*;
}
```

```
ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
server {
		listen 443;
		server_name slank.dev;

		ssl on;
		ssl_certificate /etc/pki/tls/certs/example_com_combined.crt;
		ssl_certificate_key /etc/pki/tls/private/example_com.key;

		location / {
			...(snip)...
		}
}
```

## Enable Index of ...

```
server {
  ...(snip)...
	autoindex on;
	autoindex_exact_size off;
	autoindex_localtime on;
  ...(snip)...
}
```

## Redirect from http to https automatically

```
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

## letsencrypt

```
sudo su
cd /usr/local
git clone https://github.com/certbot/certbot
cd certbot

## EXAMPLE:slank.dev
./certbot-auto certonly --standalone -d slank.dev -m admin@slank.dev --agree-tos -n
```

```
server {
  listen 443 ssl;
  ssl_certificate     /etc/letsencrypt/live/slank.dev/fullchain.pem;
  ssl_certificate_key /etc/letsencrypt/live/slank.dev/privkey.pem;
}
```

check certificates
```
cd /usr/local/certbot
./certbot-auto certificates
-------------------------------------------------------------------------------
Found the following certs:
  Certificate Name: blog.example.com
    Domains: blog.example.com
    Expiry Date: 2018-06-03 10:31:54+00:00 (VALID: 88 days)
    Certificate Path: /etc/letsencrypt/live/blog.example.com/fullchain.pem
    Private Key Path: /etc/letsencrypt/live/blog.example.com/privkey.pem
-------------------------------------------------------------------------------
```



