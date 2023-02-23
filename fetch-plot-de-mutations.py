#!/usr/bin/env python3.10
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions
"""
This script downloads German SARS-COV-2 Mutation data from
https://github.com/robert-koch-institut/SARS-CoV-2-Sequenzdaten_aus_Deutschland/"
and plots them
siehe auch https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Omikron-Faelle/Omikron-Faelle.html?__blob=publicationFile
"""
import datetime as dt
import locale
import subprocess  # noqa: S404

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd

import helper

# Set German date format for plots: Okt instead of Oct

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")


# TODO. replace by helper.download_from_url_if_old(
def fetch() -> None:
    """
    Download data from rki github account.
    """
    for fname in (
        "SARS-CoV-2-Sequenzdaten_Deutschland",
        "SARS-CoV-2-Entwicklungslinien_Deutschland",
    ):
        url = f"https://github.com/robert-koch-institut/SARS-CoV-2-Sequenzdaten_aus_Deutschland/blob/master/{fname}.csv.xz?raw=true"
        filepath = f"cache/rki-mutation-sequences/{fname}.csv.xz"

        # this will always download, since the extraction of the .xz file removes the source
        # hence helper.check_cache_file_available_and_recent is used below
        helper.download_from_url_if_old(
            url=url,
            file_local=filepath,
            max_age=3600,
            verbose=False,
        )
        # filedata = urllib.request.urlopen(url)
        # datatowrite = filedata.read()
        # with open(filepath, mode="wb") as f:
        #     f.write(datatowrite)

        # extract the .xz file
        subprocess.run(  # noqa: S607,S603
            ["xz", "-d", "-f", filepath],
            capture_output=False,
            text=False,
        )


if not helper.check_cache_file_available_and_recent(
    fname="cache/rki-mutation-sequences/SARS-CoV-2-Sequenzdaten_Deutschland.csv",
    max_age=3600,
    verbose=True,
):
    fetch()


def read_data() -> pd.DataFrame:
    # read data from CSV
    df1 = pd.read_csv(
        "cache/rki-mutation-sequences/SARS-CoV-2-Sequenzdaten_Deutschland.csv",
        sep=",",
        usecols=["IMS_ID", "RECEIVE_DATE"],
        parse_dates=[
            "RECEIVE_DATE",  # ("DATE_DRAW", "RECEIVE_DATE", "PROCESSING_DATE"):
        ],
        index_col="IMS_ID",
    )
    df2 = pd.read_csv(
        "cache/rki-mutation-sequences/SARS-CoV-2-Entwicklungslinien_Deutschland.csv",
        sep=",",
        usecols=["IMS_ID", "lineage", "scorpio_call"],
        index_col="IMS_ID",
    )

    # join dfs on ID column IMS_ID
    df = df1.join(df2)
    del df1, df2
    print(df.head)

    df.rename(columns={"RECEIVE_DATE": "Date"}, inplace=True)

    # remove word "Probable" from scorpio_call for better clustering
    df["scorpio_call"] = df["scorpio_call"].replace(
        to_replace=r"^Probable ",
        value="",
        regex=True,
    )

    return df


df_all_data = read_data()

# max_date = df_all_data["PROCESSING_DATE"].max()
# print(max_date)

# 2a. group and count by lineage and date columns
df_lineages_alltime = (
    df_all_data.groupby(["lineage", "Date"]).size().reset_index(name="count")
)

df_lineages_lastmonth = df_lineages_alltime[
    df_lineages_alltime["Date"].dt.date >= (dt.date.today() - dt.timedelta(days=62))
]

df_lineages_top_ten_alltime = (
    df_lineages_alltime.groupby("lineage")
    .sum(numeric_only=True)
    .sort_values(by="count", ascending=False)
    .head(10)
)
# df_lineages_top_ten_alltime.to_csv(
#     "cache/rki-mutation-sequences/out-ranking-lineage.csv"
# )

df_lineages_top_ten_lastmonth = (
    df_lineages_alltime.groupby("lineage")
    .sum(numeric_only=True)
    .sort_values(by="count", ascending=False)
)
df_lineages_top_ten_lastmonth = df_lineages_top_ten_lastmonth.head(10)

# # 2b. group and count by scorpio and date columns
# df_scorpio_alltime = (
#     df_all_data.groupby(["scorpio_call", "Date"]).size().reset_index(name="count")
# )

# # date_month = dt.date.today() - dt.timedelta(days=30)
# df_scorpio_lastmonth = df_scorpio_alltime[
#     df_scorpio_alltime["Date"].dt.date >= (dt.date.today() - dt.timedelta(days=62))
# ]

