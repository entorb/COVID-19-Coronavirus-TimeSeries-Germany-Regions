# plot via pandas and matplotlib
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import locale

# my helper modules
import helper

# DE date format: Okt instead of Oct
locale.setlocale(locale.LC_ALL, 'de_DE')

for datafile in glob.glob("data/de-states/de-state-*.tsv"):
    (filepath, fileName) = os.path.split(datafile)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    code = fileBaseName[9:]
    if code == "DE-total":
        code = "DE"
    # print(code)
    df = pd.read_csv(datafile, sep="\t")
    df = df[["Date", "Cases_Last_Week_Per_100000",
             "Cases_Last_Week_7Day_Percent"]]
    # use date/current as index
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df.set_index(['Date'], inplace=True)

    # negative -> 0
    df[df < 0] = 0

    ax1 = df.Cases_Last_Week_Per_100000.plot(
        color="blue", legend=False, secondary_y=False, zorder=2)
    ax1.set_zorder(2)
    # important: transparent background for line plot
    ax1.set_facecolor('none')
    ax2 = df.Cases_Last_Week_7Day_Percent.plot.area(color="red",
                                                    legend=False, secondary_y=True, zorder=1)
    ax2.set_zorder(1)

    ax1.set_ylim(0, )
    ax2.set_ylim(0, 200)

    # plt.xlabel("")
    ax1.set_xlabel("")
    ax2.set_xlabel("")

    ax1.set_ylabel('Inzidenz (7 Tage)')
    ax2.set_ylabel('Anstieg (7 Tage)')

    ax1.yaxis.label.set_color('blue')
    ax1.tick_params(axis='y', colors='blue')
    ax2.yaxis.label.set_color('red')
    ax2.tick_params(axis='y', colors='red')
    plt.title(f"Inzidenzwert und -anstieg in {code}")

    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())

    plt.grid()
    plt.tight_layout()

    plt.savefig(
        fname=f"plots-python/de-states/{fileBaseName}.png", format='png')
    plt.close()
