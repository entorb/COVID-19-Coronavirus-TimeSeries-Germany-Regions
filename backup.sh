#!/bin/sh
# initialdir=$PWD
DATE=`date +"%Y-%m-%d_%H-%M"`

rm index-online.html
wget -q -O index-online.html https://entorb.net/COVID-19-coronavirus/index.html 
zip -9 backup/covid-$DATE.zip ./* scripts-gnuplot/* data/* data/*/*

rsync -rvhu --delete --delete-excluded  entorb@entorb.net:html/COVID-19-coronavirus/ backup/web/
