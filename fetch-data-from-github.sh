#!/bin/sh
mkdir tmp

wget --quiet -P tmp https://github.com/entorb/COVID-19-Coronavirus-German-Regions/releases/download/tip/data.tgz
wget --quiet -P tmp https://github.com/entorb/COVID-19-Coronavirus-German-Regions/releases/download/tip/plots-gnuplot.tgz
wget --quiet -P tmp https://github.com/entorb/COVID-19-Coronavirus-German-Regions/releases/download/tip/maps.tgz

tar xfz tmp/data.tgz -C data/
tar xfz tmp/plots-gnuplot.tgz -C plots-gnuplot/
tar xfz tmp/maps.tgz -C maps/

rm -r tmp
