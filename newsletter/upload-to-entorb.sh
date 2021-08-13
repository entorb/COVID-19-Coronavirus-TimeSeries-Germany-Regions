#!/bin/bash

rsync -rvhu --no-perms newsletter-sender.py entorb@entorb.net:data-web-pages/covid-19/
rsync -rvhu --no-perms newsletter-view-DB.py entorb@entorb.net:data-web-pages/covid-19/

rsync -rvhu --no-perms newsletter-backend.py entorb@entorb.net:html/COVID-19-coronavirus/
rsync -rvhu --no-perms newsletter-*.html entorb@entorb.net:html/COVID-19-coronavirus/
rsync -rvhu --no-perms newsletter-frontend.js entorb@entorb.net:html/COVID-19-coronavirus/
