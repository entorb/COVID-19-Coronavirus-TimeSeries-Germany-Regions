#!/usr/bin/env python3.10
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions
"""
Helper functions collections
"""
import csv
import datetime as dt
import json
import math
import os
import time
import urllib.request
from typing import Any, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests  # for read_url_or_cachefile
from scipy.optimize import curve_fit

# multithreading
# import multiprocessing as mp  # for fetching number of CPUs
# import logging
# import threading
# import concurrent.futures

# Matplotlib: disable interactive mode
# mpl.use("Agg")  # Cairo
plt.ioff()

# ensure all output folders are present
os.makedirs(name="cache", exist_ok=True)
os.makedirs(name="cache/de-districts/", exist_ok=True)
os.makedirs(name="cache/de-divi/", exist_ok=True)
os.makedirs(name="cache/de-states/", exist_ok=True)
os.makedirs(name="cache/rki-mutation-sequences", exist_ok=True)
os.makedirs(name="cache/int/", exist_ok=True)
# os.makedirs(name="data/de-districts/latest/", exist_ok=True)
os.makedirs(name="data-json/de-districts/", exist_ok=True)
os.makedirs(name="data-json/de-states/", exist_ok=True)
os.makedirs(name="data-json/int/", exist_ok=True)
os.makedirs(name="plots-gnuplot/", exist_ok=True)
os.makedirs(name="plots-gnuplot/de-districts/", exist_ok=True)
os.makedirs(name="plots-gnuplot/de-divi/", exist_ok=True)
os.makedirs(name="plots-gnuplot/de-states/", exist_ok=True)
os.makedirs(name="plots-gnuplot/int/", exist_ok=True)
os.makedirs(name="plots-python/", exist_ok=True)
os.makedirs(name="plots-python/de-states/", exist_ok=True)
os.makedirs(name="plots-python/de-districts/", exist_ok=True)
os.makedirs(name="maps/out/de-districts/", exist_ok=True)


#
# General Helpers
#


def download_from_url_if_old(
    url: str,
    file_local: str,
    max_age: int = 3600,
    verbose: bool = False,
) -> None:
    if not check_cache_file_available_and_recent(
        fname=file_local,
        max_age=max_age,
        verbose=verbose,
    ):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:97.0) Gecko/20100101 Firefox/97.0 ",
        }
        filedata = requests.get(url, headers=headers).content
        datatowrite = filedata
        with open(file_local, mode="wb") as f:
            f.write(datatowrite)


def read_url_or_cachefile(
    url: str,
    file_cache: str,
    request_type: str = "get",
    payload: Optional[dict[str, str]] = None,
    cache_max_age: int = 1800,
    verbose: bool = True,
) -> str:
    if payload is None:
        payload = {}
    b_cache_is_recent = check_cache_file_available_and_recent(
        fname=file_cache,
        max_age=cache_max_age,
        verbose=verbose,
    )
    if not b_cache_is_recent:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0 ",
        }
        if request_type == "get":
            cont_raw = requests.get(url, headers=headers).content
        elif request_type == "post":
            cont_raw = requests.post(url, headers=headers, data=payload).content
        else:
            raise Exception("unknown request type " + request_type)
        with open(file_cache, mode="wb") as fh:
            fh.write(cont_raw)
        cont = cont_raw.decode("utf-8")
    else:
        with open(file_cache, encoding="utf-8") as fh:
            cont = fh.read()
    return cont


def read_json_file(filename: str) -> dict[str, str | int | float]:
    """
    returns list or dict
    """
    with open(filename, encoding="utf-8") as fh:
        return json.load(fh)


def write_json(
    filename: str,
    d: dict[str, Any],
    sort_keys: bool = True,
    indent: int = 2,
) -> None:
    with open(filename, mode="w", encoding="utf-8", newline="\n") as fh:
        json.dump(d, fh, ensure_ascii=False, sort_keys=sort_keys, indent=indent)


def write_json_list(
    filename: str, l: list[Any], sort_keys: bool = True, indent: int = 2
) -> None:
    with open(filename, mode="w", encoding="utf-8", newline="\n") as fh:
        json.dump(l, fh, ensure_ascii=False, sort_keys=sort_keys, indent=indent)


