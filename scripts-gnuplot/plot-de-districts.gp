#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"
data = "../data/de-districts/de-districts-zero_cases_last_week.tsv"

set style data lines
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles

set ylabel "Anzahl der Landkreise"

set xdata time
set timefmt "%Y-%m-%d"
set xtics format "%d.%m."
set key off

set yrange [0:412]
set y2range [0:100]
set ytics nomirror
set y2tics (0, 20, 40, 60, 80, 100) nomirror format "%g%%"
unset grid
set grid xtics y2tics

set title "Landkreise mit COVID-19 Neu-Infektionen in der letzten Woche"

set output "../plots-gnuplot/de-districts/zero_cases_last_week.png"
plot data u 1:2 axis x1y1 with lines dt 1 lc "blue"
unset output

set title "Landkreise mit Inzidenz > 50"
data = "../data/de-districts/de-districts-50_cases_last_week.tsv"
set output "../plots-gnuplot/de-districts/50_cases_last_week.png"
plot data u 1:2 axis x1y1 with lines dt 1 lc "blue"
unset output
