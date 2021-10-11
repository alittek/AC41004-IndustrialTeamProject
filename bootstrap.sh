#!/usr/bin/env bash

apt-get update -y && apt-get upgrade -y
apt-get install -y python3-dev python3 python3-pip mysql-server default-libmysqlclient-dev build-essential
pip3 install django pandas numpy mysqlclient matplotlib
pip3 install django-crispy-forms

mysql <<HERE
CREATE DATABASE IF NOT EXISTS theohealth; 
CREATE USER IF NOT EXISTS 'theo'@'localhost' IDENTIFIED BY 'theopass'; 
GRANT CREATE, ALTER, DROP, INSERT, INDEX, UPDATE, DELETE, SELECT, REFERENCES, RELOAD ON *.* TO 'theo'@'localhost' WITH GRANT OPTION; 
FLUSH PRIVILEGES
HERE
