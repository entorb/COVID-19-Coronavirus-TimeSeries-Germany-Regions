#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

set terminal pngcairo size 800,800


set timefmt '%Y-%m-%d' # %d.%m.%Y %H:%M
set format x '%m/%y'
set xdata time


set key top left at graph 0, graph 1

set colorsequence default
unset style # reset line styles/types to default



# set xtics 1
# set xlabel "Weeks since 2nd death reported"

# set lmargin 10

date_last = system("tail -1 ../data/int/country-DE.tsv | cut -f1")
set label 1 label1_text_right." based on JHU data of ".date_last


last_x_AT = (system("tail -1 ../data/int/country-AT.tsv | cut -f1") + 0)
last_y_AT_pm = (system("tail -1 ../data/int/country-AT.tsv | cut -f7") + 0)
last_y_absolute_AT = (system("tail -1 ../data/int/country-AT.tsv | cut -f3") + 0)
last_y_last_week_pm_AT = (system("tail -1 ../data/int/country-AT.tsv | cut -f16") + 0)

last_x_BE = (system("tail -1 ../data/int/country-BE.tsv | cut -f1") + 0)
last_y_BE_pm = (system("tail -1 ../data/int/country-BE.tsv | cut -f7") + 0)
last_y_absolute_BE = (system("tail -1 ../data/int/country-BE.tsv | cut -f3") + 0)
last_y_last_week_pm_BE = (system("tail -1 ../data/int/country-BE.tsv | cut -f16") + 0)

last_x_CA = (system("tail -1 ../data/int/country-CA.tsv | cut -f1") + 0)
last_y_CA_pm = (system("tail -1 ../data/int/country-CA.tsv | cut -f7") + 0)
last_y_absolute_CA = (system("tail -1 ../data/int/country-CA.tsv | cut -f3") + 0)
last_y_last_week_pm_CA = (system("tail -1 ../data/int/country-CA.tsv | cut -f16") + 0)

last_x_FR = (system("tail -1 ../data/int/country-FR.tsv | cut -f1") + 0)
last_y_FR_pm = (system("tail -1 ../data/int/country-FR.tsv | cut -f7") + 0)
last_y_absolute_FR = (system("tail -1 ../data/int/country-FR.tsv | cut -f3") + 0)
last_y_last_week_pm_FR = (system("tail -1 ../data/int/country-FR.tsv | cut -f16") + 0)

last_x_DE = (system("tail -1 ../data/int/country-DE.tsv | cut -f1") + 0)
last_y_DE_pm = (system("tail -1 ../data/int/country-DE.tsv | cut -f7") + 0)
last_y_absolute_DE = (system("tail -1 ../data/int/country-DE.tsv | cut -f3") + 0)
last_y_last_week_pm_DE = (system("tail -1 ../data/int/country-DE.tsv | cut -f16") + 0)

last_x_HU = (system("tail -1 ../data/int/country-HU.tsv | cut -f1") + 0)
last_y_HU_pm = (system("tail -1 ../data/int/country-HU.tsv | cut -f7") + 0)
last_y_absolute_HU = (system("tail -1 ../data/int/country-HU.tsv | cut -f3") + 0)
last_y_last_week_pm_HU = (system("tail -1 ../data/int/country-HU.tsv | cut -f16") + 0)

last_x_IR = (system("tail -1 ../data/int/country-IR.tsv | cut -f1") + 0)
last_y_IR_pm = (system("tail -1 ../data/int/country-IR.tsv | cut -f7") + 0)
last_y_absolute_IR = (system("tail -1 ../data/int/country-IR.tsv | cut -f3") + 0)
last_y_last_week_pm_IR = (system("tail -1 ../data/int/country-IR.tsv | cut -f16") + 0)

last_x_IT = (system("tail -1 ../data/int/country-IT.tsv | cut -f1") + 0)
last_y_IT_pm = (system("tail -1 ../data/int/country-IT.tsv | cut -f7") + 0)
last_y_absolute_IT = (system("tail -1 ../data/int/country-IT.tsv | cut -f3") + 0)
last_y_last_week_pm_IT = (system("tail -1 ../data/int/country-IT.tsv | cut -f16") + 0)

last_x_JP = (system("tail -1 ../data/int/country-JP.tsv | cut -f1") + 0)
last_y_JP_pm = (system("tail -1 ../data/int/country-JP.tsv | cut -f7") + 0)
last_y_absolute_JP = (system("tail -1 ../data/int/country-JP.tsv | cut -f3") + 0)
last_y_last_week_pm_JP = (system("tail -1 ../data/int/country-JP.tsv | cut -f16") + 0)