# df_scorpio_top_ten_alltime = (
#     df_scorpio_alltime.groupby("scorpio_call")
#     .sum()
#     .sort_values(by="count", ascending=False)
#     .head(50)
# )
# # df_scorpio_top_ten_alltime.to_csv(
# #     "cache/rki-mutation-sequences/out-ranking-scorpio_call.csv"
# # )

# df_scorpio_top_ten_lastmonth = (
#     df_scorpio_lastmonth.groupby("scorpio_call")
#     .sum()
#     .sort_values(by="count", ascending=False)
# )
# df_scorpio_top_ten_lastmonth = df_scorpio_top_ten_lastmonth.head(6)


# 3. sum df

# 3.1 add column of total number of sequences per day
df_sum_alltime = df_lineages_alltime.groupby("Date").sum(numeric_only=True)
df_sum_lastmonth = df_lineages_lastmonth.groupby("Date").sum(numeric_only=True)
# df_sum_alltime = df_scorpio_alltime.groupby("Date").sum()
# df_sum_lastmonth = df_scorpio_lastmonth.groupby("Date").sum()

df_sum_alltime.set_index(pd.DatetimeIndex(df_sum_alltime.index))
df_sum_lastmonth.set_index(pd.DatetimeIndex(df_sum_lastmonth.index))


df_sum_alltime = df_sum_alltime.rename(
    columns={
        "count": "sequences_total",
    },
    errors="raise",
)
df_sum_lastmonth = df_sum_lastmonth.rename(
    columns={
        "count": "sequences_total",
    },
    errors="raise",
)


def filter_timeseries_df_on_lineages(df: pd.DataFrame, lineage_name: str):
    df2 = df[df["lineage"] == lineage_name]
    df2 = df2.groupby("Date")["count"].sum()
    df2 = df2.to_frame()
    return df2


def filter_timeseries_df_on_scorpio_call(df: pd.DataFrame, scorpio_call: str):
    df2 = df[df["scorpio_call"] == scorpio_call]
    df2 = df2.groupby("Date")["count"].sum()
    df2 = df2.to_frame()
    return df2


# # these are not used
# df_date_sum["omicon BA.1"] = filter_timeseries_df_on_lineages(
#     df=df_lineages, lineage_name="BA.1"
# )["count"]
# df_date_sum["delta B.1.1.7"] = filter_timeseries_df_on_lineages(
#     df=df_lineages, lineage_name="B.1.1.7"
# )["count"]


# 4.1 add the top mutations to the sum df
for c in df_lineages_top_ten_alltime.index:
    a = filter_timeseries_df_on_lineages(df=df_lineages_alltime, lineage_name=c)
    b = a["count"]
    df_sum_alltime[c] = b


for c in df_lineages_top_ten_lastmonth.index:
    a = filter_timeseries_df_on_lineages(df=df_lineages_lastmonth, lineage_name=c)
    b = a["count"]
    df_sum_lastmonth[c] = b


# # 4.2 add the top mutations to the sum df
# for c in df_scorpio_top_ten_alltime.index:
#     a = filter_timeseries_df_on_scorpio_call(df=df_scorpio_alltime, scorpio_call=c)
#     b = a["count"]
#     df_sum_alltime[c] = b


# for c in df_scorpio_top_ten_lastmonth.index:
#     a = filter_timeseries_df_on_scorpio_call(df=df_scorpio_lastmonth, scorpio_call=c)
#     b = a["count"]
#     df_sum_lastmonth[c] = b


# replace missing / na values by 0
df_sum_alltime.fillna(0, inplace=True)
df_sum_lastmonth.fillna(0, inplace=True)


# print(df_sum_alltime)

# 5.1 convert to percent
df_pct_alltime = df_sum_alltime.copy()
for c in df_lineages_top_ten_alltime.index:
    df_pct_alltime[c] = 100.0 * df_pct_alltime[c] / df_pct_alltime["sequences_total"]
df_pct_lastmonth = df_sum_lastmonth.copy()
for c in df_lineages_top_ten_lastmonth.index:
    df_pct_lastmonth[c] = (
        100.0 * df_pct_lastmonth[c] / df_pct_lastmonth["sequences_total"]
    )
# # 5.2 convert to percent
# df_pct_alltime = df_sum_alltime.copy()
# for c in df_scorpio_top_ten_alltime.index:
#     df_pct_alltime[c] = 100.0 * df_pct_alltime[c] / df_pct_alltime["sequences_total"]
# df_pct_lastmonth = df_sum_lastmonth.copy()
# for c in df_scorpio_top_ten_lastmonth.index:
#     df_pct_lastmonth[c] = (
#         100.0 * df_pct_lastmonth[c] / df_pct_lastmonth["sequences_total"]
#     )


