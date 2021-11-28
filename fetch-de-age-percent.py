from typing import DefaultDict
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import matplotlib.ticker as mtick
import datetime as dt

# import urllib.request
import requests


import helper


def read_alterstrukur() -> DataFrame:
    """
    read Alterstruktur for DE
    """
    file = "data/DE_Bevoelkerung_nach_Altersgruppen-ges.tsv"

    df = pd.read_csv(file, sep="\t")
    # print(df)

    df.set_index("Altersgruppe", inplace=True)

    df = df.rename(
        {
            "Personen": "Bevölkerung",
        },
        axis=1,
        errors="raise",
    )
    de_sum = df["Bevölkerung"].loc["Summe"]
    df.drop("Summe", inplace=True)
    df["Bev_Proz"] = (df["Bevölkerung"] / de_sum * 100).round(1)
    return df


def read_rki_cases() -> DataFrame:
    """
    read Excel file and perform some transformations
    here the date is in columns and the age group is in rows
    -> transpose to
    date as rows and age group as columns
    index: yearweek: 202014 für 2020 cw14
    """
    excelFile = "cache\de-rki-Altersverteilung.xlsx"
    df = pd.read_excel(
        open(excelFile, "rb"), sheet_name="Fallzahlen", engine="openpyxl"
    )
    df.set_index("Altersgruppe", inplace=True)

    # # time-series of 7-Tage-Inzidenz might be intersting as well...
    # excelFile = "cache\de-rki-Altersverteilung.xlsx"
    # df_rki_inzidenz = pd.read_excel(
    #     open(excelFile, "rb"), sheet_name="7-Tage-Inzidenz", engine="openpyxl"
    # )
    # df_rki_inzidenz.set_index("Altersgruppe", inplace=True)
    # print(df_rki_inzidenz.head())

    # rename column header from 2020_14 to YearWeek : 202014 (int) etc.
    l2 = []
    for c in df.columns:
        year = int(c[0:4])
        week = int(c[5:7])
        l2.append(year * 100 + week)
    df.columns = l2

    # transpose to have yearweek as index
    # print(df.head())
    df = df.transpose()
    df.index.name = "YearWeek"
    # print(df.head())

    # rename column headers
    l2 = []
    for c in df.columns:
        c = c.replace(" - ", "-")
        l2.append(c)
    df.columns = l2

    # print(df.head())
    return df


def read_rki_deaths() -> DataFrame:
    """
    read Excel file and perform some transformations
    here the date is in rows and the age group is in columns
    index: yearweek: 202014 für 2020 cw14
    """
    excelFile = "cache\de-rki-COVID-19_Todesfaelle.xlsx"

    df = pd.read_excel(
        open(excelFile, "rb"), sheet_name="COVID_Todesfälle_KW_AG10", engine="openpyxl"
    )

    # RKI uses "<4" for values 1,2,3, fixing this via assuming 1
    # TODO: calc replacement based on sum over all ages (Sheet: COVID_Todesfälle)
    df.replace(
        to_replace="<4", value=1, inplace=True, limit=None, regex=False, method="pad"
    )

    # convert str to int for all data columns
    for col in df.columns:
        df[col] = df[col].astype(int)

    # add YearWeek as index
    df["YearWeek"] = df["Sterbejahr"] * 100 + df["Sterbewoche"]

    df.set_index("YearWeek", inplace=True)
    df = df.drop(["Sterbejahr", "Sterbewoche"], axis="columns")
    return df


def read_divi() -> DataFrame:
    """
    read CSV file and perform some transformations
    here the date is in rows and the age group is in columns
    index: yearweek: 202014 für 2020 cw14
    """
    file_local = "cache/de-divi/bund-covid-altersstruktur-zeitreihe_ab-2021-04-29.csv"

    df = pd.read_csv(file_local, sep=",")
    df["Date"] = df["Datum"].str[0:10]
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df["Year"] = pd.DatetimeIndex(df["Date"]).year
    # FutureWarning: weekofyear and week have been deprecated, please use DatetimeIndex.isocalendar().week instead
    # df["Week"] = pd.DatetimeIndex(df["Date"]).week
    # df["Week"] = df["Date"].isocalendar().week
    df["Week"] = df["Date"].map(lambda v: pd.to_datetime(v).isocalendar()[1])
    df["YearWeek"] = df["Year"] * 100 + df["Week"]
    df = df.drop(["Bundesland", "Datum", "Week", "Year", "Date"], axis="columns")

    # print(df)

    # rename column headers
    # rename column headers by extracting some int values from a string
    l2 = []
    for col in df.columns:
        col = (
            col.replace("Stratum_", "").replace("_Bis_", "-").replace("80_Plus", "80+")
        )
        l2.append(col)
    df.columns = l2

    # group by and mean / average
    df = df.groupby(["YearWeek"]).mean()
    # .round(1)
    # df["sum"] = df.sum(axis=1)
    # .round(1)
    # print(df)

    return df