last_x_KR = (system("tail -1 ../data/int/country-KR.tsv | cut -f1") + 0)
last_y_KR_pm = (system("tail -1 ../data/int/country-KR.tsv | cut -f7") + 0)
last_y_absolute_KR = (system("tail -1 ../data/int/country-KR.tsv | cut -f3") + 0)
last_y_last_week_pm_KR = (system("tail -1 ../data/int/country-KR.tsv | cut -f16") + 0)

last_x_NL = (system("tail -1 ../data/int/country-NL.tsv | cut -f1") + 0)
last_y_NL_pm = (system("tail -1 ../data/int/country-NL.tsv | cut -f7") + 0)
last_y_absolute_NL = (system("tail -1 ../data/int/country-NL.tsv | cut -f3") + 0)
last_y_last_week_pm_NL = (system("tail -1 ../data/int/country-NL.tsv | cut -f16") + 0)

last_x_PT = (system("tail -1 ../data/int/country-PT.tsv | cut -f1") + 0)
last_y_PT_pm = (system("tail -1 ../data/int/country-PT.tsv | cut -f7") + 0)
last_y_absolute_PT = (system("tail -1 ../data/int/country-PT.tsv | cut -f3") + 0)
last_y_last_week_pm_PT = (system("tail -1 ../data/int/country-PT.tsv | cut -f16") + 0)

last_x_ES = (system("tail -1 ../data/int/country-ES.tsv | cut -f1") + 0)
last_y_ES_pm = (system("tail -1 ../data/int/country-ES.tsv | cut -f7") + 0)
last_y_absolute_ES = (system("tail -1 ../data/int/country-ES.tsv | cut -f3") + 0)
last_y_last_week_pm_ES = (system("tail -1 ../data/int/country-ES.tsv | cut -f16") + 0)

last_x_CH = (system("tail -1 ../data/int/country-CH.tsv | cut -f1") + 0)
last_y_CH_pm = (system("tail -1 ../data/int/country-CH.tsv | cut -f7") + 0)
last_y_absolute_CH = (system("tail -1 ../data/int/country-CH.tsv | cut -f3") + 0)
last_y_last_week_pm_CH = (system("tail -1 ../data/int/country-CH.tsv | cut -f16") + 0)

last_x_UK = (system("tail -1 ../data/int/country-GB.tsv | cut -f1") + 0)
last_y_UK_pm = (system("tail -1 ../data/int/country-GB.tsv | cut -f7") + 0)
last_y_absolute_UK = (system("tail -1 ../data/int/country-GB.tsv | cut -f3") + 0)
last_y_last_week_pm_UK = (system("tail -1 ../data/int/country-GB.tsv | cut -f16") + 0)

last_x_US = (system("tail -1 ../data/int/country-US.tsv | cut -f1") + 0)
last_y_US_pm = (system("tail -1 ../data/int/country-US.tsv | cut -f7") + 0)
last_y_absolute_US = (system("tail -1 ../data/int/country-US.tsv | cut -f3") + 0)
last_y_last_week_pm_US = (system("tail -1 ../data/int/country-US.tsv | cut -f16") + 0)

last_x_SE = (system("tail -1 ../data/int/country-SE.tsv | cut -f1") + 0)
last_y_SE_pm = (system("tail -1 ../data/int/country-SE.tsv | cut -f7") + 0)
last_y_absolute_SE = (system("tail -1 ../data/int/country-SE.tsv | cut -f3") + 0)
last_y_last_week_pm_SE = (system("tail -1 ../data/int/country-SE.tsv | cut -f16") + 0)





title = "Death toll absolute"
set title title
set ylabel "Deaths"


# set label 11 "AT" left at first last_x_AT , first last_y_absolute_AT
# set label 12 "BE" left at first last_x_BE , first last_y_absolute_BE
# set label 13 "CA" left at first last_x_CA , first last_y_absolute_CA
# set label 14 "FR" left at first last_x_FR , first last_y_absolute_FR
# set label 15 "DE" left at first last_x_DE , first last_y_absolute_DE
# set label 16 "HU" left at first last_x_HU , first last_y_absolute_HU
# set label 17 "IR" left at first last_x_IR , first last_y_absolute_IR
# set label 18 "IT" left at first last_x_IT , first last_y_absolute_IT
# set label 19 "JP" left at first last_x_JP , first last_y_absolute_JP
# set label 20 "KR" left at first last_x_KR , first last_y_absolute_KR
# set label 21 "NL" left at first last_x_NL , first last_y_absolute_NL
# set label 22 "PT" left at first last_x_PT , first last_y_absolute_PT
# set label 23 "ES" left at first last_x_ES , first last_y_absolute_ES
# set label 24 "CH" left at first last_x_CH , first last_y_absolute_CH
# set label 25 "UK" left at first last_x_UK , first last_y_absolute_UK
# set label 26 "US" left at first last_x_US , first last_y_absolute_US
# set label 27 "SE" left at first last_x_SE , first last_y_absolute_SE


