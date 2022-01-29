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

# Further Modules
# import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

# My Helper Functions
import helper

# Set German date format for plots: Okt instead of Oct
import locale

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


def fetch_and_prepare_data() -> pd.DataFrame:
    dataFileSource = "cache\de-vaccination.csv"

    helper.download_from_url_if_old(
        url="https://raw.githubusercontent.com/robert-koch-institut/COVID-19-Impfungen_in_Deutschland/master/Aktuell_Deutschland_Bundeslaender_COVID-19-Impfungen.csv",
        file_local=dataFileSource,
        max_age=3600,
        verbose=True,
    )

    df0 = pd.read_csv(
        dataFileSource,
        sep=",",
        parse_dates=[
            "Impfdatum",
        ],
    )

    # df of doses per day
    # cols: total, dose1, dose2,...
    df = df0.groupby(["Impfdatum"])["Anzahl"].sum().reset_index()
    df = helper.pandas_set_date_index(df=df, date_column="Impfdatum")
    # rename index
    df.index.name = "Date"

    # add a series filtered on the vaccination dose nummer 1..3
    for vac_dose_no in range(1, 3 + 1, 1):
        df_tmp = df0[df0["Impfserie"] == vac_dose_no]
        df_tmp = df_tmp.groupby(["Impfdatum"])["Anzahl"].sum().reset_index()
        df_tmp = helper.pandas_set_date_index(df=df_tmp, date_column="Impfdatum")
        df["Dose" + str(vac_dose_no)] = df_tmp["Anzahl"]
    del df_tmp, vac_dose_no

    # set missing values to 0
    df.fillna(0, inplace=True)

    # add rolling averages
    cols = df.columns
    for c in cols:
        df = helper.pandas_calc_roll_av(df=df, column=c, days=7)
    del cols
    df.to_csv("data/ts-de-vaccination.tsv", sep="\t", index=True, line_terminator="\n")

    return df


def plotit(df: pd.DataFrame):
    # initialize plot
    axes = [None]
    fig, axes[0] = plt.subplots(nrows=1, ncols=1, sharex=True, dpi=100, figsize=(8, 6))

    date_last = pd.to_datetime(df.index[-1]).date()
    colors = []
    # sum_doses = df["Anzahl"].sum()

    # plot
    l1_cols = df.columns
    l2_cols_roll_av = [elem for elem in l1_cols if "_roll_av" in elem]
    i = 0
    for c in l2_cols_roll_av:
        df[c].plot(
            ax=axes[0],
            # color=colors[i],
            legend=False,
            secondary_y=False,
            # zorder=2,
            linewidth=2.0,
        )
        colors.append(axes[0].lines[i].get_color())
        i += 1

    # print(colors)

    # Labels
    fig.suptitle("COVID-19 Impfungen in Deutschland (7-Tagesmittel)")
    axes[0].legend(("Gesamt", "Erstimpfungen", "Zweitimpfungen", "Drittimpfungen"))
    axes[0].set_xlabel("")

    # y min to 0
    axes[0].set_ylim(0, None)
    # axes[0].set_title("7-Tagesmittel", fontsize=10)

    # grid
    # axes[0].set_zorder(1)
    axes[0].grid(zorder=0)
    # axes[0].patch.set_visible(False)

    # tick formatting: "1,000,000"
    axes[0].yaxis.set_major_formatter(
        mtick.FuncFormatter(lambda x, p: format(int(x), ","))
    )

    helper.mpl_add_text_source(source="RKI", date=date_last)
    fig.set_tight_layout(True)
    fig.savefig(fname=f"plots-python/de-vaccination.png", format="png")
    plt.close()


if __name__ == "__main__":
    df = fetch_and_prepare_data()
    plotit(df)
