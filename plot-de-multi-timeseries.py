#!/usr/bin/env python3.9
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions

"""
This is my test playground and template for new scripts
"""

# Built-in/Generic Imports
import datetime as dt
from this import d

# Further Modules
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick


# My Helper Functions
import helper

# Set German date format for plots: Okt instead of Oct
import locale

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


def read_data_covid():
    df = pd.read_csv(
        "data/de-states/de-state-DE-total.tsv",
        sep="\t",
        usecols=[
            "Date",
            "Cases_Last_Week_Per_Million",
            "Deaths_New",
            "DIVI_Intensivstationen_Covid_Prozent",
            "Cases_Last_Week_7Day_Percent",
        ],  # only load these columns
        parse_dates=[
            "Date",
        ],  # convert to date object if format is yyyy-mm-dd
        index_col="Date",  # choose this column as index
    )
    df["Inzidenz"] = df["Cases_Last_Week_Per_Million"] / 10
    df.drop(columns="Cases_Last_Week_Per_Million", inplace=True)
    df.rename(
        columns={
            "Deaths_New": "Deaths_Covid",
            "DIVI_Intensivstationen_Covid_Prozent": "ICU_pct",
            "Cases_Last_Week_7Day_Percent": "InzidenzChange",
        },
        inplace=True,
        errors="raise",
    )

    # filter out some values
    # df.loc[df.index.date < pd.to_datetime("2020-03-01"), "InzidenzChange"] = None
    df.loc[df.index < pd.Timestamp("2020-03-01"), "InzidenzChange"] = None

    # drop deaths of last 4 weeks, as they are not final yet
    df.loc[
        df.index >= pd.Timestamp(dt.date.today() - dt.timedelta(weeks=4)),
        "Deaths_Covid",
    ] = None

    # not for ICU!
    # df.fillna(0, inplace=True)

    df = helper.pandas_calc_roll_av(df=df, column="Deaths_Covid", days=7)
    df.drop(columns=["Deaths_Covid"], inplace=True)
    return df


def read_data_mortality():
    df = pd.read_csv(
        "data/ts-de-mortality.tsv",
        sep="\t",
        parse_dates=[
            "Date",
        ],  # convert to date object if format is yyyy-mm-dd
        index_col="Date",  # choose this column as index
    )
    df = df[df.index >= pd.to_datetime("2020-01-01")]
    df.drop(columns=["Deaths"], inplace=True)
    return df


def read_data_vaccination():
    df = pd.read_csv(
        "data/ts-de-vaccination.tsv",
        sep="\t",
        usecols=[
            "Date",
            "Anzahl_roll_av",
            "Dose1_roll_av",
            "Dose2_roll_av",
            "Dose3_roll_av",
        ],
        parse_dates=[
            "Date",
        ],  # convert to date object if format is yyyy-mm-dd
        index_col="Date",  # choose this column as index
    )
    df.rename(
        columns={
            "Anzahl_roll_av": "Anzahl_Impfungen_ges",
        },
        inplace=True,
    )
    return df


def read_data_pcr():
    df = pd.read_csv(
        "data/ts-de-pcr-tests.tsv",
        sep="\t",
        parse_dates=[
            "Date",
        ],  # convert to date object if format is yyyy-mm-dd
        index_col="Date",  # choose this column as index
    )
    # df.ffill(inplace=True)
    return df


def read_data_mutations():
    df = pd.read_csv(
        "data/ts-de-mutations.tsv",
        sep="\t",
        parse_dates=[
            "Date",
        ],  # convert to date object if format is yyyy-mm-dd
        index_col="Date",  # choose this column as index
    )
    return df

    return df_covid, df_mortality, df_vaccination, df_pcr, df_mutations


# df.ffill(inplace=True)
# no not for ICU
# df.fillna(0, inplace=True)

# print(df)
# print(df.columns)


# print(df.columns)