# set xrange [0:]
set yrange [0:]
set output '../plots-gnuplot/int/countries-deaths-absolute.png'
plot \
  '../data/int/country-IT.tsv' using (column("Date")):(column("Deaths")) title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using (column("Date")):(column("Deaths")) title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using (column("Date")):(column("Deaths")) title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using (column("Date")):(column("Deaths")) title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using (column("Date")):(column("Deaths")) title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using (column("Date")):(column("Deaths")) title "Austria" with lines lw 2, \
  '../data/int/country-GB.tsv' using (column("Date")):(column("Deaths")) title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using (column("Date")):(column("Deaths")) title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using (column("Date")):(column("Deaths")) title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using (column("Date")):(column("Deaths")) title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using (column("Date")):(column("Deaths")) title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using (column("Date")):(column("Deaths")) title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using (column("Date")):(column("Deaths")) title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using (column("Date")):(column("Deaths")) title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-JP.tsv' using (column("Date")):(column("Deaths")) title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using (column("Date")):(column("Deaths")) title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-SE.tsv' using (column("Date")):(column("Deaths")) title "Sweden" with lines lw 2 dt ".",\

unset output

set yrange [1:]
set logscale y
set title title ." - log. scaled"
set output '../plots-gnuplot/int/countries-deaths-absolute-log.png'
replot
unset output
unset logscale y


unset logscale y; unset logscale y2
# for per million plots I now try adding y2 tics
set ytics nomirror

# same scale on y and y2 axis (not working for log axis :-()
# set link y2

set y2tics ("US 9/11" 9, "US guns\n2017" 44, "US traffic 2018\nand\nflu 2018/19" 104, "US drugs\n2018" 205 , "US cancer\n2018" 1857)

set rmargin 15

title = "Death toll scaled per million population"
set title title
set ylabel "Deaths per Million Population"


# set label 11 "AT" left at first last_x_AT , first last_y_AT_pm
# set label 12 "BE" left at first last_x_BE , first last_y_BE_pm
# set label 13 "CA" left at first last_x_CA , first last_y_CA_pm
# set label 14 "FR" left at first last_x_FR , first last_y_FR_pm
# set label 15 "DE" left at first last_x_DE , first last_y_DE_pm
# set label 16 "HU" left at first last_x_HU , first last_y_HU_pm
# set label 17 "IR" left at first last_x_IR , first last_y_IR_pm
# set label 18 "IT" left at first last_x_IT , first last_y_IT_pm
# set label 19 "JP" left at first last_x_JP , first last_y_JP_pm
# set label 20 "KR" left at first last_x_KR , first last_y_KR_pm
# set label 21 "NL" left at first last_x_NL , first last_y_NL_pm
# set label 22 "PT" left at first last_x_PT , first last_y_PT_pm
# set label 23 "ES" left at first last_x_ES , first last_y_ES_pm
# set label 24 "CH" left at first last_x_CH , first last_y_CH_pm
# set label 25 "UK" left at first last_x_UK , first last_y_UK_pm
# set label 26 "US" left at first last_x_US , first last_y_US_pm
# set label 27 "SE" left at first last_x_SE , first last_y_SE_pm





output = '../plots-gnuplot/int/countries-deaths-per-million.png'
# set xrange [0:]
#set yrange [0:]
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
set yrange [0:10000]
set y2range [0:10000]
set output output
plot \
  '../data/int/country-IT.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Austria" with lines lw 2, \
  '../data/int/country-GB.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-JP.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-SE.tsv' using (column("Date")):(column("Deaths_Per_Million")) title "Sweden" with lines lw 2 dt ".", \

unset output
## replot to set y2range accordingly to yrange
#set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
#set output output
#replot
#unset output

# TODO
#set yrange [1:]
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
set yrange [1:10000]
set y2range [1:10000]
set logscale y ; set logscale y2
title = "Death toll development - scaled per million population and log"
set title title
output = '../plots-gnuplot/int/countries-deaths-per-million-log.png'
set output output
replot
unset output
## replot to set y2range accordingly to yrange
#set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
#set output output
#replot
#unset output


