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
    # if code == "DE-total":
    #     code = "DE"

    if code == 'BW' : long_name = "Baden-Württemberg"
    elif code == 'BY' : long_name = "Bayern"
    elif code == 'BE' : long_name = "Berlin"
    elif code == 'BB' : long_name = "Brandenburg" 
    elif code == 'HB' : long_name = "Bremen"
    elif code == 'HH' : long_name = "Hamburg"
    elif code == 'HE' : long_name = "Hessen"
    elif code == 'MV' : long_name = "Mecklenburg-Vorpommern"
    elif code == 'NI' : long_name = "Niedersachsen"
    elif code == 'NW' : long_name = "Nordrhein-Westfalen"
    elif code == 'RP' : long_name = "Rheinland-Pfalz"
    elif code == 'SL' : long_name = "Saarland"
    elif code == 'SN' : long_name = "Sachsen"
    elif code == 'ST' : long_name = "Sachsen-Anhalt"
    elif code == 'SH' : long_name = "Schleswig-Holstein"
    elif code == 'TH' : long_name = "Thüringen"
    elif code == 'DE-total': long_name = "Deutschland"







    # print(code)
    df = pd.read_csv(datafile, sep="\t")
    df = df[["Date", "Cases_Last_Week_Per_100000",
             "Cases_Last_Week_7Day_Percent","Deaths_Last_Week_Per_Million","DIVI_Intensivstationen_Covid_Prozent"]]
    # use date/current as index
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    df.set_index(['Date'], inplace=True)

    df = df.rename(columns={"Cases_Last_Week_Per_100000": "Inzidenz", "Cases_Last_Week_7Day_Percent": "Inzidenzanstieg", "Deaths_Last_Week_Per_Million": "Tote","DIVI_Intensivstationen_Covid_Prozent":"Intensivstationsbelegung"}, errors="raise")

    # negative -> 0
    df[df < 0] = 0


    # Plot 1: y1: Inzidenz, y2: Cases_Last_Week_7Day_Percent
    plt.suptitle(f"Inzidenzwert und -anstieg in {long_name}") # super title
    plt.title("by Torben https://entorb.net", fontsize=8) 

    ax1 = df.Inzidenz.plot(
        color="blue", legend=False, secondary_y=False, zorder=2)
    ax1.set_zorder(2)
    # important: transparent background for line plot
    ax1.set_facecolor('none')
    ax2 = df.Inzidenzanstieg.plot.area(color="red",
                                                    legend=False, secondary_y=True, zorder=1)
    ax2.set_zorder(1)

    ax1.set_ylim(0, )
    ax2.set_ylim(0, 200)

    # plt.xlabel("")
    ax1.set_xlabel("")
    ax2.set_xlabel("")

    ax1.set_ylabel('Inzidenz (7 Tage)')

    ax1.yaxis.label.set_color('blue')
    ax1.tick_params(axis='y', colors='blue')

    ax2.set_ylabel('Anstieg (7 Tage)')
    ax2.yaxis.label.set_color('red')
    ax2.tick_params(axis='y', colors='red')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter())


    # plt.grid()
    ax1.grid()
    # ax2.grid()
    plt.tight_layout()

    plt.savefig(
        fname=f"plots-python/de-states/{fileBaseName}.png", format='png')
    plt.close()


    # # Plot 2: y1: Inzidenz und , y2: Cases_Last_Week_7Day_Percent
    # plt.suptitle(f"{long_name}") # super title
    # plt.title("by Torben https://entorb.net", fontsize=8) 

    # ax1 = df.Inzidenz.plot(
    #     color="blue", legend=False, secondary_y=False, zorder=1)
    # df.Tote.plot(ax=ax1,color="black", legend=False, secondary_y=False, zorder=2)
    # ax1.set_ylabel("Wochen-Inzidenz und -Tote pro 1.000.000")
    # # ax2 = ax1.twinx()
    # ax2 = df.Intensivstationsbelegung.plot(# ax=ax2,
    #     color="red", legend=False, secondary_y=True, zorder=3)
    # ax2.set_ylabel("Intensivstationsbelegung durch COVID-19")

    # # fig, ax = plt.subplots()  #create figure and axes
    # # ax1 = ax[0]

    # # plt.xlabel("")
    # ax1.set_xlabel("")
    # ax2.set_xlabel("")    

    # # plt.tick_params(direction="in")
    # # ax1.tick_params(direction="in")
    # # ax2.tick_params(direction="in")


    # ax2.yaxis.set_major_formatter(mtick.PercentFormatter())
    # ax2.yaxis.label.set_color('red')
    # ax2.tick_params(axis='y', colors='red')
    # # ax2.legend(['Intensivstationsbelegung'],loc='best')

    # # plt.legend(["Inzidenz", "Tote", "Intensivstationsbelegung"], loc='best')

    # ax1.set_ylim(0, )
    # ax2.set_ylim(0, )

    # # plt.grid()
    # ax1.grid()
    # # ax2.grid()
    # plt.tight_layout()
    # plt.show()
    # break


