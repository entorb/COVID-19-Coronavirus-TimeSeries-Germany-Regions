# Based on
# https://raw.githubusercontent.com/ythlev/covid-19/master/run.py
# by Chang Chia-huan

import glob
import argparse
import pathlib
import json
import csv
import io
import urllib.request
import urllib.parse
import math
import statistics
import datetime
import re

# my helper modules
import helper

unit = 1000000
meta = {"colour": ["#fee5d9", "#fcbba1",
                   "#fc9272", "#fb6a4a", "#de2d26", "#a50f15"]}


d_all_date_data = {}
for f in glob.glob('data/de-districts/de-distict_timeseries-*.json'):
    lk_id = int(re.search('^.*de-distict_timeseries\-(\d+)\.json$', f).group(1))
    l = helper.read_json_file(f)
    for d in l:
        date = d['Date']
        if not d['Date'] in d_all_date_data:
            d_all_date_data[d['Date']] = {}
        del d['Timestamp'], d['Date'], d['Days_Past'], d['Days_Since_2nd_Death'], d['Cases_Change_Factor'], d['Deaths_Change_Factor']
        d_all_date_data[date][lk_id] = d
del f, d, l

property_to_plot = 'Cases_Last_Week_Per_Million'

values = []
# collect all values for autoscaling
for date_str, l_distritcs in d_all_date_data.items():
    for lk_id, d in l_distritcs.items():
        values.append(d[property_to_plot])

# generate color scale range
q = statistics.quantiles(values, n=100, method="inclusive")
step = math.sqrt(statistics.mean(values) - q[0]) / 3
threshold = [0, 0, 0, 0, 0, 0]
for i in range(1, 6):
    threshold[i] = math.pow(i * step, 2) + q[0]

# plot loop for each date
for date_str, l_distritcs in d_all_date_data.items():
    main = {}
    for lk_id, d in l_distritcs.items():

        area = lk_id
        pcapita = d[property_to_plot]
        main[area] = {'pcapita': pcapita}

    with open('maps/template_de-districts.svg', mode="r", newline="", encoding="utf-8") as file_in:
        with open(f'maps/out/de-districts-{date_str}.svg', mode="w", newline="", encoding="utf-8") as file_out:
            if threshold[5] >= 10000:
                num = "{:_.0f}"
            elif threshold[1] >= 10:
                num = "{:.0f}"
            else:
                num = "{:.2f}"

            for row in file_in:
                written = False
                for area in main:
                    if row.find('id="{}"'.format(area)) > -1:
                        i = 0
                        while i < 5:
                            if main[area]["pcapita"] >= threshold[i + 1]:
                                i += 1
                            else:
                                break
                        file_out.write(row.replace('id="{}"'.format(
                            area), 'style="fill:{}"'.format(meta["colour"][i])))
                        written = True
                        break
                if written == False:
                    if row.find('>Date') > -1:
                        file_out.write(row.replace(
                            'Date', date_str))
                    elif row.find('>level') > -1:
                        for i in range(6):
                            if row.find('level{}'.format(i)) > -1:
                                if i == 0:
                                    file_out.write(row.replace('level{}'.format(
                                        i), "&lt; " + num.format(threshold[1]).replace("_", "&#8201;")))
                                else:
                                    file_out.write(row.replace('level{}'.format(
                                        i), "≥ " + num.format(threshold[i]).replace("_", "&#8201;")))
                    else:
                        file_out.write(row)
