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


# Matplotlib setup
# Agg to prevent "Fail to allocate bitmap"
mpl.use('Agg')  # Cairo
# turn off interactive mode
plt.ioff()

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

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
# sum per bundesland: Berlin missing
# sum total
# use new complete DIVI dataset in data/de-divi/tsv/latest.tsv

# Done
# draw a line from max betten
# zoomed plot
# support 1 chart per district as well as grouped ones


#
# setup
#

dir_out = 'plots-python/icu-forecast/'
# os.makedirs(dir_out, exist_ok=True)
os.makedirs(dir_out+"/single", exist_ok=True)
os.makedirs(dir_out+"/joined", exist_ok=True)
os.makedirs(dir_out+"/de-states", exist_ok=True)

# how many weeks shall we look into the future
weeks_forcast = 2


#
# 1. data functions
#


def load_lk_data(l_lkids: list) -> DataFrame:
    """
    l_lkids : list of lkids:str
    grouping of lk data
    sum up their daily Cases_New
    calc 20-day-moving sum
    """
    # initialize new dataframe
    df_sum = pd.DataFrame()
    for lk_id in l_lkids:
        if lk_id in ('16056',):  # Eisenach
            continue

        # load cases data
        if lk_id == "11000":  # Berlin
            file_cases = f'data/de-states/de-state-BE.tsv'
        else:
            file_cases = f'data/de-districts/de-district_timeseries-{lk_id}.tsv'

        # skip missing files
        if not os.path.isfile(file_cases):
            print(f"WARN: file not found: {file_cases}")
            continue

        df_file_cases = pd.read_csv(file_cases, sep="\t")
        df_file_cases = helper.pandas_set_date_index(df_file_cases)
        date_today = pd.to_datetime(df_file_cases.index[-1]).date()

        # check for bad values
        if (df_file_cases['Cases_New'].isnull().values.any()):
            raise f"ERROR: {lk_id}: df_file_cases has bad values"
            # df_file_cases['Cases_New'] = df_file_cases['Cases_New'].fillna(0)

        # load icu bed data if there is any
        file_divi = f'data/de-divi/tsv/{lk_id}.tsv'
        if os.path.isfile(file_divi):
            df_file_divi = pd.read_csv(file_divi, sep="\t")
            df_file_divi = helper.pandas_set_date_index(df_file_divi)

            # I needed to reindex the divi df to close gaps by 0!!!
            idx = pd.date_range('2020-01-01', str(date_today))
            df_file_divi = df_file_divi.reindex(idx, fill_value=0)

            # assert same end
            assert (pd.to_datetime(
                df_file_cases.index[-1]).date() == pd.to_datetime(df_file_divi.index[-1]).date())

            # check for bad values
            if (df_file_divi['faelle_covid_aktuell_beatmet'].isnull().values.any()):
                raise f"ERROR: {lk_id}: df_file_divi has bad values"
            if (df_file_divi['betten_ges'].isnull().values.any()):
                raise f"ERROR: {lk_id}: betten_ges has bad values"

        if 'Cases_New' not in df_sum.columns:
            df_sum['Cases_New'] = df_file_cases['Cases_New']
        else:
            df_sum['Cases_New'] += df_file_cases['Cases_New']

        if os.path.isfile(file_divi):
            if 'betten_belegt' not in df_sum.columns:
                df_sum["betten_ges"] = df_file_divi["betten_ges"]
                df_sum["betten_belegt"] = df_file_divi["faelle_covid_aktuell_beatmet"]
            else:
                df_sum["betten_ges"] += df_file_divi["betten_ges"]
                df_sum["betten_belegt"] += df_file_divi["faelle_covid_aktuell_beatmet"]

    if (len(df_sum) > 0 and df_sum['betten_belegt'].isnull().values.any()):
        raise f"ERROR: {lk_id}: df_sum betten_belegt has bad values"

    df_sum['Cases_New_roll_sum_20'] = df_sum['Cases_New'].rolling(
        window=20, min_periods=1).sum()

    df_sum['quote_its_belegt_pro_Cases_New_roll_sum_20'] = df_sum["betten_belegt"] / \
        df_sum['Cases_New_roll_sum_20']

    df_sum['betten_belegt_roll'] = df_sum['betten_belegt'].rolling(
        window=7, min_periods=1).mean()

    # after calc of 20-day sum we can remove dates prior to april 2020 where three is no DIVI data
    df_sum = df_sum.loc['2020-04-01':]
    # print(df_sum.tail(30))
    return df_sum


