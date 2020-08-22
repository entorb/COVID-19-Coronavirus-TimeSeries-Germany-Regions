#!/bin/bash
echo === git pull
git pull

echo === fetching index.html -> index-online.html
wget -q -O index-online.html https://entorb.net/COVID-19-coronavirus/index.html 

echo === fetching and generating new data
echo ==== de-divi
python3 fetch-de-divi-V2.py
echo ==== de-states
python3 fetch-de-states-data.py
echo ==== de-districts
python3 fetch-de-districts.py
echo ==== countries
python3 fetch-int-country-data.py
echo ==== gen-map-de-districts
python3 gen-map-de-districts.py

# IDEA: run in background processes via appending '&'. Problem 1: how to know when ready for plotting? Problem 2: Errors are no longer displayed at the terminal


echo === plotting
rm plots-gnuplot/*/*.png
cd scripts-gnuplot
gnuplot all.gp
bash upload-to-entorb.sh
cd ..

echo  === uploading data
# (after plotting because gnuplot generates 2 data files as well)
cd data
bash upload-to-entorb.sh
cd ..

echo  === uploading maps
cd maps
bash upload-to-entorb.sh
cd ..


echo  === date of data
bash show_data_dates.sh

# echo === Check local html. Enter to copy and commit, CTRG+C to cancel
# read ok

#rsync -rvhu --delete --delete-excluded ../plots-gnuplot/* entorb@entorb.net:html/COVID-19-coronavirus/plots-gnuplot/

# scp index.html entorb@entorb.net:html/COVID-19-coronavirus/
rsync -vhu --no-perms index.html entorb@entorb.net:html/COVID-19-coronavirus/


echo  === git: add and commit
git add data/*
git commit -m "update"
git push

