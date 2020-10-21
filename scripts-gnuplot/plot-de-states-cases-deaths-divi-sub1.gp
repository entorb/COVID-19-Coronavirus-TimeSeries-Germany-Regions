#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

title = "" . long_name
set title title
# fitting

data = '../data/de-states/de-state-'.short_name.'.tsv'

# fetch data from last row of data
# x_min = ( system("head -n 2 " . data . " | tail -1 | cut -f1") + 0 )
# x_max = ( system("tail -1 " . data . " | cut -f1") + 0 )
date_last = system("tail -1 " . data . " | cut -f2")
# y_last = ( system("tail -1 " . data . " | cut -f3") + 0)
set label 1 label1_text_right." based on RKI and DIVI data of ".date_last

# set xtic add (date_last 0) 

set output '../plots-gnuplot/de-states/cases-deaths-divi-'.short_name.'.png'
plot data using (column("Date")):(column("Cases_Last_Week_Per_100000"))   title "Infizierte" axis x1y1  with lines ls 1  \
   , data using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Tote" axis x1y1 with lines ls 2  \
   , data using (column("Date")):(column("DIVI_Intensivstationen_Covid_Prozent")) title "Intensivstationen:\n Anteil COVID-19" axis x1y2 with lines ls 3 
unset output

# dt "-" 