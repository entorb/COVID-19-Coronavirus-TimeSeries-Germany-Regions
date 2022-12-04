# by Dr. Torben Menke
# https://entorb.net

# TODO: shall this go to de-states or to int/countries?

load "header.gp"

set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'blue'
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'red'
set style line 3 linetype 7 dt "-" lw 3 linecolor rgb 'red'




data = '../data/de-states/de-state-DE-total.tsv'
# data = '../data/int/country-DE.tsv'

date_last = system("tail -1 " . data . " | cut -f1")

set label 1 label1_text_right." based on RKI data of ".date_last
# set label 1 label1_text_right." based on JHU data of ".date_last


# set xlabel "Wochen"
# set xtics 1
# set xtic add (date_last 0)


set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
set format x '%d.%m'
set xdata time


set ytics nomirror
set y2tics nomirror

set ylabel "Infizierte letzte Woche" offset 0,0 textcolor ls 1
set y2label "Tote letzte Woche" offset -0,0 textcolor ls 2

set ytics textcolor ls 1
set y2tics textcolor ls 2

# x_min = -10
# set xrange [x_min:0]
# y_max=41000
mortality = 4.3/100
# mortality = 2.0/100 ; set xrange ["2020-07-01":]

# mask_zero_values(x) = (x<=0)?1/0:x

set label 2 sprintf("Skalierung: %.1f%%", mortality*100.0) left front at graph 0.28, graph 0.85 textcolor rgb "red"

set key width 0 top left width -2

# How much are the deaths in Germany delayed?
set title "Zeitverzug zwischen Infektion und Tod in Deutschland"
set yrange [0:*]

output ='../plots-gnuplot/de-states/shift-deaths-to-match-cases_DE_last-week.png'
set output output
plot data u (column("Date")):(column("Cases_Last_Week")) t "Infizierte" with lines ls 1, \
     data u (column("Date")):(column("Deaths_Last_Week")) t "Tote" axes x1y2 with lines ls 2, \
     data u (timecolumn(1)-14*24*3600):(column("Deaths_Last_Week")) t "Tote verschoben um 14 Tage" axes x1y2 with lines ls 3
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
set ylabel "Infizierte letzte Woche pro Millionen"
set y2label "Tote letzte Woche pro Millionen"

set yrange [0:*]

output = '../plots-gnuplot/de-states/shift-deaths-to-match-cases_DE_last-week_per_million.png'
set output output
plot data u (column("Date")):(column("Cases_Last_Week_Per_Million")) t "Infizierte" with lines ls 1, \
     data u (column("Date")):(column("Deaths_Last_Week_Per_Million")) t "Tote" axes x1y2 with lines ls 2, \
     data u (timecolumn(1)-14*24*3600):(column("Deaths_Last_Week_Per_Million")) t "Tote verschoben um 14 Tage" axes x1y2 with lines ls 3
unset output
# replot using correct y2 scale
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
y_max = GPVAL_DATA_Y_MAX * 1.1
set yrange [0:y_max]
set y2range [0:y_max*mortality]
set output output
replot
unset output
