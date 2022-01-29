#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is my test playground and template for new scripts
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import datetime as dt

# Further Modules
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# My Helper Functions
import helper

# Set German date format for plots: Okt instead of Oct
import locale

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


df_covid = pd.read_csv(
    "data/de-states/de-state-DE-total.tsv",
    sep="\t",
    usecols=[
        "Date",
        "Cases_Last_Week_Per_Million",
        "Deaths_New",
        "DIVI_Intensivstationen_Covid_Prozent",
    ],  # only load these columns
    parse_dates=[
        "Date",
    ],  # convert to date object if format is yyyy-mm-dd
    index_col="Date",  # choose this column as index
)
df_covid["Inzidenz"] = df_covid["Cases_Last_Week_Per_Million"] / 10
df_covid.drop(columns="Cases_Last_Week_Per_Million", inplace=True)
df_covid.rename(
    columns={
        "Deaths_New": "Deaths_Covid",
        "DIVI_Intensivstationen_Covid_Prozent": "ICU_pct",
    },
    inplace=True,
)
# not for ICU!
# df_covid.fillna(0, inplace=True)

# reordering
df_covid = df_covid[["Inzidenz", "ICU_pct", "Deaths_Covid"]]
df_covid = helper.pandas_calc_roll_av(df=df_covid, column="Deaths_Covid", days=7)
print(df_covid)


df_mortality = pd.read_csv(
    "data/ts-de-mortality.tsv",
    sep="\t",
    parse_dates=[
        "Date",
    ],  # convert to date object if format is yyyy-mm-dd
    index_col="Date",  # choose this column as index
)
# print(df_mortality)


df_vaccination = pd.read_csv(
    "data/ts-de-vaccination.tsv",
    sep="\t",
    usecols=[
        "Date",
        "Anzahl",
    ],
    parse_dates=[
        "Date",
    ],  # convert to date object if format is yyyy-mm-dd
    index_col="Date",  # choose this column as index
)
# print(df_vaccination)


df_mutations = pd.read_csv(
    "data/ts-de-mutations.tsv",
    sep="\t",
    parse_dates=[
        "Date",
    ],  # convert to date object if format is yyyy-mm-dd
    index_col="Date",  # choose this column as index
)
# print(df_mutations)

# df = pd.DataFrame()

df_covid.drop(columns=["Deaths_Covid"], inplace=True)
df_mortality.drop(columns=["Deaths"], inplace=True)


def plotit():
    # initialize plot
    axes = [None]
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True, dpi=100, figsize=(8, 20))

    date_last = pd.to_datetime(df_covid.index[-1]).date()

    i = 0
    df_covid["Inzidenz"].plot(
        ax=axes[i],
        # color=colors[i],
        legend=False,
        secondary_y=False,
        # zorder=2,
        linewidth=2.0,
    )
    i += 1

    helper.mpl_add_text_source(source="RKI", date=date_last)
    fig.set_tight_layout(True)
    fig.savefig(fname=f"plots-python/de-ts-multi.png", format="png")
    plt.close()


df = df_covid.join(df_mortality).join(df_vaccination).join(df_mutations)
# no not for ICU
# df.fillna(0, inplace=True)

# print(df)
# print(df.columns)

if __name__ == "__main__":
    pass
"""
plot:
df_covid
 Inzidenz
 ICU_pct
 Deaths_Covid_roll_av


"""
