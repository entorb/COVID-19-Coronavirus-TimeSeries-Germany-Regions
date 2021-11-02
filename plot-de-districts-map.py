#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Generates animated maps for Germany using Covid-19 data and Divi hospital data
Based on
https://raw.githubusercontent.com/ythlev/covid-19/master/run.py
by Chang Chia-huan
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import os
import sys
import glob
import subprocess
import json
import math
import statistics
import re

# my helper modules
import helper

# TODO: replace threshold magic based on all data by simple logic based on last value for cases and manually set threshold for other sets

unit = 1000000


def run_imagemagick_convert(l_imagemagick_parameters: list, wait_for_finish: bool = True):
    """
    wait_for_finish = False: the calling function needs to handle the returned process
    """
    # prepend 'convert'
    l_imagemagick_parameters.insert(0, 'convert')
    if os.name == 'posix':
        # print ('posix/Unix/Linux')
        1
    elif os.name == 'nt':
        # print ('Windows')
        # prepend 'magick
        l_imagemagick_parameters.insert(0, 'magick')
    else:
        print('unknown os')
        sys.exit(1)  # throws exception, use quit() to close silently

    process = subprocess.Popen(l_imagemagick_parameters,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    if wait_for_finish:
        stdout, stderr = process.communicate()
        if stdout != '':
            print(f'Out: {stdout}')
        if stderr != '':
            print(f'ERROR: {stderr}')
    return process


# from https://htmlcolorcodes.com/
# alternative: https://www.w3schools.com/colors/colors_picker.asp
d_color_scales = {
    'template': [
        '#aed6f1',
        '#85c1e9',
        '#5dade2',
        '#3498db',
        '#2e86c1',
        '#2874a6',
        '#21618c',
        '#1b4f72'
    ],
    'blue': [
        '#d6eaf8',
        '#85c1e9',
        '#5dade2',
        '#3498db',
        '#2e86c1',
        '#2874a6',
        '#21618c',
        '#1b4f72'
    ],
    'red':
    [
        '#e6b0aa',
        '#d98880',
        '#cd6155',
        '#c0392b',
        '#a93226',
        '#922b21',
        '#7b241c',
        '#641e16'
    ],
    'purple':
    [
        '#d2b4de',
        '#bb8fce',
        '#a569bd',
        '#8e44ad',
        '#7d3c98',
        '#6c3483',
        '#5b2c6f',
        '#4a235a'
    ],
    'green':
    [
        '#a9dfbf',
        '#7dcea0',
        '#52be80',
        '#27ae60',
        '#229954',
        '#1e8449',
        '#196f3d',
        '#145a32'
    ]
}

d_all_date_data = {}
l_month = []
count = 0
for f in glob.glob('data/de-districts/de-district_timeseries-*.json'):
    count += 1
    lk_id = int(re.search('^.*de-district_timeseries\-(\d+)\.json$', f).group(1))
    l = helper.read_json_file(f)
    for d in l:
        date = d['Date']
        thisMonth = date[0:7]
        # skip old data points
        if thisMonth in ('2020-01', '2020-02'):
            continue
        # add to list of months for later creations of 1 gif per month
        if count == 1:
            if thisMonth not in l_month:
                l_month.append(thisMonth)
        if not d['Date'] in d_all_date_data:
            d_all_date_data[d['Date']] = {}
        # del d['Timestamp'], d['Date'], d['Days_Past'], d['Days_Since_2nd_Death']
        d_all_date_data[date][lk_id] = d
del f, d, l, count

# check if last date has as many values as the 2nd last, of not drop it
dates = sorted(d_all_date_data.keys())
if len(d_all_date_data[dates[-1]]) != len(d_all_date_data[dates[-2]]):
    print("WARNING: last date is incomplete, so removing it")
    del d_all_date_data[dates[-1]]
del dates


# property_to_plot = 'Deaths_Last_Week_Per_Million'
l_subprocesses = []
d_latest_svg_file = {}  # store the last generated file per property
# for property_to_plot in ('Cases_Per_Million',):
for property_to_plot in ('Cases_Last_Week_Per_100000', 'Cases_Per_Million', 'DIVI_Intensivstationen_Betten_belegt_Prozent', 'DIVI_Intensivstationen_Covid_Prozent'):
    print(f"=== start {property_to_plot}")

    # # fmpeg -i animated.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4
    # command = ['ffmpeg', '-y', '-i', f'maps/de-districts-{property_to_plot}.gif', '-movflags', 'faststart', '-pix_fmt', 'yuv420p', '-vf',
    #            'scale=trunc(iw/2)*2:trunc(ih/2)*2', f'maps/de-districts-{property_to_plot}.mp4']
    # process = subprocess.Popen(command,
    #                            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    #                            universal_newlines=True)
    # # wait_for_finish
    # stdout, stderr = process.communicate()
    # if stdout != '':
    #     print(f'Out: {stdout}')
    # if stderr != '':
    #     print(f'ERROR: {stderr}')

    if property_to_plot == 'Cases_Last_Week_Per_100000':
        meta = {"colour": d_color_scales['blue']}
    elif property_to_plot == 'Cases_Per_Million':
        meta = {"colour": d_color_scales['red']}
    elif property_to_plot == 'DIVI_Intensivstationen_Covid_Prozent':
        meta = {"colour": d_color_scales['purple']}
    elif property_to_plot == 'DIVI_Intensivstationen_Betten_belegt_Prozent':
        meta = {"colour": d_color_scales['green']}
    else:
        assert 1 == 2, f"Error: color for {property_to_plot} is undefined"

    # values = []
    # # collect all values for autoscaling
    # # TODO filter here on selected month as well?
    # for date_str, l_districts in d_all_date_data.items():
    #     for lk_id, d in l_districts.items():
    #         if property_to_plot in d and d[property_to_plot] != None and d[property_to_plot] > 0:
    #             values.append(d[property_to_plot])
    # del d, l_districts, lk_id

    # # generate color scale range
    # threshold = [0, 0, 0, 0, 0, 0, 0]
    # print(f"{property_to_plot} min={min(values)} max={max(values)}")
    # V1 taken from template
    # q = statistics.quantiles(values, n=100, method="inclusive")
    # step = math.sqrt(statistics.mean(values) - q[0]) / 3
    # for i in range(1, 7):
    #     threshold[i] = math.pow(i * step, 2) + q[0]
    # del q, step, i

    # V2
    # threshold = statistics.quantiles(values, n=7+1, method="exclusive")

    # V3: linear distribution: very simple, but nice for % values
    # data_min = min(values)
    # data_max = max(values)
    # span = data_max-data_min
    # if property_to_plot == 'Cases_Per_Million':
    #     step = span ** (1.0/8)
    #     for i in range(7):
    #         threshold[i] = data_min + step**(1+i)
    #     # rounding of thresholds
    #     for i in range(7):
    #         if threshold[i] > 1000000:
    #             threshold[i] = int(round(threshold[i], -5))
    #         elif threshold[i] > 100000:
    #             threshold[i] = int(round(threshold[i], -4))
    #         elif threshold[i] > 10000:
    #             threshold[i] = int(round(threshold[i], -3))
    #         elif threshold[i] > 1000:
    #             threshold[i] = int(round(threshold[i], -2))
    #         elif threshold[i] > 100:
    #             threshold[i] = int(round(threshold[i], -1))
    #         elif threshold[i] > 10:
    #             threshold[i] = int(round(threshold[i], 0))
    #         elif threshold[i] > 1:
    #             threshold[i] = int(round(threshold[i], 1))

    # if property_to_plot in ('DIVI_Intensivstationen_Covid_Prozent', 'DIVI_Intensivstationen_Betten_belegt_Prozent'):
    #     step = span / 8
    #     for i in range(7):
    #         threshold[i] = data_min+(1+i)*step
    # # V4: exponential distribution: step to the power of i
    # else:
    #     # if property_to_plot in ('Cases_Last_Week_Per_100000', 'Cases_Per_Million'):
    #     step = span ** (1.0/8)
    #     for i in range(7):
    #         threshold[i] = data_min + step**(1+i)

    # manual setting of color scale
    if property_to_plot == 'Cases_Per_Million':
        threshold = [1, 10, 100, 1000, 10000, 50000, 100000]
    elif property_to_plot == 'Cases_Last_Week_Per_100000':
        threshold = [1, 5, 10, 25, 50, 100, 200]
    elif property_to_plot == 'DIVI_Intensivstationen_Covid_Prozent':
        threshold = [1, 10, 20, 30, 40, 50, 75]
    elif property_to_plot == 'DIVI_Intensivstationen_Betten_belegt_Prozent':
        threshold = [30, 40, 50, 60, 70, 80, 90]

    # read template and generate image per day
    with open('maps/template_de-districts.svg', mode="r", newline="", encoding="utf-8") as file_in:
        # plot loop for each date
        # date_str = '2020-04-24'
        # l_districts = d_all_date_data[date_str]
        print(f"generating SVGs")
        for date_str, l_districts in d_all_date_data.items():
            # skip date if for this month I already have a month .gif
            thisMonth = date_str[0:7]
            if os.path.isfile(f'maps/out/de-districts/{property_to_plot}-{thisMonth}.gif'):
                continue

            file_in.seek(0, 0)  # reset file pointer
            main = {}
            at_least_one_value_found = False
            for lk_id, d in l_districts.items():
                area = lk_id
                if property_to_plot in d and d[property_to_plot] != None:
                    pcapita = d[property_to_plot]
                    at_least_one_value_found = True
                else:
                    pcapita = -1
                main[area] = {'pcapita': pcapita}

            # do not create an svg if not areas with data for property_to_plot are available
            if not at_least_one_value_found:
                continue

            outfile = f'maps/out/de-districts/{property_to_plot}-{date_str}.svg'
            # overwritting per date, until it holds the latest file
            d_latest_svg_file[property_to_plot] = outfile

            # skip svg generation if I have not cleaned up, for faster gif generation debugging
            if os.path.isfile(outfile):
                continue

            with open(outfile, mode="w", newline="", encoding="utf-8") as file_out:
                # decide on the digits for the legend
                if property_to_plot == 'DIVI_Intensivstationen_Covid_Prozent':
                    num = "{:.0f}%"
                elif property_to_plot == 'DIVI_Intensivstationen_Betten_belegt_Prozent':
                    num = "{:.0f}%"
                # elif threshold[7-1] >= 10000:
                #     num = "{:.0f}"
                # elif threshold[1] >= 10:
                #     num = "{:.0f}"
                else:
                    num = "{:.0f}"

                for row in file_in:
                    written = False
                    # 1. check if the row contains any of the known area codes (lk_id)
                    for area in main:
                        if row.find('id="{}"'.format(area)) > -1:
                            # paint white if we have no value
                            if main[area]["pcapita"] == -1:
                                file_out.write(row.replace('id="{}"'.format(
                                    area), 'style="fill:{}"'.format("#ffffff")))
                            # else paint it in the correct color
                            else:
                                i = 0
                                while i <= 7-1:
                                    if main[area]["pcapita"] > threshold[i]:
                                        i += 1
                                    else:
                                        break
                                file_out.write(row.replace('id="{}"'.format(
                                    area), 'style="fill:{}"'.format(meta["colour"][i])))
                            written = True
                            break
                    if written == False:
                        # 2. check if row contains Date placeholder
                        if row.find('>!!!Date!!!') > -1:
                            file_out.write(row.replace(
                                '!!!Date!!!', date_str))
                        # 3. check if row contains Label placeholder
                        elif row.find('>!!!Level') > -1:
                            for i in range(7+1):
                                if row.find('!!!Level{}'.format(i)) > -1:
                                    if i == 0:
                                        file_out.write(row.replace('!!!Level{}'.format(
                                            i), "≤ " + num.format(threshold[i]).replace("_", "&#8201;")))
                                    else:
                                        file_out.write(row.replace('!!!Level{}'.format(
                                            i), "> " + num.format(threshold[i-1]).replace("_", "&#8201;")))
                        # 4. check if row contains legend color box
                        elif row.find('<path fill="#') > -1:
                            s = row
                            for i in range(7+1):
                                s = s.replace(
                                    d_color_scales["template"][i], meta["colour"][i])
                            file_out.write(s)
                        # 5. check if row contains Title
                        elif row.find('!!!TITLE!!!') > -1:
                            if property_to_plot == 'Cases_Last_Week_Per_100000':
                                file_out.write(row.replace(
                                    '!!!TITLE!!!', 'Neu-Infizierte 7 Tage pro 100000 EW'))
                            elif property_to_plot == 'Cases_Per_Million':
                                file_out.write(row.replace(
                                    '!!!TITLE!!!', 'Infizierte pro Millionen EW.'))
                            elif property_to_plot == 'DIVI_Intensivstationen_Covid_Prozent':
                                file_out.write(row.replace(
                                    '!!!TITLE!!!', 'Intensivstationen: COVID-19 Patienten'))
                            elif property_to_plot == 'DIVI_Intensivstationen_Betten_belegt_Prozent':
                                file_out.write(row.replace(
                                    '!!!TITLE!!!', 'Intensivstationen: Betten belegt'))
                            else:
                                file_out.write(row.replace(
                                    '!!!TITLE!!!', property_to_plot.replace("_", " ")))
                        else:
                            file_out.write(row)
        #     break
        # break
    l_subprocesses = []
    print(f"svg -> month-gif")
    for month in l_month:
        if f"{property_to_plot}-{month}" in ['DIVI_Intensivstationen_Betten_belegt_Prozent-2020-03', 'DIVI_Intensivstationen_Covid_Prozent-2020-03']:
            # we do not have DIVI data for 03/2020
            continue
        l = glob.glob(f'maps/out/de-districts/{property_to_plot}-{month}*.svg')
        if len(l) == 0:
            continue
        # convert -size 480x maps/out/de-districts/Cases_Last_Week_Per_100000-2020-03*.svg -resize 480x -coalesce -fuzz 2% +dither -layers Optimize maps/out/de-districts/Cases_Last_Week_Per_100000-2020-03.gif
        l_imagemagick_parameters = [
            '-size', '480x', f'maps/out/de-districts/{property_to_plot}-{month}*.svg', '-resize', '480x', '-coalesce', '-fuzz', '2%', '+dither', '-layers', 'Optimize', f'maps/out/de-districts/{property_to_plot}-{month}.gif']

        # parallel processing ran into mem limits, fixed by editing the /etc/ImageMagick-6/policy.xml file
        process = run_imagemagick_convert(
            l_imagemagick_parameters, wait_for_finish=False)
        l_subprocesses.append(process)

        # single processing
        # process = run_imagemagick_convert(
        #     l_imagemagick_parameters, wait_for_finish=True)

    # wait for subprocesses to finish
    for process in l_subprocesses:
        stdout, stderr = process.communicate()
        if stdout != '':
            print(f'Out: {stdout}')
        if stderr != '':
            print(f'ERROR: {stderr}')

    # generate a static image for the latest date
    l_imagemagick_parameters = [
        f'{d_latest_svg_file[property_to_plot]}', '-resize', '480x', '-coalesce', '-fuzz', '2%', '+dither', '-layers', 'Optimize', f'maps/de-districts-{property_to_plot}-latest.gif'
    ]
    run_imagemagick_convert(l_imagemagick_parameters)

    # cleanup the svg to reduce space on file system
    for f in glob.glob('maps/out/de-districts/*.svg'):
        os.remove(f)
        pass

    outfile = f'maps/de-districts-{property_to_plot}.gif'

    print(f"join monthly gifs")
    l_imagemagick_parameters = [
        f'maps/out/de-districts/{property_to_plot}-*.gif', '-coalesce', '-fuzz', '2%', '+dither', '-layers', 'Optimize', outfile
    ]
    run_imagemagick_convert(l_imagemagick_parameters)

    # delete gif of last month, as this is not be complete and thus shall not be commited
    l = sorted(glob.glob(f'maps/out/de-districts/{property_to_plot}-*.gif'))
    os.remove(l.pop())

    # set delay of 0.25s for all frames
    l_imagemagick_parameters = [
        outfile, '-delay', '250x1000', outfile
    ]
    run_imagemagick_convert(l_imagemagick_parameters)

    # clone last frame and set longer delay time of 2s
    l_imagemagick_parameters = [
        outfile, '(', '-clone', '-1', '-set', 'delay', '2000x1000', ')', outfile
    ]
    run_imagemagick_convert(l_imagemagick_parameters)

    print(f'converting {property_to_plot}.gif -> .mp4')
    # from https://unix.stackexchange.com/questions/40638/how-to-do-i-convert-an-animated-gif-to-an-mp4-or-mv4-on-the-command-line

    # fmpeg -i animated.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4
    command = ['ffmpeg', '-y', '-loglevel', 'warning', '-i', outfile, '-movflags', 'faststart', '-pix_fmt', 'yuv420p', '-vf',
               'scale=trunc(iw/2)*2:trunc(ih/2)*2', f'maps/de-districts-{property_to_plot}.mp4']
    process = subprocess.Popen(command,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    # wait_for_finish
    stdout, stderr = process.communicate()
    if stdout != '':
        print(f'Out: {stdout}')
    if stderr != '':
        print(f'ERROR: {stderr}')

    # # create copies with shorter and longer delay
    # # this does not work: all have the same speed :-(
    # delay_variants = (100, 250, 500)
    # for delay in delay_variants:
    #     outfileDelay = f'maps/de-districts-{property_to_plot}-{delay}.gif'
    #     run_imagemagick_convert([
    #         outfile, '-delay', f'{delay}x1000', outfileDelay
    #     ])
    #     run_imagemagick_convert([
    #         outfileDelay, '(', '-clone', '-1', '-set', 'delay', '2000x1000', ')', outfileDelay
    #     ])


print("End of script reached")
