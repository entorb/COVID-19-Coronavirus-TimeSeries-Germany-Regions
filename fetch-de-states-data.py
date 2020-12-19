#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data provided by https://github.com/swildermann/COVID-19
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import os
import time
import csv
import urllib.request
# import json

# from matplotlib import pyplot as plt

# my helper modules
import helper

# TODO: persisting caching of doubling time fit results for reducing runtime

# args = helper.read_command_line_parameters()
download_file = 'cache/download-de-federalstates-timeseries.csv'


def download_new_data():
    url = "https://covid19publicdata.blob.core.windows.net/rki/covid19-germany-federalstates.csv"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(download_file, mode='wb') as f:
        f.write(datatowrite)


def read_csv_to_dict() -> dict:
    """
    read and convert the source csv file, containing: federalstate,infections,deaths,date,newinfections,newdeaths
    re-calc _New via helper.prepare_time_series
    add _Per_Million via helper.add_per_million_via_lookup
    """

    global d_ref_states
    # Preparations
    d_states_data = {'BW': [], 'BY': [], 'BE': [], 'BB': [], 'HB': [], 'HH': [], 'HE': [], 'MV': [
    ], 'NI': [], 'NW': [], 'RP': [], 'SL': [], 'SN': [], 'ST': [], 'SH': [], 'TH': []}
    # add German sum
    d_states_data['DE-total'] = []
    d_german_sums = {}  # date -> 'infections', 'deaths', 'new infections', 'new deaths'

    # data body
    with open(download_file, mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        for row in csv_reader:
            d = {}
            s = row['date']
            l = s.split("-")
            d['Date'] = helper.date_format(
                int(l[0]), int(l[1]), int(l[2]))
            d['Cases'] = int(row["infections"])
            d['Deaths'] = int(row["deaths"])

            if row["federalstate"] == 'Baden-Württemberg':
                d_states_data['BW'].append(d)
            elif row["federalstate"] == 'Bavaria':
                d_states_data['BY'].append(d)
            elif row["federalstate"] == 'Berlin':
                d_states_data['BE'].append(d)
            elif row["federalstate"] == 'Brandenburg':
                d_states_data['BB'].append(d)
            elif row["federalstate"] == 'Bremen':
                d_states_data['HB'].append(d)
            elif row["federalstate"] == 'Hamburg':
                d_states_data['HH'].append(d)
            elif row["federalstate"] == 'Hesse':
                d_states_data['HE'].append(d)
            elif row["federalstate"] == 'Lower Saxony':
                d_states_data['NI'].append(d)
            elif row["federalstate"] == 'North Rhine-Westphalia':
                d_states_data['NW'].append(d)
            elif row["federalstate"] == 'Mecklenburg-Western Pomerania':
                d_states_data['MV'].append(d)
            elif row["federalstate"] == 'Rhineland-Palatinate':
                d_states_data['RP'].append(d)
            elif row["federalstate"] == 'Saarland':
                d_states_data['SL'].append(d)
            elif row["federalstate"] == 'Saxony':
                d_states_data['SN'].append(d)
            elif row["federalstate"] == 'Saxony-Anhalt':
                d_states_data['ST'].append(d)
            elif row["federalstate"] == 'Schleswig-Holstein':
                d_states_data['SH'].append(d)
            elif row["federalstate"] == 'Thuringia':
                d_states_data['TH'].append(d)
            else:
                assert 1 == 2, f"ERROR: unknown state: {row['federalstate']}"

            # add to German sum
            if d['Date'] not in d_german_sums:
                d2 = {}
                d2['Cases'] = d['Cases']
                d2['Deaths'] = d['Deaths']
            else:
                d2 = d_german_sums[d['Date']]
                d2['Cases'] += d['Cases']
                d2['Deaths'] += d['Deaths']
            d_german_sums[d['Date']] = d2
            del d2

    # German sum -> same dict
    for datum in d_german_sums.keys():
        d = d_german_sums[datum]
        d['Date'] = datum  # add date field
        d_states_data['DE-total'].append(d)
    del d_german_sums, d

    # check if DE-total of today and yesterday are equal, if so: remove last date
    if d_states_data['DE-total'][-1]['Cases'] == d_states_data['DE-total'][-2]['Cases']:
        print("WARNING: DE cases sum is unchanged")
        for code in d_states_data:
            d_states_data[code].pop()
    print(f"DE-States Last Date: {d_states_data['DE-total'][-1]['Date']}")

    for code in d_states_data.keys():
        l_time_series = d_states_data[code]

        # add days past, _New, _Last_Week, etc
        l_time_series = helper.prepare_time_series(l_time_series)

        for i in range(len(l_time_series)):
            d = l_time_series[i]
            # add per Million rows
            d = helper.add_per_million_via_lookup(d, d_ref_states, code)

        d_states_data[code] = l_time_series

    return d_states_data


def fit_doubling_or_halftime() -> dict:
    for code, l_time_series in d_states_data.items():
        print(f'fitting doubling time for {code}')

        # if code != 'DE-total':  # TODO
        #     continue

        # # fit cases data V2: based on CasesNew instead of Cases and interpreting T<0 -> halftime
        dataCases = []
        for i in range(1, len(l_time_series)):  # TODO
            # for i in range(10, 60):
            # x= day , y = cases
            dataCases.append(
                (
                    l_time_series[i]['Days_Past'],
                    l_time_series[i]['Cases_Last_Week_Per_100000']
                    # l_time_series[i]['Cases_New_Per_Million']
                    # this set to very noisy results, so using Last_week data instead
                )
            )

        fit_series_res = helper.series_of_fits(
            dataCases, fit_range=14, max_days_past=365, mode='exp')
        for i in range(0, len(l_time_series)):
            this_Doubling_Time = ""
            this_days_past = l_time_series[i]['Days_Past']
            if this_days_past in fit_series_res:
                this_Doubling_Time = fit_series_res[this_days_past]
            l_time_series[i]['Cases_Last_Week_Doubling_Time'] = this_Doubling_Time
            # debugging
            # print(l_time_series[i]['Days_Past'], this_Doubling_Time)

        d_states_data[code] = l_time_series
    return d_states_data


# this is based on a copy from fetch-de-districts.py
def join_with_divi_data() -> dict:
    d_divi_data = helper.read_json_file('cache/de-divi/de-divi-V3-states.json')
    for bl_code, l_time_series in d_states_data.items():
        assert bl_code in d_divi_data, f"Error: BL {bl_code} missing in DIVI data"
        if bl_code[0:2] != '11':
            l_divi_time_series = d_divi_data[bl_code]
        d_divi_time_series = {}
        for d in l_divi_time_series:
            d_divi_time_series[d['Date']] = d

        for d in l_time_series:
            if d['Date'] not in d_divi_time_series:
                continue
            d['DIVI_Intensivstationen_Covid_Prozent'] = d_divi_time_series[d['Date']
                                                                           ]['faelle_covid_aktuell_proz']
            d['DIVI_Intensivstationen_Betten_belegt_Prozent'] = d_divi_time_series[d['Date']
                                                                                   ]['betten_belegt_proz']

        d_states_data[bl_code] = l_time_series
    return d_states_data


def export_data(d_states_data: dict):
    # export JSON and CSV
    for code in d_states_data.keys():
        outfile = f'data/de-states/de-state-{code}.tsv'
        l_time_series = d_states_data[code]

        helper.write_json(
            f'data/de-states/de-state-{code}.json', l_time_series)

        with open(outfile, mode='w', encoding='utf-8', newline='\n') as fh:
            csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
                'Days_Past', 'Date',
                'Cases', 'Deaths',
                'Cases_New', 'Deaths_New',
                'Cases_Last_Week', 'Deaths_Last_Week',
                'Cases_Per_Million', 'Deaths_Per_Million',
                'Cases_New_Per_Million', 'Deaths_New_Per_Million',
                'Cases_Last_Week_Per_Million', 'Deaths_Last_Week_Per_Million',
                'Cases_Last_Week_Per_100000',
                #                'Cases_Doubling_Time', 'Deaths_Doubling_Time',
                'DIVI_Intensivstationen_Covid_Prozent', 'DIVI_Intensivstationen_Betten_belegt_Prozent',
                'Cases_Last_Week_Doubling_Time'
            ]
            )
            csvwriter.writeheader()
            for d in l_time_series:
                csvwriter.writerow(d)


