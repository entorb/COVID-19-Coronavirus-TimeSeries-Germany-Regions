#!/bin/bash

# rsync -rvhu --delete --delete-excluded ../plots-excel/* entorb@entorb.net:html/COVID-19-coronavirus/plots-excel/
rsync -rvhu --quiet --delete --delete-excluded --no-perms ../maps/*.gif entorb@entorb.net:html/COVID-19-coronavirus/maps/
rsync -rvhu --quiet --delete --delete-excluded --no-perms ../maps/*.mp4 entorb@entorb.net:html/COVID-19-coronavirus/maps/