# calc 7-day moving average
df_sum_alltime_roll_av = df_sum_alltime.copy()
df_pct_alltime_roll_av = df_pct_alltime.copy()
df_sum_lastmonth_roll_av = df_sum_lastmonth.copy()
df_pct_lastmonth_roll_av = df_pct_lastmonth.copy()

for c in df_sum_alltime_roll_av.columns:
    df_sum_alltime_roll_av[c] = (
        df_sum_alltime_roll_av[c].rolling(window=7, min_periods=1).mean().round(1)
    )
    df_pct_alltime_roll_av[c] = (
        df_pct_alltime_roll_av[c].rolling(window=7, min_periods=1).mean().round(5)
    )

for c in df_sum_lastmonth_roll_av.columns:
    df_sum_lastmonth_roll_av[c] = (
        df_sum_lastmonth_roll_av[c].rolling(window=7, min_periods=1).mean().round(1)
    )
    df_pct_lastmonth_roll_av[c] = (
        df_pct_lastmonth_roll_av[c].rolling(window=7, min_periods=1).mean().round(5)
    )


df_sum_alltime_roll_av.to_csv(
    "data/ts-de-mutations.tsv",
    sep="\t",
    index=True,
    lineterminator="\n",
)


def plot_format(fig, axes, date_last, filename) -> None:
    # Labels
    plt.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
    axes[0].set_xlabel("")

    # grid
    axes[0].grid(zorder=0)

    helper.mpl_add_text_source(source="RKI", date=date_last)
    fig.set_tight_layout(True)
    fig.savefig(fname=filename, format="png")

    # remove all lines
    while len(axes[0].lines) > 0:
        axes[0].get_lines().remove(axes[0].lines[0])
    # plt.cla()
    # plt.clf()
    plt.close()


def plotit() -> None:
    plotit1()
    plotit2()
    plotit3()


def plotit1() -> None:
    # initialize plot
    axes = [None]
    fig, axes[0] = plt.subplots(nrows=1, ncols=1, sharex=True, dpi=100, figsize=(8, 6))

    df = df_pct_alltime
    assert df.index.dtype == "datetime64[ns]"
    date_last = pd.to_datetime(df.index[-1]).date()
    # print(df.index.dtype)

    for c in df_lineages_top_ten_alltime.index:
        df[c].plot(linewidth=1.0, legend=True)
    # for c in df_scorpio_top_ten_alltime.index:
    #     df[c].plot(linewidth=1.0, legend=True)

    fig.suptitle("SARS-CoV-2 Mutationen in DE: Anteile")
    # y min to 0
    axes[0].set_ylim(0, 100)
    # tick formatter
    axes[0].get_yaxis().set_major_formatter(mtick.PercentFormatter(decimals=0))
    plot_format(fig, axes, date_last, filename="plots-python/mutations-de-all.png")


def plotit2() -> None:
    # initialize plot
    axes = [None]
    fig, axes[0] = plt.subplots(nrows=1, ncols=1, sharex=True, dpi=100, figsize=(8, 6))

    df = df_pct_lastmonth
    assert df.index.dtype == "datetime64[ns]"
    date_last = pd.to_datetime(df.index[-1]).date()

    for c in df_lineages_top_ten_lastmonth.index:
        df[c].plot(linewidth=2.0, legend=True)
    # for c in df_scorpio_top_ten_lastmonth.index:
    #     df[c].plot(linewidth=2.0, legend=True)
    fig.suptitle("SARS-CoV-2 Mutationen in DE: Anteile letzte 2 Monate")
    # y min to 0
    axes[0].set_ylim(0, 100)
    # tick formatter
    axes[0].get_yaxis().set_major_formatter(mtick.PercentFormatter(decimals=0))
    plot_format(
        fig,
        axes,
        date_last,
        filename="plots-python/mutations-de-lastmonth.png",
    )


def plotit3() -> None:
    # initialize plot
    axes = [None]
    fig, axes[0] = plt.subplots(nrows=1, ncols=1, sharex=True, dpi=100, figsize=(8, 6))

    df = df_sum_alltime_roll_av
    assert df.index.dtype == "datetime64[ns]"
    date_last = pd.to_datetime(df.index[-1]).date()

    for c in df_lineages_top_ten_alltime.index:
        df[c].plot(linewidth=2.0, legend=True)
    # for c in df_scorpio_top_ten_alltime.index:
    #     df[c].plot(linewidth=2.0, legend=True)
    fig.suptitle("SARS-CoV-2 Mutationen in DE: Anzahl 7-Tages-Mittel")
    # y min to 0
    axes[0].set_ylim(0, None)
    # tick formatter
    # axes[0].get_yaxis().set_major_formatter(mtick.PercentFormatter(decimals=0))
    plot_format(
        fig,
        axes,
        date_last,
        filename="plots-python/mutations-de-all-absolute.png",
    )


if __name__ == "__main__":
    plotit()