def filter_rki_cases(df_rki, start_yearweek: int = 202001, end_yearweek: int = 203053):
    """
    filters on yearweek
    returns DF, sum_cases
    """
    # optionally: filter on date range
    df_rki = df_rki[df_rki.index >= start_yearweek]
    df_rki = df_rki[df_rki.index <= end_yearweek]

    # calc sum and drop column
    sum_cases = df_rki["Gesamt"].sum()
    df_rki = df_rki.drop(
        "Gesamt",
        axis="columns",
    )
    print(f"{sum_cases} Fälle")

    d = {}
    for col in df_rki.columns:
        d[col] = df_rki[col].sum()

    d2 = {
        "0-9": df_rki["0-4"].sum() + df_rki["5-9"].sum(),
        "10-19": df_rki["10-14"].sum() + df_rki["15-19"].sum(),
        "20-29": df_rki["20-24"].sum() + df_rki["25-29"].sum(),
        "30-39": df_rki["30-34"].sum() + df_rki["35-39"].sum(),
        "40-49": df_rki["40-44"].sum() + df_rki["45-49"].sum(),
        "50-59": df_rki["50-54"].sum() + df_rki["55-59"].sum(),
        "60-69": df_rki["60-64"].sum() + df_rki["65-69"].sum(),
        "70-79": df_rki["70-74"].sum() + df_rki["75-79"].sum(),
        "80-89": df_rki["80-84"].sum() + df_rki["85-89"].sum(),
        "80+": df_rki["80-84"].sum() + df_rki["85-89"].sum() + df_rki["90+"].sum(),
    }
    # merge dicts
    d.update(d2)
    df = pd.DataFrame.from_dict(d, orient="index", columns=["Covid_Fälle"])
    df["Covid_Fälle_Proz"] = (df["Covid_Fälle"] / sum_cases * 100).round(1)

    # print(df)
    return (df, sum_cases)


def filter_rki_deaths(df_rki, start_yearweek: int = 202001, end_yearweek: int = 203053):
    """
    returns df, sum
    """
    # optionally: filter on date range
    df_rki = df_rki[df_rki.index >= start_yearweek]
    df_rki = df_rki[df_rki.index <= end_yearweek]

    # calc sum
    sum_death = 0
    for col in df_rki.columns:
        sum_death += df_rki[col].sum()
    print(f"{sum_death} Deaths")

    d = {
        "0-9": df_rki["AG 0-9 Jahre"].sum(),
        "10-19": df_rki["AG 10-19 Jahre"].sum(),
        "20-29": df_rki["AG 20-29 Jahre"].sum(),
        "30-39": df_rki["AG 30-39 Jahre"].sum(),
        "40-49": df_rki["AG 40-49 Jahre"].sum(),
        "50-59": df_rki["AG 50-59 Jahre"].sum(),
        "60-69": df_rki["AG 60-69 Jahre"].sum(),
        "70-79": df_rki["AG 70-79 Jahre"].sum(),
        "80+": df_rki["AG 80-89 Jahre"].sum() + df_rki["AG 90+ Jahre"].sum(),
        "80-89": df_rki["AG 80-89 Jahre"].sum(),
        "90+": df_rki["AG 90+ Jahre"].sum(),
    }
    df = pd.DataFrame.from_dict(d, orient="index", columns=["Covid_Tote"])
    df["Covid_Tote_Proz"] = (df["Covid_Tote"] / sum_death * 100).round(3)
    # print(df)

    return (df, sum_death)


def filter_divi(df_divi, start_yearweek: int = 202001, end_yearweek: int = 203053):

    print(df_divi)

    # optionally: filter on date range
    df_divi = df_divi[df_divi.index >= start_yearweek]
    df_divi = df_divi[df_divi.index <= end_yearweek]

    # sum_icu = 0
    # for col in df_divi.columns:
    #     sum_icu += df_divi[col].sum()
    # print(f"{sum_icu} ICU")

    # print(df_divi)
    # df = df_divi["sum"].mean()
    # df[]
    # print(df_divi)
    # exit()

    d = {}
    for col in df_divi.columns:
        d[col] = df_divi[col].mean()

    df = pd.DataFrame.from_dict(d, orient="index", columns=["ICU"])
    print(df)
    # sum_icu includes the unknown age fraction
    sum_icu = int(df["ICU"].sum())
    df = df.drop(["Unbekannt"], axis="index")
    # sum_icu does not include the unknown age fraction
    sum_icu2 = int(df["ICU"].sum())
    df["ICU"] = df["ICU"].round(0).astype(int)
    df.loc["0-9"] = df.loc["17_Minus"] / 2
    df.loc["10-19"] = df.loc["17_Minus"] / 2
    df.loc["20-29"] = df.loc["18-29"]

    df["ICU_Proz"] = (df["ICU"] / sum_icu2 * 100).round(1)

    # print(df)

    # exit()

    return df, sum_icu