def plotit(df: pd.DataFrame):
    # initialize plot
    axes = [None]

    num_plots = 9
    fig, axes = plt.subplots(
        nrows=num_plots, ncols=1, sharex=True, dpi=100, figsize=(10, 20)
    )

    date_last = pd.to_datetime(df_covid.index[-1]).date()

    i = 0
    axes[i].set_title("Inzidenz")
    df["Inzidenz"].plot(
        ax=axes[i],
        linewidth=2.0,
    )

    i += 1
    axes[i].set_title("Wöchentliche PCR Test (in Millionen)")
    df["TestsMill"].dropna().plot(
        ax=axes[i],
        linewidth=2.0,
    )

    i += 1
    axes[i].set_title("PCR Positiv-Rate")
    df["PosRate"].dropna().plot(
        ax=axes[i],
        linewidth=2.0,
    )
    axes[i].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    i += 1
    axes[i].set_title("Anteil COVID-Patienten auf den Intensivstationen")
    df["ICU_pct"].plot(
        ax=axes[i],
        linewidth=2.0,
    )
    axes[i].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

    i += 1
    axes[i].set_title("Impfungen (in Millionen, 7-Tages-Mittel)")
    (df["Anzahl_Impfungen_ges"] / 1000000).plot(
        ax=axes[i],
        legend=True,
        linewidth=2.0,
    )
    (df["Dose1_roll_av"] / 1000000).plot(
        ax=axes[i],
        legend=True,
        linewidth=2.0,
    )
    (df["Dose2_roll_av"] / 1000000).plot(
        ax=axes[i],
        legend=True,
        linewidth=2.0,
    )
    (df["Dose3_roll_av"] / 1000000).plot(
        ax=axes[i],
        legend=True,
        linewidth=2.0,
    )
    axes[i].legend(("Gesamt", "Erstimpfungen", "Zweitimpfungen", "Drittimpfungen"))

    i += 1
    df["Deaths_Covid_roll_av"].plot(
        ax=axes[i],
        linewidth=2.0,
    )
    axes[i].set_title("Tägliche COVID Opfer (7-Tages-Mittel)")

    i += 1
    axes[i].set_title("Tägliche Todesfälle alle Ursachen (7-Tages-Mittel)")
    df["Deaths_roll_av"].plot(
        ax=axes[i],
        linewidth=2.0,
    )

    i += 1
    axes[i].set_title("Sequenzierte Virus Mutanten (7-Tages-Mittel)")
    for mutation in df_mutations.columns[1:9]:
        df[mutation].plot(
            ax=axes[i],
            legend=True,
            linewidth=2.0,
        )

    i += 1
    axes[i].set_title("7-Tages-Inzidenzanstieg")
    df["InzidenzChange"].plot(
        ax=axes[i],
        # color=colors[i],
        legend=False,
        secondary_y=False,
        # zorder=2,
        linewidth=2.0,
    )
    axes[i].yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
    axes[i].set_ylim(0, 100)

    # layout tuning
    for i in range(0, num_plots):
        axes[i].set_xlabel("")
        axes[i].grid(zorder=0)
        if i != 6:  # Deaths_roll_av
            axes[i].set_ylim(0, None)

    #    axes2 = axes[0].twiny()

    axes[0].tick_params(
        axis="x", bottom=False, top=True, labelbottom=False, labeltop=True
    )

    axes[4].tick_params(
        # axis="x", bottom=False, top=True, labelbottom=False, labeltop=True
        axis="x",
        bottom=True,
        top=False,
        labelbottom=True,
        labeltop=False,
    )

    for i in range(0, num_plots):
        axes[i].xaxis.set_major_locator(mdates.MonthLocator(interval=1))

    helper.mpl_add_text_source(source="RKI, DIVI, Destatis", date=date_last)
    fig.set_tight_layout(True)
    fig.savefig(fname=f"plots-python/de-multi-timeseries.png", format="png")

    axes[0].set_xlim(dt.date.today() - dt.timedelta(days=180), None)
    fig.savefig(fname=f"plots-python/de-multi-timeseries-180.png", format="png")

    plt.close()


if __name__ == "__main__":
    df_covid = read_data_covid()
    df_mortality = read_data_mortality()
    df_vaccination = read_data_vaccination()
    df_pcr = read_data_pcr()
    df_mutations = read_data_mutations()

    # merge
    df = (
        df_covid.join(df_mortality).join(df_vaccination).join(df_pcr).join(df_mutations)
    )

    plotit(df)


"""
plot:
df_covid
 Inzidenz
 ICU_pct
 Deaths_Covid_roll_av

df_mortality
 Deaths_roll_av

df_vaccination
 Anzahl_Impfungen_ges

df_pcr
 TestsMill
 PosRate
"""
