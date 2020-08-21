#!/bin/bash

cd /home/entorb/html/COVID-19-coronavirus

mkdir tmp-dl

wget --quiet -P tmp-dl https://github.com/entorb/COVID-19-Coronavirus-German-Regions/releases/download/tip/data.tgz
wget --quiet -P tmp-dl https://github.com/entorb/COVID-19-Coronavirus-German-Regions/releases/download/tip/plots-gnuplot.tgz
wget --quiet -P tmp-dl https://github.com/entorb/COVID-19-Coronavirus-German-Regions/releases/download/tip/maps.tgz

tar xfz tmp-dl/data.tgz -C data/
tar xfz tmp-dl/plots-gnuplot.tgz -C plots-gnuplot/
tar xfz tmp-dl/maps.tgz -C maps/

chmod o+r -R /home/entorb/html/COVID-19-coronavirus

rm -r tmp-dl