def plotit(df, outfile, title_time, sum_cases: int, sum_deaths: int, sum_icu: int):
    # select subset of columns
    df = df[["Bev_Proz", "Covid_Fälle_Proz", "ICU_Proz", "Covid_Tote_Proz"]]
    # drop null value rows
    df = df.dropna()
    # print(df)
    # manually drop some rows
    # df = df.drop("80-89").drop("90+")

    myPlot = df.plot.barh(
        legend=True,
        use_index=True,
        linewidth=2.0,
        zorder=1,
        width=0.8,
        color=["green", "blue", "red", "black"],
        figsize=(9, 6),
    )
    plt.legend(
        [
            "Anteil ges. Bevölkerung",
            "Anteil ges. Covid Fälle",
            "Anteil Intensivbetten (gemittelt)",
            "Anteil ges. Covid Tote",
        ]
    )

    plt.gca().invert_yaxis()
    # myPlot.set_xlim(0.1, 100)
    # plt.gca().set_xscale("log")
    myPlot.set_xlim(0, 68)
    plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter())
    plt.gca().xaxis.set_major_locator(mtick.MultipleLocator(5))

    plt.title(
        f"Covid pro Altersgruppe in DE {title_time}\n{sum_cases} Fälle, {sum_deaths} Tote, {sum_icu} ICU Betten (gemittelt)"
    )

    # plt.xlabel("Prozent")
    plt.grid(axis="x")
    plt.ylabel("Alter (Jahre)")
    plt.tight_layout()
    plt.savefig(fname=f"plots-python/{outfile}.png", format="png")


def main():
    # fetch_rki_cases()
    file_local = "cache/de-rki-Altersverteilung.xlsx"
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Altersverteilung.xlsx?__blob=publicationFile"
    helper.download_from_url_if_old(url=url, file_local=file_local)

    # fetch_rki_deaths()
    file_local = "cache/de-rki-COVID-19_Todesfaelle.xlsx"
    url = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Projekte_RKI/COVID-19_Todesfaelle.xlsx?__blob=publicationFile"
    helper.download_from_url_if_old(url=url, file_local=file_local)

    # fetch_divi()
    file_local = "cache/de-divi/bund-covid-altersstruktur-zeitreihe_ab-2021-04-29.csv"
    url = "https://diviexchange.blob.core.windows.net/%24web/bund-covid-altersstruktur-zeitreihe_ab-2021-04-29.csv"
    helper.download_from_url_if_old(url=url, file_local=file_local)

    df_rki_deaths = read_divi()

    df_alterstrukur = read_alterstrukur()
    df_rki_cases = read_rki_cases()
    df_rki_deaths = read_rki_deaths()
    df_divi_icu = read_divi()

    start_year = 2020
    start_week = 1
    end_year = 2021
    end_week = 25

    df_cases, sum_cases = filter_rki_cases(
        df_rki=df_rki_cases,
        start_yearweek=start_year * 100 + start_week,
        end_yearweek=end_year * 100 + end_week,
    )
    df_deaths, sum_deaths = filter_rki_deaths(
        df_rki=df_rki_deaths,
        start_yearweek=start_year * 100 + start_week,
        end_yearweek=end_year * 100 + end_week,
    )
    df_icu, sum_icu = filter_divi(
        df_divi=df_divi_icu,
        start_yearweek=start_year * 100 + start_week,
        end_yearweek=end_year * 100 + end_week,
    )

    df = df_cases.join([df_deaths, df_alterstrukur, df_icu])
    # print(df)
    plotit(
        df=df,
        outfile="de_age_percent_1_pre_2021_summer",
        title_time="bis Sommer 2021",
        sum_cases=sum_cases,
        sum_deaths=sum_deaths,
        sum_icu=sum_icu,
    )

    start_year = 2021
    start_week = 26
    end_year = 2030
    end_week = 1

    df_cases, sum_cases = filter_rki_cases(
        df_rki=df_rki_cases,
        start_yearweek=start_year * 100 + start_week,
        end_yearweek=end_year * 100 + end_week,
    )
    df_deaths, sum_deaths = filter_rki_deaths(
        df_rki=df_rki_deaths,
        start_yearweek=start_year * 100 + start_week,
        end_yearweek=end_year * 100 + end_week,
    )
    df_icu, sum_icu = filter_divi(
        df_divi=df_divi_icu,
        start_yearweek=start_year * 100 + start_week,
        end_yearweek=end_year * 100 + end_week,
    )

    df = df_cases.join([df_deaths, df_alterstrukur, df_icu])
    # print(df)
    plotit(
        df=df,
        outfile="de_age_percent_2_post_2021_summer",
        title_time="seit Sommer 2021",
        sum_cases=sum_cases,
        sum_deaths=sum_deaths,
        sum_icu=sum_icu,
    )


if __name__ == "__main__":
    main()
