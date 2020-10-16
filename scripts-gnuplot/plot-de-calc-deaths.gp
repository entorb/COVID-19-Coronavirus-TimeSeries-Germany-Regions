#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'red' 
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'blue' 



set title "Abschätzung der Dunkelziffer der Infektionen\nAnnahmen: Infizierte sterben nach 2 Wochen mit Wahrscheinlichkeit von 1%"
# set ylabel "Cases"
# set xlabel "Days since first data"
set ylabel "Infektionen"
set xlabel "Tage"
set xtics 7

data = '../data/de-states/de-state-DE-total.tsv'


f(x)=N0 * exp(x * log(2)/T)
N0 = 10000.0
T = 5.0

# use only last 7 days for fit at require the number to be at least 2
set xrange [-20.1:-13.9]


fit f(x) data using (column("Days_Past")-14):(column("Deaths")*100) via N0, T
#b = log(2)/T

# delete fit logfile
`rm fit.log`

# set timefmt '%Y-%m-%d'
# set xdata time
# set format x "%d.%m"

date_last = system("tail -1 " . data . " | cut -f2")
cases_last = ( system("tail -1 " . data . " | cut -f3") + 0)

set label 1 label1_text_right." based on RKI data of ".date_last


set label 2 \
 sprintf("\
 Fit Ergebnisse\n\
 Verdopplungszeit: %.1f Tage\n\
 Abschätzung Infizierte heute: %d\n\
 = %.3f%% der DE Bevölkerung\n\
 Vergleich Abschätzung zu offizieller Fallzahl: %.1fx höher\
 "\
 , T, f(0) , f(0) / 83019200 * 100, f(0)/cases_last \
 ) \
 right front at graph 0.98, graph 0.98

set key left center width -2

set xtic add (date_last 0) 
set logscale y
set xrange [-35:0]
# set samples 300
set output '../plots-gnuplot/de-states/calc-cases-from-deaths-DE-total.png'
plot data using (column("Days_Past")-14):(column("Deaths")*100) title "geschätze Infizierte" with linespoints ls 1 ,\
     data using (column("Days_Past")):(column("Cases")) title "positiv getestet" with linespoints ls 2 ,\
     (x<=-20.25)?1/0:f(x) title "Fit/Modell" with lines ls 1 dt "-" linecolor rgb 'black' 

unset output
