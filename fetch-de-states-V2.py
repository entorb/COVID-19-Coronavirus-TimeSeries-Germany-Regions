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
import os
import time
import datetime
import csv
import json


# process bar
from tqdm import tqdm

# my helper modules
import helper


def fetch_json_as_dict_from_url_and_reduce_to_list(url: str) -> list:
    # TODO: replace by helper.read_url_or_cachefile
    """
    removes some of the returned structure
    """
    d_json = helper.fetch_json_as_dict_from_url(url)
    l2 = d_json['features']
    l3 = [v['attributes'] for v in l2]
    return l3


def helper_read_from_cache_or_fetch_from_url(url: str, file_cache: str, readFromCache: bool = True):
    """
    readFromCache=True -> not calling the API, but returning cached data
    readFromCache=False -> calling the API, and writing cache to filesystem
    """
    if readFromCache:
        readFromCache = helper.check_cache_file_available_and_recent(
            fname=file_cache, max_age=1800, verbose=False)

    json_cont = []
    if readFromCache == True:  # read from cache
        with open(file_cache, mode='r', encoding='utf-8') as json_file:
            json_cont = json.load(json_file)
    elif readFromCache == False:  # fetch and write to cache
        json_cont = fetch_json_as_dict_from_url_and_reduce_to_list(url)
        with open(file_cache, mode='w', encoding='utf-8', newline='\n') as fh:
            json.dump(json_cont, fh, ensure_ascii=False)
    return json_cont


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
        "&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22AnzahlFall%22%2C%22outStatisticFieldName%22%3A%22SumAnzahlFall%22%7D%2C%0D%0A%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22AnzahlTodesfall%22%2C%22outStatisticFieldName%22%3A%22SumAnzahlTodesfall%22%7D%5D" +\
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

    l_time_series = helper_read_from_cache_or_fetch_from_url(
        url=url, file_cache=file_cache, readFromCache=readFromCache)

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

    l_time_series = []

    # entry = one data point
    for entry in l_time_series_fetched:
        d = {}
        # covert to int
        d['Cases'] = int(entry['SumAnzahlFall'])
        d['Deaths'] = int(entry['SumAnzahlTodesfall'])
        # these are calculated below
        # d['Cases_New'] = int(entry['AnzahlFall'])
        # d['Deaths_New'] = int(entry['AnzahlTodesfall'])
        # Rename 'Meldedatum' (ms) -> Timestamp (s)
        d['Timestamp'] = int(entry['Meldedatum'] / 1000)

        # add Date
        d['Date'] = helper.convert_timestamp_to_date_str(
            d['Timestamp'])

        l_time_series.append(d)

    l_time_series = helper.prepare_time_series(l_time_series)

    # for i in range(len(l_time_series)):
    #     d = l_time_series[i]
    #     # _Per_Million
    #     d = helper.add_per_million_via_lookup(d, d_ref_landkreise, lk_id)
    #     l_time_series[i] = d

    #     data_t.append(d['Days_Past'])
    #     data_cases.append(d['Cases'])
    #     data_deaths.append(d['Deaths'])
    #     data_cases_new.append((d['Days_Past'], d['Cases_New']))
    #     data_deaths_new.append((d['Days_Past'], d['Deaths_New']))

    # # perform fit for last 7 days to obtain doubling time
    # data = list(zip(data_t, data_cases))
    # fit_series_res = helper.series_of_fits(
    #     data, fit_range=7, max_days_past=14)

    # for i in range(len(l_time_series)):
    #     entry = l_time_series[i]
    #     this_doubling_time = ""
    #     this_days_past = entry['Days_Past']
    #     if this_days_past in fit_series_res:
    #         this_doubling_time = fit_series_res[this_days_past]
    #     entry['Cases_Doubling_Time'] = this_doubling_time
    #     l_time_series[i] = entry

    return l_time_series


def download_all_data():
    d_states_data = {}

    # l2 = ('16068',)
    # for lk_id in d_ref_landkreise.keys():
    # for lk_id in tqdm(('09562',)):

    for bl_id in range(1, 17):
        code = helper.BL_code_from_BL_ID(bl_id)
        print(code)

        l_time_series = fetch_and_prepare_bl_time_series(bl_id)
        d_states_data[bl_id] = l_time_series

    return d_states_data


download_all_data()
