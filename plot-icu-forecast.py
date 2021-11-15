# from datetime import timedelta  # , date
import helper
import glob
import shutil
import datetime
import os
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.dates import MonthLocator, YearLocator, WeekdayLocator

# import matplotlib.ticker as ticker
import locale
import datetime as dt


# Matplotlib setup
# Agg to prevent "Fail to allocate bitmap"
mpl.use("Agg")  # Cairo
# turn off interactive mode
plt.ioff()

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")

# info : see icu-forecase/howto
# model:
# 1. calculating a moving sum of  20-day-cases
# 2. calculating the ratio of the icu-beds to the 20-day-cases-sum
# 3. calculating the average of that ratio for the last 7 days
# 4. assuming this ratio is constant for the forecast
# 5. use last weeks case data to model the future cases, using different 7-day-change models
# 6. calculate the moving sum of 20-days-cases
# 7. multiply by found ratio icu-beds to the 20-day-cases-sum to convert to beds


# TODO:
# switch data source to Risklayer?
# parallel / multiprocessing to speedup
# add todays beds to prognose [0]
# if cases series has more data than divi data, use them instead of dropping them

# Done
# draw a line from max betten
# zoomed plot
# support 1 chart per district as well as grouped ones
# sum total
# sum per bundesland: Berlin missing
# use new complete DIVI dataset in data/de-divi/tsv/latest.tsv


#
# setup
#

dir_out = "plots-python/icu-forecast/"
os.makedirs(dir_out + "/single", exist_ok=True)
os.makedirs(dir_out + "/de-district-group", exist_ok=True)
os.makedirs(dir_out + "/de-states", exist_ok=True)

# how many weeks shall we look into the future
weeks_forcast = 2


#
# 1. data functions
#
def load_divi_data() -> DataFrame:
    """
    load complete set of all divi data
    calc betten_belegt
    old: rename faelle_covid_aktuell_invasiv_beatmet -> betten_covid
    new: rename faelle_covid_aktuell -> betten_covid
    """
    df = pd.read_csv(f"data/de-divi/downloaded/latest.csv", sep=",")

    # select columns
    df["betten_ges"] = df["betten_frei"] + df["betten_belegt"]

    df = df[
        [
            "date",
            "bundesland",
            "gemeindeschluessel",
            "faelle_covid_aktuell",
            "betten_ges",
            "betten_frei",
            "betten_belegt",
        ]
    ]

    # check for for bad values
    if df["faelle_covid_aktuell"].isnull().values.any():
        raise f"ERROR: faelle_covid_aktuell has bad values"
    if df["betten_ges"].isnull().values.any():
        raise f"ERROR: betten_ges has bad values"

    df = df.rename(
        {
            "faelle_covid_aktuell": "betten_covid",
        },
        axis=1,
        errors="raise",
    )

    # print(df.tail())

    return df


df_divi_all = load_divi_data()

date_divi_data_str = df_divi_all["date"].max()
# date_divi_data_str = "2021-11-01"
date_divi_data = dt.date.fromisoformat(date_divi_data_str)
date_divi_data_dt = dt.datetime(
    date_divi_data.year, date_divi_data.month, date_divi_data.day
)
# exit()

# print(len(df_divi_all))
# exit(90)


def sum_lk_divi_data(l_lk_ids: list) -> DataFrame:
    """
    filters df_divi_all by l_lk_ids
    sums up betten_covid and betten_ges
    """
    assert len(l_lk_ids) > 0
    global df_divi_all
    df = df_divi_all
    # print(len(df))
    df = df[df["gemeindeschluessel"].isin(l_lk_ids)]
    # print(df.tail())

    assert len(df) > 0, f"ERROR: no divi data for lk_ids: {l_lk_ids}"

    df = df.groupby(["date"]).agg({"betten_covid": "sum", "betten_ges": "sum"})
    # print("df len")
    # print(len(df))

    df.index = pd.to_datetime(df.index)

    date_last = pd.to_datetime(df.index[-1]).date()
    # I needed to reindex the divi df to close gaps by 0!!!
    idx = pd.date_range("2020-01-01", date_last)
    df = df.reindex(idx, fill_value=0)

    # print(df.tail())
    return df


