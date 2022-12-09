#!/usr/bin/env python3.10
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions
"""
Plots DE Stats and Districts
"""
import datetime as dt
import glob
import locale
import math
import multiprocessing as mp
import os
import time

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

import helper

# Set German date format for plots: Okt instead of Oct

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

timestart = time.time()


# Matplotlib setup
# Agg to prevent "Fail to allocate bitmap"
mpl.use("Agg")  # Cairo


def calc_doubling_time(percent_7day: float) -> float:
    """convert 7-day-increase of incidence into doubling time"""
    tD = -7 / math.log((1 / (percent_7day + 1)), 2)
    return tD


assert calc_doubling_time(1.00) == 7


def plot_layout(fig, axes: list, colors: tuple, thisIsDE_total: bool = False):
    """
    Axis layout, label text and range
    """
    # shared x axis
    # remove label as date is obvious
    axes[1].set_xlabel("")

    # top plot
    axes[0].set_title("Inzidenzwert und -anstieg", fontsize=10)
    axes[1].set_title("Tote und Intensivstationsbelegung", fontsize=10)
    # axis label
    axes[0].set_ylabel("Inzidenz (7 Tage)")
    axes[0].right_ax.set_ylabel("Inzidenzanstieg (7 Tage)")
    axes[1].set_ylabel("Tote (7 Tage pro Millionen)")
    axes[1].right_ax.set_ylabel("Intensivstationen Anteil COVID-Patienten")
    # axis range
    axes[0].set_ylim(
        0,
    )  # 0,550
    axes[0].right_ax.set_ylim(0, 150)
    axes[1].set_ylim(
        0,
    )  # 0,250
    axes[1].right_ax.set_ylim(0, 50)
    # tick freq
    # all are set to make charts better compareable
    # axes[0].yaxis.set_major_locator(mtick.MultipleLocator(50)) # uncommented, since some regions have incidences > 2000 nowadays
    axes[0].right_ax.yaxis.set_major_locator(mtick.MultipleLocator(25))
    axes[1].yaxis.set_major_locator(mtick.MultipleLocator(25))
    axes[1].right_ax.yaxis.set_major_locator(mtick.MultipleLocator(10))
    # tick format
    axes[0].yaxis.set_major_formatter(mtick.FormatStrFormatter("%d"))
    axes[0].right_ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    axes[1].yaxis.set_major_formatter(mtick.FormatStrFormatter("%d"))
    axes[1].right_ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    # color of label and ticks
    axes[0].yaxis.label.set_color(colors[0][0])
    axes[0].tick_params(axis="y", colors=colors[0][0])
    axes[0].right_ax.yaxis.label.set_color(colors[0][1])
    axes[0].right_ax.tick_params(axis="y", colors=colors[0][1])
    axes[1].yaxis.label.set_color(colors[1][0])
    axes[1].tick_params(axis="y", colors=colors[1][0])
    axes[1].right_ax.yaxis.label.set_color(colors[1][1])
    axes[1].right_ax.tick_params(axis="y", colors=colors[1][1])
    # zorder problem
    # 1. per axis
    # 2. per series in axis including grid
    # Problem: can't solve the problem, that data of the secondary y axis is plotted below the grid of the 1st axis
    axes[0].grid(axis="both")
    axes[0].set_zorder(axes[0].right_ax.get_zorder() + 1)
    axes[0].set_axisbelow(True)  # for grid below the lines
    axes[0].right_ax.set_axisbelow(True)  # for grid below the lines
    axes[0].patch.set_visible(False)
    axes[1].set_axisbelow(True)  # for grid below the lines
    axes[1].grid(axis="both")
    axes[1].set_zorder(axes[1].right_ax.get_zorder() + 1)
    axes[1].right_ax.set_axisbelow(True)  # for grid below the lines
    axes[1].patch.set_visible(False)

    # # add label text to bottom right
    helper.mpl_add_text_source(source="RKI and DIVI", date=date_last)
    # plt.gcf().text(
    #     1.0,
    #     0.5,
    #     s="by Torben https://entorb.net , based on RKI and DIVI data",
    #     fontsize=8,
    #     horizontalalignment="right",
    #     verticalalignment="center",
    #     rotation="vertical",
    # )

    # add label text to bottom right
    plt.gcf().text(
        0.97,
        0.5,
        s=(
            "Verdopplungszeit: 25%% : %d Tage, 50%% : %d Tage, 100%% : 7 Tage"
            % (round(calc_doubling_time(0.25), 0), round(calc_doubling_time(0.5), 0))
        ),
        fontsize=8,
        horizontalalignment="right",
        verticalalignment="center",
        color=colors[0][1],
    )

    if thisIsDE_total is False:
        # add label text to bottom left
        plt.gcf().text(
            0.12,
            0.5,
            s=("Vergleich DE-gesamt"),
            fontsize=8,
            horizontalalignment="left",
            verticalalignment="center",
            color=colors[2][0],
        )
        # plt.gcf().text(0.09, 0.055, s=("DE-gesamt"),
        #                fontsize=8, horizontalalignment='left', verticalalignment='center', color=colors[2][1])

    fig.set_tight_layout(True)


