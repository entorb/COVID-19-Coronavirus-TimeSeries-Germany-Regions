import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

import urllib.request
import subprocess

import helper

# siehe auch https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Situationsberichte/Omikron-Faelle/Omikron-Faelle.html?__blob=publicationFile


def fetch():
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
        "cache/rki-mutation-sequences/SARS-CoV-2-Sequenzdaten_Deutschland.csv", sep=","
    )
    df2 = pd.read_csv(
        "cache/rki-mutation-sequences/SARS-CoV-2-Entwicklungslinien_Deutschland.csv",
        sep=",",
    )

    # join dfs on ID column IMS_ID
    df = df1.set_index("IMS_ID").join(df2.set_index("IMS_ID"))
    del df1, df2
    # convert date_str to date
    for c in ("DATE_DRAW", "RECEIVE_DATE", "PROCESSING_DATE"):
        df[c] = pd.to_datetime(df[c], format="%Y-%m-%d")

    # remove word "Probable" from scorpio_call for better clustering
    df["scorpio_call"] = df["scorpio_call"].replace(
        to_replace=r"^Probable ", value="", regex=True
    )
    return df


df_all_data = read_data()

# max_date = df_all_data["PROCESSING_DATE"].max()
# print(max_date)

# 1. lineage column
df_lineages = (
    df_all_data.groupby(["lineage", "RECEIVE_DATE"]).size().reset_index(name="count")
)
df_lineages_top_ten = (
    df_lineages.groupby("lineage")
    .sum()
    .sort_values(by="count", ascending=False)
    .head(50)
)
# print(df_top_ten_seq)
df_lineages_top_ten.to_csv("cache/rki-mutation-sequences/out-ranking-lineage.csv")


# 2. scorpio_call column
df_scorpio_call = (
    df_all_data.groupby(["scorpio_call", "RECEIVE_DATE"])
    .size()
    .reset_index(name="count")
)

df_scorpio_call_top_ten = (
    df_scorpio_call.groupby("scorpio_call")
    .sum()
    .sort_values(by="count", ascending=False)
)
# df_top_ten_scorpio_call = df_top_ten_scorpio_call.head(10)
df_scorpio_call_top_ten = df_scorpio_call_top_ten[
    df_scorpio_call_top_ten["count"] > 1000
]
# print(df_top_ten_scorpio_call)
df_scorpio_call_top_ten.to_csv(
    "cache/rki-mutation-sequences/out-ranking-scorpio_call.csv"
)


# 3. sum

df_date_sum = df_lineages.groupby("RECEIVE_DATE").sum()

df_date_sum = df_date_sum.rename(
    {
        "count": "sequences_total",
    },
    axis=1,
    errors="raise",
)
# print(df_date_sum)


def filter_timeseries_df_on_lineages(df: pd.DataFrame, lineage_name: str):
    df2 = df[df["lineage"] == lineage_name]
    df2.set_index(["RECEIVE_DATE"], inplace=True)
    df2 = df2["count"].to_frame()
    # print(df2)
    return df2


def filter_timeseries_df_on_scorpio_call(df: pd.DataFrame, scorpio_call: str):
    df2 = df[df["scorpio_call"] == scorpio_call]
    df2.set_index(["RECEIVE_DATE"], inplace=True)
    df2 = df2["count"].to_frame()
    # print(df2)
    return df2


# these are not used
df_date_sum["omicon BA.1"] = filter_timeseries_df_on_lineages(
    df=df_lineages, lineage_name="BA.1"
)["count"]
df_date_sum["delta B.1.1.7"] = filter_timeseries_df_on_lineages(
    df=df_lineages, lineage_name="B.1.1.7"
)["count"]


# 4 add the top mutations to the sum df

for c in df_scorpio_call_top_ten.index:
    df_date_sum[c] = filter_timeseries_df_on_scorpio_call(
        df=df_scorpio_call, scorpio_call=c
    )["count"]

# replace missing / na values by 0
df_date_sum = df_date_sum.fillna(0)


# convert to percent
df_date_pct = df_date_sum.copy()
for c in df_scorpio_call_top_ten.index:
    df_date_pct[c] = 100.0 * df_date_pct[c] / df_date_pct["sequences_total"]


# calc 7-day moving average
df_date_sum_roll_av = df_date_sum.copy()
df_date_pct_roll_av = df_date_pct.copy()

for c in df_date_sum_roll_av.columns:
    df_date_sum_roll_av[c] = (
        df_date_sum_roll_av[c].rolling(window=7, min_periods=1).mean().round(1)
    )
    df_date_pct_roll_av[c] = (
        df_date_pct_roll_av[c].rolling(window=7, min_periods=1).mean().round(5)
    )


df_date_sum_roll_av.to_csv("cache/rki-mutation-sequences/out-date_sum_roll_av.csv")


# plotting

df = df_date_pct

date_last = pd.to_datetime(df.index[-1]).date()

# df["sequences_total"].plot(linewidth=2.0, legend=True, zorder=1)
for c in df_scorpio_call_top_ten.index:
    df[c].plot(linewidth=2.0, legend=True)

plt.title(f"SARS-CoV-2 Mutationen in DE: Anteile")
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

df = df_date_pct
df = df[df.index >= "2021-12-01"]
df["Omicron (BA.1-like)"].plot(linewidth=2.0, legend=False)

plt.title(f"Omicron (BA.1-like) in DE: Anteil")
plt.xlabel("")
plt.gca().set_ylim(auto=True)
plt.gca().set_ylim(bottom=0)
plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
plt.grid(axis="both")
helper.mpl_add_text_source(source="RKI", date=date_last)
plt.tight_layout()
plt.savefig(fname=f"plots-python/mutations-de-omicron.png", format="png")
plt.close()


df = df_date_sum
for c in df_scorpio_call_top_ten.index:
    df[c].plot(linewidth=2.0, legend=True)

plt.title(f"SARS-CoV-2 Mutationen in DE: Anzahl")
plt.xlabel("")
plt.ylabel("Anzahl der Sequenzierungen")
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
