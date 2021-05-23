#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Source: https://www.intensivregister.de/#/intensivregister
primary data store is in data/de-divi/de-divi-V2.json. from there the tsv files are re-created at every run
Deprecated, since DIVI now provides data in CSV format. See fetch-de-divi-V3.py
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import sys
import csv
from datetime import datetime
import re

# my helper modules
import helper

filename = 'data/de-divi/de-divi-V2'

datestr = datetime.now().strftime("%Y-%m-%d")

d_data_all = helper.read_json_file(filename+'.json')

del d_data_all['Deutschland']  # this is re-calculated at each run


# check if date is already in data set
if d_data_all['Bayern'][-1]['Date'] == datestr:
    print(
        f"WARNING: Date: {datestr} already in data file: {filename+'.json'}  -->  SKIPPING")
    sys.exit()


def extractAreaTagTitleData(cont: str) -> list:
    # Example
    # <area shape="RECT" title="Thüringen
    # Anzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung: 63
    # Anteil COVID-19 Patienten/innen pro Intensivbett: 6,0%" coords="380,430,423,447">
    myPattern = 'title="([^"]+)"'
    myRegExp = re.compile(myPattern)
    myMatches = myRegExp.findall(cont)
    del cont, myPattern, myRegExp
    # remove duplicates
    d = {}
    for match in myMatches:
        d[match] = 1
    myMatches = list(sorted(d.keys()))
    del d, match
    return myMatches


def extractBundeslandKeyValueData(s1: str) -> list:
    # 'Baden-Württemberg\rAnzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung: 456\rAnteil COVID-19 Patienten/innen pro Intensivbett: 11,9%'
    l1 = s1.split("\r")
    if len(l1) == 1:
        l1 = s1.split("\n")
    bundesland = l1.pop(0)
    global d_data_all
    if bundesland not in d_data_all:
        d_data_all[bundesland] = []
    d = {}
    for s2 in l1:
        l2 = s2.split(': ')
        key = l2[0]
        value = l2[1]

        # remove percent sign from end
        if value[-1] == '%':
            value = value[0: -1]

        # remove 1000 separator .
        pattern = re.compile(r'(?<=\d)\.(?=\d)')
        value = pattern.sub('', value)

        # fix decimal separator 0,5 -> 0.5
        pattern = re.compile(r'(?<=\d),(?=\d)')
        value = pattern.sub('.', value)
        test = float('11.9')
        # convert value to numeric format
        if value.isdigit():
            value = int(value)
        else:
            try:
                value = float(value)
            except ValueError:
                1

        if isinstance(value, str):
            print("ERROR: values is string")

        d[key] = value
    return (bundesland, d)


def fetch_betten():
    # fetch data per bundesland, having many duplicates
    cont = helper.read_url_or_cachefile(
        url="https://diviexchange.z6.web.core.windows.net/gmap_betten.htm", cachefile='cache/de-divi/de-divi-betten.html', cache_max_age=3600, verbose=True)
    myMatches = extractAreaTagTitleData(cont)
    # example
    # 'Schleswig-Holstein\rFreie Betten: 507\rBelegte Betten: 536\rAnteil freier Betten an Gesamtzahl: 48.6%'

    global d_data_all

    # extract data
    for s1 in myMatches:
        bundesland, d1 = extractBundeslandKeyValueData(s1)

        d2 = {}
        d2['Date'] = datestr
        d2['Int Betten belegt'] = d1['Belegte Betten']
        d2['Int Betten gesamt'] = d1['Freie Betten'] + d1['Belegte Betten']
        d_data_all[bundesland].append(d2)
        1
    del myMatches, s1, bundesland, d1, d2


def fetch_covid():
    # fetch data per bundesland, having many duplicates
    cont = helper.read_url_or_cachefile(
        url="https://diviexchange.z6.web.core.windows.net/gmap_covid.htm", cachefile='cache/de-divi/de-divi-covid.html', cache_max_age=3600, verbose=True)
    myMatches = extractAreaTagTitleData(cont)
    # 'Baden-Württemberg\rAnzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung: 456\rAnteil COVID-19 Patienten/innen pro Intensivbett: 11,9%'

    global d_data_all

    # extract data
    for s1 in myMatches:
        bundesland, d1 = extractBundeslandKeyValueData(s1)

        d2 = d_data_all[bundesland][-1]

        assert d2['Date'] == datestr
        # d2['Prozent COVID-19 pro Intensivbett'] = d1['Anteil COVID-19 Patienten/innen pro Intensivbett']
        # = COVID-19 Patienten / Betten gesamt
        d2['Int COVID-19 Patienten'] = d1['Anzahl COVID-19 Patienten/innen in intensivmedizinischer Behandlung']
        d_data_all[bundesland][-1] = d2
        1
    del myMatches, s1, bundesland, d1, d2


def calc_de_sum():
    global d_data_all
    d_de_sum = {}
    for state, l_time_series in d_data_all.items():
        for d in l_time_series:
            if not d['Date'] in d_de_sum:
                d_de_sum[d['Date']] = {}
            for key, value in d.items():
                if key == 'Date':
                    continue
                if value == None:
                    continue
                if not key in d_de_sum[d['Date']]:
                    d_de_sum[d['Date']][key] = 0
                d_de_sum[d['Date']][key] += value
    # flatten the dict
    l = []
    for date, d in d_de_sum.items():
        d2 = d
        d2['Date'] = date
        l.append(d2)

    d_data_all['Deutschland'] = l


def export_data():
    global d_data_all
    helper.write_json(filename+'.json',
                      d_data_all, sort_keys=False, indent=1)


def export_time_series():
    # Idea: Betten pro Einwohner
    for state, l_time_series in d_data_all.items():
        if state != 'Deutschland':
            code = d_states_ref_map_name_code[state]
        else:
            code = 'DE'
        with open(f'data/de-divi/de-divi-{code}.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
            csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
                'Date', 'Int Betten gesamt', 'Int Betten belegt', 'Prozent Int Betten belegt', 'Int COVID-19 Patienten', 'Prozent Int COVID-19 Patienten'
            ])
            csvwriter.writeheader()
            for d in l_time_series:
                d2 = d
                gesamt = d2['Int Betten gesamt']
                belegt = d2['Int Betten belegt']
                if 'Int COVID-19 Patienten' in d2 and d2['Int COVID-19 Patienten'] != None:
                    covid = d2['Int COVID-19 Patienten']
                    d2['Prozent Int COVID-19 Patienten'] = round(
                        100*covid/gesamt, 1)
                else:
                    d2['Int COVID-19 Patienten'] = None
                    d2['Prozent Int COVID-19 Patienten'] = None

                d2['Prozent Int Betten belegt'] = round(100*belegt/gesamt, 1)
                csvwriter.writerow(d2)


d_states_ref = helper.read_ref_data_de_states()
d_states_ref_map_name_code = {}
for code, d in d_states_ref.items():
    d_states_ref_map_name_code[d['State']] = code


fetch_betten()
fetch_covid()
calc_de_sum()
export_time_series()
export_data()