def read_data(datafile: str) -> pd.DataFrame:
    #
    # Read and setup data
    #
    df = pd.read_csv(
        datafile,
        sep="\t",
        parse_dates=[
            "Date",
        ],
        index_col="Date",
        usecols=[
            "Date",
            "Cases_Last_Week_Per_Million",
            "Cases_Last_Week_7Day_Percent",
            "Deaths_Last_Week_Per_Million",
            "DIVI_Intensivstationen_Covid_Prozent",
        ],
    )

    df["Inzidenz"] = df["Cases_Last_Week_Per_Million"] / 10
    df.drop(
        columns=[
            "Cases_Last_Week_Per_Million",
        ],
        inplace=True,
    )
    # nicer names for the data colums
    df = df.rename(
        columns={
            "Cases_Last_Week_7Day_Percent": "Inzidenzanstieg",
            "Deaths_Last_Week_Per_Million": "Tote",
            "DIVI_Intensivstationen_Covid_Prozent": "Intensivstationsbelegung",
        },
        errors="raise",
    )
    df[df < 0] = 0
    # drop deaths of last 4 weeks, as they are not final numbers
    date_4w = dt.date.today() - dt.timedelta(weeks=4)
    df.loc[df.index.date >= date_4w, "Tote"] = None
    # negative values -> 0
    return df


# DE as reference
df_DE = read_data(datafile="data/de-states/de-state-DE-total.tsv")

date_last = pd.to_datetime(df_DE.index[-1]).date()


def plot_it(df: pd.DataFrame, code: str, long_name: str, mode: str):
    """
    source: de-states or de-districts
    """

    # Discarded idea:
    # initialize only once, to speedup!
    # TODO: try out if creating once and than using fig = copy.copy(fig_template)
    # to prevent "Fail to allocate bitmap" -> no working
    fig, axes = plt.subplots(
        nrows=2,
        ncols=1,
        sharex=True,
        figsize=(8, 8),
        dpi=100,  # default = 6.4,4.8
    )

    fig.suptitle(f"COVID-19 in {long_name}")  # super title

    # define colors for data
    colors = (("blue", "red"), ("purple", "green"), ("grey", "grey"))

    if code == "DE-total":
        b_thisIsDE_total = True
    else:
        b_thisIsDE_total = False

    #
    # plot the data
    #
    df["Inzidenz"].plot(
        ax=axes[0],
        secondary_y=False,
        color=colors[0][0],
        legend=False,
        zorder=3,
        linewidth=2.0,
    )
    df["Inzidenzanstieg"].plot.area(
        ax=axes[0],
        secondary_y=True,
        color=colors[0][1],
        legend=False,
        zorder=1,
        linewidth=1.0,
    )
    df["Tote"].plot(
        ax=axes[1],
        secondary_y=False,
        color=colors[1][0],
        legend=False,
        zorder=3,
        linewidth=2.0,
    )
    df["Intensivstationsbelegung"].plot.area(
        ax=axes[1],
        secondary_y=True,
        color=colors[1][1],
        legend=False,
        zorder=1,
        linewidth=1.0,
    )

    if b_thisIsDE_total is False:
        global df_DE
        # DE data for comparison
        df_DE["Inzidenz"].plot(
            ax=axes[0],
            secondary_y=False,
            color=colors[2][0],
            legend=False,
            zorder=2,
            linewidth=2.0,
        )
        df_DE["Tote"].plot(
            ax=axes[1],
            secondary_y=False,
            color=colors[2][1],
            legend=False,
            zorder=2,
            linewidth=2.0,
        )

    plot_layout(fig=fig, axes=axes, colors=colors, thisIsDE_total=b_thisIsDE_total)

    # plt.show()

    if mode == "de-states":
        fname = f"plots-python/de-states/de-state-{code}.png"
    elif mode == "de-districts":
        fname = f"plots-python/de-districts/de-district-{code}.png"
    else:
        raise ValueError
    plt.savefig(fname=fname, format="png")

    # cleanup
    fig.clf()
    axes[0].cla()
    axes[1].cla()
    plt.close("all")
    plt.close(fig)
    plt.close()


def doit_bl(datafile: str):
    """for Bundesländer"""
    (filepath, fileName) = os.path.split(datafile)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    code = fileBaseName[9:]
    long_name = helper.d_BL_name_from_BL_Code[code]
    df = read_data(datafile=datafile)
    plot_it(df=df, code=code, long_name=long_name, mode="de-states")


def doit_lk(datafile: str):
    """ "for Landkreise"""
    (filepath, fileName) = os.path.split(datafile)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    code = fileBaseName[-5:]
    if code == "16056":  # Eisenach was merged with 16063: LK Wartburgkreis
        return
    global d_landkreisNames
    long_name = d_landkreisNames[code]
    df = read_data(datafile=datafile)
    plot_it(df=df, code=code, long_name=long_name, mode="de-districts")


d_landkreisNames = helper.read_json_file(
    "data/de-districts/mapping_landkreis_ID_name.json",
)


def main():
    # now via multiprocessing
    pool = mp.Pool(processes=mp.cpu_count())

    # plot for states
    l_pile_of_work = []
    # for datafile in ("data/de-states/de-state-BY.tsv",):
    for datafile in glob.glob("data/de-states/de-state-*.tsv"):
        l_pile_of_work.append(datafile)
        # doit_bl(datafile=datafile)
    res = pool.map(doit_bl, l_pile_of_work)

    # same for districts
    l_pile_of_work = []
    # for datafile in ("data/de-districts/de-district_timeseries-02000.tsv",):
    for datafile in glob.glob("data/de-districts/de-district_timeseries-*.tsv"):
        l_pile_of_work.append(datafile)
        # doit_lk(datafile=datafile)
    res = pool.map(doit_lk, l_pile_of_work)  # noqa: F841


if __name__ == "__main__":
    main()
    print("runtime: %ds on %d CPUs" % (time.time() - timestart, mp.cpu_count()))
# 164s single processing -> 27s multiprocessing
