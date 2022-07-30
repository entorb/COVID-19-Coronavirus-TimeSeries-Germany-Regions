#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

load "header.gp"

# set terminal pngcairo size 640,480 font 'Verdana,9'

# set datafile commentschars '#'
# # set datafile missing '#'
# set datafile separator "\t"


set style data linespoints
set style increment user # important!!! switch between linetypes (default) and userdefined linestyles
set style line 1 linetype 7 dt 1 lw 2 linecolor rgb 'blue' 
set style line 2 linetype 7 dt 1 lw 2 linecolor rgb 'red' 
set style line 3 linetype 7 dt 1 lw 2 linecolor rgb 'black' 


data_BW = '../data/de-divi/de-divi-BW.tsv'; title_BW = 'Krankenhausauslastung in Baden-Württemberg'
data_BY = '../data/de-divi/de-divi-BY.tsv'; title_BY = 'Krankenhausauslastung in Bayern'
data_BE = '../data/de-divi/de-divi-BE.tsv'; title_BE = 'Krankenhausauslastung in Berlin'
data_BB = '../data/de-divi/de-divi-BB.tsv'; title_BB = 'Krankenhausauslastung in Brandenburg'
data_HB = '../data/de-divi/de-divi-HB.tsv'; title_HB = 'Krankenhausauslastung in Bremen'
data_HH = '../data/de-divi/de-divi-HH.tsv'; title_HH = 'Krankenhausauslastung in Hamburg'
data_HE = '../data/de-divi/de-divi-HE.tsv'; title_HE = 'Krankenhausauslastung in Hessen'
data_MV = '../data/de-divi/de-divi-MV.tsv'; title_MV = 'Krankenhausauslastung in Mecklenburg-Vorpommern'
data_NI = '../data/de-divi/de-divi-NI.tsv'; title_NI = 'Krankenhausauslastung in Niedersachsen'
data_NW = '../data/de-divi/de-divi-NW.tsv'; title_NW = 'Krankenhausauslastung in Nordrhein-Westfalen'
data_RP = '../data/de-divi/de-divi-RP.tsv'; title_RP = 'Krankenhausauslastung in Rheinland-Pfalz'
data_SL = '../data/de-divi/de-divi-SL.tsv'; title_SL = 'Krankenhausauslastung in Saarland'
data_SN = '../data/de-divi/de-divi-SN.tsv'; title_SN = 'Krankenhausauslastung in Sachsen'
data_ST = '../data/de-divi/de-divi-ST.tsv'; title_ST = 'Krankenhausauslastung in Sachsen-Anhalt'
data_SH = '../data/de-divi/de-divi-SH.tsv'; title_SH = 'Krankenhausauslastung in Schleswig-Holstein'
data_TH = '../data/de-divi/de-divi-TH.tsv'; title_TH = 'Krankenhausauslastung in Thüringen'

set yrange [0:100]

set ylabel "Belegung"

set timefmt '%Y-%m-%d'
set xdata time
set format x "%d.%m"

set xtics 1*24*3600

# set title "%A%"
# set output "../plots-gnuplot/de-divi/de-divi-%A%.png"
# plot data_%A% using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
# unset output


set title title_BW
set output "../plots-gnuplot/de-divi/de-divi-BW.png"
plot data_BW using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_BY
set output "../plots-gnuplot/de-divi/de-divi-BY.png"
plot data_BY using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_BE
set output "../plots-gnuplot/de-divi/de-divi-BE.png"
plot data_BE using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_BB
set output "../plots-gnuplot/de-divi/de-divi-BB.png"
plot data_BB using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_HB
set output "../plots-gnuplot/de-divi/de-divi-HB.png"
plot data_HB using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_HH
set output "../plots-gnuplot/de-divi/de-divi-HH.png"
plot data_HH using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_HE
set output "../plots-gnuplot/de-divi/de-divi-HE.png"
plot data_HE using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_MV
set output "../plots-gnuplot/de-divi/de-divi-MV.png"
plot data_MV using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_NI
set output "../plots-gnuplot/de-divi/de-divi-NI.png"
plot data_NI using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_NW
set output "../plots-gnuplot/de-divi/de-divi-NW.png"
plot data_NW using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_RP
set output "../plots-gnuplot/de-divi/de-divi-RP.png"
plot data_RP using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_SL
set output "../plots-gnuplot/de-divi/de-divi-SL.png"
plot data_SL using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_SN
set output "../plots-gnuplot/de-divi/de-divi-SN.png"
plot data_SN using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_ST
set output "../plots-gnuplot/de-divi/de-divi-ST.png"
plot data_ST using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_SH
set output "../plots-gnuplot/de-divi/de-divi-SH.png"
plot data_SH using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output

set title title_TH
set output "../plots-gnuplot/de-divi/de-divi-TH.png"
plot data_TH using 1:2 t "ICU low", '' using 1:3 t "ICU high", '' using 1:4 t "ICU ECMO" 
unset output





# set style data histograms
# set style histogram rowstacked
# set boxwidth 1 relative
# set style fill solid 1.0 border -1

# set output "test-divi-BW.png"
# plot data_BW using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-BY.png"
# plot data_BY using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-BE.png"
# plot data_BE using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-BB.png"
# plot data_BB using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-HB.png"
# plot data_HB using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-HH.png"
# plot data_HH using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-HE.png"
# plot data_HE using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-MV.png"
# plot data_MV using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-NI.png"
# plot data_NI using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-NW.png"
# plot data_NW using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-RP.png"
# plot data_RP using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-SL.png"
# plot data_SL using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-SN.png"
# plot data_SN using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-ST.png"
# plot data_ST using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-SH.png"
# plot data_SH using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output
# set output "test-divi-TH.png"
# plot data_TH using ($2/3) t "ICU low", '' using ($3/3) t "ICU high", '' using ($4/3):xticlabels(1) t "ICU ECMO"
# unset output