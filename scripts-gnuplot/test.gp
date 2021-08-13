#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

set terminal pngcairo size 640,480 font 'Verdana,9'

set output "test.png"
plot sin(x)
unset output