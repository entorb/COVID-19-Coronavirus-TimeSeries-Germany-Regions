import os
import pandas as pd
from pandas.core.frame import DataFrame
import matplotlib.pyplot as plt
# import matplotlib.ticker as ticker

from datetime import timedelta, date


def load_lk_data(l_lkids: list) -> DataFrame:
    """
    l_lkids : list of lkids:str
    grouping of lk data
    sum up their daily Cases_New
    calc 20-day-moving sum
    """
    # initialize new dataframe
    df_sum = pd.DataFrame()
    for lkid in l_lkids:

        df_file_cases = pd.read_csv(
            f'data/de-districts/de-district_timeseries-{lkid}.tsv', sep="\t")
        # use date as index
        df_file_cases['Date'] = pd.to_datetime(
            df_file_cases['Date'], format='%Y-%m-%d')
        df_file_cases.set_index(['Date'], inplace=True)

        file_divi = f'data/de-divi/tsv/{lkid}.tsv'
        if os.path.isfile(file_divi):
            df_file_divi = pd.read_csv(
                file_divi, sep="\t")
            # use date as index
            df_file_divi['Date'] = pd.to_datetime(
                df_file_divi['Date'], format='%Y-%m-%d')
            df_file_divi.set_index(['Date'], inplace=True)

        if 'Cases_New' not in df_sum.index:
            df_sum['Cases_New'] = df_file_cases['Cases_New']
        else:
            df_sum['Cases_New'] += df_file_cases['Cases_New']

        if os.path.isfile(file_divi):
            if 'betten_belegt' not in df_sum.index:
                df_sum["betten_ges"] = df_file_divi["betten_ges"]
                df_sum["betten_belegt"] = df_file_divi["faelle_covid_aktuell_beatmet"]
            else:
                df_sum["betten_ges"] += df_file_divi["betten_ges"]
                df_sum["betten_belegt"] += df_file_divi["faelle_covid_aktuell_beatmet"]
            # print(df_sum.tail(5))

    df_sum['Cases_New_roll_sum_20'] = df_sum['Cases_New'].rolling(
        window=20, min_periods=1).sum()

    df_sum['quote_its_belegt_pro_Cases_New_roll_sum_20'] = df_sum["betten_belegt"] / \
        df_sum['Cases_New_roll_sum_20']

    df_sum['betten_belegt_roll'] = df_sum['betten_belegt'].rolling(
        window=7, min_periods=1).mean()

    # print(df_sum.tail(20))

    return df_sum


# "09563": "Fürth (Kreisfreie Stadt)",
# "09573": "Fürth (Landkreis)",
df = load_lk_data(l_lkids=("09563", "09573"))
# print(df_cases.tail(5))


def plot_1_cases(df: DataFrame, filename: str):
    """
    plot 1.png
    """

    fig, axes = plt.subplots(figsize=(6, 8))

    colors = ('blue', 'black')

    myPlot = df['Cases_New'].plot(
        linewidth=1.0, legend=False, zorder=1, color=colors[0])
    df['Cases_New_roll_sum_20'].plot(
        linewidth=2.0, legend=False, zorder=2, color=colors[1], secondary_y=True)

    axes.set_ylim(0, )
    axes.right_ax.set_ylim(0, )

    plt.title('Fallzahlen Stadt & Landkreis Fürth')
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


plot_1_cases(df=df, filename="its-belegung/out/1.png")


def plot_2_its_per_20day_cases(df: DataFrame, filename: str):
    """
    plot 2.png
    """

    fig, axes = plt.subplots(figsize=(6, 8))

    colors = ('blue', 'black')

    myPlot = df['quote_its_belegt_pro_Cases_New_roll_sum_20'].plot(
        linewidth=2.0, legend=False, zorder=1, color=colors[0])

    axes.set_ylim(0, 0.030)

    plt.title('Quote ITS-Belegung pro 20-Tage-Fallzahl (Klinikum Fürth)')
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


plot_2_its_per_20day_cases(df=df, filename="its-belegung/out/2.png")

# print(df["quote_its_belegt_pro_Cases_New_roll_sum_20"].tail(7))
quote = df["quote_its_belegt_pro_Cases_New_roll_sum_20"].tail(7).mean()


def plot_3_cases(df: DataFrame, filename: str):
    """
    plot 3.png
    """

    fig, axes = plt.subplots(figsize=(6, 8))

    colors = ('blue', 'black', 'lightskyblue')

    myPlot = df['betten_belegt'].plot(
        linewidth=1.0, legend=False, zorder=1, color=colors[2])
    df['betten_belegt_roll'].plot(
        linewidth=2.0, legend=False, zorder=1, color=colors[0])

    df['Cases_New_roll_sum_20'].plot(
        linewidth=2.0, legend=False, zorder=2, color=colors[1], secondary_y=True)

    axes.set_ylim(0, )
    axes.right_ax.set_ylim(0, )

    plt.title('Fallzahlen Stadt & Landkreis Fürth')
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


plot_3_cases(df=df, filename="its-belegung/out/3.png")


# Fälle der 1 Woche für 3 Wochen fortschreiben

dt_latest_date = pd.to_datetime(df.index[-1]).date()
df_last7 = df["Cases_New"].tail(7)
print(df_last7)

df_prognose = pd.DataFrame()
# 1 Woche
for week in range(1, 3+1):
    for i in range(0, 7):
        new_row = {"Date": dt_latest_date +
                   timedelta(days=+i+7*week), "Cases_New_10%": df_last7[i] * pow(1.1, week), "Cases_New_20%": df_last7[i] * pow(1.2, week), "Cases_New_30%": df_last7[i] * pow(1.3, week)}
        df_prognose = df_prognose.append(new_row, ignore_index=True)

# use date as index
df_prognose['Date'] = pd.to_datetime(
    df_prognose['Date'], format='%Y-%m-%d')
df_prognose.set_index(['Date'], inplace=True)

# add value
# fetch last index and convert to datetime and convert to date
# print(dt_latest_date)
# print(dt_latest_date + timedelta(days=+1))

# df_calc = pd.DataFrame(columns=["Date", "Cases_New"], index=pd.to_datetime([]))
# (columns=["Date", "Cases_New"])


print(df_prognose)


# dti = pd.date_range(dt_latest_date + timedelta(days=+1), periods=14, freq="D")

# df_calc = dti.to_frame(index=False)
