#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

data = '../data/int/countries-latest-selected.tsv'

date_last = system("tail -1 " . data . " | cut -f2")

set label 1 label1_text_right." based on JHU data of ".date_last

set xtics rotate by 60 offset 1,0 right
# set bmargin 10.5
set style fill solid 0.5 border 0
set boxwidth 0.75 relative
set key off
set yrange [0:]

title = "Deaths"
set title title
set ylabel "Deaths"
set output '../plots-gnuplot/int/countries-latest-selected-deaths.png'
plot data using (column("Deaths")):xticlabels(1) with boxes ls 11
unset output
#
title = title." - Log Scale"
set title title
set logscale y
set output '../plots-gnuplot/int/countries-latest-selected-deaths-log.png'
set yrange [1:]
replot
unset output
unset logscale y
unset yrange

title = "Deaths per Million Population"
set title title
set ylabel "Deaths per Million Population"
set output '../plots-gnuplot/int/countries-latest-selected-deaths-per-mill.png'
plot data using (column("Deaths_Per_Million")):xticlabels(1) with boxes ls 11
unset output
#
title = title." - Log Scale"
set title title
set logscale y
set output '../plots-gnuplot/int/countries-latest-selected-deaths-per-mill-log.png'
replot
unset output
unset logscale y

title = "Duplications until hitting Italy's deaths per capita\n(larger means more time to prepare)"
set title title
set yrange [0:]
deaths_per_million_of_IT = system ("grep Italy ../data/int/countries-latest-selected.tsv| tail -1 | cut -f7") + 0
#print deaths_per_million_of_IT
set ylabel "Duplications"
# TODO
# set output '../plots-gnuplot/int/countries-duplications-until-IT-level-of-deaths.png'
# plot data using (log(deaths_per_million_of_IT/column("Deaths_Per_Million"))/log(2)):xticlabels(1) with boxes ls 11
# unset output

title = "Calculated Case Mortality: Deaths per Reported Infections"
set title title
set ylabel "Calculated Case Mortality: Deaths per Reported Infections"
set ytics format "%g%%"
set output '../plots-gnuplot/int/countries-deaths-per-infections.png'
plot data using (100.0 * column("Deaths")/column("Cases")):xticlabels(1) with boxes ls 11
unset output
set ytics format "%g"

title = "Comparing Calculated Case Mortality to Deaths per Capita"
set title title
set xtics rotate by 0
set xlabel "Deaths per Million Population"
set output '../plots-gnuplot/int/countries-mortality-vs-deaths-ppm.png'
plot data using (column("Deaths_Per_Million")):(100.0 * column("Deaths")/column("Cases")) with points ls 1
unset output



# text will be inserted later on
set label 2 "" right front at graph 0.3, graph 0.6
set ylabel "Deaths"
set xlabel "Days"

set ytics nomirror
set y2label "Duplication Time (Days)" tc ls 5 offset -2,0
set y2tics tc ls 5
set y2range [14:0]



# set lmargin 9

# this is no longer updated daily, since the exponential growth has ended after 30.03.2020

