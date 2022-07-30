#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

set title ""
# set ylabel "Cases"
# set xlabel "Days since first data"
set ylabel "Infektionen"
set xlabel "Tage"
set xtics 7

set ytics nomirror
set y2label "Verdopplungszeit (Tage)" tc ls 5 offset -2,0
set y2tics tc ls 5
set y2range [70:0]


# prepare data file for fit results
# write header line into fit output file
fit_data_file = "../data/de-states/de-states-cases-gnuplot-fit.tsv"
set print fit_data_file
print "State\tShort\ta\tb\tCases\tCases_Doubling_Time\tfactor t+1\tcases t+1\tfactor t+7\tcases t+7"
unset print

# text will be inserted later on
set label 2 "" right front at graph 0.98, graph 0.22
col_name = 'Fälle' # infections
short_name = 'BW' ; long_name = "Baden-Württemberg" ; load "plot-de-states-fit-sub1.gp"
short_name = 'BY' ; long_name = "Bayern" ; load "plot-de-states-fit-sub1.gp"
short_name = 'BE' ; long_name = "Berlin" ; load "plot-de-states-fit-sub1.gp"
short_name = 'BB' ; long_name = "Brandenburg" ; load "plot-de-states-fit-sub1.gp"
short_name = 'HB' ; long_name = "Bremen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'HH' ; long_name = "Hamburg" ; load "plot-de-states-fit-sub1.gp"
short_name = 'HE' ; long_name = "Hessen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'MV' ; long_name = "Mecklenburg-Vorpommern" ; load "plot-de-states-fit-sub1.gp"
short_name = 'NI' ; long_name = "Niedersachsen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'NW' ; long_name = "Nordrhein-Westfalen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'RP' ; long_name = "Rheinland-Pfalz" ; load "plot-de-states-fit-sub1.gp"
short_name = 'SL' ; long_name = "Saarland" ; load "plot-de-states-fit-sub1.gp"
short_name = 'SN' ; long_name = "Sachsen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'ST' ; long_name = "Sachsen-Anhalt" ; load "plot-de-states-fit-sub1.gp"
short_name = 'SH' ; long_name = "Schleswig-Holstein" ; load "plot-de-states-fit-sub1.gp"
short_name = 'TH' ; long_name = "Thüringen" ; load "plot-de-states-fit-sub1.gp"
short_name = 'DE-total' ; long_name = "Deutschland" ; load "plot-de-states-fit-sub1.gp"

# delete fit logfile
`rm fit.log`

