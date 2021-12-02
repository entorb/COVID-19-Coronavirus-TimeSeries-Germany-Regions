#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
converts the incidence data into a kind of histogram time series
"""

# TODO:
# use rolling for finding the slope
# https://stackoverflow.com/questions/49838315/python-pandas-apply-a-function-to-dataframe-rolling

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# my helper modules
import helper

# 1. create empty data frame
# 2. loop over all district data files, extract their 7-day incidence and increment the relevant field in the data frame
# 3. plot
# 4. to the same for deaths
# 5. to the same for the 7-day chance of the incidence in %

# TODO: 2 functions: prepare data and plot data


def read_and_prepare_data():
    # create empty data frame, based on data for Hamburg
    df_file = pd.read_csv(
        "data/de-districts/de-district_timeseries-02000.tsv", sep="\t"
    )
    df = pd.DataFrame()
    # df['Date'] = df_file['Date']

    # use date as index
    df["Date"] = pd.to_datetime(df_file["Date"], format="%Y-%m-%d")
    df.set_index(["Date"], inplace=True)

    # incidence groups
    # =0, <5, <10, <25, <50, <100, <200, >=200
    # df['0'] = 0
    # df['5'] = 0
    # df['10'] = 0
    # df['25'] = 0
    # df['50'] = 0
    # df['100'] = 0
    # df['200'] = 0
    # df['400'] = 0
    # df['999'] = 0

    df[">0"] = 0
    df[">5"] = 0
    df[">10"] = 0
    df[">25"] = 0
    df[">50"] = 0
    df[">100"] = 0
    df[">200"] = 0
    df[">400"] = 0

    # df['=0'] = 0
    # df['<5'] = 0
    # df['<10'] = 0
    # df['<25'] = 0
    # df['<50'] = 0
    # df['<100'] = 0
    # df['<200'] = 0
    # df['<400'] = 0

    df["+1%"] = 0
    df["+25%"] = 0
    df["+50%"] = 0
    df["+100%"] = 0
    df["+200%"] = 0
    df["-1%"] = 0
    df["-25%"] = 0
    df["-50%"] = 0
    df["-75%"] = 0
    df["-100%"] = 0

    count = 0

    # loop over all districts data file and read them as data frames
    for filename in glob.glob("data/de-districts/de-district_timeseries-*.tsv"):
        if "16056" in filename:
            # Eisenach problem, again...
            continue

        df_file = pd.read_csv(filename, sep="\t")
        df_file["Date"] = pd.to_datetime(df_file["Date"], format="%Y-%m-%d")
        df_file.set_index(["Date"], inplace=True)

        # convert Cases_Last_Week_Per_Million to Cases_Last_Week_Per_100000
        df_file["Cases_Last_Week_Per_100000"] = (
            df_file["Cases_Last_Week_Per_Million"] / 10
        )

        # is_000 = df_file['Cases_Last_Week_Per_100000'] == 0
        # is_005 = (df_file['Cases_Last_Week_Per_100000'] > 0) & (
        #     df_file['Cases_Last_Week_Per_100000'] < 5)
        # is_010 = (df_file['Cases_Last_Week_Per_100000'] >= 5) & (
        #     df_file['Cases_Last_Week_Per_100000'] < 10)
        # is_025 = (df_file['Cases_Last_Week_Per_100000'] >= 10) & (
        #     df_file['Cases_Last_Week_Per_100000'] < 25)
        # is_050 = (df_file['Cases_Last_Week_Per_100000'] >= 25) & (
        #     df_file['Cases_Last_Week_Per_100000'] < 50)
        # is_100 = (df_file['Cases_Last_Week_Per_100000'] >= 50) & (
        #     df_file['Cases_Last_Week_Per_100000'] < 100)
        # is_200 = (df_file['Cases_Last_Week_Per_100000'] >= 100) & (
        #     df_file['Cases_Last_Week_Per_100000'] < 200)
        # is_400 = (df_file['Cases_Last_Week_Per_100000'] >= 200) & (
        #     df_file['Cases_Last_Week_Per_100000'] < 400)
        # is_999 = (df_file['Cases_Last_Week_Per_100000'] >= 400)

        gt_000 = df_file["Cases_Last_Week_Per_100000"] > 0
        gt_005 = df_file["Cases_Last_Week_Per_100000"] >= 5
        gt_010 = df_file["Cases_Last_Week_Per_100000"] >= 10
        gt_025 = df_file["Cases_Last_Week_Per_100000"] >= 25
        gt_050 = df_file["Cases_Last_Week_Per_100000"] >= 50
        gt_100 = df_file["Cases_Last_Week_Per_100000"] >= 100
        gt_200 = df_file["Cases_Last_Week_Per_100000"] >= 200
        gt_400 = df_file["Cases_Last_Week_Per_100000"] >= 400

        # lt_005 = (df_file['Cases_Last_Week_Per_100000'] < 5)
        # lt_010 = (df_file['Cases_Last_Week_Per_100000'] < 10)
        # lt_025 = (df_file['Cases_Last_Week_Per_100000'] < 25)
        # lt_050 = (df_file['Cases_Last_Week_Per_100000'] < 50)
        # lt_100 = (df_file['Cases_Last_Week_Per_100000'] < 100)
        # lt_200 = (df_file['Cases_Last_Week_Per_100000'] < 200)
        # lt_400 = (df_file['Cases_Last_Week_Per_100000'] < 400)

        # df['0'] += is_000 * 1
        # df['5'] += is_005 * 1
        # df['10'] += is_010 * 1
        # df['25'] += is_025 * 1
        # df['50'] += is_050 * 1
        # df['100'] += is_100 * 1
        # df['200'] += is_200 * 1
        # df['400'] += is_400 * 1
        # df['999'] += is_999 * 1

        df[">0"] += gt_000 * 1
        df[">5"] += gt_005 * 1
        df[">10"] += gt_010 * 1
        df[">25"] += gt_025 * 1
        df[">50"] += gt_050 * 1
        df[">100"] += gt_100 * 1
        df[">200"] += gt_200 * 1
        df[">400"] += gt_400 * 1

        # df['=0'] += is_000 * 1
        # df['<5'] += lt_005 * 1
        # df['<10'] += lt_010 * 1
        # df['<25'] += lt_025 * 1
        # df['<50'] += lt_050 * 1
        # df['<100'] += lt_100 * 1
        # df['<200'] += lt_200 * 1
        # df['<400'] += lt_400 * 1

        # +X%
        gt_p001p = df_file["Cases_Last_Week_7Day_Percent"] >= 1
        gt_p025p = df_file["Cases_Last_Week_7Day_Percent"] >= 25
        gt_p050p = df_file["Cases_Last_Week_7Day_Percent"] >= 50
        gt_p100p = df_file["Cases_Last_Week_7Day_Percent"] >= 100
        gt_p200p = df_file["Cases_Last_Week_7Day_Percent"] >= 200
        gt_m001p = df_file["Cases_Last_Week_7Day_Percent"] <= -1
        gt_m025p = df_file["Cases_Last_Week_7Day_Percent"] <= -25
        gt_m050p = df_file["Cases_Last_Week_7Day_Percent"] <= -50
        gt_m075p = df_file["Cases_Last_Week_7Day_Percent"] <= -75
        gt_m100p = df_file["Cases_Last_Week_7Day_Percent"] <= -100

        df["+1%"] += gt_p001p * 1
        df["+25%"] += gt_p025p * 1
        df["+50%"] += gt_p050p * 1
        df["+100%"] += gt_p100p * 1
        df["+200%"] += gt_p200p * 1
        df["-1%"] += gt_m001p * 1
        df["-25%"] += gt_m025p * 1
        df["-50%"] += gt_m050p * 1
        df["-75%"] += gt_m075p * 1
        df["-100%"] += gt_m100p * 1
        count += 1
        # TODO
        # if count >= 10:
        #     break
    # print(df.tail())

    df.to_csv("cache/hist-de-districts.csv")
    return df


# TODO
# df = read_and_prepare_data()
# os.remove("cache/hist-de-districts.csv")

if (
    helper.check_cache_file_available_and_recent(
        fname="cache/hist-de-districts.csv", max_age=0, verbose=True
    )
    == False
):
    df = read_and_prepare_data()
else:
    df = pd.read_csv("cache/hist-de-districts.csv")
    df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")
    df.set_index(["Date"], inplace=True)

date_last = pd.to_datetime(df.index[-1]).date()


def CntToPerc(x):
    return x / 412 * 100


def PercToCnt(x):
    return x / 100 * 412


# print(df)


def plot_hist_de_districts_Cases_Last_Week_Per_100000():
    # plt.style.use('default')
    # plotting
    # plt.ion()
    # plt.close("all")
    # plt.figure()
    # df.plot(y='025')

    # df_hist = df[['0', '5', '10', '25', '50', '100', '200', '400', '999']]
    df_sums_gt = df[[">0", ">5", ">10", ">25", ">50", ">100", ">200", ">400"]]
    # df_sums_lt = df[['=0', '<5', '<10', '<25',
    #                  '<50', '<100', '<200', '<400', '>400']]

    # df_hist.plot.bar(stacked=True, width=1.0)
    # # plt.ylim(top=412)
    # plt.savefig(fname='plots-python/hist-de-districts-bar.png', format='png')
    # plt.show()

    # print(df_sums_gt.head())

    myPlot = df_sums_gt.plot()

    # fig, ax = myplot.subplots(constrained_layout=True)

    # plt.ylabel('Anzahl')
    plt.title("Anzahl der Landkreise pro Inzidenz-Intervall")

    plt.tight_layout()
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt[">0"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt[">5"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt[">10"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt[">25"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt[">50"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt[">100"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt[">200"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt[">400"])

    # secaxy = plt.secondary_yaxis('right', functions=(CntToPerc, PercToCnt))
    # secaxy.set_ylabel('Percent')

    helper.mpl_add_text_source(source="RKI", date=date_last)
    plt.ylim(0, 412)
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig(
        fname="plots-python/hist-de-districts-Cases_Last_Week_Per_100000.png",
        format="png",
    )
    # plt.show()


def plot_hist_de_districts_Cases_Last_Week_7Day_Percent_Incr():
    df_sums_gt = df[["+1%", "+25%", "+50%", "+100%", "+200%"]]

    myPlot = df_sums_gt.plot()
    plt.title("Anzahl der Landkreise pro Inzidenz-Anstiegs-Intervall")

    plt.tight_layout()
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["+1%"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["+25%"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["+50%"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["+100%"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["+200%"])

    helper.mpl_add_text_source(source="RKI", date=date_last)
    plt.ylim(0, 412)
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig(
        fname="plots-python/hist-de-districts-Cases_Last_Week_7Day_Percent-Incr.png",
        format="png",
    )


def plot_hist_de_districts_Cases_Last_Week_7Day_Percent_Decr():
    df_sums_gt = df[["-1%", "-25%", "-50%", "-75%", "-100%"]]

    myPlot = df_sums_gt.plot()
    plt.title("Anzahl der Landkreise pro Inzidenz-Abnahme-Intervall")

    plt.tight_layout()
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["-1%"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["-25%"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["-50%"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["-75%"])
    plt.fill_between(list(df_sums_gt.index.values), df_sums_gt["-100%"])

    helper.mpl_add_text_source(source="RKI", date=date_last)
    plt.ylim(0, 412)
    plt.xlabel("")
    plt.ylabel("")
    plt.savefig(
        fname="plots-python/hist-de-districts-Cases_Last_Week_7Day_Percent-Decr.png",
        format="png",
    )


plot_hist_de_districts_Cases_Last_Week_Per_100000()

plot_hist_de_districts_Cases_Last_Week_7Day_Percent_Incr()
plot_hist_de_districts_Cases_Last_Week_7Day_Percent_Decr()
