import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import locale

import urllib.request
import subprocess

import helper

# siehe auch https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Omikron-Faelle/Omikron-Faelle.html?__blob=publicationFile

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

# TODO. replace by helper.download_from_url_if_old(
def fetch():
    """
    fetch/download data from rki github account
    """
    for fname in (
        "SARS-CoV-2-Sequenzdaten_Deutschland",
        "SARS-CoV-2-Entwicklungslinien_Deutschland",
    ):
        url = f"https://github.com/robert-koch-institut/SARS-CoV-2-Sequenzdaten_aus_Deutschland/blob/master/{fname}.csv.xz?raw=true"
        filepath = f"cache/rki-mutation-sequences/{fname}.csv.xz"
        filedata = urllib.request.urlopen(url)
        datatowrite = filedata.read()
        with open(filepath, mode="wb") as f:
            f.write(datatowrite)

        # extract the .xz file
        subprocess.run(["xz", "-d", "-f", filepath], capture_output=False, text=False)


if not helper.check_cache_file_available_and_recent(
    fname=f"cache/rki-mutation-sequences/SARS-CoV-2-Sequenzdaten_Deutschland.csv",
    max_age=1800,
    verbose=True,
):
    fetch()


def read_data() -> pd.DataFrame:
    # read data from CSV
    df1 = pd.read_csv(
        "cache/rki-mutation-sequences/SARS-CoV-2-Sequenzdaten_Deutschland.csv",
        sep=",",
        usecols=["IMS_ID", "RECEIVE_DATE"],
    )
    df2 = pd.read_csv(
        "cache/rki-mutation-sequences/SARS-CoV-2-Entwicklungslinien_Deutschland.csv",
        sep=",",
        usecols=["IMS_ID", "lineage", "scorpio_call"],
    )

    # join dfs on ID column IMS_ID
    df = df1.set_index("IMS_ID").join(df2.set_index("IMS_ID"))
    del df1, df2
    # convert date_str to date
    for c in ("RECEIVE_DATE",):  # ("DATE_DRAW", "RECEIVE_DATE", "PROCESSING_DATE"):
        df[c] = pd.to_datetime(df[c], format="%Y-%m-%d")

    # remove word "Probable" from scorpio_call for better clustering
    df["scorpio_call"] = df["scorpio_call"].replace(
        to_replace=r"^Probable ", value="", regex=True
    )
    return df


df_all_data = read_data()

# max_date = df_all_data["PROCESSING_DATE"].max()
# print(max_date)

# # 2a. group and count by lineage and date columns
# df_lineages = (
#     df_all_data.groupby(["lineage", "RECEIVE_DATE"]).size().reset_index(name="count")
# )
# df_lineages_top_ten = (
#     df_lineages.groupby("lineage")
#     .sum()
#     .sort_values(by="count", ascending=False)
#     .head(50)
# )
# # print(df_top_ten_seq)
# df_lineages_top_ten.to_csv("cache/rki-mutation-sequences/out-ranking-lineage.csv")


# 2b. group and count by scorpio and date columns
df_scorpio_alltime = (
    df_all_data.groupby(["scorpio_call", "RECEIVE_DATE"])
    .size()
    .reset_index(name="count")
)

# date_month = dt.date.today() - dt.timedelta(days=30)
df_scorpio_lastmonth = df_scorpio_alltime[
    df_scorpio_alltime["RECEIVE_DATE"].dt.date
    >= (dt.date.today() - dt.timedelta(days=62))
]

df_scorpio_top_ten_alltime = (
    df_scorpio_alltime.groupby("scorpio_call")
    .sum()
    .sort_values(by="count", ascending=False)
)
df_scorpio_top_ten_alltime = df_scorpio_top_ten_alltime.head(10)
# df_scorpio_top_ten = df_scorpio_top_ten[df_scorpio_top_ten["count"] > 1000]
# print(df_top_ten_scorpio_call)
df_scorpio_top_ten_alltime.to_csv(
    "cache/rki-mutation-sequences/out-ranking-scorpio_call.csv"
)

df_scorpio_top_ten_lastmonth = (
    df_scorpio_lastmonth.groupby("scorpio_call")
    .sum()
    .sort_values(by="count", ascending=False)
)
df_scorpio_top_ten_lastmonth = df_scorpio_top_ten_lastmonth.head(6)


# 3. sum df

# 3.1 add column of total number of sequences per day
df_sum_alltime = df_scorpio_alltime.groupby("RECEIVE_DATE").sum()
df_sum_lastmonth = df_scorpio_lastmonth.groupby("RECEIVE_DATE").sum()

df_sum_alltime = df_sum_alltime.rename(
    {
        "count": "sequences_total",
    },
    axis=1,
    errors="raise",
)
df_sum_lastmonth = df_sum_lastmonth.rename(
    {
        "count": "sequences_total",
    },
    axis=1,
    errors="raise",
)


# def filter_timeseries_df_on_lineages(df: pd.DataFrame, lineage_name: str):
#     df2 = df[df["lineage"] == lineage_name]
#     df2.set_index(["RECEIVE_DATE"], inplace=True)
#     df2 = df2["count"].to_frame()
#     # print(df2)
#     return df2


