#!/bin/bash
source ~/.bash_profile

cd ~/GitHub/RealEstateAnalysis/
#python initial_load.py
python main.py

export RET_DB_URL=$(heroku config:get RET_DB_URL --app real-estate-trends)
python ~/GitHub/RealEstateDBConvert/main.py