unset logscale y
unset logscale y2







title = "Weekly deaths per million"
set title title
set ylabel "Weekls deaths per million"


# set label 11 "AT" left at first last_x_AT , first last_y_last_week_pm_AT
# set label 12 "BE" left at first last_x_BE , first last_y_last_week_pm_BE
# set label 13 "CA" left at first last_x_CA , first last_y_last_week_pm_CA
# set label 14 "FR" left at first last_x_FR , first last_y_last_week_pm_FR
# set label 15 "DE" left at first last_x_DE , first last_y_last_week_pm_DE
# set label 16 "HU" left at first last_x_HU , first last_y_last_week_pm_HU
# set label 17 "IR" left at first last_x_IR , first last_y_last_week_pm_IR
# set label 18 "IT" left at first last_x_IT , first last_y_last_week_pm_IT
# set label 19 "JP" left at first last_x_JP , first last_y_last_week_pm_JP
# set label 20 "KR" left at first last_x_KR , first last_y_last_week_pm_KR
# set label 21 "NL" left at first last_x_NL , first last_y_last_week_pm_NL
# set label 22 "PT" left at first last_x_PT , first last_y_last_week_pm_PT
# set label 23 "ES" left at first last_x_ES , first last_y_last_week_pm_ES
# set label 24 "CH" left at first last_x_CH , first last_y_last_week_pm_CH
# set label 25 "UK" left at first last_x_UK , first last_y_last_week_pm_UK
# set label 26 "US" left at first last_x_US , first last_y_last_week_pm_US
# set label 27 "SE" left at first last_x_SE , first last_y_last_week_pm_SE


unset y2tics
set y2tics add ("US 9/11" 9,"US total mortality\n2017" 8638.0/52.14)
set y2tics add ("US cancer\nper day" 1857.0/52.14)


# for deaths new I used smooth bezier , but using deaths_last_week is more robust
# set xrange [0:]
#set yrange [0:]
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
set yrange [0:300]
set y2range [0:300]

output = '../plots-gnuplot/int/countries-deaths-last_week-per-million.png'
set output output
plot \
  '../data/int/country-IT.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Italy" with lines lw 2, \
  '../data/int/country-IR.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Iran" with lines lw 2, \
  '../data/int/country-DE.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Germany" with lines lw 2, \
  '../data/int/country-FR.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "France" with lines lw 2, \
  '../data/int/country-ES.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Spain" with lines lw 2, \
  '../data/int/country-AT.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Austria" with lines lw 2, \
  '../data/int/country-GB.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "United Kingdom" with lines lw 2, \
  '../data/int/country-US.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "US" with lines lw 2, \
  '../data/int/country-BE.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Belgium" with lines lw 2 dt "-", \
  '../data/int/country-CA.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Canada" with lines lw 2 dt "-", \
  '../data/int/country-HU.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Hungary" with lines lw 2 dt "-", \
  '../data/int/country-NL.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Netherlands" with lines lw 2 dt "-", \
  '../data/int/country-PT.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Portugal" with lines lw 2 dt "-", \
  '../data/int/country-CH.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Switzerland" with lines lw 2 dt "-", \
  '../data/int/country-JP.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Japan" with lines lw 2 dt "-", \
  '../data/int/country-KR.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Korea, South" with lines lw 2 dt "-",\
  '../data/int/country-SE.tsv' using (column("Date")):(column("Deaths_Last_Week_Per_Million")) title "Sweden" with lines lw 2 dt ".",\

unset output
## replot to set y2range accordingly to yrange
#set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
#set output output
#replot
#unset output


# Log plot
unset y2tics
set y2tics add ("US 9/11" 9,"US total mortality\n2017" 8638.0/52.14)
set y2tics add ("US cancer\nper day" 1857.0/52.14)
set y2tics add ("US guns\nper day" 44.0/52.14, "US traffic \nor flu\nper day" 104.0/52.14, "US drugs\nper day" 205.0/52.14)

# set yrange [0.01:]
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
set yrange [0.01:1000]
set y2range [0.01:1000]
set logscale y ; set logscale y2
set title title ." - log. scaled"
output= '../plots-gnuplot/int/countries-deaths-last_week-per-million-log.png'
set output output
replot
unset output
## replot to set y2range accordingly to yrange
#set y2range[GPVAL_Y_MIN:GPVAL_Y_MAX]
#set output output
#replot
#unset output

#print GPVAL_Y_MIN
#print GPVAL_Y_MAX

# show variables GPVAL

unset logscale y ; unset logscale y2


set xtics autofreq