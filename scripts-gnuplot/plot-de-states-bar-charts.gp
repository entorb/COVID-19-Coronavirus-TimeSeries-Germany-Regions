#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

fit_data_file = "../data/de-states/de-states-cases-gnuplot-fit.tsv"

set title ""
# set ylabel "Cases"
# set xlabel "Days since first data"
# let's plot the fit data as boxes
set title "Fitergebnis Verdopplungszeit (Tage)"
set ylabel "Verdopplungszeit (Tage)"
set xtics rotate by 60 offset 1,0 right
# set ytics format "%.1f" 
set bmargin 10.5
set style fill solid 0.5 border 0
set boxwidth 0.75 relative
set key off
set yrange [0:]
y_value_de = ( system("tail -1 " . fit_data_file . " | cut -f6") + 0)
# set output '../plots-gnuplot/de-states/cases-de-fit-doubling-time.png'
# plot fit_data_file using (column("Cases_Doubling_Time")):xticlabels(1) with boxes ls 11, y_value_de with lines ls 12
# unset output



set ytics format "%g%%" 
set title "Fitergebnis Zunahme Infektionen pro Tag"
set ylabel "Zunahme Infektionen pro Tag"
y_value_de = ( system("tail -1 " . fit_data_file . " | cut -f7") + 0)
y_value_de = (y_value_de-1)*100
# set output '../plots-gnuplot/de-states/cases-de-fit-increase-1-day.png'
# plot fit_data_file using ((column("factor t+1")-1)*100):xticlabels(1) with boxes ls 11, y_value_de with lines ls 12
# unset output
set ytics format "%g" 

# Plotting the latest number of infections per 1 Mill pop
set title "Infektionen pro 1 Millionen Einwohner"
set ylabel "Infektionen pro 1 Mill Einwohner"
data = '../data/de-states/de-states-latest.tsv'
y_value_de = ( system("tail -1 " . data . " | cut -f10") + 0)

set output '../plots-gnuplot/de-states/cases-de-states-latest-per-million.png'
plot data using (column("Cases_Per_Million")):xticlabels(1) with boxes ls 11, y_value_de with lines ls 12
unset output

unset yrange
unset style
unset boxwidth
unset bmargin
unset xtics
unset ytics
