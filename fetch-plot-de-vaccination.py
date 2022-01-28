#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This script downloads COVID-19 vaccination data by RKI from
https://github.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/blob/master/Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen.csv
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"


# Built-in/Generic Imports
import urllib.request

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker
import locale

# my helper modules
import helper


# DE date format: Okt instead of Oct
locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

dataFileSource = "cache\de-vaccination.csv"

if not helper.check_cache_file_available_and_recent(
    fname=dataFileSource,
    max_age=0,  # 0s because git pulled files are "new"
    verbose=False,
):
    url = "https://raw.githubusercontent.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/master/Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen.csv"
    filedata = urllib.request.urlopen(url)
    datatowrite = filedata.read()
    with open(dataFileSource, mode="wb") as f:
        f.write(datatowrite)


df = pd.read_csv(dataFileSource, sep=",")
df = helper.pandas_set_date_index(df=df, date_column="Impfdatum")

sum_doses = df["Anzahl"].sum()

# sum
df_doses_per_day = df.groupby(["Impfdatum"])["Anzahl"].sum().reset_index()
df_doses_per_day = helper.pandas_set_date_index(
    df=df_doses_per_day, date_column="Impfdatum"
)

date_last = pd.to_datetime(df.index[-1]).date()

# 1 gefiltert auf Erst-Impfungen
df1 = df[df["Impfserie"] == 1]
df1 = df1.groupby(["Impfdatum"])["Anzahl"].sum().reset_index()
df1 = helper.pandas_set_date_index(df=df1, date_column="Impfdatum")
df_doses_per_day["Anzahl1"] = df1["Anzahl"]
del df1

# 2 gefiltert auf Zweit-Impfungen
df2 = df[df["Impfserie"] == 2]
df2 = df2.groupby(["Impfdatum"])["Anzahl"].sum().reset_index()
df2 = helper.pandas_set_date_index(df=df2, date_column="Impfdatum")
df2 = df2[df2.index >= "2021-01-10"]
df_doses_per_day["Anzahl2"] = df2["Anzahl"]
del df2

# 3 gefiltert auf Dritt-Impfungen
df3 = df[df["Impfserie"] == 3]
df3 = df3.groupby(["Impfdatum"])["Anzahl"].sum().reset_index()
df3 = helper.pandas_set_date_index(df=df3, date_column="Impfdatum")
df3 = df3[df3.index >= "2021-08-25"]

df_doses_per_day["Anzahl3"] = df3["Anzahl"]
del df3


# add rolling averages
df_doses_per_day = helper.pandas_calc_roll_av(
    df=df_doses_per_day, column="Anzahl", days=7
)
df_doses_per_day = helper.pandas_calc_roll_av(
    df=df_doses_per_day, column="Anzahl1", days=7
)
df_doses_per_day = helper.pandas_calc_roll_av(
    df=df_doses_per_day, column="Anzahl2", days=7
)
df_doses_per_day = helper.pandas_calc_roll_av(
    df=df_doses_per_day, column="Anzahl3", days=7
)

# initialize plot (
axes = [
    "",
]
fig, axes[0] = plt.subplots(
    nrows=1, ncols=1, sharex=True, dpi=100, figsize=(8, 6)  # default = 6.4,4.8
)

fig.suptitle(f"COVID-19 Impfungen in Deutschland (7-Tagesmittel)")

# plot
df_doses_per_day["Anzahl_roll_av"].plot(
    ax=axes[0],
    # color=colors[0][0],
    legend=False,
    secondary_y=False,
    zorder=2,
    linewidth=2.0,
)
df_doses_per_day["Anzahl1_roll_av"].plot(
    ax=axes[0],
    # color=colors[0][0],
    legend=False,
    secondary_y=False,
    zorder=2,
    linewidth=2.0,
)
df_doses_per_day["Anzahl2_roll_av"].plot(
    ax=axes[0],
    # color=colors[0][0],
    legend=False,
    secondary_y=False,
    zorder=2,
    linewidth=2.0,
)
df_doses_per_day["Anzahl3_roll_av"].plot(
    ax=axes[0],
    # color=colors[0][0],
    legend=False,
    secondary_y=False,
    zorder=2,
    linewidth=2.0,
)

axes[0].set_ylim(
    0,
)
axes[0].set_xlabel("")
# axes[0].set_title("7-Tagesmittel", fontsize=10)
axes[0].set_zorder(1)
axes[0].grid(zorder=0)
# axes[0].patch.set_visible(False)

# add text to bottom right
helper.mpl_add_text_source(source="RKI", date=date_last)


plt.legend(("Gesamt", "Erstimpfungen", "Zweitimpfungen", "Drittimpfungen"))

axes[0].get_yaxis().set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ","))
)

fig.tight_layout()

# plt.show()
# pass


plt.savefig(fname=f"plots-python/de-vaccination.png", format="png")
plt.close()