def convert_timestamp_to_date_str(ts: int) -> str:
    """
    converts a ms timestamp to date string (without time)
    format: 2020-03-29
    """
    d = dt.datetime.fromtimestamp(ts)
    # s = f"{d}"
    # 2020-03-29 01:00:00
    s = d.strftime("%Y-%m-%d")
    return s


def date_format(y: int, m: int, d: int) -> str:
    return "%04d-%02d-%02d" % (y, m, d)


#
# Pandas Helper
#


def pandas_set_date_index(
    df: pd.DataFrame, date_column: str | dt.date = "Date"
) -> pd.DataFrame:
    """
    use date as index
    source format: str of yyyy-mm-dd or dt.date
    """
    if type(date_column) == dt.date:
        df[date_column] = pd.to_datetime(df[date_column])
    elif type(date_column) == str:
        df[date_column] = pd.to_datetime(df[date_column], format="%Y-%m-%d")
    assert df[date_column].dtype == "datetime64[ns]"
    # dt_index = pd.DatetimeIndex(df[date_column].values)
    # df = df.set_index(dt_index) # problem: this does not remove the source column
    df = df.set_index([date_column])
    assert df.index.dtype == "datetime64[ns]"
    return df


def pandas_calc_roll_av(
    df: pd.DataFrame,
    column: str,
    days: int = 7,
    digits: int = 1,
) -> pd.DataFrame:
    """calc rolling average over column"""
    assert type(days) == int
    # assert type(df[column]) in (int, float)
    df[column + "_roll_av"] = (
        df[column].rolling(window=days, min_periods=1).mean().round(digits)
    )
    return df


#
# Matplotlib Helper
#


def mpl_add_text_source(
    source: str = "RKI and DIVI", date: Optional[dt.date] = None
) -> None:
    date = date or dt.date.today()
    plt.gcf().text(
        1.0,
        0.0,
        s=f"by Torben https://entorb.net , based on {source} data of {date}",
        fontsize=8,
        horizontalalignment="right",
        verticalalignment="bottom",
        rotation="vertical",
    )


#
# COVID-19 Helpers
#


# def BL_code_from_BL_ID(bl_id: int) -> str:
#     """
#     converts Bundesland/ BL_IDs to Codes: 01 -> 1 -> SH
#     """
#     bl_id = int(bl_id)  # for security

#     return d[bl_id]


d_BL_code_from_BL_ID = {
    0: "DE-total",
    1: "SH",
    2: "HH",
    3: "NI",
    4: "HB",
    5: "NW",
    6: "HE",
    7: "RP",
    8: "BW",
    9: "BY",
    10: "SL",
    11: "BE",
    12: "BB",
    13: "MV",
    14: "SN",
    15: "ST",
    16: "TH",
}


d_BL_ID_from_BL_code = {
    "DE-total": 0,
    "SH": 1,
    "HH": 2,
    "NI": 3,
    "HB": 4,
    "NW": 5,
    "HE": 6,
    "RP": 7,
    "BW": 8,
    "BY": 9,
    "SL": 10,
    "BE": 11,
    "BB": 12,
    "MV": 13,
    "SN": 14,
    "ST": 15,
    "TH": 16,
}

d_BL_name_from_BL_Code = {
    "BW": "Baden-Württemberg",
    "BY": "Bayern",
    "BE": "Berlin",
    "BB": "Brandenburg",
    "HB": "Bremen",
    "HH": "Hamburg",
    "HE": "Hessen",
    "MV": "Mecklenburg-Vorpommern",
    "NI": "Niedersachsen",
    "NW": "Nordrhein-Westfalen",
    "RP": "Rheinland-Pfalz",
    "SL": "Saarland",
    "SN": "Sachsen",
    "ST": "Sachsen-Anhalt",
    "SH": "Schleswig-Holstein",
    "TH": "Thüringen",
    "DE-total": "Deutschland",
}

d_lk_name_from_lk_id = read_json_file(
    "data/de-districts/mapping_landkreis_ID_name.json",
)


