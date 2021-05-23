#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

data = "../data/int/country-".country_code.".tsv"

# fetch data from last row of data
x_min = ( system("head -n 2 " . data . " | tail -1 | cut -f1") + 0 )
x_max = ( system("tail -1 " . data . " | cut -f1") + 0 )
# fetch data from last row of data
y_last = ( system("tail -1 " . data . " | cut -f4") + 0)
date_last = system("tail -1 " . data . " | cut -f2")

# print country_name

title = "Fitting Deaths in ".country_name
set title title
set label 1 label1_text_right." based on JHU data of ".date_last

# fitting
# fit only the last 14 days and death > 2
set xrange [-6.1:0.1]
set yrange [1.9:]
f(x)=a * exp(b * x)
a = y_last # initial value
b = 0.24
fit f(x) data using (column("Days_Past")):(column("Deaths")) via a, b
t_doubling = log(2) / b

print sprintf (country_code."\t%.1f days", t_doubling)
# write fit results to file
set print fit_data_file append
print sprintf (  country_name."\t".country_code."\t%d\t%.3f\t%.3f\t%.3f\t%.3f\t%d\t%.3f\t%d", y_last, a, b, t_doubling, exp(b * 1), y_last * exp(b * 1), exp(b * 7), y_last * exp(b * 7)   )
unset print 
# guide lines
# f2(x)=a2 * exp(log(2)/2 * x)
# f3(x)=a3 * exp(log(2)/3 * x)
# fit f2(x) data using 1:col via a2
# fit f3(x) data using 1:col via a3

# set xtic add (date_last 0) 

unset xlabel
set xtic add ("30.04.20" 0) center
set xtic add ("" -7) center
set xtic add ("16.04.20" -14) center
set xtic add ("" -21) center
set xtic add ("02.04.20" -28) center
set xtic add ("" -35) center
set xtic add ("19.03.20" -42) center
set xtic add ("" -49) center
set xtic add ("05.03.20" -56) center

# print country_name

# plot range filters != fit range filters 
# set xrange [x_min:x_max+1]
set xrange [-60:x_max+1]
set yrange [0:] 
# set ytics nomirror
# set y2range [1:2]
# set y2label "Change Factor" 
# set y2tics autofreq 
set key top left box
# plot 1: lin scale
set label 2 sprintf("Fit Results\nDoubling Time: %.1f Days\nIncrease 1 Day: %.0f%%\n  -> %d Deaths\nIncrease 7 Days: %.0f%%\n  -> %d Deaths", t_doubling, (exp(b * 1)-1)*100, y_last * exp(b * 1), (exp(b * 7)-1)*100, y_last * exp(b * 7) )
set label 3 "" .y_last right at first x_max - 2, first y_last 
set output '../plots-gnuplot/int/deaths-'.country_code.'-fit.png'
plot data using (column("Days_Past")):(column("Deaths")) title "Deaths" with points ls 1 \
, f(x) title sprintf ("7 Day Fit/Trend") with lines ls 2 \
, data using (column("Days_Past")):(column("Deaths_Doubling_Time")) title "Doubling Time" axis x1y2 with lines ls 5

unset output
# , f2(x) title sprintf ("model 2 days doubling") with lines \
# , f3(x) title sprintf ("model 3 days doubling") with lines
# , data using 1:13 title "change factor" axes x1y2 with linespoints ls 21
# plot 2: log scale
set logscale y
set yrange [1:] 
set title title ." - Log Scale"
set output '../plots-gnuplot/int/deaths-'.country_code.'-fit-log.png'
replot
unset output
unset logscale y