def forecast(df_data: DataFrame, l_prognosen_prozente: list, quote: float):
    """
    Fälle der letzten Woche für X Wochen in die Zukunft prognostizieren
    returns list of dataframes
    """
    date_today = pd.to_datetime(df_data.index[-1]).date()
    df_last21 = df_data["Cases_New"].tail(21).to_frame(name='Cases_New')
    ds_last7 = df_data["Cases_New"].tail(7)

    l_df_prognosen = []
    # gen as many df as prozente given
    for proz in l_prognosen_prozente:
        df_prognose = pd.DataFrame()
        for week in range(1, weeks_forcast+1):
            for i in range(1, 7+1):
                day = date_today + datetime.timedelta(days=+ i + 7*(week-1))
                case_prognose = ds_last7[i-1] * pow(1+proz/100, week)
                new_row = {"Date": day, "Cases_New": case_prognose}
                df_prognose = df_prognose.append(
                    new_row, ignore_index=True)
        df_prognose = helper.pandas_set_date_index(df_prognose)
        l_df_prognosen.append(df_prognose)  # add to list of dataframes

    # calc 20 day sum
    for i in range(len(l_df_prognosen)):
        df_prognose = l_df_prognosen[i]
        # prepend last 21 days to calc the 20 day sum
        df_prognose = df_last21.append(df_prognose)
        df_prognose['Cases_New_roll_sum_20'] = df_prognose['Cases_New'].rolling(
            window=20, min_periods=1).sum()
        # drop the 21 days again
        df_prognose = df_prognose.iloc[21:]
        df_prognose['betten_belegt_calc'] = (
            quote * df_prognose['Cases_New_roll_sum_20']).round(1)
        l_df_prognosen[i] = df_prognose
    return l_df_prognosen


#
# 2. plotting functions
#


def plot_1_cases(df: DataFrame, filename: str, landkreis_name: str):
    """
    plot 1.png
    """

    fig, axes = plt.subplots(figsize=(8, 6))

    colors = ('blue', 'black')

    myPlot = df['Cases_New'].plot(
        linewidth=1.0, legend=False, zorder=1, color=colors[0])
    df['Cases_New_roll_sum_20'].plot(
        linewidth=2.0, legend=False, zorder=2, color=colors[1], secondary_y=True)

    axes.set_ylim(0, )
    axes.right_ax.set_ylim(0, )

    plt.title(f'{landkreis_name}: Fallzahlen und 20-Tagessumme')
    axes.set_xlabel("")
    axes.set_ylabel('Fälle täglich')
    axes.right_ax.set_ylabel('Fälle 20-Tage-Summe')
    # color of label and ticks
    axes.yaxis.label.set_color(colors[0])
    axes.right_ax.yaxis.label.set_color(colors[1])
    axes.tick_params(axis='y', colors=colors[0])
    axes.right_ax.tick_params(axis='y', colors=colors[1])
    # grid
    axes.set_axisbelow(True)  # for grid below the lines
    axes.grid(zorder=-1)

    plt.tight_layout()
    plt.savefig(fname=filename, format='png')


def plot_2_its_per_20day_cases(df: DataFrame, filename: str, landkreis_name: str):
    """
    plot 2.png
    """

    fig, axes = plt.subplots(figsize=(8, 6))

    colors = ('blue', 'black')

    myPlot = df['quote_its_belegt_pro_Cases_New_roll_sum_20'].plot(
        linewidth=2.0, legend=False, zorder=1, color=colors[0])

    axes.set_ylim(0, 0.030)

    plt.title(f'{landkreis_name}: Quote ITS-Belegung pro 20-Tage-Fallzahl')
    axes.set_xlabel("")
    axes.set_ylabel('')
    # color of label and ticks
    axes.yaxis.label.set_color(colors[0])
    axes.tick_params(axis='y', colors=colors[0])
    # grid
    axes.set_axisbelow(True)  # for grid below the lines
    axes.grid(zorder=-1)

    plt.tight_layout()
    plt.savefig(fname=filename, format='png')


