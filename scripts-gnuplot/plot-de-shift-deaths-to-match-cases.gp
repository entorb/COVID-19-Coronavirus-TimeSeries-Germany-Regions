#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

# TODO: shall this go to de-states or to int/countries?

load "header.gp"

set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'blue' 
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'red' 
set style line 3 linetype 7 dt "-" lw 2 linecolor rgb 'black' 




data = '../data/de-states/de-state-DE-total.tsv'
# data = '../data/int/country-DE.tsv'

date_last = system("tail -1 " . data . " | cut -f2")

set label 1 label1_text_right." based on RKI data of ".date_last
# set label 1 label1_text_right." based on JHU data of ".date_last


set xlabel "Wochen"
set xtics 1
set xtic add (date_last 0)




set ytics nomirror
set y2tics nomirror

set ylabel "Infektionen letzte Woche" offset 0,0 textcolor rgb 'blue' 
set y2label "Tote letzte Woche" offset -0,0 textcolor rgb 'red' 

set ytics textcolor rgb 'blue' 
set y2tics textcolor rgb 'red' 

x_min = -10

set xrange [x_min:0]
# y_max=41000
mortality = 4.3/100
mortality = 2.0/100

# mask_zero_values(x) = (x<=0)?1/0:x

set label 2 sprintf("Skalierung: %.1f%%", mortality*100.0) right front at graph 0.99, graph 0.95 textcolor rgb "red"

set key width 0 top left

# How much are the deaths in Germany delayed?
set title "Zeitverzug zwischen Infizierten und Toten"
set yrange [0:*]

output ='../plots-gnuplot/de-states/shift-deaths-to-match-cases_DE_last-week.png'
set output output
plot data u (column("Days_Past"))/7:(column("Cases_Last_Week")) t "Infizierte" ,\
     data u (column("Days_Past"))/7:(column("Deaths_Last_Week")) t "Tote" axes x1y2, \
     data u (column("Days_Past")-14)/7:(column("Deaths_Last_Week")) t "Verschoben um 14 Tage" axes x1y2 with lines lc rgb "red"
unset output
# replot using correct y2 scale
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
y_max = GPVAL_DATA_Y_MAX * 1.1
set yrange [0:y_max]
set y2range [0:y_max*mortality] 
set output output
replot
unset output


# cases last week per million
set ylabel "Infektionen letzte Woche pro Millionen" 
set y2label "Tote letzte Woche pro Millionen"

set yrange [0:*]

output = '../plots-gnuplot/de-states/shift-deaths-to-match-cases_DE_last-week_per_million.png'
set output output
plot data u (column("Days_Past"))/7:(column("Cases_Last_Week_Per_Million")) t "Infizierte" ,\
     data u (column("Days_Past"))/7:(column("Deaths_Last_Week_Per_Million")) t "Tote" axes x1y2, \
     data u (column("Days_Past")-14)/7:(column("Deaths_Last_Week_Per_Million")) t "Verschoben um 14 Tage" axes x1y2 with lines lc rgb "red"
unset output
# replot using correct y2 scale
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
y_max = GPVAL_DATA_Y_MAX * 1.1
set yrange [0:y_max]
set y2range [0:y_max*mortality] 
set output output
replot
unset output


# Forecast
set key width 0 top right
set xrange [x_min:2]
set arrow 3 nohead back from first 0, graph 0 to first 0, graph 0.85 dashtype "-"
set label 2 at graph 0.99, graph 0.05

title = "Prognose der Opferzahlen, basiert auf den Infektionen"

# DE
region = "Deutschland"
data = '../data/de-states/de-state-DE-total.tsv'
output = '../plots-gnuplot/de-states/forecasting-deaths-DE.png'
load 'plot-de-shift-deaths-to-match-cases-sub1.gp'

# Bayern
region = "Bayern"
data = '../data/de-states/de-state-BY.tsv'
output = '../plots-gnuplot/de-states/forecasting-deaths-BY.png'
load 'plot-de-shift-deaths-to-match-cases-sub1.gp'

# Erlangen
region = "Erlangen"
data = '../data/de-districts/de-district_timeseries-09562.tsv'
output = '../plots-gnuplot/de-states/forecasting-deaths-Erlangen.png'
load 'plot-de-shift-deaths-to-match-cases-sub1.gp'

