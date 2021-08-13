#!/usr/bin/gnuplot

# by Torben Menke
# https://entorb.net

# set terminal png noenhanced large size 640,480
set terminal pngcairo size 640,480 font 'Verdana,9'
# set terminal svg size 640,480 fname 'Verdana, Helvetica, Arial, sans-serif' rounded dashed

set datafile commentschars '#'
# set datafile missing '#'
set datafile separator "\t"

set encoding utf8

label1_text_right = "by Torben https://entorb.net"
set label 1 label1_text_right rotate by 90 center at screen 0.985, screen 0.5

# data
set style line 1 linetype 7 dt 3 lw 2 linecolor rgb 'black' 
# fit
set style line 2 linetype 7 dt "-" lw 2 linecolor rgb 'black' 
# model 1
set style line 3 linetype 7 dt 4 lw 2 linecolor rgb 'red' 
# model 2
set style line 4 linetype 7 dt 5 lw 2 linecolor rgb 'blue' 

# dublication time
set style line 5 linetype 7 dt "." lw 2 linecolor rgb 'blue' 

# change factor
# set style line 21 linetype 7 dt 5 lw 2 linecolor rgb 'green' 
# boxplot
set style line 11 linetype 8 dt 1 lw 1 linecolor rgb "red"
# guide line
set style line 12 linetype 7 dt 1 lw 2 linecolor rgb 'grey' 

set grid xtics ytics
set xtics mirror
set ytics mirror 

set fit quiet

set key top left box
