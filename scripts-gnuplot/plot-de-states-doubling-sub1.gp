#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

title = "Trend der Neu-Infektionen in ".long_name
set title title
# fitting

data = '../data/de-states/de-state-'.short_name.'.tsv'

# fetch data from last row of data
# x_min = ( system("head -n 2 " . data . " | tail -1 | cut -f1") + 0 )
# x_max = ( system("tail -1 " . data . " | cut -f1") + 0 )
date_last = system("tail -1 " . data . " | cut -f1")
# y_last = ( system("tail -1 " . data . " | cut -f3") + 0)
set label 1 label1_text_right." based on RKI data of ".date_last

# set xtic add (date_last 0) 

set output '../plots-gnuplot/de-states/cases-de-doubling-'.short_name.'.png'
plot data using (column("Date")):(column("Cases_Last_Week_Per_100000")) title "Infektionen" with lines lw 2 dt 1 lc "blue" \
, data using (column("Date")):(column("Cases_Last_Week_Doubling_Time")>0?column("Cases_Last_Week_Doubling_Time"):1/0) title "Verdopplungszeit" axis x1y2 with lines ls 5 dt "-" linecolor rgb "red" \
, data using (column("Date")):(column("Cases_Last_Week_Doubling_Time")<0?-column("Cases_Last_Week_Doubling_Time"):1/0) title "Halbwertszeit" axis x1y2 with lines ls 5 dt "." linecolor rgb "sea-green"
unset output
