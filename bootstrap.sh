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

if ! [ -L /home/vagrant/.bashrc ]; then
	rm -f /home/vagrant/.bashrc
	ln -fs /vagrant/.bashrc /home/vagrant/.bashrc
fi

WORK_DIR="/vagrant/theohealth"
alias "theo-run"="python3 $WORK_DIR/manage.py migrate; python3 $WORKDIR/manage.py runserver 0:9000"
DJANGO_DIR=/vagrant/theohealth

theo() {
	case $1 in
		run)
			python3 manage.py migrate
			python3 manage.py runserver 0:9000
			;;
		shell)
			python3 manage.py shell
			;;
		mysql)
			mysql -u theo --password=theopass theohealth
			;;
		*)
			echo ""
			echo "use python3, NOT python (it's a different version of python"
			echo ""
			echo -e "\e[31mDo NOT use Git wihin Vagrant\e[0m"
			echo "use git locally on windows"
			echo ""
			echo "theo run -- start the server at port 9000"
			echo "theo shell -- open interactive python shell initialized with django environment variables"
			echo "theo mysql -- opens a mysql shell. Logs in using the following information:"
			echo "	user: theo"
			echo "	password: theopass"
			echo "	database: theohealth"
			echo "theo help -- show this help message"
			;;
	esac

}
theo help