# fit_data_file = "../data/int/countries-gnuplot-fit.tsv"
# set print fit_data_file
# print "Country\tCode\ta\tb\tDeaths\tDeaths_Doubling_Time\tFactor at t+1\tDeaths at t+1\tFactor at t+7\tDeaths at t+7"
# unset print
# set xtics 7 rotate by 0
# country_code = "AT" ; country_name = "Austria" ; load "plot-countries-sub1.gp"
# country_code = "BE" ; country_name = "Belgium" ; load "plot-countries-sub1.gp"
# country_code = "CA" ; country_name = "Canada" ; load "plot-countries-sub1.gp"
# country_code = "CZ" ; country_name = "Czechia" ; load "plot-countries-sub1.gp"
# country_code = "DK" ; country_name = "Denmark" ; load "plot-countries-sub1.gp"
# country_code = "FI" ; country_name = "Finland" ; load "plot-countries-sub1.gp"
# country_code = "FR" ; country_name = "France" ; load "plot-countries-sub1.gp"
# country_code = "DE" ; country_name = "Germany" ; load "plot-countries-sub1.gp"
# country_code = "GR" ; country_name = "Greece" ; load "plot-countries-sub1.gp"
# country_code = "HU" ; country_name = "Hungary" ; load "plot-countries-sub1.gp"
# country_code = "IR" ; country_name = "Iran" ; load "plot-countries-sub1.gp"
# country_code = "IT" ; country_name = "Italy" ; load "plot-countries-sub1.gp"
# country_code = "JP" ; country_name = "Japan" ; load "plot-countries-sub1.gp"
# country_code = "NL" ; country_name = "Netherlands" ; load "plot-countries-sub1.gp"
# country_code = "PT" ; country_name = "Portugal" ; load "plot-countries-sub1.gp"
# country_code = "KR" ; country_name = "South Korea" ; load "plot-countries-sub1.gp"
# country_code = "ES" ; country_name = "Spain" ; load "plot-countries-sub1.gp"
# country_code = "SE" ; country_name = "Sweden" ; load "plot-countries-sub1.gp"
# country_code = "CH" ; country_name = "Switzerland" ; load "plot-countries-sub1.gp"
# country_code = "TR" ; country_name = "Turkey" ; load "plot-countries-sub1.gp"
# country_code = "GB" ; country_name = "United Kingdom" ; load "plot-countries-sub1.gp"
# country_code = "US" ; country_name = "United States" ; load "plot-countries-sub1.gp"
# # delete fit logfile
# `rm fit.log`

unset xrange
unset yrange
unset label 2
unset label 3
unset xlabel
unset ylabel
set xtics autofreq
set ytics mirror
unset y2tics
unset y2label
unset ytics
set ytics

# let's plot the fit data as boxes
set title "Fit Result: Deaths Doubling Time (Days)"
set ylabel "Deaths Doubling Time (Days)"
set xtics rotate by 60 offset 1,0 right
set ytics 7 format "%g" 
unset bmargin
set style fill solid 0.5 border 0
set boxwidth 0.75 relative
set key off
set yrange [0:21]
# y_value_de = ( system("tail -1 " . fit_data_file . " | cut -f6") + 0)
# set output '../plots-gnuplot/int/countries-fit-deaths-doubling-time.png'
# plot fit_data_file using (column("Deaths_Doubling_Time")):xticlabels(1) with boxes ls 11
# unset output
set yrange [0:*]
set ytics autofreq format "%g%%" 
set title "Fit Result: Increase of Deaths per Day"
set ylabel "Increase Deaths per Day"
# TODO
# y_value_de = ( system("tail -1 " . fit_data_file . " | cut -f7") + 0)
# y_value_de = (y_value_de-1)*100
# set output '../plots-gnuplot/int/countries-fit-deaths-increase-1-day.png'
# plot fit_data_file using ((column("Factor at t+1")-1)*100):xticlabels(1) with boxes ls 11
# unset output
set ytics autofreq format "%g" 

# combining the duplications until reaching IT level from countries-latest-selected.tsv and the duplication time from countries-gnuplot-fit.tsv
# this needs the python script join-country-latest-and-fit-data.py to run first after plotting
set title "Days until hitting Italy's deaths per capita\nbased on current deaths and fitted duplication time"
set ylabel "Days (estimated)"
set yrange [0:28]
set ytics 0,7
out = system ("cd .. ; python3 join-country-latest-and-fit-data.py ; cd scripts-gnuplot")
print out
data = '../data/int/countries-joined_selected_and_gnuplot_fit.tsv'
# TODO
# set output '../plots-gnuplot/int/countries-days-until-IT-level-of-deaths.png'
# plot data u (column("Days till deaths/pop of Italy")):xticlabels(1) with boxes ls 11
# unset output
unset yrange
set ytics autofreq
# plot and fit time series








reset ; load "plot-countries-deaths.gp"
