#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

set title "Sterbefälle in Deutschland"
# set xlabel "Days since first data"
set timefmt '%d.%m.' # %d.%m.%Y %H:%M
set format x '%d.%m'
set xdata time
# set xlabel ""
# set xtics 7

# set ylabel "Neu-Infizierte pro 100.000/7 (rot) und Tote pro 1.000.000/7 (schwarz)"
# set ytics nomirror
# set yrange [0:]
# set ytics 25


set style line 1 linetype 7 lw 2 dt 1 linecolor rgb 'red' 
set style line 2 linetype 7 lw 2 dt 1 linecolor rgb 'black' 
set style line 3 linetype 7 lw 2 dt 1 linecolor rgb 'blue' 
set style line 4 linetype 7 lw 2 dt 1 linecolor rgb 'magenta' 

# lw 2 dt 1 lc "red"
# lw 2 dt 1 linecolor rgb "black"
# linecolor rgb "blue" 


set key left center

# text will be inserted later on
set label 2 "" right front at graph 0.98, graph 0.22


data = '../data/de-mortality.tsv'

# fetch data from last row of data
# x_min = ( system("head -n 2 " . data . " | tail -1 | cut -f1") + 0 )
# x_max = ( system("tail -1 " . data . " | cut -f1") + 0 )
# date_last = system("tail -1 " . data . " | cut -f2")
# y_last = ( system("tail -1 " . data . " | cut -f3") + 0)
set label 1 label1_text_right." based on Destatis and RKI data" # of ".date_last

# set xtic add (date_last 0) 

set output '../plots-gnuplot/de-mortality.png'
plot data using (column("Day")):(column("2016_2019_mean_roll"))   title "2016-19" axis x1y1  with lines ls 1   \
    , data using (column("Day")):(column("2020_roll")) title "2020" axis x1y1 with lines ls 2 \
    , data using (column("Day")):(column("2020_roll")-column("2016_2019_mean_roll")) title "Differenz" axis x1y1 with lines ls 4 \
    , data using (column("Day")):(column("Deaths_Covid_2020_roll")) title "Covid-19" axis x1y1 with lines ls 3 
unset output

