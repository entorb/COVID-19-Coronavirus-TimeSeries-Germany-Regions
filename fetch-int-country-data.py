#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data provided by https://github.com/pomber/covid19
Data is enriched by calculated values and exported
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# TODO: modify cache to plot old data via
# ,\n\s+\{[\n]\s+"date": "2020-4-1",[^\]]*\]
# -> ]

# Built-in/Generic Imports
import os
import time
import urllib.request
import csv

# further modules
# process bar
from tqdm import tqdm

# my helper modules
import helper

file_cache = 'cache/download-countries-timeseries.json'


def download_new_data():
    """
    downloads the data from the source to the cache dir
    """
    url = "https://pomber.github.io/covid19/timeseries.json"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(file_cache, mode='wb') as f:
        f.write(datatowrite)


def read_json_data() -> dict:
    """
    reads downloaded cached json file contents
    renames some country names according to ref database
    calls prepare_time_series
    adds _Per_Million fields
    NO LONGER exports as json file
    returns as a dict
    """
    d_json_downloaded = helper.read_json_file(file_cache)
    del d_json_downloaded['Diamond Princess']
    del d_json_downloaded['MS Zaandam']
    # del d_json_downloaded['Diamond Princess']

    # rename some countries
    d_countries_to_rename = {}
    d_countries_to_rename['US'] = 'United States'
    d_countries_to_rename['Korea, South'] = 'South Korea'
    d_countries_to_rename['Taiwan*'] = 'Taiwan'
    d_countries_to_rename['Burma'] = 'Myanmar'
    d_countries_to_rename['Cote d\'Ivoire'] = 'Ivory Coast'
    d_countries_to_rename['West Bank and Gaza'] = 'Palestinian Territory'
    d_countries_to_rename['Timor-Leste'] = 'Timor Leste'
    d_countries_to_rename['Holy See'] = 'Vatican'
    for country_name_old, country_name_new in d_countries_to_rename.items():
        d_json_downloaded[country_name_new] = d_json_downloaded[country_name_old]
        del d_json_downloaded[country_name_old]

    # remove the not needed ones from the ref list
    l_to_del_from_ref = []
    for country in d_countries_ref.keys():
        if country not in d_json_downloaded.keys():
            l_to_del_from_ref.append(country)
    for country in l_to_del_from_ref:
        del d_countries_ref[country]

    d_countries = {}
    # re-format date using my date_format(y,m,d) function
    for country, country_data in d_json_downloaded.items():
        if country == 'Summer Olympics 2020':
            continue
        assert country in d_countries_ref, "E: Country missing in ref list d_countries_ref"
        l_time_series = []

        pop = read_population(country)
        if pop != None:
            pop_in_million = pop / 1000000
        else:
            pop_in_million = None

        for entry in country_data:
            d = {}
            # entry in country_data:
            s = entry['date']
            l = s.split("-")
            d['Date'] = helper.date_format(int(l[0]), int(l[1]), int(l[2]))
            d['Cases'] = int(entry['confirmed'])
            d['Deaths'] = int(entry['deaths'])
            l_time_series.append(d)

        l_time_series = helper.prepare_time_series(l_time_series)

        for i in range(len(l_time_series)):
            d = l_time_series[i]

            # _Per_Million
            d = helper.add_per_million(d, pop_in_million)
            l_time_series[i] = d

        d_countries[country] = l_time_series

    return d_countries


