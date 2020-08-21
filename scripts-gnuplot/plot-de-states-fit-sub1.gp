#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

title = "Infektionen in ".long_name
set title title
# fitting

data = '../data/de-states/de-state-'.short_name.'.tsv'

# fetch data from last row of data
x_min = ( system("head -n 2 " . data . " | tail -1 | cut -f1") + 0 )
x_max = ( system("tail -1 " . data . " | cut -f1") + 0 )
date_last = system("tail -1 " . data . " | cut -f2")
y_last = ( system("tail -1 " . data . " | cut -f3") + 0)
set label 1 label1_text_right." based on RKI data of ".date_last


# fit setting

# FOR SOME STRANGE REASON THIS IS NOT WORKING, So fitting againt number column insteays since first datanot working: Singular matrix
# set timefmt '%d.%m.%Y %H:%M'
# set xdata time
# x0 = 1582884000 # unix time of 28.02.20 10:00
# f(x)=a * exp(b * (x-x0))
# fit f(x) data using 2:col via a, b

# doubling time
# 2 * a = a * exp (b * t) 
# ln 2  = b * t
# -> t = ln (2) / b

f(x)=a * exp(b * x)
a = y_last # initial value
b = 0.24

# use only last 7 days for fit at require the number to be at least 2
set xrange [-6.1:0.1]
set yrange [1.9:]

set xtic add (date_last 0) 

fit f(x) data using (column("Days_Past")):(column("Cases")) via a, b

# stats data using (column("Days_Past")):(column("Cases")) nooutput
# x_max = STATS_max_x
t_doubling = log(2) / b

print sprintf (short_name."\t%.1f days", t_doubling)
# write fit results to file
set print fit_data_file append
print sprintf (  long_name."\t".short_name."\t%d\t%.3f\t%.3f\t%.3f\t%.3f\t%d\t%.3f\t%d", y_last, a, b, t_doubling, exp(b * 1), y_last * exp(b * 1), exp(b * 7), y_last * exp(b * 7)   )
unset print 

set xrange [x_min:x_max+1]


# plot 1: lin scale
set label 2 sprintf("Fit Ergebnisse\nVerdopplungszeit: %.1f Tage\nZunahme 1 Tag: %.0f%%\n  -> %d ".col_name."\nZunahme 7 Tage: %.0f%%\n  -> %d ".col_name."", t_doubling, (exp(b * 1)-1)*100, y_last * exp(b * 1), (exp(b * 7)-1)*100, y_last * exp(b * 7) )
set label 3 "" .y_last right at first x_max - 0.25, first y_last * 1.20
set yrange [0:]
set output '../plots-gnuplot/de-states/cases-de-fit-'.short_name.'.png'
plot data using (column("Days_Past")):(column("Cases")) title "Daten" with points ls 1 \
, f(x) title sprintf ("7-Tages Fit/Trend") with lines ls 2 \
, data using (column("Days_Past")):(column("Cases_Doubling_Time")) title "Verdopplungszeit" axis x1y2 with lines ls 5
unset output
# plot 2: log scale
set logscale y
set title title ." - Logarithmische Skalierung"
set yrange [1:]
set output '../plots-gnuplot/de-states/cases-de-fit-'.short_name.'-log.png'
replot
unset output
unset logscale y