def prepare_time_series(
    l_time_series: list[dict[str, int | float | str]]
) -> list[dict[str, int | float | str]]:
    """
    assumes items in l_time_series are dicts having the following keys: Date, Cases, Deaths
    sorts l_time_series by Date
    if cases at last entry equals 2nd last entry, than remove last entry, as sometime the source has a problem.
    loops over l_time_series and calculates the
      _New values per item/day
      _Last_Week
    """
    # if no data is fetched, return empty list
    if len(l_time_series) == 0:
        return []

    # some checks
    d = l_time_series[0]
    assert "Date" in d
    assert "Cases" in d
    assert "Deaths" in d
    assert isinstance(d["Date"], str)
    assert isinstance(d["Cases"], int)
    assert isinstance(d["Deaths"], int)
    assert isinstance(l_time_series[-1]["Date"], str)
    last_date = dt.datetime.strptime(l_time_series[-1]["Date"], "%Y-%m-%d")

    # ensure sorting by date
    l_time_series = sorted(l_time_series, key=lambda x: x["Date"], reverse=False)

    # NO, THIS RESULTS IN DATA SEAMING TO OLD
    # if lastdate and lastdate-1 have the same number of cases, than drop lastdate
    # if l_time_series[-1]['Cases'] == l_time_series[-2]['Cases']:
    #     l_time_series.pop()

    # to ensure that each date is unique
    l_dates_processed: list[str] = []

    last_cases = 0
    last_deaths = 0
    days_since_2_deaths = 0

    for i in range(len(l_time_series)):
        d = l_time_series[i]

        # ensure that each date is unique
        assert d["Date"] not in l_dates_processed
        assert isinstance(d["Date"], str)
        assert isinstance(d["Cases"], int)
        assert isinstance(d["Deaths"], int)
        l_dates_processed.append(d["Date"])

        this_date = dt.datetime.strptime(d["Date"], "%Y-%m-%d")
        d["Days_Past"] = (this_date - last_date).days

        # days_since_2_deaths
        d["Days_Since_2nd_Death"] = None
        if d["Deaths"] >= 2:  # is 2 a good value?
            d["Days_Since_2nd_Death"] = days_since_2_deaths
            days_since_2_deaths += 1

        # _New since yesterday
        d["Cases_New"] = d["Cases"] - last_cases
        d["Deaths_New"] = d["Deaths"] - last_deaths
        assert isinstance(d["Cases_New"], int)
        assert isinstance(d["Deaths_New"], int)

        # sometimes values are corrected, leading to negative values, which I replace by 0
        if d["Cases_New"] < 0:
            d["Cases_New"] = 0
        if d["Deaths_New"] < 0:
            d["Deaths_New"] = 0

        # delta of _Last_Week = last 7 days
        d["Cases_Last_Week"] = 0
        d["Deaths_Last_Week"] = 0
        if i >= 7:
            # TM: this is correct, I double checked it ;-)
            d7 = l_time_series[i - 7]
            d["Cases_Last_Week"] = d["Cases"] - d7["Cases"]
            d["Deaths_Last_Week"] = d["Deaths"] - d7["Deaths"]

            # Cases_Last_Week_7Day_Percent and Deaths_Last_Week_7Day_Percent
            d["Cases_Last_Week_7Day_Percent"] = 0
            if d7["Cases_Last_Week"] >= 2:  # min 2 to reduce noise
                d["Cases_Last_Week_7Day_Percent"] = round(
                    (d["Cases_Last_Week"] - d7["Cases_Last_Week"])
                    / d7["Cases_Last_Week"]
                    * 100,
                    1,
                )
            d["Deaths_Last_Week_7Day_Percent"] = 0
            if d7["Deaths_Last_Week"] >= 2:  # min 2 to reduce noise
                d["Deaths_Last_Week_7Day_Percent"] = round(
                    (d["Deaths_Last_Week"] - d7["Deaths_Last_Week"])
                    / d7["Deaths_Last_Week"]
                    * 100,
                    1,
                )

        # sometimes values are corrected, leading to negative values, which I replace by 0
        if d["Cases_Last_Week"] < 0:
            d["Cases_Last_Week"] = 0
        if d["Deaths_Last_Week"] < 0:
            d["Deaths_Last_Week"] = 0

        # Deaths_Per_Cases
        d["Deaths_Per_Cases"] = None
        if d["Cases"] > 0 and d["Deaths"] > 0:
            d["Deaths_Per_Cases"] = round(d["Deaths"] / d["Cases"], 3)
        # Deaths_Per_Cases_Last_Week
        d["Deaths_Per_Cases_Last_Week"] = None
        if (
            i >= 7
            and d["Cases_Last_Week"]
            and d["Deaths_Last_Week"]
            and d["Cases_Last_Week"] > 0
            and d["Deaths_Last_Week"] > 0
        ):
            d["Deaths_Per_Cases_Last_Week"] = round(
                d["Deaths_Last_Week"] / d["Cases_Last_Week"],
                3,
            )

        last_cases = d["Cases"]
        last_deaths = d["Deaths"]

        l_time_series[i] = d

    return l_time_series


