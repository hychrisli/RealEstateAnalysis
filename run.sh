#!/bin/bash
source ~/.bash_profile

cd ~/GitHub/RealEstateAnalysis/
#scrapy crawl api_search_probe

#export PATH=$PATH:/usr/lib/python2.7/site-packages
#
python initial_load.py
#python ~/GitHub/RealEstateAnalysis/main.py >> ~/Data/RealEstateAnalysis/logs/daily_run_`date +%Y-%m-%d`.log
#
#
#export RET_DB_URL=$(heroku config:get RET_DB_URL --app real-estate-trends)
#python ~/GitHub/RealEstateDBConvert/main.py >> ~/Data/RealEstateAnalysis/logs/daily_run_`date +%Y-%m-%d`.log
