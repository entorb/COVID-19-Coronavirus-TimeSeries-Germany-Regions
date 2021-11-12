# plot via pandas and matplotlib
# from matplotlib.colors import LogNorm
import glob
import os
from pandas.core.frame import DataFrame
from math import log
import locale
import matplotlib as mpl
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import pandas as pd
import helper  # my helper modules

# Matplotlib setup
# Agg to prevent "Fail to allocate bitmap"
mpl.use('Agg')  # Cairo
# turn off interactive mode
plt.ioff()


# import numpy as np


# plt.style.use('ggplot')

# DE date format: Okt instead of Oct
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')


d_nameToCode = {
    'BW': "Baden-Württemberg", 'BY': "Bayern", 'BE': "Berlin", 'BB': "Brandenburg", 'HB': "Bremen", 'HH': "Hamburg", 'HE': "Hessen", 'MV': "Mecklenburg-Vorpommern", 'NI': "Niedersachsen", 'NW': "Nordrhein-Westfalen", 'RP': "Rheinland-Pfalz", 'SL': "Saarland", 'SN': "Sachsen", 'ST': "Sachsen-Anhalt", 'SH': "Schleswig-Holstein", 'TH': "Thüringen", 'DE-total': "Deutschland"
}


def calc_doubling_time(percent_7day: float) -> float:
    """ convert 7-day-increase of incidence into doubling time"""
    tD = -7/log((1/(percent_7day+1)), 2)
    return tD


assert calc_doubling_time(1.00) == 7


def plot_layout(fig, axes: list, colors: list, thisIsDE_total: bool = False):
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
    axes[0].set_ylabel('Inzidenz (7 Tage)')
    axes[0].right_ax.set_ylabel('Inzidenzanstieg (7 Tage)')
    axes[1].set_ylabel('Tote (7 Tage pro Millionen)')
    axes[1].right_ax.set_ylabel('Intensivstationen Anteil COVID-Patienten')
    # axis range
    axes[0].set_ylim(0, )  # 0,550
    axes[0].right_ax.set_ylim(0, 150)
    axes[1].set_ylim(0, )  # 0,250
    axes[1].right_ax.set_ylim(0, 40)
    # tick freq
    # all are set to make charts better compareable
    axes[0].yaxis.set_major_locator(ticker.MultipleLocator(50))
    axes[0].right_ax.yaxis.set_major_locator(ticker.MultipleLocator(25))
    axes[1].yaxis.set_major_locator(ticker.MultipleLocator(25))
    axes[1].right_ax.yaxis.set_major_locator(ticker.MultipleLocator(10))
    # tick format
    axes[0].yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    axes[0].right_ax.yaxis.set_major_formatter(
        ticker.PercentFormatter(decimals=0))
    axes[1].yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
    axes[1].right_ax.yaxis.set_major_formatter(
        ticker.PercentFormatter(decimals=0))
    # color of label and ticks
    axes[0].yaxis.label.set_color(colors[0][0])
    axes[0].tick_params(axis='y', colors=colors[0][0])
    axes[0].right_ax.yaxis.label.set_color(colors[0][1])
    axes[0].right_ax.tick_params(axis='y', colors=colors[0][1])
    axes[1].yaxis.label.set_color(colors[1][0])
    axes[1].tick_params(axis='y', colors=colors[1][0])
    axes[1].right_ax.yaxis.label.set_color(colors[1][1])
    axes[1].right_ax.tick_params(axis='y', colors=colors[1][1])
    # zorder problem
    # 1. per axis
    # 2. per series in axis including grid
    # Problem: can't solve the problem, that data of the secondary y axis is plotted below the grid of the 1st axis
    axes[0].grid(axis='both')
    axes[0].set_zorder(axes[0].right_ax.get_zorder()+1)
    axes[0].set_axisbelow(True)  # for grid below the lines
    axes[0].right_ax.set_axisbelow(True)  # for grid below the lines
    axes[0].patch.set_visible(False)
    axes[1].set_axisbelow(True)  # for grid below the lines
    axes[1].grid(axis='both')
    axes[1].set_zorder(axes[1].right_ax.get_zorder()+1)
    axes[1].right_ax.set_axisbelow(True)  # for grid below the lines
    axes[1].patch.set_visible(False)

    # add label text to bottom right
    plt.gcf().text(1.0, 0.5, s="by Torben https://entorb.net , based on RKI and DIVI data", fontsize=8,
                   horizontalalignment='right', verticalalignment='center', rotation='vertical')

    # add label text to bottom right
    plt.gcf().text(0.97, 0.5, s=("Verdopplungszeit: 25%% : %d Tage, 50%% : %d Tage, 100%% : 7 Tage" %
                                 (round(calc_doubling_time(0.25), 0),
                                  round(calc_doubling_time(0.5), 0))
                                 ),
                   fontsize=8, horizontalalignment='right', verticalalignment='center', color=colors[0][1])

    if thisIsDE_total == False:
        # add label text to bottom left
        plt.gcf().text(0.12, 0.5, s=("Vergleich DE-gesamt"),
                       fontsize=8, horizontalalignment='left', verticalalignment='center', color=colors[2][0])
        # plt.gcf().text(0.09, 0.055, s=("DE-gesamt"),
        #                fontsize=8, horizontalalignment='left', verticalalignment='center', color=colors[2][1])

    fig.tight_layout()


