source ~/.bash_profile
python ~/GitHub/RealEstateAnalysis/main.py >> ~/Data/RealEstateAnalysis/logs/daily_run_`date +%Y-%m-%d`.log


export RET_DB_URL=$(heroku config:get RET_DB_URL --app real-estate-trends)
python ~/GitHub/RealEstateDBConvert/main.py >> ~/Data/RealEstateAnalysis/logs/daily_run_`date +%Y-%m-%d`.log