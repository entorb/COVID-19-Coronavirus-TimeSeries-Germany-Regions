# plot via pandas and matplotlib
# from matplotlib.colors import LogNorm
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import locale
# import numpy as np

import helper  # my helper modules


# plt.style.use('ggplot')

# DE date format: Okt instead of Oct
locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')


d_nameToCode = {
    'BW': "Baden-Württemberg", 'BY': "Bayern", 'BE': "Berlin", 'BB': "Brandenburg", 'HB': "Bremen", 'HH': "Hamburg", 'HE': "Hessen", 'MV': "Mecklenburg-Vorpommern", 'NI': "Niedersachsen", 'NW': "Nordrhein-Westfalen", 'RP': "Rheinland-Pfalz", 'SL': "Saarland", 'SN': "Sachsen", 'ST': "Sachsen-Anhalt", 'SH': "Schleswig-Holstein", 'TH': "Thüringen", 'DE-total': "Deutschland"
}


for datafile in glob.glob("data/de-states/de-state-*.tsv"):
    # for datafile in ("data/de-states/de-state-DE-total.tsv",):
    (filepath, fileName) = os.path.split(datafile)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    code = fileBaseName[9:]
    long_name = d_nameToCode[code]

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

    #
    # initialize plot
    #
    fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, figsize=(8, 8)  # default = 6.4,4.8
                             , dpi=100
                             )

    fig.suptitle(f"COVID-19 in {long_name}")  # super title
    axes[0].set_title("Inzidenzwert und -anstieg", fontsize=10)
    axes[1].set_title("Tote und Intensivstationsbelegung", fontsize=10)

    # define colors for data
    colors = (('blue', 'red'), ('purple', 'green'))

    #
    # plot the data
    #
    df["Inzidenz"].plot(ax=axes[0], color=colors[0][0], legend=False,
                        secondary_y=False, zorder=2, linewidth=2.0)
    df["Inzidenzanstieg"].plot.area(
        ax=axes[0], color=colors[0][1], legend=False, secondary_y=True, zorder=1)
    df["Tote"].plot(ax=axes[1], color=colors[1][0], legend=False,
                    secondary_y=False, zorder=2, linewidth=2.0)
    df["Intensivstationsbelegung"].plot.area(
        ax=axes[1], color=colors[1][1], legend=False, secondary_y=True, zorder=1, linewidth=2.0)

    #
    # Axis layout, text and range
    #

    # axes[0].autoscale()
    axes[0].set_ylim(0, 550)
    axes[0].right_ax.set_ylim(0, 200)
    axes[1].set_ylim(0, 250)
    axes[1].right_ax.set_ylim(0, 50)

    axes[0].set_ylabel('Inzidenz (7 Tage)')
    axes[0].yaxis.label.set_color(colors[0][0])
    axes[0].tick_params(axis='y', colors=colors[0][0])
    axes[1].set_ylabel('Tote (7 Tage pro Millionen)')
    axes[1].yaxis.label.set_color(colors[1][0])
    axes[1].tick_params(axis='y', colors=colors[1][0])
    axes[1].grid(zorder=0)

    axes[0].right_ax.set_ylabel(
        'Inzidenzanstieg (7 Tage)')
    axes[0].right_ax.yaxis.label.set_color(colors[0][1])
    axes[0].right_ax.tick_params(axis='y', colors=colors[0][1])
    axes[0].right_ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    axes[1].right_ax.set_ylabel(
        'Intensivstationen Anteil COVID-Patienten')
    axes[1].right_ax.yaxis.label.set_color(colors[1][1])
    axes[1].right_ax.tick_params(axis='y', colors=colors[1][1])
    axes[1].right_ax.yaxis.set_major_formatter(mtick.PercentFormatter())

    axes[1].set_xlabel("")

    # zorder problem
    # 1. per axis
    # 2. per series in axis including grid
    # Problem: can't solve the problem, that data of the seconday y axis is plotted below the grid of the 1st axis
    axes[0].grid(zorder=-1)
    axes[1].grid(zorder=-1)

    axes[0].set_zorder(axes[0].right_ax.get_zorder()+1)
    axes[0].patch.set_visible(False)
    axes[1].set_zorder(axes[1].right_ax.get_zorder()+1)
    axes[1].patch.set_visible(False)

    # print(axes[0].get_zorder(), axes[0].right_ax.get_zorder())
    # axes[0].grid(zorder=0)
    # axes[0].set_zorder(2)
    # axes[0].right_ax.set_zorder(1)
    # axes[0].set_facecolor('none')
    # # axes[1].grid(zorder=0)
    # axes[1].set_zorder(2)
    # axes[1].right_ax.set_zorder(1)
    # axes[1].set_facecolor('none')

    # add text to bottom right
    plt.gcf().text(1.0, 0.5, s="by Torben https://entorb.net , based on RKI and DIVI data", fontsize=8,
                   horizontalalignment='right', verticalalignment='center', rotation='vertical')

    fig.tight_layout()
    # plt.show()

    plt.savefig(
        fname=f"plots-python/de-states/{fileBaseName}.png", format='png')
    plt.close()