def export_latest_data(d_ref_states, d_states_data: dict):
    d_states_latest = helper.extract_latest_data(d_ref_states, d_states_data)

    # # d_states_latest = dict(d_ref_states)
    # for code in d_states_latest.keys():
    #     assert code in d_states_data.keys()
    #     l_state = d_states_data[code]
    #     d_latest = l_state[-1]
    #     d_states_latest[code]['Date_Latest'] = d_latest['Date']
    #     for key in ('Cases', 'Deaths', 'Cases_New', 'Deaths_New', 'Cases_Per_Million', 'Deaths_Per_Million'):
    #         d_states_latest[code][key] = d_latest[key]
    with open('data/de-states/de-states-latest.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
        csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore',
                                   fieldnames=('State', 'Code', 'Population', 'Pop Density',
                                               'Date_Latest',
                                               'Cases', 'Deaths',
                                               'Cases_New', 'Deaths_New',
                                               'Cases_Per_Million',
                                               'Deaths_Per_Million', 'DoublingTime_Cases_Last_Week_Per_100000', 'Slope_Cases_Last_Week_Percent', 'Slope_Deaths_Last_Week_Percent')
                                   )
        csvwriter.writeheader()
        for code in sorted(d_states_latest.keys()):
            d = d_states_latest[code]
            d['Code'] = code
            if code == 'DE-total':  # DE as last row
                d_de = dict(d)
                continue
            csvwriter.writerow(
                d
            )
        del d, code
        # add # to uncomment the DE total sum last line
        d_de['State'] = '# Deutschland'
        csvwriter.writerow(d_de)
        del d_de

    helper.write_json(
        f'data/de-states/de-states-latest.json', d_states_latest)

    l_for_export = []
    for code in sorted(d_states_latest.keys(), key=str.casefold):
        d2 = d_states_latest[code]
        d2['Code'] = code
        l_for_export.append(d2)
    helper.write_json(
        filename='data/de-states/de-states-latest-list.json', d=l_for_export)


d_ref_states = helper.read_ref_data_de_states()


download_new_data()
d_states_data = read_csv_to_dict()

d_states_data = fit_doubling_or_halftime()

d_states_data = join_with_divi_data()

export_data(d_states_data)
export_latest_data(d_ref_states, d_states_data)

# 1
