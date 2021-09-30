#!/usr/bin/env bash

apt-get update -y && apt-get upgrade -y
apt-get install -y python3-dev python3 python3-pip mysql-server default-libmysqlclient-dev build-essential
pip3 install django pandas numpy mysqlclient

mysql <<HERE
CREATE DATABASE IF NOT EXISTS theohealth; 
CREATE USER IF NOT EXISTS 'theo'@'localhost' IDENTIFIED BY 'theopass'; 
GRANT CREATE, ALTER, DROP, INSERT, INDEX, UPDATE, DELETE, SELECT, REFERENCES, RELOAD ON *.* TO 'theo'@'localhost' WITH GRANT OPTION; 
FLUSH PRIVILEGES
HERE

# create a symbolic link from /vagrant/theo.sh to ~/theo.sh so that this script can be inclused in .bashrc
if ! [ -L /home/vagrant/theo.sh ]; then
	ln -fs /vagrant/theo.sh /home/vagrant/theo.sh
fi

# add a call to theo.sh to ~/.bashrc
if ! [ $(grep "theo.sh" /home/vagrant/.bashrc | wc -m) -gt 0 ] ; 
then 
	cat << HERE >> /home/vagrant/.bashrc
if [ -f theo.sh ]; then
	. theo.sh
fi
HERE
fi
