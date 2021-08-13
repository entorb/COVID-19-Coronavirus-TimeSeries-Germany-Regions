#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

set terminal pngcairo size 640,800


set title ""
# set xlabel "Datum"

# now lets compare several stats
set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
set format x '%d.%m'
set xdata time

# TODO:
# set term windows


set key top left at graph 0, graph 1 font 'Verdana,6'

set colorsequence default
unset style # reset line styles/types to default


date_last = system("tail -1 ../data/de-states/de-state-BW.tsv | cut -f1")
set label 1 label1_text_right." based on RKI data of ".date_last

title = "Infizierte in absoluten Zahlen"
set title title
set ylabel "Infizierte"


set yrange [0:]
set output '../plots-gnuplot/de-states/cases-de-absolute.png'
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Cases")) title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Cases")) title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Cases")) title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Cases")) title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Cases")) title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Cases")) title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Cases")) title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Cases")) title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Cases")) title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Cases")) title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Cases")) title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Cases")) title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Cases")) title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Cases")) title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Cases")) title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Cases")) title "Bremen" with lines lw 2 dt "-", \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases")) title "Deutschland" with lines , \

set yrange [1:]
set logscale y

set title title ." - log. skaliert"
set output '../plots-gnuplot/de-states/cases-de-absolute-log.png'
replot
unset output
unset logscale y


title = "Infizierte pro 1 Mill. Einwohner"
set title title
set ylabel "Infizierte pro 1 Mill. Einwohner"
set yrange [0:]
set output '../plots-gnuplot/de-states/cases-de-per-million.png'
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Bremen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases_Per_Million")) title "Deutschland" with lines lw 4 dt 1 linecolor rgb "red", \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases")) title "Deutschland" with lines , \

set yrange [1:]
set logscale y
set title title ." - log. skaliert"
set output '../plots-gnuplot/de-states/cases-de-per-million-log.png'
replot
unset output
unset logscale y


set key top right at graph 1, graph 1
title = "Täglich Neu-Infizierte pro 1 Mill. Einwohner"
set title title
set ylabel "Täglich Neu-Infizierte pro 1 Mill. Einwohner"
set yrange [0:]
set output '../plots-gnuplot/de-states/cases-de-new-per-million.png'
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Bremen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases_New_Per_Million")) smooth bezier title "Deutschland" with lines lw 4 dt 1 linecolor rgb "red", \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases")) title "Deutschland" with lines , \

set yrange [1:]
set logscale y
set title title ." - log. skaliert"
set output '../plots-gnuplot/de-states/cases-de-new-per-million-log.png'
replot
unset output
unset logscale y




title = "Neu Infizierte in 7 Tagen pro 1 Mill. Einwohner"
set title title
set ylabel "Neu Infizierte in 7 Tagen pro 1 Mill. Einwohner"
set yrange [0:]
output = '../plots-gnuplot/de-states/cases-de-last_week-per-million.png'
set output output
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Bremen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Cases_Last_Week_Per_Million")) title "Deutschland" with lines lw 4 dt 1 linecolor rgb "red", \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Deaths")) title "Deutschland" with lines , \

set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output output
replot
unset output

set yrange [1:]
set logscale y
set logscale y2
set title title ." - log. skaliert"
output = '../plots-gnuplot/de-states/cases-de-last_week-per-million-log.png'
set output output
replot
unset output
unset logscale y
unset logscale y2






# Deaths: only per million
set ytics nomirror
set y2tics ("DE HIV\n2018" 5, "DE Drogen\n2019" 17, "DE Verkehr\n2019" 39, "DE Suizid\n2017" 111, "DE Grippe\n2017" 302, "DE Krebs\n2017" 2741, "DE Tote\n2018" 11502)

set rmargin 15

set key top left at graph 0, graph 1
title = "Verstorbene pro 1 Mill. Einwohner"
set title title
set ylabel "Verstorbene pro 1 Mill. Einwohner"
#set yrange [0:]
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
y_max = 3000
set yrange [0:y_max]
set y2range [0:y_max]
output = '../plots-gnuplot/de-states/deaths-de-per-million.png'
set output output
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Bremen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Deutschland" with lines lw 4 dt 1 linecolor rgb "red", \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Deaths")) title "Deutschland" with lines , \

#set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
#set output output
#replot
#unset output