def sum_bl_divi_data(bl_id: int) -> DataFrame:
    """
    filters df_divi_all by l_lk_ids
    sums up betten_covid and betten_ges
    """
    assert type(bl_id) == int
    global df_divi_all
    df = df_divi_all
    # print(df.head())
    df = df_divi_all[df_divi_all["bundesland"] == bl_id]
    # print(df.head())
    df = df.groupby(["date"]).agg({"betten_covid": "sum", "betten_ges": "sum"})
    df.index = pd.to_datetime(df.index)

    date_last = pd.to_datetime(df.index[-1]).date()
    # I needed to reindex the divi df to close gaps by 0!!!
    idx = pd.date_range("2020-01-01", date_last)
    df = df.reindex(idx, fill_value=0)

    # print(df.tail())
    return df


def sum_DE_divi_data() -> DataFrame:
    """
    filters df_divi_all by l_lk_ids
    sums up betten_covid and betten_ges
    """
    global df_divi_all
    df = df_divi_all.groupby(["date"]).agg({"betten_covid": "sum", "betten_ges": "sum"})
    df.index = pd.to_datetime(df.index)

    date_last = pd.to_datetime(df.index[-1]).date()
    # I needed to reindex the divi df to close gaps by 0!!!
    idx = pd.date_range("2020-01-01", date_last)
    df = df.reindex(idx, fill_value=0)

    # print(df.tail())
    return df


# l_lk_ids = ("02000", "11000")
# df_divi = sum_lk_divi_data(l_lk_ids)
# exit()


def load_and_sum_lk_case_data(l_lk_ids: list) -> DataFrame:
    """
    l_lk_ids : list of lk_ids:str
    grouping of lk data
    sum up their daily Cases_New
    calc 20-day-moving sum
    """
    for lk_id in l_lk_ids:
        assert type(lk_id) == int, f"not integer {lk_id}"
    # initialize new dataframe
    df_sum = pd.DataFrame()
    for lk_id in l_lk_ids:
        if lk_id in (16056,):  # Eisenach
            continue

        # load cases data
        if lk_id == 11000:  # Berlin
            file_cases = f"data/de-states/de-state-BE.tsv"
        else:
            file_cases = (
                f'data/de-districts/de-district_timeseries-{"%05d" % lk_id}.tsv'
            )

        # skip missing files
        if not os.path.isfile(file_cases):
            print(f"ERROR: file not found: {file_cases}")
            exit(1)

        df_file_cases = pd.read_csv(file_cases, sep="\t")
        df_file_cases = helper.pandas_set_date_index(df_file_cases)

        # check for bad values
        if df_file_cases["Cases_New"].isnull().values.any():
            raise f"ERROR: {lk_id}: df_file_cases has bad values"
            # df_file_cases['Cases_New'] = df_file_cases['Cases_New'].fillna(0)

        if "Cases_New" not in df_sum.columns:
            df_sum["Cases_New"] = df_file_cases["Cases_New"]
        else:
            df_sum["Cases_New"] += df_file_cases["Cases_New"]

    # print(df_sum.tail(30))
    return df_sum


def load_bl_case_data(bl_code: str) -> DataFrame:
    """
    Bundesland-Data
    """
    # load cases data
    file_cases = f"data/de-states/de-state-{bl_code}.tsv"

    # skip missing files
    assert os.path.isfile(file_cases), f"ERROR: file not found {file_cases}"

    df = pd.read_csv(file_cases, sep="\t")
    # print(df.head())
    df = helper.pandas_set_date_index(df)
    df = df["Cases_New"].to_frame()
    # print(df.head())

    # check for bad values
    if df["Cases_New"].isnull().values.any():
        raise f"ERROR: {file_cases} has bad values"

    if "Cases_New" not in df.columns:
        df["Cases_New"] = df["Cases_New"]
    else:
        df["Cases_New"] += df["Cases_New"]

    return df


