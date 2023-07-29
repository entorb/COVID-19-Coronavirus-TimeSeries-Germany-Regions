#!/bin/sh

git pull
python3 fetch-de-mortality.py
git add .
git commit -m "update mortality"

cd scripts-gnuplot
gnuplot plot-de-mortality.gp
cd ..

rsync -rvhu --delete --delete-excluded --no-perms plots-gnuplot/de-mortality*.png entorb@entorb.net:html/COVID-19-coronavirus/plots-gnuplot/
