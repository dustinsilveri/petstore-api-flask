#!/bin/bash

#/etc/init.d/mariadb start &

/usr/bin/mysqld_safe --basedir=/usr &
sleep 5
mysqladmin --silent --wait=30 ping || exit 1
mysql -e 'GRANT ALL PRIVILEGES ON *.* TO "root"@"%";'
mysql -e 'CREATE DATABASE flask_api;'
mysql -e 'flush privileges;'

touch log_1.log

python3 api.py