def join_cases_divi(df_cases: DataFrame, df_divi: DataFrame) -> DataFrame:
    # initialize new dataframe
    # print(df_cases.head())
    # print(df_divi.head())
    df_sum = df_cases
    del df_cases
    df_sum["betten_covid"] = df_divi["betten_covid"]
    df_sum["betten_ges"] = df_divi["betten_ges"]

    df_sum["Cases_New_roll_sum_20"] = (
        df_sum["Cases_New"].rolling(window=20, min_periods=1).sum()
    )

    df_sum["quote_betten_covid_pro_cases_roll_sum_20"] = (
        df_sum["betten_covid"] / df_sum["Cases_New_roll_sum_20"]
    )

    df_sum["betten_belegt_roll"] = (
        df_sum["betten_covid"].rolling(window=7, min_periods=1).mean()
    )

    # after calc of 20-day sum we can remove dates prior to april 2020 where there is no DIVI data available
    df_sum = df_sum.loc["2020-04-01":]

    return df_sum


def forecast(df_data: DataFrame, l_prognosen_prozente: list, quote: float):
    """
    Fälle der letzten Woche für X Wochen in die Zukunft prognostizieren
    returns list of dataframes
    """
    # date_today = pd.to_datetime(df_data.index[-1]).date()
    date_today = date_divi_data
    df_last21 = df_data["Cases_New"].tail(21).to_frame(name="Cases_New")
    ds_last7 = df_data["Cases_New"].tail(7)

    l_df_prognosen = []
    # gen as many df as prozente given
    for proz in l_prognosen_prozente:
        df_prognose = pd.DataFrame()
        # new_row = {"Date": date_today,
        #            "Cases_New": df_data["Cases_New"].tail(1)}
        # df_prognose = df_prognose.append(
        #     new_row, ignore_index=True)
        for week in range(1, weeks_forcast + 1):
            for i in range(1, 7 + 1):
                day = date_today + datetime.timedelta(days=+i + 7 * (week - 1))
                case_prognose = ds_last7[i - 1] * pow(1 + proz / 100, week)
                new_row = {"Date": day, "Cases_New": case_prognose}
                df_prognose = df_prognose.append(new_row, ignore_index=True)
        df_prognose = helper.pandas_set_date_index(df_prognose)
        l_df_prognosen.append(df_prognose)  # add to list of dataframes

    # calc 20 day sum
    for i in range(len(l_df_prognosen)):
        df_prognose = l_df_prognosen[i]
        # prepend last 21 days to calc the 20 day sum
        df_prognose = df_last21.append(df_prognose)
        df_prognose["Cases_New_roll_sum_20"] = (
            df_prognose["Cases_New"].rolling(window=20, min_periods=1).sum()
        )
        # drop the 21 days again
        df_prognose = df_prognose.iloc[21:]
        df_prognose["betten_covid_calc"] = (
            quote * df_prognose["Cases_New_roll_sum_20"]
        ).round(1)

        # TODO: add todays value as starting point

        # new_datetime = df_prognose.index[0:]+pd.Timedelta('-1 days')

        # # df_prognose.loc[date_divi_data_dt].insert(3000)
        # data = {'betten_covid_calc': 3000}
        # df_prognose = df_prognose.append(
        #     pd.DataFrame(data, index=[new_datetime]))
        # print(df_prognose.head())
        # print(df_prognose.tail())
        # exit()

        l_df_prognosen[i] = df_prognose

    return l_df_prognosen


#
# 2. plotting functions
#