def timeseries_export_drop_irrelevant_columns(
    l_time_series: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    keys_to_drop = ("Days_Past",)
    for i in range(len(l_time_series)):
        d = l_time_series[i]
        for key in keys_to_drop:
            if key in d:
                del d[key]
        l_time_series[i] = d
    return l_time_series


def extract_latest_data(
    d_ref_data: dict[str, Any], d_data_all: dict[str, Any]
) -> dict[str, Any]:
    d_data_latest = dict(d_ref_data)
    for code, l_time_series in d_data_all.items():
        assert code in d_data_latest
        if len(l_time_series) == 0:  # handling of empty data set
            continue
        d = l_time_series[-1]
        d_data_latest[code]["Date_Latest"] = d["Date"]
        for key in (
            "Cases",
            "Deaths",
            "Cases_New",
            "Deaths_New",
            "Cases_Per_Million",
            "Deaths_Per_Million",
            "Cases_Last_Week",
            "Deaths_Last_Week",
            "Cases_Last_Week_Per_Million",
            "Deaths_Last_Week_Per_Million",
            "Cases_Last_Week_Per_100000",
            "Cases_Last_Week_7Day_Percent",
            "Deaths_Last_Week_7Day_Percent",
        ):
            d_data_latest[code][key] = d[key]
        d_slopes = fit_slopes(l_time_series)
        for key, value in d_slopes.items():
            d_data_latest[code][key] = value

        # for key, value in calc_7_day_change_percent(l_time_series).items():
        #     d_data_latest[code][key] = value
    return d_data_latest


def add_per_million_via_lookup(
    d: dict[str, Any], d_ref: dict[str, Any], code: str
) -> dict[str, Any]:
    pop_in_million = d_ref[code]["Population"] / 1000000
    return add_per_million(d=d, pop_in_million=pop_in_million)


def add_per_million(d: dict[str, Any], pop_in_million: float) -> dict[str, Any]:
    for key in (
        "Cases",
        "Deaths",
        "Cases_New",
        "Deaths_New",
        "Cases_Last_Week",
        "Deaths_Last_Week",
    ):
        perMillion = 0
        if key in d and d[key] is not None and pop_in_million:
            perMillion = d[key] / pop_in_million
            if key in ("Deaths_New",):
                perMillion = round(perMillion, 3)
            elif key in ("Deaths_Last_Week",):
                perMillion = round(perMillion, 2)
            else:
                perMillion = int(round(perMillion, 3))
        # else:
        #     perMillion = 0  # if pop is unknown
        d[key + "_Per_Million"] = perMillion
    d["Cases_Last_Week_Per_100000"] = d["Cases_Last_Week_Per_Million"] / 10
    return d


def check_cache_file_available_and_recent(
    fname: str,
    max_age: int = 3600,
    verbose: bool = False,
) -> bool:
    b_cache_good = True
    if not os.path.exists(fname):
        if verbose:
            print(f"No Cache available: {fname}")
        b_cache_good = False
    if b_cache_good and time.time() - os.path.getmtime(fname) > max_age:
        if verbose:
            print(f"Cache too old: {fname}")
        b_cache_good = False
    return b_cache_good


def fetch_json_as_dict_from_url(url: str) -> dict[str, Any]:
    if not url.lower().startswith("http"):
        raise ValueError from None
    filedata = urllib.request.urlopen(url)  # noqa: S310
    contents = filedata.read()
    d_json = json.loads(contents.decode("utf-8"))
    # retry on error:
    if "error" in d_json:
        print("retrying upon error...")
        time.sleep(3)
        filedata = urllib.request.urlopen(url)  # noqa: S310
        contents = filedata.read()
        d_json = json.loads(contents.decode("utf-8"))
    assert "error" not in d_json, d_json["error"]["details"][0] + "\n" + url
    return d_json


def extract_x_and_y_data(data: tuple[float, float]) -> tuple[float, float]:
    """
    data of (x,y) -> data_x, data_y
    """
    # V1: manual
    # data_x = []
    # data_y = []
    # for pair in data:
    #     data_x.append(pair[0])
    #     data_y.append(pair[1])

    # V2: via unzip
    data_x, data_y = zip(*data)
    return data_x, data_y


#
# Helpers for fitting
#


def extract_data_according_to_fit_ranges(
    data: list,
    fit_range_x: tuple,
    fit_range_y: tuple,
) -> tuple:
    """
    filters the data on which we fit
    data ist list of (x,y) value pairs
    """
    data_x_for_fit = []
    data_y_for_fit = []
    if len(data) == 0:
        return (data_x_for_fit, data_y_for_fit)
    assert len(data[0]) == 2  # pairs of (x,y)
    for i in range(len(data)):
        if (
            data[i][0] >= fit_range_x[0]
            and data[i][0] <= fit_range_x[1]
            and data[i][1] >= fit_range_y[0]
            and data[i][1] <= fit_range_y[1]
        ):
            data_x_for_fit.append(data[i][0])
            data_y_for_fit.append(data[i][1])
    assert len(data_x_for_fit) == len(data_x_for_fit)
    return (data_x_for_fit, data_y_for_fit)


def fit_slopes(l_time_series: list[dict[str, Any]]) -> dict[str, float]:
    """
    fit data of !only! last 7 days via linear regression: y=m*x+b , b = last value
    returns dict with 2 keys: "Slope_Cases_New_Per_Million" and "Slope_Deaths_New_Per_Million"
    """
    d_slopes = {}
    data_cases_new_pm = []
    data_deaths_new_pm = []
    data_cases_last_week = []
    data_cases_last_week_percent = []
    # data_deaths_last_week_percent = []

    # TODO: should I increase againg reduce to 14 days?
    days_used_for_slope_fit = 7
    # TODO: convert to % instead of Per_Million
    avg_Cases_Last_Week = 0
    avg_Deaths_Last_Week = 0
    sum_Cases_Last_Week = 0
    sum_Deaths_Last_Week = 0
    # for i in range(len(l_time_series)):
    # TM: this is correct ant returns last 7 entries: -7 .. -1
    for i in range(-days_used_for_slope_fit, 0):
        d = l_time_series[i]
        sum_Cases_Last_Week += d["Cases_Last_Week"]
        sum_Deaths_Last_Week += d["Deaths_Last_Week"]
    if sum_Cases_Last_Week > 0:
        avg_Cases_Last_Week = sum_Cases_Last_Week / days_used_for_slope_fit
    if sum_Deaths_Last_Week > 0:
        avg_Deaths_Last_Week = sum_Deaths_Last_Week / days_used_for_slope_fit
    del sum_Cases_Last_Week, sum_Deaths_Last_Week

    # Cases Percent
    if avg_Cases_Last_Week > 0:
        for i in range(-days_used_for_slope_fit, 0):
            d = l_time_series[i]
            data_cases_last_week_percent.append(
                (d["Days_Past"], d["Cases_Last_Week"] / avg_Cases_Last_Week * 100),
            )
        N0, m = 0, 0
        d_res = fit_routine(data=data_cases_last_week_percent, mode="lin")
        if "fit_res" in d_res:
            N0, m = d_res["fit_res"]
        d_slopes["Slope_Cases_Last_Week_Percent"] = round(m, 1)

    # Deaths Percent
    if avg_Deaths_Last_Week > 0:
        for i in range(-days_used_for_slope_fit, 0):
            d = l_time_series[i]
            data_cases_last_week_percent.append(
                (d["Days_Past"], d["Deaths_Last_Week"] / avg_Deaths_Last_Week * 100),
            )
        N0, m = 0, 0
        d_res = fit_routine(data=data_cases_last_week_percent, mode="lin")
        if "fit_res" in d_res:
            N0, m = d_res["fit_res"]
        d_slopes["Slope_Deaths_Last_Week_Percent"] = round(m, 1)

    for i in range(-days_used_for_slope_fit, 0):
        d = l_time_series[i]
        data_cases_new_pm.append((d["Days_Past"], d["Cases_Last_Week_Per_Million"]))
        data_deaths_new_pm.append((d["Days_Past"], d["Deaths_Last_Week_Per_Million"]))
        data_cases_last_week.append((d["Days_Past"], 0.0 + d["Cases_Last_Week"]))
        # SOLVED: why does the fit not work well when using Cases_Last_Week instead of Cases_Last_Week_Per_Million ??? d['Cases_Last_Week']/10 again works... -> because of bad start values for T

    # Cases_New_Per_Million
    N0, m = 0, 0
    d_res = fit_routine(data=data_cases_new_pm, mode="lin")
    if "fit_res" in d_res:
        N0, m = d_res["fit_res"]
    d_slopes["Slope_Cases_New_Per_Million"] = round(m, 2)

    # Deaths_New_Per_Million
    N0, m = 0, 0
    d_res = fit_routine(data=data_deaths_new_pm, mode="lin")
    if "fit_res" in d_res:
        N0, m = d_res["fit_res"]
    d_slopes["Slope_Deaths_New_Per_Million"] = round(m, 2)

    # Cases_Last_Week
    # only perform fit of doubling time if more than 100 new cases today and yesterday
    if data_cases_last_week[-1][1] >= 100:
        N0, doubling_time = 0, 0
        d_res = fit_routine(data=data_cases_last_week, mode="exp")
        if "fit_res" in d_res:
            N0, doubling_time = d_res["fit_res"]
            if doubling_time > 1 and doubling_time <= 60:
                d_slopes["DoublingTime_Cases_Last_Week_Per_100000"] = round(
                    doubling_time,
                    1,
                )
                # TODO: DoublingTime_Cases_Last_Week_Per_100000 -> DoublingTime_Cases_Last_Week
    else:
        print(f"not fitting: {data_cases_last_week[-1][1]}")

    return d_slopes


# Fit functions with coefficients as parameters
def fit_function_exp_growth(t, N0, T) -> float:
    """
    N0 = values at t = 0
    T = time it takes for t duplication: f(t+T) = 2 x f(t)
    """
    # previously b = ln(2)/T used, but this is better as T = doubling time is directly returned
    return N0 * np.exp(t * math.log(2) / T)


def fit_function_linear(t, N0, m) -> float:
    """
    y  = N0 + m * t
    N0 : offset / value at t=0 (today)
    m  : slope
    """
    return m * t + N0


def fit_routine(
    data: list,
    mode: str = "exp",
    fit_range_x: tuple = (-np.inf, np.inf),
    fit_range_y: tuple = (-np.inf, np.inf),
) -> dict:
    """
    data: list of x,y pairs
    """
    assert len(data) >= 2
    assert mode in ("exp", "lin")
    (data_x_for_fit, data_y_for_fit) = extract_data_according_to_fit_ranges(
        data,
        fit_range_x,
        fit_range_y,
    )
    if len(data_x_for_fit) < 3:
        return {}
    if mode == "lin":
        fit_function = fit_function_linear
        bounds_lower = (-np.inf, -np.inf)  # low(N0), low(slope)
        bounds_upper = (np.inf, np.inf)  # up (N0), up (slope)
    else:  # mode == "exp"
        fit_function = fit_function_exp_growth
        bounds_lower = (1, -365)  # low(N0), low(T)
        bounds_upper = (np.inf, 365)  # up (N0), up (T)

    d = {}
    # min 3 values in list
    # only if not all y data values are equal
    # and data_y_for_fit.count(data_y_for_fit[0]) < len(data_y_for_fit):
    if len(data_x_for_fit) < 3:
        return {}

    # initial guess of parameters
    if data_y_for_fit[-1] > 0:
        initial_guess_y0 = float(data_y_for_fit[-1])
    else:
        initial_guess_y0 = 10.0

    if mode == "lin":
        p0 = [initial_guess_y0, 1.0]
    else:  # mode = 'exp'
        # for exp we need to know if the slope is pos or negative
        # I have no better idea than performing a linear fit first
        lin_fit_res = curve_fit(fit_function_linear, data_x_for_fit, data_y_for_fit)[0]
        if lin_fit_res[0] > 0:
            initial_guess_y0 = lin_fit_res[0]
        lin_fit_slope_m = lin_fit_res[1]

        if abs(lin_fit_slope_m) < 1.0 / 10:
            # print(f"linear slope too small: {lin_fit_slope_m}")
            return {}

        if lin_fit_slope_m > 0:
            p0 = [initial_guess_y0, 10.0]
        else:
            p0 = [initial_guess_y0, -10.0]

        # print(f"debugging: lin-slope = {lin_fit_slope_m}, y={data_y_for_fit}")

    # Do the actual fitting
    try:
        fit_res, fit_res_cov = curve_fit(
            fit_function,
            data_x_for_fit,
            data_y_for_fit,
            p0,
            # bounds: ( min of all parameters) , (max of all parameters) )
            bounds=(bounds_lower, bounds_upper),
        )

        # y_next_day = fit_function(1, fit_res[0], fit_res[1])
        # y_next_day_delta = y_next_day - data_y_for_fit[-1]
        # factor_increase_next_day = ""
        # if data_y_for_fit[-1] > 0:
        #     factor_increase_next_day = y_next_day / data_y_for_fit[-1]

        d = {"fit_res": fit_res, "fit_res_cov": fit_res_cov}
        # print(f"debugging: fit_res_1 = {fit_res[1]}")
        if mode == "exp" and abs(fit_res[1]) < 1:
            print("T %.2f is very small" % fit_res[1])

    except (RuntimeError, ValueError) as error:
        # Exception, RuntimeWarning
        print(error)
    return d


def series_of_fits(
    data: list,
    fit_range: int = 7,
    max_days_past=14,
    mode="exp",
) -> dict:
    """
    perform a series of fits: per day on data of 7 days back
    fit_range: fit over how many days
    max_days_past: how far in the past shall we go
    = (fitted in range [x-6, x])
    mode: exp or lin
    returns dict: day -> doubling_time (neg for halftime)
    """
    fit_series_res = {}
    # remove y=0 values from start until first non-null
    #    while len(data) > 0 and data[0][1] == 0:
    #        data.pop(0)
    if len(data) < 7:
        return {}
    if -max_days_past < min(data[0]):
        max_days_past = -min(data[0]) - 3
    # range(0, -7, -1): does not include -7, it has only 0,-1,..-6 = 7 values
    for last_day_for_fit in range(0, -max_days_past, -1):
        # this loop starts at t=0 and moves to t=-max_days_past

        # extracting/filtering the data matching the time interval
        (data_x_for_fit, data_y_for_fit) = extract_data_according_to_fit_ranges(
            data,
            fit_range_x=(last_day_for_fit - fit_range + 0.1, last_day_for_fit + 0.1),
            fit_range_y=(-np.inf, np.inf),
        )
        # +0.1 to ensure that last day is included and that lastday - 7 is not included, so 7 days!

        if sum(data_y_for_fit) == 0:
            continue

        # shift x-values to always end with t=x=0
        data_x_for_fit = [x - last_day_for_fit for x in data_x_for_fit]
        data_modified = list(zip(data_x_for_fit, data_y_for_fit))

        # debugging
        # print(last_day_for_fit)
        # if last_day_for_fit == -999:
        #     print("debugging")

        d = fit_routine(data=data_modified, mode=mode)
        # d={} if fit fails
        if len(d) != 0:
            # dict: day -> doubling_time (neg for halftime)
            this_doubling_time = round(d["fit_res"][1], 1)
            fit_series_res[last_day_for_fit] = this_doubling_time
        # else:
        #     print(
        #         f"debugging: last day={last_day_for_fit}, data={data_y_for_fit}")

    return fit_series_res


def read_ref_data_de_states() -> dict[str, Any]:
    """
    read pop etc from ref table and returns it as dict of dict
    """
    d_states_ref: dict[str, Any] = {}
    with open("data/ref_de-states.tsv", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f, delimiter="\t")
        for row in csv_reader:
            d = {
                "State": row["State"],
                "Population": int(row["Population"]),
                "Pop Density": float(row["Pop Density"]),
            }
            d_states_ref[row["Code"]] = d
    return d_states_ref
