#!/usr/bin/env python3
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions

"""
This script downloads COVID-19 vaccination data by RKI from
https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Testzahl.html
-> 
https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Testzahlen-gesamt.xlsx?__blob=publicationFile
"""

# Built-in/Generic Imports
import datetime as dt

# Further Modules
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

# My Helper Functions
import helper

# Set German date format for plots: Okt instead of Oct
import locale

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


# 51/2021 -> date of sunday
def convert2date(s: str) -> dt.date:
    year, week = s.split("/")
    date = dt.date.fromisocalendar(int(week), int(year), 7)
    return date


def fetch_and_prepare_data() -> pd.DataFrame:
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

    df["Date"] = df["Kalenderwoche"].apply(lambda x: convert2date(x))

    df = helper.pandas_set_date_index(df=df, date_column="Date")

    df2 = pd.DataFrame()
    df2["TestsMill"] = (df["Anzahl Testungen"] / 1e6).round(3)
    df2["PosRate"] = (100.0 * df["Positiv getestet"] / df["Anzahl Testungen"]).round(3)
    # df2["TestsMill"] =

    df2.to_csv("data/ts-de-pcr-tests.tsv", sep="\t", index=True, line_terminator="\n")

    return df2


def plotit(df: pd.DataFrame):
    # initialize plot
    axes = [None]
    fig, axes[0] = plt.subplots(nrows=1, ncols=1, sharex=True, dpi=100, figsize=(8, 6))

    # plot
    df["TestsMill"].plot(ax=axes[0], secondary_y=False, linewidth=2.0, legend=False)
    df["PosRate"].plot(ax=axes[0], secondary_y=True, linewidth=2.0, legend=False)

    colors = []
    colors.append(axes[0].lines[0].get_color())
    colors.append(axes[0].right_ax.lines[0].get_color())
    # overwrite color 2
    colors[1] = "green"
    axes[0].right_ax.lines[0].set_color(colors[1])

    # Labels
    fig.suptitle("Anzahl PCR-Tests und Positv-Rate in DE")
    axes[0].set_ylabel("PCR Tests (Mill pro Woche)", color=colors[0])
    axes[0].right_ax.set_ylabel("Positiv-Rate", color=colors[1])
    axes[0].set_xlabel("")

    # y min to 0
    axes[0].set_ylim(0, None)
    axes[0].right_ax.set_ylim(0, None)

    # grid
    # axes[0].set_zorder(1)
    axes[0].grid(zorder=0)
    # axes[0].patch.set_visible(False)
    # axes[0].grid(axis="both")

    # tick color
    axes[0].tick_params(axis="y", colors=colors[0])
    axes[0].right_ax.tick_params(colors=colors[1])

    # tick formatting
    axes[0].right_ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    date_last = pd.to_datetime(df.index[-1]).date()
    helper.mpl_add_text_source(source="RKI", date=date_last)
    fig.set_tight_layout(True)
    plt.savefig(fname=f"plots-python/de-pcr-tests.png", format="png")
    plt.close()


if __name__ == "__main__":
    df = fetch_and_prepare_data()
    plotit(df)