def plot_3_betten_belegt(df: DataFrame, filename: str, landkreis_name: str):
    """
    plot 3.png
    """

    fig, axes = plt.subplots(figsize=(8, 6))

    colors = ('blue', 'black', 'lightskyblue')

    myPlot = df['betten_belegt'].plot(
        linewidth=1.0, legend=False, zorder=1, color=colors[2])
    df['betten_belegt_roll'].plot(
        linewidth=2.0, legend=False, zorder=1, color=colors[0])

    df['Cases_New_roll_sum_20'].plot(
        linewidth=2.0, legend=False, zorder=2, color=colors[1], secondary_y=True)

    axes.set_ylim(0, )
    axes.right_ax.set_ylim(0, )

    plt.title(f'{landkreis_name}: ICU Bettenbelegung')
    axes.set_xlabel("")
    axes.set_ylabel('Betten belegt')
    axes.right_ax.set_ylabel('Fälle 20-Tage-Summe')
    # color of label and ticks
    axes.yaxis.label.set_color(colors[0])
    axes.right_ax.yaxis.label.set_color(colors[1])
    axes.tick_params(axis='y', colors=colors[0])
    axes.right_ax.tick_params(axis='y', colors=colors[1])
    # grid
    axes.set_axisbelow(True)  # for grid below the lines
    axes.grid(zorder=-1)

    plt.tight_layout()
    plt.savefig(fname=filename, format='png')


def plot_4_cases_prognose(df: DataFrame, l_df_prognosen: list, l_prognosen_prozente: list, filepath: str, landkreis_name: str):
    fig, axes = plt.subplots(figsize=(8, 6))

    # drop some data from the plot
    date_min = '2020-09-01'
    date_max = str(pd.to_datetime(l_df_prognosen[0].index[-1]).date())
    date_today = str(pd.to_datetime(df.index[-1]).date())
    df = df.loc[date_min:]

    max_value = df['betten_belegt'].max()
    max_value_date = df['betten_belegt'].idxmax()

    myPlot = df.iloc[:]['betten_belegt'].plot(
        linewidth=1.0, zorder=1, label="_nolegend_")

    axes.hlines(y=max_value, xmin=max_value_date, xmax=date_max,
                color='grey', linestyles='--')

    l_df_prognosen[0]["betten_belegt_calc"].plot(
        linewidth=2.0, label=f"{l_prognosen_prozente[0]}% (aktuell)")
    for i in reversed(range(1, len(l_df_prognosen))):
        l_df_prognosen[i]["betten_belegt_calc"].plot(
            linewidth=2.0, label=f"{l_prognosen_prozente[i]}%")

    axes.set_ylim(0, )
    axes.tick_params(right=True, labelright=True)

    # {weeks_forcast} Wochen
    title = f'{landkreis_name}: Prognose ITS Bettenbedarf'
    plt.title(title)
    axes.set_xlabel("")
    axes.set_ylabel('ITS Betten')
    axes.set_axisbelow(True)  # for grid below the lines
    axes.grid(zorder=-1)

    plt.gcf().text(1.0, 0.0, s=f"by Torben https://entorb.net , based on RKI and DIVI data of {date_today}", fontsize=8,
                   horizontalalignment='right', verticalalignment='bottom', rotation='vertical')

    plt.legend(title='Inzidenz-Prognose')
    # axes.locstr = 'lower left'

    plt.tight_layout()
    plt.savefig(fname=filepath, format='png')

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

    t = axes.text(pd.to_datetime(df.index[-15]).date(), max_value, "Bisheriges Maximum",
                  verticalalignment='center', horizontalalignment='center')
    t.set_bbox(dict(facecolor='white', edgecolor='white', alpha=0.5))

    plt.savefig(fname=filepath.replace(".png", "-zoom.png"), format='png')
    # cleanup
    fig.clf()
    axes.cla()
    plt.close('all')
    plt.close(fig)
    plt.close()


