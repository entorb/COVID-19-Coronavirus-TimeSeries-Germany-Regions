#!/bin/bash

# rsync -rvhu --delete --delete-excluded ../plots-excel/* entorb@entorb.net:html/COVID-19-coronavirus/plots-excel/
rsync -rvhu --quiet --delete --delete-excluded --no-perms ../plots-gnuplot/* entorb@entorb.net:html/COVID-19-coronavirus/plots-gnuplot/
