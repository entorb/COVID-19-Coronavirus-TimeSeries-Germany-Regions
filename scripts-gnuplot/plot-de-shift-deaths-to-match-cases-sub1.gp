set title title . " für " . region
set yrange [0:*]
set output output
plot data u (column("Days_Past"))/7:(column("Cases_Last_Week_Per_Million")) t "Infektionen" ,\
     data u (column("Days_Past"))/7:(column("Deaths_Last_Week_Per_Million")) t "Tote" axes x1y2, \
     data u (column("Days_Past")+14<0?1/0:column("Days_Past")+14)/7:(column("Cases_Last_Week_Per_Million")*mortality) t "Prognose" axes x1y2 with lines lc rgb "red"
unset output
# replot using correct y2 scale
# bug in Gnuplot 5.2: GPVAL_Y_MAX is set to GPVAL_DATA_Y_MAX , so hard coding the range
y_max = GPVAL_DATA_Y_MAX * 1.1
set yrange [0:y_max]
set y2range [0:y_max*mortality] 
set output output
replot
unset output