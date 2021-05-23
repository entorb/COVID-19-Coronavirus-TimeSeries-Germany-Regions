#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

set title ""
# set xlabel "Days since first data"
set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
set format x '%d.%m'
set xdata time
# set xlabel ""
# set xtics 7

set style line 1 linetype 7 lw 2 dt 1 linecolor rgb 'blue' 
set style line 2 linetype 7 lw 2 dt 1 linecolor rgb 'black' 
set style line 3 linetype 7 lw 2 dt 1 linecolor rgb 'red' 

set ylabel "Neu-Infizierte pro 100.000/7 (rot) und Tote pro 1.000.000/7 (schwarz)"
set ytics nomirror
set yrange [0:]
set ytics 25

set y2label "Intensivstationsbelegung durch COVID-19 (%)" tc ls 3 offset -1,0
set y2tics tc ls 3 format "%g%%"
set y2tics 5
# set y2range [0:20]

set key width -2 height +.5 spacing 1.5 center top

# text will be inserted later on
set label 2 "" right front at graph 0.98, graph 0.22
short_name = 'BW' ; long_name = "Baden-Württemberg" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'BY' ; long_name = "Bayern" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'BE' ; long_name = "Berlin" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'BB' ; long_name = "Brandenburg" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'HB' ; long_name = "Bremen" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'HH' ; long_name = "Hamburg" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'HE' ; long_name = "Hessen" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'MV' ; long_name = "Mecklenburg-Vorpommern" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'NI' ; long_name = "Niedersachsen" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'NW' ; long_name = "Nordrhein-Westfalen" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'RP' ; long_name = "Rheinland-Pfalz" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'SL' ; long_name = "Saarland" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'SN' ; long_name = "Sachsen" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'ST' ; long_name = "Sachsen-Anhalt" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'SH' ; long_name = "Schleswig-Holstein" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'TH' ; long_name = "Thüringen" ; load "plot-de-states-cases-deaths-divi-sub1.gp"
short_name = 'DE-total' ; long_name = "Deutschland" ; load "plot-de-states-cases-deaths-divi-sub1.gp"