def read_ref_selected_countries() -> dict:
    """
    reads data for selected countries from tsv file and returns it as dict
    the population value of this field is no longer used, since I switched to using d_ref_country_database instead
    """
    d_selected_countries = {}
    with open('data/ref_selected_countries.tsv', mode='r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, dialect='excel', delimiter="\t")
        for row in csv_reader:
            # skip commented lines
            if row["Country"][0] == '#':
                continue
            d = {}
            for key in ('Code',):
                d[key] = row[key]
            for key in ('Population',):
                d[key] = int(row[key])
            for key in ('Pop_Density', 'GDP_mon_capita'):
                d[key] = float(row[key])
            d_selected_countries[row["Country"]] = d
    return d_selected_countries


def extract_latest_date_data():
    """
    for all countries in json: extract latest entry
    write to data/int/countries-latest-all.tsv and data/int/countries-latest-all.json
    """

    d_countries_latest = helper.extract_latest_data(
        d_countries_ref, d_countries_timeseries)

    l_for_export = []
    with open('data/int/countries-latest-all.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
        csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
            'Country', 'Population', 'Date', 'Cases',
            'Deaths', 'Cases_Per_Million', 'Deaths_Per_Million', 'Cases_Last_Week_Per_Million',
            'Deaths_Last_Week_Per_Million', 'Continent', 'Code', 'DoublingTime_Cases_Last_Week_Per_100000'
        ])
        # 'Cases_Last_Week',
        csvwriter.writeheader()

        for country in sorted(d_countries_latest.keys(), key=str.casefold):
            d2 = d_countries_latest[country]
            d2['Country'] = country

            csvwriter.writerow(d2)
            l_for_export.append(d2)

    # JSON export
    helper.write_json(
        filename='data/int/countries-latest-all.json', d=l_for_export, sort_keys=True)

    # for selected countries write to separate file, for Gnuplot plotting
    with open('data/int/countries-latest-selected.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
        csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
            'Country', 'Date',
            'Population',
            'Cases', 'Deaths',
            'Cases_Per_Million', 'Deaths_Per_Million'
        ])
        csvwriter.writeheader()
        for country in sorted(d_selected_countries.keys(), key=str.casefold):
            l_time_series = d_countries_timeseries[country]
            d = l_time_series[-1]  # last entry for this country
            d2 = d
            d2["Country"] = country
            d2['Population'] = d_selected_countries[country]['Population']
            csvwriter.writerow(d2)


def check_for_further_interesting_countries():
    """
    checks if in the json data are countries with many deaths that are missing in my selection for closer analysis
    """
    global d_countries_timeseries
    global d_selected_countries
    min_death = 10
    min_confirmed = 1000
    min_death_per_million = 100
    print("further interesting countries")
    print("Country\tConfirmed\tDeaths\tDeathsPerMillion")
#    list_of_countries = sorted(d_countries_timeseries.keys(), key=str.casefold)
    for country in sorted(d_countries_timeseries.keys(), key=str.casefold):
        if country in d_selected_countries.keys():
            continue
        l_country_data = d_countries_timeseries[country]
        entry = l_country_data[-1]  # latest entry
        # if entry['Cases'] >= min_confirmed or entry['Deaths'] >= min_death:
        if entry['Deaths_Per_Million'] and entry['Deaths_Per_Million'] >= min_death_per_million:
            print(
                f"{country}\t{entry['Cases']}\t{entry['Deaths']}\t{int(entry['Deaths_Per_Million'])}")


def fit_doubling_time():
    """
    fit time series for doubling time
    """
    global d_countries_timeseries
    global d_selected_countries
    # TODO!
    # l = []
    # l.append('South Korea')
    # for country in l:
    for country in tqdm(d_countries_timeseries.keys()):
        # for country in d_selected_countries.keys():
        # print(country)
        # country_code = d_selected_countries[country]['Code']
        l_country_data = d_countries_timeseries[country]
        # pop_in_Mill = d_selected_countries[country]['Population'] / 1000000

        # for fits of doubling time
        data_t = []
        data_cases = []
        data_deaths = []

        for i in range(len(l_country_data)):
            entry = l_country_data[i]

            # for fits of doubling time
            data_t.append(entry['Days_Past'])
            data_cases.append(entry['Cases'])
            data_deaths.append(entry['Deaths'])

            l_country_data[i] = entry

        # fit the doubling time each day
        # data = list(zip(data_t, data_cases))
        # fit_series_res_cases = helper.series_of_fits(
        #     data, fit_range=7, max_days_past=28)
        data = list(zip(data_t, data_deaths))
        fit_series_res_deaths = helper.series_of_fits(
            data, fit_range=7, max_days_past=60)

        for i in range(len(l_country_data)):
            entry = l_country_data[i]
            entry['Cases_Doubling_Time'] = ""
            entry['Deaths_Doubling_Time'] = ""
            this_DaysPast = entry['Days_Past']
            # if this_DaysPast in fit_series_res_cases:
            #     entry['Cases_Doubling_Time'] = fit_series_res_cases[this_DaysPast]
            if this_DaysPast in fit_series_res_deaths:
                entry['Deaths_Doubling_Time'] = fit_series_res_deaths[this_DaysPast]
            l_country_data[i] = entry

        d_countries_timeseries[country] = l_country_data


