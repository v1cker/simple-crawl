while :
do 
	if [ $(ps -ef | grep -c "scrapy crawl main") -lt 8 ]
	then
		nohup scrapy crawl main -L CRITICAL &
		echo [+]$(date "+%m-%d %H:%M") "Begain" >> run.log
	else
		sleep 20
		echo "[-]" $(date "+%m-%d %H:%M") “waiting...” >> run.log
	fi
done