def plot_it(
    df: DataFrame,
    l_df_prognosen: list,
    l_prognosen_prozente: list,
    filepath: str,
    landkreis_name: str,
):
    fig, axes = plt.subplots(figsize=(8, 6))

    # drop some data from the plot
    date_min = "2020-09-01"
    date_max = str(pd.to_datetime(l_df_prognosen[0].index[-1]).date())
    date_today = str(pd.to_datetime(df.index[-1]).date())
    df = df.loc[date_min:]

    max_value = df["betten_covid"].max()
    max_value_date = df["betten_covid"].idxmax()

    myPlot = df.iloc[:]["betten_covid"].plot(
        linewidth=1.0, zorder=1, label="_nolegend_"
    )

    axes.hlines(
        y=max_value, xmin=max_value_date, xmax=date_max, color="grey", linestyles="--"
    )

    l_df_prognosen[0]["betten_covid_calc"].plot(
        linewidth=2.0, label=f"{l_prognosen_prozente[0]}% (aktuell)"
    )
    for i in reversed(range(1, len(l_df_prognosen))):
        l_df_prognosen[i]["betten_covid_calc"].plot(
            linewidth=2.0, label=f"{l_prognosen_prozente[i]}%"
        )

    axes.set_ylim(
        0,
    )
    axes.tick_params(right=True, labelright=True)

    # {weeks_forcast} Wochen
    global weeks_forcast
    title = f"{landkreis_name}: {weeks_forcast} Wochen Prognose ITS Bettenbedarf"
    plt.title(title)
    axes.set_xlabel("")
    axes.set_ylabel("Bedarf an ITS Betten durch COVID Patienten")
    axes.set_axisbelow(True)  # for grid below the lines
    axes.grid(zorder=-1)

    helper.mpl_add_text_source(date=date_today)

    plt.legend(title="Inzidenz-Prognose")
    # axes.locstr = 'lower left'

    plt.tight_layout()
    plt.savefig(fname=filepath, format="png")

    # zoomed plot
    # TODO: better title?
    # plt.title(title + " zoom")
    date_min2 = pd.to_datetime(df.index[-45]).date()
    date_max2 = pd.to_datetime(l_df_prognosen[0].index[-1]).date()
    axes.set_xlim([date_min2, date_max2])

    # set grid to week
    # no, because than the month info is lost
    # wloc = WeekdayLocator()
    # axes.xaxis.set_major_locator(wloc)

    t = axes.text(
        pd.to_datetime(df.index[-15]).date(),
        max_value,
        "bisheriges Maximum",
        verticalalignment="center",
        horizontalalignment="center",
    )
    t.set_bbox(dict(facecolor="white", edgecolor="white", alpha=0.75))

    # print(date_today)
    # print(df.tail())
    # print(l_df_prognosen[0].head())
    # axes.vlines(x=date_today, ymin=0, ymax=10000,
    #             color='grey', linestyles='--')

    plt.savefig(fname=filepath.replace(".png", "-zoom.png"), format="png")
    # cleanup
    fig.clf()
    axes.cla()
    plt.close("all")
    plt.close(fig)
    plt.close()


