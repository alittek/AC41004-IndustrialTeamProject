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
