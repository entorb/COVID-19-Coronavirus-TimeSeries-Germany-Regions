# Forecast
set key width 0 top right
x_min = -8
set xrange [x_min:2]
set arrow 3 nohead back from first 0, graph 0 to first 0, graph 0.85 dashtype "-"
set label 2 at graph 0.99, graph 0.05

title = "Prognose der Opferzahlen, basierend auf den Infektionen"

# DE
region = "Deutschland"
data = '../data/de-states/de-state-DE-total.tsv'
output = '../plots-gnuplot/de-states/forecasting-deaths-DE.png'
load 'plot-de-shift-deaths-to-match-cases-sub1.gp'

# Bayern
region = "Bayern"
data = '../data/de-states/de-state-BY.tsv'
output = '../plots-gnuplot/de-states/forecasting-deaths-BY.png'
load 'plot-de-shift-deaths-to-match-cases-sub1.gp'

# Erlangen
region = "Erlangen"
data = '../data/de-districts/de-district_timeseries-09562.tsv'
output = '../plots-gnuplot/de-states/forecasting-deaths-Erlangen.png'
load 'plot-de-shift-deaths-to-match-cases-sub1.gp'