def doit(
    title="", l_lk_ids: list = (), bl_id: int = -1, mode="de-district", filename=""
):
    """
    mode:
    district: 1 Landkreis
    district-group: multiple districts, requires filename
    state
    DE
    """
    assert mode in ("de-district", "de-district-group", "de-state", "DE-total")
    # ensure lk_ids are a unique list
    l_lk_ids = list(set(l_lk_ids))

    if 16056 in l_lk_ids:  # Eisenach
        l_lk_ids.remove(16056)

    if mode == "de-district":
        assert len(l_lk_ids) == 1
        lk_id = l_lk_ids[0]
        assert lk_id > 1000, f"lk_id {lk_id} is invalid"
        df_divi = sum_lk_divi_data(l_lk_ids=l_lk_ids)
        if l_lk_ids[0] == 11000:  # Berlin
            # Berlin as it is 1 set in DIVI, but multiple in RKI
            title = "Berlin"
            df_cases = load_bl_case_data(bl_code="BE")
        else:
            df_cases = load_and_sum_lk_case_data(l_lk_ids=l_lk_ids)
            title = helper.d_lk_name_from_lk_id["%05d" % lk_id]
        filepath = f'{dir_out}/single/{"%05d" % lk_id}.png'

    elif mode == "de-district-group":
        assert filename != "", f"ERROR: filename missing for {title}"
        assert len(l_lk_ids) > 0, f"ERROR lk_ids empty for {title}"
        assert title != "", f"ERROR: title empty for filename {filename}"
        # print(title)
        # print(l_lk_ids)
        df_divi = sum_lk_divi_data(l_lk_ids=l_lk_ids)
        df_cases = load_and_sum_lk_case_data(l_lk_ids=l_lk_ids)
        filepath = f"{dir_out}/de-district-group/{filename}.png"

    elif mode == "de-state":
        df_divi = sum_bl_divi_data(bl_id=bl_id)
        bl_code = helper.d_BL_code_from_BL_ID[int(bl_id)]
        df_cases = load_bl_case_data(bl_code=bl_code)
        title = helper.d_BL_name_from_BL_Code[bl_code]
        filepath = f"{dir_out}/de-states/{bl_code}.png"

    elif mode == "DE-total":
        df_divi = sum_DE_divi_data()
        df_cases = load_bl_case_data(bl_code="DE-total")
        filepath = f"{dir_out}/de-states/DE-total.png"
        title = "Deutschland gesamt"

    # filter out data newer than latest DIVI data
    # print(df.tail(3))
    global date_divi_data_dt
    df_cases = df_cases[df_cases.index <= date_divi_data_dt]
    # print(df.tail(3))

    df_data = join_cases_divi(df_cases=df_cases, df_divi=df_divi)
    del df_divi, df_cases

    #  print(df_data.tail())
    quote = df_data["quote_betten_covid_pro_cases_roll_sum_20"].tail(7).mean()

    # Inzidenzänderung
    # inzidenz diese Woche
    inzidenz1 = df_data["Cases_New"].tail(7).sum()
    inzidenz2 = df_data["Cases_New"].tail(14).sum() - inzidenz1

    if inzidenz2 != 0:
        change = round((inzidenz1 / inzidenz2 - 1) * 100, 1)
    else:
        change = 0

    l_prognosen_prozente = (change, -25, 0, 25, 50)

    l_df_prognosen = forecast(
        df_data=df_data, l_prognosen_prozente=l_prognosen_prozente, quote=quote
    )

    # TODO
    plot_it(
        df=df_data,
        l_df_prognosen=l_df_prognosen,
        l_prognosen_prozente=l_prognosen_prozente,
        filepath=filepath,
        landkreis_name=title,
    )


# Modelltests mit Daten von Erlangen
# print("Erlangen")
# doit(mode="de-district", l_lk_ids=(9562,))


print("DE-total")
doit(mode="DE-total")

print("de-states")
for i in range(1, 16 + 1):
    doit(mode="de-state", bl_id=i)


print("de-district-group")
# loop over grouped landkreise
# generated via icu-groups.py
l_groupes = helper.read_json_file("data/de-divi/lk-groups.json")
for d in l_groupes:
    title = d["title"]
    id = d["id"]
    l_lk_ids = [int(x) for x in d["lk_ids"]]
    doit(
        mode="de-district-group", title=title, l_lk_ids=l_lk_ids, filename=str(d["id"])
    )

# test

print("de-districts")
l_lk_ids = helper.read_json_file("data/de-divi/lkids.json")
for lk_id in l_lk_ids:
    lk_id = int(lk_id)
    if lk_id == 16056:  # Eisenach
        continue
    doit(mode="de-district", l_lk_ids=(lk_id,))


# # Unna: 4 Wochen Prognose für @doc_emed
# print("Unna")
# weeks_forcast = 4
# doit(mode="de-district", l_lk_ids=(5978,))
# #