def export_time_series_all_countries():
    for country in d_countries_timeseries.keys():
        code = read_country_code(country)
        if not code:
            continue
        l_time_series = d_countries_timeseries[country]
        l_time_series = helper.timeseries_export_drop_irrelevant_columns(
            l_time_series)

        helper.write_json(
            f'data/int/country-{code}.json', l_time_series)

        with open(f'data/int/country-{code}.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
            csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore', fieldnames=[
                'Date',
                'Cases', 'Deaths',
                'Cases_New', 'Deaths_New',
                'Cases_Last_Week', 'Deaths_Last_Week',
                'Cases_Per_Million', 'Deaths_Per_Million',
                'Cases_New_Per_Million', 'Deaths_New_Per_Million',
                'Cases_Last_Week_Per_Million', 'Deaths_Last_Week_Per_Million',
                'Cases_Doubling_Time', 'Deaths_Doubling_Time',
                'Days_Since_2nd_Death',
            ])
            csvwriter.writeheader()

            for d in l_time_series:
                d2 = d
                csvwriter.writerow(d2)


def read_population(country_name: str, verbose: bool = False) -> int:
    pop = d_countries_ref[country_name]["Population"]
    if verbose and pop == None:
        print(f"No Population found for {country_name}")
    return pop


def read_continent(country_name: str) -> str:
    continent = d_countries_ref[country_name]["Continent"]
    return continent


def read_country_code(country_name: str) -> str:
    code = None
    if country_name in d_countries_ref:
        code = d_countries_ref[country_name]["Code"]
    return code


def read_ref_data_countries() -> dict:
    d_countries_ref = {}
    d_ref_country_database = helper.read_json_file(
        'data/ref_country_database.json')
    for key, d in d_ref_country_database.items():
        d2 = {}
        code = d["ISO"]
        name = key
        if name == 'Republic of the Congo':
            name = 'Congo (Brazzaville)'
        elif name == 'Democratic Republic of the Congo':
            name = 'Congo (Kinshasa)'
        pop = d['Population']
        if pop != None:
            pop = int(pop)
        if pop == 0:
            pop = None
        continent = d['Continent']
        # move Turkey from Asia to Europe
        if name == 'Turkey':
            continent = 'EU'

        if continent != None:
            if continent == 'AF':
                continent = 'Africa'
            elif continent == 'AN':
                continent = 'Antarctica'
            elif continent == 'AS':
                continent = 'Asia'
            elif continent == 'EU':
                continent = 'Europe'
            elif continent == 'NA':
                continent = 'North America'
            elif continent == 'SA':
                continent = 'South America'
            elif continent == 'OC':
                continent = 'Oceania'
            else:
                assert 1 == 2, f"E: continent missing for {name}"

        d2["Code"] = code
        d2['Continent'] = continent
        d2["Population"] = pop
        d_countries_ref[name] = d2

    return d_countries_ref


d_countries_ref = read_ref_data_countries()


# d_ref_country_database = helper.read_json_file(
#     'data/ref_country_database.json')


d_selected_countries = read_ref_selected_countries()

if not helper.check_cache_file_available_and_recent(fname=file_cache, max_age=1800, verbose=True):
    download_new_data()

d_countries_timeseries = read_json_data()
check_for_further_interesting_countries()
extract_latest_date_data()
export_time_series_all_countries()
print(
    f"int: countries: latest date in DE set: {d_countries_timeseries['Germany'][-1]['Date']}")
