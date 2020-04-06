

# Wordpressの環境構築

## 必要なパッケージのインストール

```
# yum -y install php-mysql php-common php php-cgi php-fpm php-gd php-mbstring
# yum -y install http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm
# vim /etc/yum.repos.d/nginx.repo
# yum -y install nginx
# vim /etc/php-fpm.d/www.conf
; RPM: apache Choosed to be able to access some dir as httpd
user = nginx
; RPM: Keep a group allowed to write in log dir.
group = nginx
# yum -y install http://dev.mysql.com/get/mysql-community-release-el6-5.noarch.rpm
# vim /etc/httpd/conf/httpd/conf
DocumentRoot "/var/www/html/wordpress" 
```

## webサーバのセットアップ

## wordpressをインストール、設定
まずwordpressをダウンロードして、所定のディレクトリに展開して、nginxで扱える権限を追加

```
# wget http://ja.wordpress.org/wordpress-3.6.1-ja.tar.gz
# tar xzf wordpress-3.6.1-ja.tar.gz
# mv wordpress /var/www
# chown -R nginx.nginx wordpress
```


