#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

# set xlabel "Days since first data"
set timefmt '%d.%m.' # %d.%m.%Y %H:%M
set format x '%d.%m'
set xdata time
# set xlabel ""
# set xtics 7

set ylabel "Sterbefälle"
# set ytics nomirror
# set yrange [0:]
set ytics 500


set style line 1 linetype 7 lw 2 dt 1 linecolor rgb 'black' 
set style line 2 linetype 7 lw 2 dt 1 linecolor rgb 'red' 
set style line 3 linetype 7 lw 2 dt 1 linecolor rgb 'blue' 
set style line 4 linetype 7 lw 2 dt 1 linecolor rgb 'magenta'
set style line 5 linetype 7 lw 2 dt 1 linecolor rgb 'brown'

# lw 2 dt 1 lc "red"
# lw 2 dt 1 linecolor rgb "black"
# linecolor rgb "blue" 



# text will be inserted later on
set label 2 "" right front at graph 0.98, graph 0.22


data = '../data/de-mortality.tsv'

set title "Tägliche Sterbefälle in Deutschland"
set label 1 label1_text_right." based on Destatis data" # of ".date_last

set key right top

set output '../plots-gnuplot/de-mortality.png'
plot \
      data using (column("Day")):(column("2016_roll_av")) title "2016" axis x1y1 with lines ls 5 \
    , data using (column("Day")):(column("2017_roll_av")) title "2017" axis x1y1 with lines ls 4 \
    , data using (column("Day")):(column("2018_roll_av")) title "2018" axis x1y1 with lines ls 3 \
    , data using (column("Day")):(column("2019_roll_av")) title "2019" axis x1y1 with lines ls 1 \
    , data using (column("Day")):(column("2020_roll_av"))   title "2020" axis x1y1  with lines ls 2 lw 4 \
    , data using (column("Day")):(column("2021_roll_av"))   title "2021" axis x1y1  with lines ls 6 lw 4 \
    , data using (column("Day")):(column("2022_roll_av"))   title "2022" axis x1y1  with lines ls 8 lw 4
unset output

set terminal pngcairo size 640,800 font 'Verdana,9'
# set key right center

set key width -4.5
set title "Tägliche Sterbefälle in Deutschland gesamt und an COVID-19 Jahr 2020"
set label 1 label1_text_right." based on Destatis and RKI data" # of ".date_last

set style fill solid 0.4 border rgb "gray60"

set arrow nohead from graph 0, first 0 to graph 1, first 0
set output '../plots-gnuplot/de-mortality-covid.png'
plot \
      data using (column("Day")):(column("2016_2019_roll_av_min")):(column("2016_2019_roll_av_max")) title "Bandbreite 2016-19" with filledcurve lc rgb "gray60" \
    , data using (column("Day")):(column("2016_2019_mean_roll_av"))   title "Mittelwert 2016-19" axis x1y1  with lines ls 1   \
    , data using (column("Day")):(column("2020_roll_av")) title "2020" axis x1y1 with lines ls 2 \
    , data using (column("Day")):(column("2020_roll_av")-column("2016_2019_mean_roll_av")) title "Differenz 2020 zu Mittelwert" axis x1y1 with lines ls 4 \
    , data using (column("Day")):(column("Deaths_Covid_2020_roll_av")) title "COVID-19" axis x1y1 with lines ls 3 
unset output

set title "Tägliche Sterbefälle in Deutschland gesamt und an COVID-19 Jahr 2021"
set arrow nohead from graph 0, first 0 to graph 1, first 0
set output '../plots-gnuplot/de-mortality-covid-2021.png'
plot \
      data using (column("Day")):(column("2016_2019_roll_av_min")):(column("2016_2019_roll_av_max")) title "Bandbreite 2016-19" with filledcurve lc rgb "gray60" \
    , data using (column("Day")):(column("2016_2019_mean_roll_av"))   title "Mittelwert 2016-19" axis x1y1  with lines ls 1   \
    , data using (column("Day")):(column("2021_roll_av")) title "2021" axis x1y1 with lines ls 2\
    , data using (column("Day")):(column("2021_roll_av")-column("2016_2019_mean_roll_av")) title "Differenz 2021 zu Mittelwert" axis x1y1 with lines ls 4 \
    , data using (column("Day")):(column("Deaths_Covid_2021_roll_av")) title "COVID-19" axis x1y1 with lines ls 3 
unset output

set title "Tägliche Sterbefälle in Deutschland gesamt und an COVID-19 Jahr 2022"
set arrow nohead from graph 0, first 0 to graph 1, first 0
set output '../plots-gnuplot/de-mortality-covid-2022.png'
plot \
      data using (column("Day")):(column("2016_2019_roll_av_min")):(column("2016_2019_roll_av_max")) title "Bandbreite 2016-19" with filledcurve lc rgb "gray60" \
    , data using (column("Day")):(column("2016_2019_mean_roll_av"))   title "Mittelwert 2016-19" axis x1y1  with lines ls 1   \
    , data using (column("Day")):(column("2022_roll_av")) title "2022" axis x1y1 with lines ls 2\
    , data using (column("Day")):(column("2022_roll_av")-column("2016_2019_mean_roll_av")) title "Differenz 2022 zu Mittelwert" axis x1y1 with lines ls 4 \
    , data using (column("Day")):(column("Deaths_Covid_2022_roll_av")) title "COVID-19" axis x1y1 with lines ls 3 
unset output