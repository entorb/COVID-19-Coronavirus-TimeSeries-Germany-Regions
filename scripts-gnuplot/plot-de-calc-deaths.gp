# by Dr. Torben Menke
# https://entorb.net

# 17.10.2020: Umstellung von Exp Fit auf Lin Fit, da exp Anstieg der Gesamtzahl keinen Sinn mehr macht

# TODO: use  (timecolumn(1)-14*24*3600) instead of Days_Past
 # how to the fitting than???

load "header.gp"

set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'red'
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'blue'


death_offset = 21 #
fit_days = 7


set title "Abschätzung der Dunkelziffer der Infektionen\nAnnahmen: Infizierte sterben nach 3 Wochen mit Wahrscheinlichkeit von 1%"
# set ylabel "Cases"
# set xlabel "Days since first data"
set ylabel "Infizierte"
set xlabel "Tage"
set xtics 7

data = '../data/de-states/de-state-DE-total.tsv'

date_last = system("tail -1 " . data . " | cut -f1")
date_death_offset = system("tail -".death_offset." " . data . " | head -1 | cut -f1")

cases_last = ( system("tail -1 " . data . " | cut -f2") + 0)
deaths_last = ( system("tail -1 " . data . " | cut -f3") + 0)


f_exp(x)=N0 * exp(x * log(2)/T)
N0 = deaths_last + 0.0
T = 50.0

f_lin(x)= b + m*x
m = 1000.0
b = deaths_last + 0.0

# use only last 7 days (shifted by 14 days) for fit and require the number to be at least 2
xmin_for_fit = -(death_offset+fit_days-0.75)
set xrange [xmin_for_fit:-(death_offset+0.25)]

# set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
# set format x '%d.%m'
# set xdata time
# set xrange [date_death_offset:date_last]

fit f_exp(x) data using (column("Days_Past")-death_offset):(column("Deaths")*100) via N0, T
fit f_lin(x) data using (column("Days_Past")-death_offset):(column("Deaths")*100) via b,m

# delete fit logfile
`rm fit.log`

# set timefmt '%Y-%m-%d'
# set xdata time
# set format x "%d.%m"

set label 1 label1_text_right." based on RKI data of ".date_last


set label 2 \
 sprintf("\
 Fit Ergebnisse\n\
 Abschätzung Infizierte heute: %d\n\
 = %.3f%% der DE Bevölkerung\n\
 Vergleich Abschätzung zu\noffizieller Fallzahl: %.1fx höher\
 "\
 , f_lin(0) \
 , f_lin(0) / 83019200 * 100 \
 , f_lin(0)/cases_last \
 ) \
 right front at graph 0.98, graph 0.6
#  Verdopplungszeit Opfer: %d Tage\n\
# Exp Vergleich Abschätzung zu\noffizieller Fallzahl: %.1fx höher\


set key right bottom width -2

set xtic add (date_last 0)
#set logscale y
set xrange [-35:0]
set yrange  [0:]
# set samples 300md
set output '../plots-gnuplot/de-states/calc-cases-from-deaths-DE-total.png'
plot data using (column("Days_Past")-death_offset):(column("Deaths")*100) title "geschätze Infizierte" with linespoints ls 1 ,\
     data using (column("Days_Past")):(column("Cases")) title "positiv getestet" with linespoints ls 2 ,\
     (x<=xmin_for_fit)?1/0:f_lin(x) title "Fit/Modell" with lines ls 1 dt "-" linecolor rgb 'black'

#     (x<=xmin_for_fit)?1/0:f_exp(x) title "ExpFit/Modell" with lines ls 1 dt "-" linecolor rgb 'black' ,\

unset output