#set yrange [1:]
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
set yrange [1:y_max]
set y2range [1:y_max]

set logscale y
set logscale y2
set title title ." - log. skaliert"
output = '../plots-gnuplot/de-states/deaths-de-per-million-log.png'
set output output
replot
unset output

#set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
#set output output
#replot
#unset output
unset logscale y
unset logscale y2
unset y2tics


set y2tics ("DE Suizid\n2017" 111.0/365, "DE Krebs\n2017" 2741.0/365, "DE Tote\n2018" 11502.0/365)


set key top right at graph 1, graph 1
title = "Täglich Verstorbene pro 1 Mill. Einwohner"
set title title
set ylabel "Täglich Verstorbene pro 1 Mill. Einwohner"
y_max = 50
set yrange [0:y_max]
output = '../plots-gnuplot/de-states/deaths-de-new-per-million.png'
set output output
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Bremen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Deaths_New_Per_Million")) smooth bezier title "Deutschland" with lines lw 4 dt 1 linecolor rgb "red", \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Deaths")) title "Deutschland" with lines , \

set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output output
replot
unset output

set y2tics add ("DE HIV\n2018" 5.0/365, "DE Drogen\n2019" 17.0/365, "DE Verkehr\n2019" 39.0/365)

set yrange [0.1:y_max]
set logscale y
set logscale y2
set title title ." - log. skaliert"
output = '../plots-gnuplot/de-states/deaths-de-new-per-million-log.png'
set output output
replot
unset output

set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
set output output
replot
unset output

unset logscale y
unset logscale y2

unset y2tics


set y2tics ("DE Drogen\n2019" 17.0/7, "DE Verkehr\n2019" 39.0/7,"DE Suizid\n2017" 111.0/7, "DE Krebs\n2017" 2741.0/7, "DE Tote\n2018" 11502.0/7)


title = "Wöchentlich Verstorbene pro 1 Mill. Einwohner"
set title title
set ylabel "Wöchentlich Verstorbene pro 1 Mill. Einwohner"
#set yrange [0:]
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
y_max = 300
set yrange [0:y_max]
set y2range [0:y_max]

output = '../plots-gnuplot/de-states/deaths-de-last_week-per-million.png'
set output output
plot \
  '../data/de-states/de-state-NW.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Nordrhein-Westfalen" with lines lw 2, \
  '../data/de-states/de-state-BY.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Bayern" with lines lw 2, \
  '../data/de-states/de-state-BW.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Baden-Württemberg" with lines lw 2, \
  '../data/de-states/de-state-NI.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Niedersachsen" with lines lw 2, \
  '../data/de-states/de-state-HE.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Hessen" with lines lw 2, \
  '../data/de-states/de-state-RP.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Rheinland-Pfalz" with lines lw 2, \
  '../data/de-states/de-state-BE.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Berlin" with lines lw 2, \
  '../data/de-states/de-state-HH.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Hamburg" with lines lw 2, \
  '../data/de-states/de-state-SN.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Sachsen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SH.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Schleswig-Holstein" with lines lw 2 dt "-", \
  '../data/de-states/de-state-BB.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Brandenburg" with lines lw 2 dt "-", \
  '../data/de-states/de-state-TH.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Thüringen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-ST.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Sachsen-Anhalt" with lines lw 2 dt "-", \
  '../data/de-states/de-state-SL.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Saarland" with lines lw 2 dt "-", \
  '../data/de-states/de-state-MV.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Mecklenburg-Vorpommern" with lines lw 2 dt "-", \
  '../data/de-states/de-state-HB.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Bremen" with lines lw 2 dt "-", \
  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Deutschland" with lines lw 4 dt 1 linecolor rgb "red", \

unset output
#  '../data/de-states/de-state-DE-total.tsv' using (column("Date")):(column("Deaths")) title "Deutschland" with lines , \

#set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
#set output output
#replot
#unset output

set y2tics add ("DE HIV\n2018" 5.0/7)

#set yrange [0.1:]
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
set yrange [0.1:y_max]
set y2range [0.1:y_max]

set logscale y
set logscale y2
set title title ." - log. skaliert"
output = '../plots-gnuplot/de-states/deaths-de-last_week-per-million-log.png'
set output output
replot
unset output

#set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
#set output output
#replot
#unset output

unset logscale y
unset logscale y2

