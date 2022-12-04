#!/usr/bin/env python3.10
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions
"""
This script downloads COVID-19 / coronavirus data of German disticts (Landkreise) provided by
GUI: https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_0/
"""
# Built-in/Generic Imports
import csv
import json
import time

from tqdm import tqdm  # process bar

import helper


# idea:
# fetch data from risklayer instead:
# http://www.risklayer-explorer.com/media/data/events/GermanyValues.csv


# Further details and Endpoints
# LK_ID is https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel
# Amtliche Gemeindeschlüssel (AGS)
# bzw Kreisschlüssel ohne letzte 3 Stellen
# 03 2 54 021 = Hildesheim
#   03 Niedersachsen
#    2 ehemaliger Regierungsbezirk Hannover
#   54 Landkreis Hildesheim
# ( 021 Stadt Hildesheim)
# -> LK_ID = 03254

# Endpoint: RKI_Landkreisdaten
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0

# f=json or f=html
# via f=html can be experimented using a nice form

# resultRecordCount: max=2000 -> multiple calls needed


# Endpoint: Covid19_RKI_Sums
# API-Doc: https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0
# API-Test: https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=html&where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&token=
# Examples
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=json&where=(Bundesland%3D%27Baden-W%C3%BCrttemberg%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=ObjectId%2CSummeFall%2CMeldedatum&orderByFields=Meldedatum%20asc&resultOffset=0&resultRecordCount=2000&cacheHint=true
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=json&where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=Meldedatum%2C+IdBundesland%2C+IdLandkreis&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&resultRecordCount=&sqlFormat=none&token=

# # Report of cases and deaths per Bundesland using sum
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=html&where=IdBundesland%3D%2702%27&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=true&orderByFields=Bundesland%2C+Meldedatum+asc&groupByFieldsForStatistics=Bundesland%2C+Meldedatum&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22SummeFall%22%2C%22outStatisticFieldName%22%3A%22SumSummeFall%22%7D%2C%0D%0A%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22SummeTodesfall%22%2C%22outStatisticFieldName%22%3A%22SumSummeTodesfall%22%7D%5D&having=&resultOffset=&resultRecordCount=&sqlFormat=none&token=

# List of Bundesländer and lastest number of cases/deaths, not time series
# Endpoint: Coronafälle_in_den_Bundesländern
# -> BL_mit_EW_und_Faellen
# API-Doc
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0
# API-Test
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/Coronaf%C3%A4lle_in_den_Bundesl%C3%A4ndern/FeatureServer/0/query?f=json&where=1%3D1&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&orderByFields=Fallzahl%20desc&resultOffset=0&resultRecordCount=25&cacheHint=true

# Example
# Man / Woman & Age Distribution
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?f=html&where=(Geschlecht%3C%3E%27unbekannt%27%20AND%20Altersgruppe%3C%3E%27unbekannt%27%20AND%20NeuerFall%20IN(0%2C%201))%20AND%20(Bundesland%3D%27Nordrhein-Westfalen%27)&returnGeometry=false&spatialRel=esriSpatialRelIntersects&outFields=*&groupByFieldsForStatistics=Altersgruppe%2CGeschlecht&orderByFields=Altersgruppe%20asc&outStatistics=%5B%7B%22statisticType%22%3A%22sum%22%2C%22onStatisticField%22%3A%22AnzahlFall%22%2C%22outStatisticFieldName%22%3A%22value%22%7D%5D&cacheHint=true


# Endpoint: RKI_COVID19
# API-Doc
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0
# API-Test
# https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_COVID19/FeatureServer/0/query?where=1%3D1&objectIds=&time=&resultType=none&outFields=*&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&orderByFields=Meldedatum&groupByFieldsForStatistics=&outStatistics=%0D%0A&having=&resultOffset=&resultRecordCount=&sqlFormat=none&f=html&token=


# args = helper.read_command_line_parameters()

# here I store the fetched ref_data_from
d_ref_landkreise = {}


# small helper functions


def get_lk_name_from_lk_id(lk_id: str) -> str:
    global d_ref_landkreise
    # name = d_ref_landkreise[lk_id]['county']
    name = f"{d_ref_landkreise[lk_id]['LK_Name']} ({d_ref_landkreise[lk_id]['LK_Typ']})"
    return name


# Code functions


def fetch_ref_landkreise(readFromCache: bool = True) -> dict:
    """
    fetches ref-data for the German districts (Landkreise) via rest API from arcgis
    GUI
    1: https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4/page/page_1/
    # /bca904a683844e7784141559b540dbc2
    2: https://npgeo-de.maps.arcgis.com/apps/opsdashboard/index.html
    Api Explorer
    https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0

    converts/flattens the retrieved json a bit and use the district ID lk_id as key for the returned dict
    write the json to cache folder in file system, using utf-8 encoding

    returns the data as list of dicts
    """
    file_cache = "cache/de-districts/de-districts.json"

    max_allowed_rows_to_fetch = 2000
    url = (
        "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?f=json"
        + "&where=1%3D1"
        + "&outFields=*"
        + "&orderByFields=BL_ID%2C+AGS"
        + "&resultRecordCount="
        + str(max_allowed_rows_to_fetch)
        + "&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&resultType=none&distance=0.0&units=esriSRUnit_Meter&returnGeodetic=false"
        + "&returnGeometry=false&returnCentroid=false&featureEncoding=esriDefault&multipatchOption=xyFootprint&maxAllowableOffset=&geometryPrecision=&outSR=&datumTransformation=&applyVCSProjection=false&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnExtentOnly=false&returnQueryGeometry=false&returnDistinctValues=false&cacheHint=false"
        + "&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset="
        + "&returnZ=false&returnM=false&returnExceededLimitFeatures=true&quantizationParameters=&sqlFormat=none&token="
    )

    cont = helper.read_url_or_cachefile(
        url=url,
        cachefile=file_cache,
        request_type="get",
        cache_max_age=0,  # 0s because git pulled files are "new"
        verbose=False,
    )
    json_cont = json.loads(cont)
    # flatten the json structure
    l2 = json_cont["features"]
    l_time_series = [v["attributes"] for v in l2]
    assert len(l_time_series) < max_allowed_rows_to_fetch
    return l_time_series


def fetch_and_prepare_ref_landkreise() -> dict:
    l_landkreise = fetch_ref_landkreise(readFromCache=True)
    d_landkreise = {}

    # convert list to dict, using lk_id as key
    for d_this_landkreis in l_landkreise:
        lk_id = d_this_landkreis["RS"]  # RS = LK_ID ; county = LK_Name

        # 16056 Eisenach was merged with 16063: LK Wartburgkreis
        # see https://www.eisenach.de/rathaus/fusion-der-stadt-eisenach
        if lk_id == "16056":  # Eisenach
            continue

        assert type(lk_id) == str
        assert lk_id.isdecimal() is True

        d = {}
        d["Population"] = d_this_landkreis["EWZ"]
        assert type(d["Population"]) == int
        d["BL_Name"] = d_this_landkreis["BL"]
        d["BL_Code"] = helper.d_BL_code_from_BL_ID[int(d_this_landkreis["BL_ID"])]
        d["LK_Name"] = d_this_landkreis["GEN"]
        d["LK_Name"] = (
            d["LK_Name"]
            .replace("Region Hannover", "Hannover")
            .replace("Regionalverband ", "")
        )
        d["LK_Typ"] = d_this_landkreis["BEZ"]
        d_landkreise[lk_id] = d

    del d_this_landkreis

    helper.write_json(
        filename="data-json/de-districts/ref-de-districts.json",
        d=d_landkreise,
        sort_keys=True,
    )

    with open(
        "data/de-districts/ref-de-districts.tsv",
        mode="w",
        encoding="utf-8",
        newline="\n",
    ) as fh_csv:
        csvwriter = csv.DictWriter(
            fh_csv,
            delimiter="\t",
            extrasaction="ignore",
            fieldnames=[
                "LK_ID",
                "LK_Name",
                "LK_Typ",
                "Population",
                "BL_Code",
                "BL_Name",
            ],
        )
        csvwriter.writeheader()
        for lk_id in sorted(d_landkreise.keys()):
            d = d_landkreise[lk_id]
            d["LK_ID"] = lk_id
            csvwriter.writerow(d)
        del lk_id, d

    # assure we did not loose any
    # assert len(l_landkreise) == len(d_landkreise)

    return d_landkreise


def gen_mapping_BL2LK_json():
    """
    generates a mapping table of BL_Code <-> LK_ID
    dict: key1 = BC_Code -> list of LK_IDs:
    {"SH": {"BL_Name": "Schleswig-Holstein", "LK_IDs": [["01001", "Flensburg"], ["01002", "Kiel"], ..] ..}..}
    """
    global d_ref_landkreise
    d_bundeslaender = {}
    d_landkreis_id_name_mapping = {}  # lk_id -> name
    for lk_id in d_ref_landkreise.keys():
        lk = d_ref_landkreise[lk_id]
        d_landkreis_id_name_mapping[lk_id] = get_lk_name_from_lk_id(lk_id)
        if lk["BL_Code"] not in d_bundeslaender.keys():
            d = {}
            l_lk_ids = []
            l_lk_ids.append((lk_id, lk["LK_Name"]))
            d["BL_Name"] = lk["BL_Name"]
            d["LK_IDs"] = l_lk_ids

            d_bundeslaender[lk["BL_Code"]] = d
        else:
            d_bundeslaender[lk["BL_Code"]]["LK_IDs"].append((lk_id, lk["LK_Name"]))

    helper.write_json(
        "data/de-districts/mapping_bundesland_landkreis.json",
        d_bundeslaender,
    )
    helper.write_json(
        "data/de-districts/mapping_landkreis_ID_name.json",
        d_landkreis_id_name_mapping,
    )


def fetch_landkreis_time_series(lk_id: str, readFromCache: bool = True) -> list:
    """
    for a given lk_id: fetches its time series and returns as list
    Fetches data from arcgis Covid19_RKI_Sums endpoint: Bundesland, Landkreis, etc.
    # API Explorer
    # https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0

    readFromCache=True -> not calling the API, but returning cached data
    readFromCache=False -> calling the API, and writing cache to filesystem

    returns data as list, ordered by date
    """
    file_cache = f"cache/de-districts/district_timeseries-{lk_id}.json"

    max_allowed_rows_to_fetch = 2000

    url = (
        "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query"
        + "?f=json"
        + "&where=(IdLandkreis='"
        + lk_id
        + "')"
        + "&outFields=Meldedatum%2CSummeFall%2C+SummeTodesfall"
        + "&orderByFields=Meldedatum"
        + "&resultRecordCount="
        + str(max_allowed_rows_to_fetch)
        + "&objectIds=&time=&resultType=none&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false"
        + "&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&sqlFormat=none&token="
    )
    # %2C+AnzahlFall%2C+AnzahlTodesfall

    # example
    # https://services7.arcgis.com/mOBPykOjAyBO2ZKk/ArcGIS/rest/services/Covid19_RKI_Sums/FeatureServer/0/query?f=html&where=(IdLandkreis='14612')&outFields=Meldedatum%2CSummeFall%2C+SummeTodesfall%2C+AnzahlFall%2C+AnzahlTodesfall&orderByFields=Meldedatum&objectIds=&time=&resultType=none&returnIdsOnly=false&returnUniqueIdsOnly=false&returnCountOnly=false&returnDistinctValues=false&cacheHint=false&groupByFieldsForStatistics=&outStatistics=&having=&resultOffset=&sqlFormat=none&token=
    # f=json
    # &outFields=*

    retryNo = 0
    while retryNo <= 3:
        cont = helper.read_url_or_cachefile(
            url=url,
            cachefile=file_cache,
            request_type="get",
            cache_max_age=0,  # 0s because git pulled files are "new"
            verbose=False,
        )
        json_cont = json.loads(cont)
        if "features" in json_cont:
            break
        else:
            retryNo += 1
            time.sleep(3)
            print(f"retrying LK {lk_id} #{retryNo}")

    # flatten the json structure
    l2 = json_cont["features"]
    l_time_series = [v["attributes"] for v in l2]

    assert len(l_time_series) < max_allowed_rows_to_fetch
    return l_time_series


def fetch_and_prepare_lk_time_series(lk_id: str) -> list:
    """
    calles fetch_landkreis_time_series
    convert and add fields of time series list
    returns list
    """
    l_time_series_fetched = fetch_landkreis_time_series(lk_id=lk_id, readFromCache=True)

    l_time_series = []

    # entry = one data point
    for entry in l_time_series_fetched:
        d = {
            # covert to int
            "Cases": int(entry["SummeFall"]),
            "Deaths": int(entry["SummeTodesfall"]),
            "Date": helper.convert_timestamp_to_date_str(
                int(entry["Meldedatum"] / 1000),
            ),
        }
        # calc Date from 'Meldedatum' (ms)
        l_time_series.append(d)
    l_time_series = helper.prepare_time_series(l_time_series)

    for i in range(len(l_time_series)):
        d = l_time_series[i]
        # _Per_Million
        d = helper.add_per_million_via_lookup(d, d_ref_landkreise, lk_id)
        l_time_series[i] = d

    return l_time_series


def download_all_data():
    d_districts_data = {}

    # l2 = ('16068',)
    # for lk_id in d_ref_landkreise.keys():
    # for lk_id in tqdm(('09562',)):
    for lk_id in tqdm(d_ref_landkreise.keys()):
        # lk_name = get_lk_name_from_lk_id(lk_id)
        # print(f"{lk_id} {lk_name}")

        # 03353   LK Harburg      252776
        # 09562   SK Erlangen     111962
        # 09563   SK Fürth        127748

        # data = []
        l_lk_time_series = fetch_and_prepare_lk_time_series(lk_id)
        # the following was used for multiple fitting to derive a time series of the doubling time
        # # l_lk_time_series = fetch_landkreis_time_series(lk_id, readFromCache=True)
        # for entry in l_lk_time_series:
        #     # choose columns for fitting
        #     data.append((entry['Days_Past'], entry['Cases']))

        d_districts_data[lk_id] = l_lk_time_series

    return d_districts_data


def join_with_divi_data(d_districts_data: dict) -> dict:
    d_divi_data = helper.read_json_file("cache/de-divi/de-divi-V3.json")
    for lk_id, l_lk_time_series in d_districts_data.items():
        # all Berlin Districts are in divi at 11000
        if lk_id[0:2] == "11":
            l_divi_time_series = d_divi_data["11000"]
        elif lk_id not in d_divi_data:
            continue
        #        assert lk_id in d_divi_data, f"Error: LK {lk_id} missing in DIVI data"
        if lk_id[0:2] != "11":
            l_divi_time_series = d_divi_data[lk_id]
        d_divi_time_series = {}
        for d in l_divi_time_series:
            d_divi_time_series[d["Date"]] = d

        for d in l_lk_time_series:
            if d["Date"] not in d_divi_time_series:
                continue
            d["DIVI_Intensivstationen_Covid_Prozent"] = d_divi_time_series[d["Date"]][
                "faelle_covid_aktuell_proz"
            ]
            d["DIVI_Intensivstationen_Betten_belegt_Prozent"] = d_divi_time_series[
                d["Date"]
            ]["betten_belegt_proz"]

        d_districts_data[lk_id] = l_lk_time_series

    return d_districts_data


def export_data(d_districts_data: dict):
    """export timeseries as JSON and CSV"""
    for lk_id, l_time_series in d_districts_data.items():
        l_time_series = helper.timeseries_export_drop_irrelevant_columns(l_time_series)
        file_out = f"data-json/de-districts/de-district_timeseries-{lk_id}.json"
        helper.write_json(
            file_out,
            d=l_time_series,
            sort_keys=True,
            indent=1,
        )

        file_out = f"data/de-districts/de-district_timeseries-{lk_id}.tsv"
        with open(
            file_out,
            mode="w",
            encoding="utf-8",
            newline="\n",
        ) as fh_csv:
            csvwriter = csv.DictWriter(
                fh_csv,
                delimiter="\t",
                extrasaction="ignore",
                fieldnames=[
                    "Date",
                    "Cases",
                    "Deaths",
                    "Cases_New",
                    "Deaths_New",
                    "Cases_Last_Week",
                    "Deaths_Last_Week",
                    "Cases_Per_Million",
                    "Deaths_Per_Million",
                    "Cases_New_Per_Million",
                    "Deaths_New_Per_Million",
                    "Cases_Last_Week_Per_Million",
                    "Deaths_Last_Week_Per_Million",
                    "DIVI_Intensivstationen_Covid_Prozent",
                    "DIVI_Intensivstationen_Betten_belegt_Prozent",
                    "Cases_Last_Week_7Day_Percent",
                ],
            )
            csvwriter.writeheader()
            for d in l_time_series:
                csvwriter.writerow(d)


def export_latest_data(d_districts_data: dict):
    d_districts_latest = helper.extract_latest_data(d_ref_landkreise, d_districts_data)
    d_for_export_V1 = d_districts_latest
    l_for_export_V2 = []
    for lk_id, d in d_districts_latest.items():
        if len(d_districts_data[lk_id]) == 0:  # handling of empty data set
            continue
        # V1: dict (lk_id) -> dict
        # V2: list of ficts
        # d_for_export_V1[lk_id] = d
        d["Landkreis"] = get_lk_name_from_lk_id(lk_id)
        d["Bundesland"] = d["BL_Name"]
        del d["BL_Name"]
        # divi data is not returned by helper.extract_latest_data and mostly not available at latest day, so using the date of the previous day instead
        if "DIVI_Intensivstationen_Covid_Prozent" in d_districts_data[lk_id][-1]:
            d["DIVI_Intensivstationen_Covid_Prozent"] = d_districts_data[lk_id][-1][
                "DIVI_Intensivstationen_Covid_Prozent"
            ]
            d["DIVI_Intensivstationen_Betten_belegt_Prozent"] = d_districts_data[lk_id][
                -1
            ]["DIVI_Intensivstationen_Betten_belegt_Prozent"]
        elif "DIVI_Intensivstationen_Covid_Prozent" in d_districts_data[lk_id][-2]:
            d["DIVI_Intensivstationen_Covid_Prozent"] = d_districts_data[lk_id][-2][
                "DIVI_Intensivstationen_Covid_Prozent"
            ]
            d["DIVI_Intensivstationen_Betten_belegt_Prozent"] = d_districts_data[lk_id][
                -2
            ]["DIVI_Intensivstationen_Betten_belegt_Prozent"]
        d_for_export_V2 = d
        d_for_export_V2["LK_ID"] = lk_id
        l_for_export_V2.append(d_for_export_V2)

    # Export as JSON
    helper.write_json(
        "data-json/de-districts/de-districts-results.json",
        d=d_for_export_V1,
        sort_keys=True,
    )

    helper.write_json(
        filename="data-json/de-districts/de-districts-results-V2.json",
        d=l_for_export_V2,
        sort_keys=True,
    )

    # Export as CSV
    with open(
        "data/de-districts/de-districts-results.tsv",
        mode="w",
        encoding="utf-8",
        newline="\n",
    ) as fh_csv:
        csvwriter = csv.DictWriter(
            fh_csv,
            delimiter="\t",
            extrasaction="ignore",
            fieldnames=[
                "Landkreis",
                "Bundesland",
                "Population",
                "Cases",
                "Deaths",
                "Cases_Per_Million",
                "Deaths_Per_Million",
                "DIVI_Intensivstationen_Covid_Prozent",
                "DIVI_Intensivstationen_Betten_belegt_Prozent",
                "DoublingTime_Cases_Last_Week_Per_100000",
            ],
        )

        csvwriter.writeheader()

        for _lk_id, d in d_for_export_V1.items():
            csvwriter.writerow(d)


d_ref_landkreise = fetch_and_prepare_ref_landkreise()
# generate and export a mapping table
gen_mapping_BL2LK_json()

d_districts_data = download_all_data()

d_districts_data = join_with_divi_data(d_districts_data)

# count_zero_cases_last_week(d_districts_data)
export_latest_data(d_districts_data)
export_data(d_districts_data)
