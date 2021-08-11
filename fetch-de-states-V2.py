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


def flatten_json(d_json: dict) -> list:
    """
    removes some of the returned structure
    """
    l2 = d_json['features']
    l3 = [v['attributes'] for v in l2]
    return l3


# def helper_read_from_cache_or_fetch_from_url(url: str, file_cache: str):
#     """
#     readFromCache=True -> not calling the API, but returning cached data
#     readFromCache=False -> calling the API, and writing cache to filesystem
#     """

#     cont = helper.read_url_or_cachefile(
#         url=url, cachefile=file_cache, request_type='get', cache_max_age=3600, verbose=False)
#     json_cont = json.loads(cont)
#     # flatten the json structure
#     l2 = json_cont['features']
#     l3 = [v['attributes'] for v in l2]
#     return l3


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
        d['Cases'] = int(entry['SumAnzahlFall'])
        d['Deaths'] = int(entry['SumAnzahlTodesfall'])
        # Rename 'Meldedatum' (ms) -> Timestamp (s)
        d['Timestamp'] = int(entry['Meldedatum'] / 1000)

        # add Date
        d['Date'] = helper.convert_timestamp_to_date_str(
            d['Timestamp'])

        l_time_series.append(d)

    l_time_series = helper.prepare_time_series(l_time_series)
    for i in range(len(l_time_series)):
        d = l_time_series[i]
        # add per Million rows
        d = helper.add_per_million_via_lookup(d, d_ref_states, code)
    return l_time_series


def download_all_data():
    d_states_data = {}

    for bl_id in range(1, 17):
        code = helper.BL_code_from_BL_ID(bl_id)
        print(code)

        l_time_series = fetch_and_prepare_bl_time_series(bl_id)
        d_states_data[code] = l_time_series

    return d_states_data


d_ref_states = helper.read_ref_data_de_states()
download_all_data()
