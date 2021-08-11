#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 / coronavirus data of German regions (Bu8ndesländer) provided by
GUI: https://experience.arcgis.com/
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import csv
import json

# my helper modules
import helper


def fetch_bundesland_time_series(bl_id: str, readFromCache: bool = True) -> list:
    """
    for a given bl_id: fetches its time series and returns as list
    Fetches data from arcgis Covid19_RKI_Sums endpoint: Bundesland, Landkreis, etc.
    # API Explorer
    https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0
    Report of cases and deaths per Bundesland using sum
    https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=html&where=IdBundesland%3D%2702%27&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=true&orderByFields=Bundesland%2C+Meldedatum+asc&groupByFieldsForStatistics=Bundesland%2C+Meldedatum&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22SummeFall%22%2C%22outStatisticFieldName%22%3A%22SumSummeFall%22%7D%2C%0D%0A%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22SummeTodesfall%22%2C%22outStatisticFieldName%22%3A%22SumSummeTodesfall%22%7D%5D&having=&resultOffset=&resultRecordCount=&sqlFormat=none&token=

    via f=html can be experimented using a nice form
    readFromCache=True -> not calling the API, but returning cached data
    readFromCache=False -> calling the API, and writing cache to filesystem

    returns data as list, ordered by date
    """
    code = helper.BL_code_from_BL_ID(int(bl_id))
    file_cache = f"cache/de-states/state_timeseries-{code}.json"

    max_allowed_rows_to_fetch = 2000

    url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query" +\
        "?f=json" +\
        "&where=IdBundesland='" + str(bl_id) + "'" + \
        "&outFields=*" +\
        "&orderByFields=Bundesland%2C+Meldedatum+asc" +\
        "&groupByFieldsForStatistics=Bundesland%2C+Meldedatum" +\
        "&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22SummeFall%22%2C%22outStatisticFieldName%22%3A%22SumSummeFall%22%7D%2C%0D%0A%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22SummeTodesfall%22%2C%22outStatisticFieldName%22%3A%22SumSummeTodesfall%22%7D%5D" +\
        "&objectIds=" +\
        "&time=" +\
        "&resultType=none" +\
        "&returnIdsOnly=false" +\
        "&returnUniqueIdsOnly=false" +\
        "&returnCountOnly=false" +\
        "&returnDistinctValues=false" +\
        "&cacheHint=true" +\
        "&having=" +\
        "&resultOffset=" +\
        "&resultRecordCount=" +\
        "&sqlFormat=none" +\
        "&token="

    cont = helper.read_url_or_cachefile(
        url=url, cachefile=file_cache, request_type='get', cache_max_age=3600, verbose=False)
    json_cont = json.loads(cont)
    # flatten the json structure
    l2 = json_cont['features']
    l_time_series = [v['attributes'] for v in l2]
    assert len(l_time_series) < max_allowed_rows_to_fetch
    return l_time_series


def fetch_and_prepare_bl_time_series(bl_id: int) -> list:
    """
    calles fetch_landkreis_time_series
    convert and add fields of time series list
    returns list
    writes json and tsv to filesystem
    """
    l_time_series_fetched = fetch_bundesland_time_series(
        bl_id=bl_id, readFromCache=True)

    code = helper.BL_code_from_BL_ID(bl_id)

    l_time_series = []

    # entry = one data point
    for entry in l_time_series_fetched:
        d = {}
        # covert to int
        d['Cases'] = int(entry['SumSummeFall'])
        d['Deaths'] = int(entry['SumSummeTodesfall'])
        # Rename 'Meldedatum' (ms) -> Timestamp (s)
        d['Timestamp'] = int(entry['Meldedatum'] / 1000)

        # add Date
        d['Date'] = helper.convert_timestamp_to_date_str(
            d['Timestamp'])

        l_time_series.append(d)

    l_time_series = helper.prepare_time_series(l_time_series)
    return l_time_series


def download_all_data():
    d_states_data = {}

    for bl_id in range(1, 17):
        code = helper.BL_code_from_BL_ID(bl_id)
        print(code)

        l_time_series = fetch_and_prepare_bl_time_series(bl_id)
        d_states_data[code] = l_time_series

    # add to German sum
    d_german_sums = {}
    for code, l_time_series in d_states_data.items():
        for d in l_time_series:
            if d['Date'] not in d_german_sums:
                d2 = {}
                d2['Cases'] = d['Cases']
                d2['Deaths'] = d['Deaths']
            else:
                d2 = d_german_sums[d['Date']]
                d2['Cases'] += d['Cases']
                d2['Deaths'] += d['Deaths']
            d2['Date'] = d['Date']
            d_german_sums[d['Date']] = d2

    # German sum -> same dict
    l_time_series_de = []
    for date in sorted(d_german_sums.keys()):
        d = d_german_sums[date]
        l_time_series_de.append(d)
    d_states_data['DE-total'] = helper.prepare_time_series(l_time_series_de)
    del d_german_sums, d, l_time_series_de

    # add per Million rows
    for code, l_time_series in d_states_data.items():
        for i in range(len(l_time_series)):
            d = l_time_series[i]
            # add per Million rows
            d = helper.add_per_million_via_lookup(d, d_ref_states, code)
            l_time_series[i] = d
        d_states_data[code] = l_time_series
    return d_states_data


# old functions from V1
def fit_doubling_or_halftime(d_states_data) -> dict:
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
def join_with_divi_data(d_states_data) -> dict:
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
            f'data/de-states/de-state-{code}.json', d=l_time_series, sort_keys=True)

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
                'Cases_Last_Week_Doubling_Time', 'Cases_Last_Week_7Day_Percent'
            ]
            )
            csvwriter.writeheader()
            for d in l_time_series:
                csvwriter.writerow(d)


def export_latest_data(d_ref_states, d_states_data: dict):
    d_states_latest = helper.extract_latest_data(d_ref_states, d_states_data)

    with open('data/de-states/de-states-latest.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
        csvwriter = csv.DictWriter(fh, delimiter='\t', extrasaction='ignore',
                                   fieldnames=('State', 'Code', 'Population', 'Pop Density',
                                               'Date_Latest',
                                               'Cases', 'Deaths',
                                               'Cases_New', 'Deaths_New',
                                               'Cases_Per_Million',
                                               'Deaths_Per_Million', 'DoublingTime_Cases_Last_Week_Per_100000', 'Slope_Cases_Last_Week_Percent', 'Slope_Deaths_Last_Week_Percent', 'Cases_Last_Week_7Day_Percent')
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
d_states_data = download_all_data()

d_states_data = fit_doubling_or_halftime(d_states_data)
d_states_data = join_with_divi_data(d_states_data)
export_data(d_states_data)
export_latest_data(d_ref_states, d_states_data)
