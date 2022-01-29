#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 vaccination data by RKI from
https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Testzahl.html
-> 
https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Testzahlen-gesamt.xlsx?__blob=publicationFile
"""

# Built-in/Generic Imports
import datetime as dt

# Further Modules
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import locale

# My Helper Functions
import helper

# DE date format: Okt instead of Oct
locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


excelFile = "cache/de-rki-pcr-Testzahlen-gesamt.xlsx"

# as file is stored in cache folder which is not part of the commit, we can use the caching here
helper.download_from_url_if_old(
    url="https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Testzahlen-gesamt.xlsx?__blob=publicationFile",
    file_local=excelFile,
    max_age=3600,
    verbose=True,
)


# if not helper.check_cache_file_available_and_recent(
#     fname=f"cache/rki-pcr-Testzahlen-gesamt.xlsx",
#     max_age=1800,
#     verbose=True,
# ):
#     fetch()


df = pd.read_excel(
    open(excelFile, "rb"), sheet_name="1_Testzahlerfassung", engine="openpyxl"
)

# drop first row
df.drop(
    [
        0,
    ],
    inplace=True,
)

df.drop(df.tail(1).index, inplace=True)  # drop last n rows

# df[["week", "year"]] = df["Kalenderwoche"].str.split("/", expand=True)

# 51/2021 -> date of sunday
def convert2date(s: str) -> dt.date:
    year, week = s.split("/")
    date = dt.date.fromisocalendar(int(week), int(year), 7)
    return date


df["Date"] = df["Kalenderwoche"].apply(lambda x: convert2date(x))

df = helper.pandas_set_date_index(df=df, date_column="Date")


df["TestsMill"] = df["Anzahl Testungen"] / 1e6
df["PosRate"] = 100.0 * df["Positiv getestet"] / df["Anzahl Testungen"]

# df = df[["Anzahl Testungen", "Positiv getestet"]]

# df = df[["Anzahl Testungen", "Positiv getestet"]]
print(df.tail())

# plot
fig, ax = plt.subplots(figsize=(8, 6))
colors = ["blue", "red"]
df["TestsMill"].plot(ax=ax, linewidth=2.0, legend=False, color=colors[0])
df["PosRate"].plot(
    ax=ax, secondary_y=True, linewidth=2.0, legend=False, color=colors[1]
)

ax.set_ylim(
    0,
)
ax.right_ax.set_ylim(
    0,
)

plt.title(f"Anzahl PCR-Tests und Positv-Rate in DE", loc="center")
ax.set_ylabel("PCR Tests (Mill pro Woche)", color=colors[0])
ax.right_ax.set_ylabel("Positiv-Rate", color=colors[1])

ax.tick_params(axis="y", colors=colors[0])
ax.right_ax.tick_params(colors=colors[1])
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

plt.gcf().autofmt_xdate()
# TODO: neither is working
ax.xaxis.set_label("")
plt.xlabel("")

ax.grid(axis="both")
date_last = pd.to_datetime(df.index[-1]).date()
helper.mpl_add_text_source(source="RKI", date=date_last)
plt.tight_layout()
plt.savefig(fname=f"plots-python/de-pcr-tests.png", format="png")
plt.close()