def read_data(datafile: str) -> DataFrame:
    #
    # Read and setup data
    #
    df = pd.read_csv(datafile, sep="\t")
    df = df[["Date",
             "Cases_Last_Week_Per_Million",
             "Cases_Last_Week_7Day_Percent",
             "Deaths_Last_Week_Per_Million",
             "DIVI_Intensivstationen_Covid_Prozent"]]

    # use date/current as index
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df.set_index(['Date'], inplace=True)

    df["Inzidenz"] = df["Cases_Last_Week_Per_Million"]/10
    df.drop("Cases_Last_Week_Per_Million", axis=1, inplace=True)
    # nicer names for the data colums
    df = df.rename({
        "Cases_Last_Week_7Day_Percent": "Inzidenzanstieg",
        "Deaths_Last_Week_Per_Million": "Tote",
        "DIVI_Intensivstationen_Covid_Prozent": "Intensivstationsbelegung"
    }, axis=1, errors="raise")
    # negative values -> 0
    df[df < 0] = 0
    return df


def plot_it(df: DataFrame, code: str, long_name: str, source: str):
    """
    source: de-states or de-districts
    """

    # Discarded idea:
    # initialize only once, to speedup!
    # to prevent "Fail to allocate bitmap" -> no working
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(8, 8)  # default = 6.4,4.8
                             , dpi=100
                             )

    fig.suptitle(f"COVID-19 in {long_name}")  # super title

    # define colors for data
    colors = (('blue', 'red'), ('purple', 'green'), ('grey', 'grey'))

    if code == "DE-total":
        b_thisIsDE_total = True
    else:
        b_thisIsDE_total = False

    #
    # plot the data
    #
    df["Inzidenz"].plot(ax=axes[0], color=colors[0][0], legend=False,
                        secondary_y=False, zorder=3, linewidth=2.0)
    df["Inzidenzanstieg"].plot.area(
        ax=axes[0], color=colors[0][1], legend=False, secondary_y=True, zorder=1)
    df["Tote"].plot(ax=axes[1], color=colors[1][0], legend=False,
                    secondary_y=False, zorder=3, linewidth=2.0)
    df["Intensivstationsbelegung"].plot.area(
        ax=axes[1], color=colors[1][1], legend=False, secondary_y=True, zorder=1, linewidth=2.0)

    if b_thisIsDE_total == False:
        # DE data for comparison
        df_DE["Inzidenz"].plot(ax=axes[0], color=colors[2][0], legend=False,
                               secondary_y=False, zorder=2, linewidth=2.0)
    if b_thisIsDE_total == False:
        # DE data for comparison
        df_DE["Tote"].plot(ax=axes[1], color=colors[2][1], legend=False,
                           secondary_y=False, zorder=2, linewidth=2.0)

    plot_layout(fig=fig, axes=axes, colors=colors,
                thisIsDE_total=b_thisIsDE_total)

    # plt.show()

    if source == "de-states":
        fname = f"plots-python/de-states/de-state-{code}.png"
    elif source == "de-districts":
        fname = f"plots-python/de-districts/de-district-{code}.png"
    plt.savefig(
        fname=fname, format='png')

    # cleanup
    fig.clf()
    axes[0].cla()
    axes[1].cla()
    plt.close('all')
    plt.close(fig)
    plt.close()


# DE as reference
df_DE = read_data(datafile="data/de-states/de-state-DE-total.tsv")


# plot for states
# for datafile in ("data/de-states/de-state-BY.tsv",):
for datafile in glob.glob("data/de-states/de-state-*.tsv"):
    (filepath, fileName) = os.path.split(datafile)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    code = fileBaseName[9:]
    long_name = d_nameToCode[code]

    df = read_data(datafile=datafile)

    plot_it(df=df, code=code,
            long_name=long_name, source="de-states")


d_landkreisNames = helper.read_json_file(
    "data/de-districts/mapping_landkreis_ID_name.json")

# same for districts
# for datafile in ("data/de-districts/de-district_timeseries-02000.tsv",):
for datafile in glob.glob("data/de-districts/de-district_timeseries-*.tsv"):
    (filepath, fileName) = os.path.split(datafile)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    code = fileBaseName[-5:]
    if code == "16056":  # Eisenach was merged with 16063: LK Wartburgkreis
        continue
    long_name = d_landkreisNames[code]

    df = read_data(datafile=datafile)

    print(code, long_name)
    plot_it(df, code, long_name, "de-districts")