def filter_timeseries_df_on_scorpio_call(df: pd.DataFrame, scorpio_call: str):
    df2 = df[df["scorpio_call"] == scorpio_call]
    df2.set_index(["RECEIVE_DATE"], inplace=True)
    df2 = df2["count"].to_frame()
    # print(df2)
    return df2


# # these are not used
# df_date_sum["omicon BA.1"] = filter_timeseries_df_on_lineages(
#     df=df_lineages, lineage_name="BA.1"
# )["count"]
# df_date_sum["delta B.1.1.7"] = filter_timeseries_df_on_lineages(
#     df=df_lineages, lineage_name="B.1.1.7"
# )["count"]


# 4 add the top mutations to the sum df

for c in df_scorpio_top_ten_alltime.index:
    df_sum_alltime[c] = filter_timeseries_df_on_scorpio_call(
        df=df_scorpio_alltime, scorpio_call=c
    )["count"]


for c in df_scorpio_top_ten_lastmonth.index:
    df_sum_lastmonth[c] = filter_timeseries_df_on_scorpio_call(
        df=df_scorpio_lastmonth, scorpio_call=c
    )["count"]


# replace missing / na values by 0
df_sum_alltime = df_sum_alltime.fillna(0)
df_sum_lastmonth = df_sum_lastmonth.fillna(0)


# convert to percent
df_pct_alltime = df_sum_alltime.copy()
for c in df_scorpio_top_ten_alltime.index:
    df_pct_alltime[c] = 100.0 * df_pct_alltime[c] / df_pct_alltime["sequences_total"]
df_pct_lastmonth = df_sum_lastmonth.copy()
for c in df_scorpio_top_ten_lastmonth.index:
    df_pct_lastmonth[c] = (
        100.0 * df_pct_lastmonth[c] / df_pct_lastmonth["sequences_total"]
    )


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


df_sum_alltime_roll_av.to_csv("cache/rki-mutation-sequences/out-date_sum_roll_av.csv")


# plotting
fig, ax = plt.subplots(figsize=(8, 6))
df = df_pct_alltime
date_last = pd.to_datetime(df.index[-1]).date()
# df["sequences_total"].plot(linewidth=2.0, legend=True, zorder=1)
for c in df_scorpio_top_ten_alltime.index:
    df[c].plot(linewidth=1.0, legend=True)
plt.title(f"SARS-CoV-2 Mutationen in DE: Anteile", loc="left")
plt.xlabel("")
plt.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
plt.grid(axis="both")
plt.gcf().autofmt_xdate()
plt.gca().set_ylim(0, 100)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
helper.mpl_add_text_source(source="RKI", date=date_last)
plt.tight_layout()
plt.savefig(fname=f"plots-python/mutations-de-all.png", format="png")
plt.close()

fig, ax = plt.subplots(figsize=(8, 6))
df = df_pct_lastmonth
date_last = pd.to_datetime(df.index[-1]).date()
# df["sequences_total"].plot(linewidth=2.0, legend=True, zorder=1)
for c in df_scorpio_top_ten_lastmonth.index:
    df[c].plot(linewidth=2.0, legend=True)
plt.title(f"SARS-CoV-2 Mutationen in DE: Anteile letzte 2 Monate", loc="left")
plt.xlabel("")
plt.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
plt.grid(axis="both")
plt.gcf().autofmt_xdate()
plt.gca().set_ylim(0, 100)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
helper.mpl_add_text_source(source="RKI", date=date_last)
plt.tight_layout()
plt.savefig(fname=f"plots-python/mutations-de-lastmonth.png", format="png")
plt.close()

# fig, ax = plt.subplots(figsize=(8, 6))
# df = df_pct_alltime
# df = df[df.index >= "2021-12-01"]
# df["Omicron (BA.1-like)"].plot(linewidth=2.0, legend=False)

# plt.title(f"Omicron (BA.1-like) in DE: Anteil", loc="left")
# plt.xlabel("")
# plt.gca().set_ylim(auto=True)
# plt.gca().set_ylim(bottom=0)
# plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
# plt.grid(axis="both")
# helper.mpl_add_text_source(source="RKI", date=date_last)
# plt.tight_layout()
# plt.savefig(fname=f"plots-python/mutations-de-omicron.png", format="png")
# plt.close()


fig, ax = plt.subplots(figsize=(8, 6))
# df = df_sum_alltime
df = df_sum_alltime_roll_av
for c in df_scorpio_top_ten_alltime.index:
    df[c].plot(linewidth=2.0, legend=True)

plt.title(f"SARS-CoV-2 Mutationen in DE: Anzahl 7-Tages-Mittel", loc="left")
plt.xlabel("")
plt.ylabel("Anzahl der tägl. Sequenzierungen")
plt.legend(loc="upper left", bbox_to_anchor=(1.0, 1.0))
plt.grid(axis="both")
plt.gcf().autofmt_xdate()
plt.gca().set_ylim(auto=True)
plt.gca().set_ylim(
    0,
)
helper.mpl_add_text_source(source="RKI", date=date_last)
plt.tight_layout()
plt.savefig(fname=f"plots-python/mutations-de-all-absolute.png", format="png")
plt.close()
