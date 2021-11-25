#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
fetches mortality data from Destatis
see https://www.destatis.de/DE/Themen/Querschnitt/Corona/Gesellschaft/bevoelkerung-sterbefaelle.html
data: https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/Tabellen/sonderauswertung-sterbefaelle.html;jsessionid=3B59CB1FA0C08C059243535606A41FBF.internet8721
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
# import codecs
# import urllib
# import requests
# import csv
# import json
# import requests
import os

import pandas as pd
import openpyxl

# import csv
import urllib.request

from pandas.core.frame import DataFrame

# my helper modules
import helper


# 1. read my covid data
# 1.1 after de-states-V2 only 1 day is missing: add 0 data for missing 01.01.2020
l = [0] * 1  # 1 day
df1 = pd.DataFrame(data={"Deaths_Covid": l})

# read my data
df0 = pd.read_csv("data/de-states/de-state-DE-total.tsv", sep="\t")

# extract only date and Death_New columns
df2 = pd.DataFrame()
df2["Date"] = df0["Date"]
df2["Deaths_Covid"] = df0["Deaths_New"]
del df0

# remove 29.2.
df2 = df2[~df2["Date"].isin(("2020-02-29", "2024-02-29", "2028-02-29"))]

# ensure first row is from 02.01. (for prepending only 1 missing day)
assert df2.iloc[0]["Date"] == "2020-01-02", (
    "Error of start date, expecting 2020-01-02, got : " + df2.iloc[0]["Date"]
)

# prepend 1.1.2020
df3 = DataFrame()
df3["Deaths_Covid"] = df1["Deaths_Covid"].append(df2["Deaths_Covid"], ignore_index=True)

del df1, df2
df3["Deaths_Covid_roll"] = (
    df3["Deaths_Covid"].rolling(window=7, min_periods=1).mean().round(1)
)


df_covid_2020 = (
    df3[0 : 1 * 365]
    .reset_index(drop=True)
    .rename(
        {
            "Deaths_Covid": "Deaths_Covid_2020",
            "Deaths_Covid_roll": "Deaths_Covid_2020_roll",
        },
        axis=1,
        errors="raise",
    )
)

df_covid_2021 = (
    df3[1 * 365 : 2 * 365]
    .reset_index(drop=True)
    .rename(
        {
            "Deaths_Covid": "Deaths_Covid_2021",
            "Deaths_Covid_roll": "Deaths_Covid_2021_roll",
        },
        axis=1,
        errors="raise",
    )
)


# pd.DataFrame()
# df_covid_2020["Deaths_Covid_2020"] = df1["Deaths_Covid"].append(
#     df2["Deaths_Covid"], ignore_index=True
# )
# df_covid_2020["Deaths_Covid_2020_roll"] = (
#     df_covid_2020["Deaths_Covid_2020"].rolling(window=7, min_periods=1).mean().round(1)
# )
# df_covid_2021 = (
#     df_covid_2020[1 * 365 :].rename(
#         {
#             "Deaths_Covid_2020": "Deaths_Covid_2021",
#             "Deaths_Covid_2020_roll": "Deaths_Covid_2021_roll",
#         },
#         axis=1,
#         errors="raise",
#     )
# ).reset_index()
# print(df_covid_2021.tail())
# exit()

# 2. fetch and parse Excel of mortality data from Destatis

excelFile = "cache\de-mortality.xlsx"


if not helper.check_cache_file_available_and_recent(
    fname=excelFile, max_age=1800, verbose=False
):
    url = "https://www.destatis.de/DE/Themen/Gesellschaft-Umwelt/Bevoelkerung/Sterbefaelle-Lebenserwartung/Tabellen/sonderauswertung-sterbefaelle.xlsx?__blob=publicationFile"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(excelFile, mode="wb") as f:
        f.write(datatowrite)


# data_only : read values instead of formulas
workbookIn = openpyxl.load_workbook(excelFile, data_only=True)
sheetIn = workbookIn["D_2016_2021_Tage"]

l_dates = []
l_deaths2021 = []
l_deaths2020 = []
l_deaths2019 = []
l_deaths2018 = []
l_deaths2017 = []
l_deaths2016 = []
for col in range(2, 368):
    day = sheetIn.cell(column=col, row=9).value
    # we skip the 29.02. for each year
    if day == "29.02.":
        continue
    l_dates.append(day)
    l_deaths2021.append(sheetIn.cell(column=col, row=10).value)
    l_deaths2020.append(sheetIn.cell(column=col, row=11).value)
    l_deaths2019.append(sheetIn.cell(column=col, row=12).value)
    l_deaths2018.append(sheetIn.cell(column=col, row=13).value)
    l_deaths2017.append(sheetIn.cell(column=col, row=14).value)
    l_deaths2016.append(sheetIn.cell(column=col, row=15).value)


data = zip(
    l_dates,
    l_deaths2016,
    l_deaths2017,
    l_deaths2018,
    l_deaths2019,
    l_deaths2020,
    l_deaths2021,
)

df = pd.DataFrame(data, columns=["Day", "2016", "2017", "2018", "2019", "2020", "2021"])

df["2016_roll"] = df["2016"].rolling(window=7, min_periods=1).mean().round(1)
df["2017_roll"] = df["2017"].rolling(window=7, min_periods=1).mean().round(1)
df["2018_roll"] = df["2018"].rolling(window=7, min_periods=1).mean().round(1)
df["2019_roll"] = df["2019"].rolling(window=7, min_periods=1).mean().round(1)
df["2020_roll"] = df["2020"].rolling(window=7, min_periods=1).mean().round(1)
df["2021_roll"] = df["2021"].rolling(window=7, min_periods=1).mean().round(1)
df["2016_2019_mean"] = df.iloc[:, [1, 2, 3, 4]].mean(axis=1)  # not column 0 = day
df["2016_2019_mean_roll"] = (
    df["2016_2019_mean"].rolling(window=7, min_periods=1).mean().round(1)
)

df["2016_2019_roll_max"] = df.iloc[:, [7, 8, 9, 10]].max(axis=1)
df["2016_2019_roll_min"] = df.iloc[:, [7, 8, 9, 10]].min(axis=1)

df = df.join(df_covid_2020).join(df_covid_2021)
print(df.tail(100))

df.to_csv("data/de-mortality.tsv", sep="\t", index=False)