def doit(landkreis_name, l_lkids, group='de-district'):
    # unique list
    l_lkids = list(set(l_lkids))
    if "16056" in l_lkids:  # Eisenach
        l_lkids.remove("16056")

    df_data = load_lk_data(l_lkids=l_lkids)
    quote = df_data["quote_its_belegt_pro_Cases_New_roll_sum_20"].tail(
        7).mean()

    # Inzidenzänderung
    # inzidenz diese Woche
    inzidenz1 = df_data["Cases_New"].tail(7).sum()
    inzidenz2 = df_data["Cases_New"].tail(14).sum()-inzidenz1

    if inzidenz2 != 0:
        change = round((inzidenz1 / inzidenz2 - 1) * 100, 1)
    else:
        change = 0

    l_prognosen_prozente = (change, -25, 0, 25, 50)

    l_df_prognosen = forecast(
        df_data=df_data,
        l_prognosen_prozente=l_prognosen_prozente,
        quote=quote)

    if group == "de-district":
        if (len(l_lkids) > 1):
            # we are handling joined districts
            filepath = f"{dir_out}/joined/{'_'.join(l_lkids)}.png"
        else:
            filepath = f"{dir_out}/single/{l_lkids[0]}.png"
    elif group == "de-state":
        bl_id = l_lkids[0][0:2]
        bl_code = helper.d_BL_code_from_BL_ID(int(bl_id))
        bl_name = helper.d_BL_name_from_BL_Code[bl_code]
        landkreis_name = bl_name
        filepath = f"{dir_out}/de-states/{bl_code}.png"

    elif group == "DE-total":
        bl_code = "DE-total"
        filepath = f"{dir_out}/de-states/{bl_code}.png"
        landkreis_name = "Deutschland gesamt"

    plot_4_cases_prognose(
        df=df_data, l_df_prognosen=l_df_prognosen, l_prognosen_prozente=l_prognosen_prozente, filepath=filepath, landkreis_name=landkreis_name)


d_lkid2name = helper.read_json_file(
    "data/de-districts/mapping_landkreis_ID_name.json")


#
# Landkreise oder Landkreisgruppe auswählen
#

l_groupes = []
l_groupes.append(("Fürth Stadt + LK", ("09563", "09573")))
l_groupes.append(("Erlangen und ERH", ("09562", "09572")))
l_groupes.append(("Harburg und Lüneburg", ("03353", "03355")))

# loop over grouped landkreise
for group in l_groupes:
    landkreis_name = group[0]
    l_lkids = group[1]
    doit(landkreis_name=landkreis_name, l_lkids=l_lkids)


# loop over all district that have Divi data
for file in glob.glob("data/de-divi/tsv/*.tsv"):
    (filepath, fileName) = os.path.split(file)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    lkid = fileBaseName
    if (lkid == "16056"):  # Eisenach
        continue
    if lkid == "11000":
        landkreis_name = "Berlin"
    else:
        landkreis_name = d_lkid2name[lkid]
    doit(landkreis_name=landkreis_name, l_lkids=(lkid,))

# sum up districts to bundeslaender
for i in range(1, 16+1):
    # blid = 02 für HH etc
    blid = "%02d" % i
    l_lkids = []
    for file in sorted(glob.glob(f"data/de-divi/tsv/{blid}*.tsv")):
        (filepath, fileName) = os.path.split(file)
        (fileBaseName, fileExtension) = os.path.splitext(fileName)
        lkid = fileBaseName
        l_lkids.append(lkid)
    landkreis_name = helper.d_BL_code_from_BL_ID(int(blid))
    doit(landkreis_name=landkreis_name, l_lkids=l_lkids, group="de-state")

# sum up DE-total
l_lkids = []
for file in sorted(glob.glob(f"data/de-divi/tsv/*.tsv")):
    (filepath, fileName) = os.path.split(file)
    (fileBaseName, fileExtension) = os.path.splitext(fileName)
    lkid = fileBaseName
    l_lkids.append(lkid)
landkreis_name = "Deutschland gesamt"
doit(landkreis_name=landkreis_name, l_lkids=l_lkids, group="DE-total")


# l_lkids = ("09563",)
# "09563": "Fürth (Kreisfreie Stadt)",
# "09573": "Fürth (Landkreis)",

# model test plots, to verify my coding against Dirk's
# plot_1_cases(
#     df=df_data, filename=f"icu-forecast-howto/1_tm.png", landkreis_name=landkreis_name)
# plot_2_its_per_20day_cases(
#     df=df_data, filename=f"icu-forecast-howto/2_tm.png", landkreis_name=landkreis_name)
# plot_3_betten_belegt(
#     df=df_data, filename=f"icu-forecast-howto/3_tm.png", landkreis_name=landkreis_name)
