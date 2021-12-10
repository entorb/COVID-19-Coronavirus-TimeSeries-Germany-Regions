#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
fetched German hospital occupancy data from DIVI https://www.intensivregister.de
lk_id sind https://de.wikipedia.org/wiki/Amtlicher_Gemeindeschl%C3%BCssel
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import os
import os.path
import re
import csv

# import requests  # for read_url_or_cachefile

# my helper modules
import helper


def extractLinkList(cont: str) -> list:
    # myPattern = '<a href="(/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-[^"]+/download)"'
    myPattern = r'<a href="(/divi-intensivregister-tagesreport-archiv-csv/viewdocument/\d+?/divi-intensivregister-[^"]*)"'
    #    /divi-intensivregister-tagesreport-archiv-csv/viewdocument/5330/divi-intensivregister-2020-12-21-12-15
    myRegExp = re.compile(myPattern)
    myMatches = myRegExp.findall(cont)
    assert len(myMatches) > 10, "Error: no csv download links found"
    return myMatches


def fetch_latest_csv():
    """
    fetches the latest (top) file from https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table
    output: latest.csv (overwrites old file)
    #"""

    # url = (
    #     "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table"
    # )
    # file = "cache/de-divi/list-csv-page-1.html"
    # payload = {"filter_order_Dir": "DESC", "filter_order": "tbl.ordering", "start": 0}
    # # "cid[]": "0", "category_id": "54", "task": "", "8ba87835776d29f4e379a261512319f1": "1"

    # cont = helper.read_url_or_cachefile(
    #     url=url,
    #     cachefile=file,
    #     request_type="post",
    #     payload=payload,
    #     cache_max_age=0,
    #     verbose=True,
    # )

    # # extract link of from <a href="/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-28-12-15/download"

    # l_csv_urls = extractLinkList(cont=cont)

    # # reduce list to the 5 latest files
    # # commented out, since at 07.07.2020 at the source the table sourting was strange, so that the new files where not on top of the list
    # # while len(l_csv_urls) > 5:
    # #     l_csv_urls.pop()

    # d_csvs_in_table = {}

    # # loop over urls to replace outdated files by latest file per day
    # # '/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-25-12-15/download'
    # # '/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-25-12-15-2/download'
    # for url in l_csv_urls:
    #     url = f"https://www.divi.de{url}"
    #     # '/divi-intensivregister-tagesreport-archiv-csv/viewdocument/5330/divi-intensivregister-2020-12-21-12-15'
    #     filename = re.search(
    #         r"/divi-intensivregister-tagesreport-archiv-csv/viewdocument/\d+?/divi-intensivregister-(\d{4}\-\d{2}\-\d{2})[^/]",
    #         url,
    #     ).group(1)
    #     d_csvs_in_table[filename] = url
    # del l_csv_urls, filename, url

    # l = sorted(d_csvs_in_table.keys())
    # latest_filename = l[-1]
    # latest_url = d_csvs_in_table[latest_filename]

    file = f"data/de-divi/downloaded/latest.csv"

    url = "https://diviexchange.blob.core.windows.net/%24web/zeitreihe-tagesdaten.csv"

    cont = helper.read_url_or_cachefile(
        url=url,
        cachefile=file,
        request_type="get",
        payload={},
        cache_max_age=0,  # 0s because the git pull created files are "new"
        verbose=True,
    )


# def fetch_all_csvs():
#     """
#     fetches the all files from https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table
#     only keeps the latest file per day
#     """

#     url = (
#         "https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table"
#     )
#     cachefile = "cache/de-divi/list-csv-page-1.html"
#     payload = {"filter_order_Dir": "DESC", "filter_order": "tbl.ordering", "start": 0}
#     # "cid[]": "0", "category_id": "54", "task": "", "8ba87835776d29f4e379a261512319f1": "1"

#     cont = helper.read_url_or_cachefile(
#         url=url,
#         cachefile=cachefile,
#         request_type="post",
#         payload=payload,
#         cache_max_age=0,
#         verbose=True,
#     )

#     # extract link of from <a href="/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-28-12-15/download"

#     l_csv_urls = extractLinkList(cont=cont)

#     # reduce list to the 5 latest files
#     # commented out, since at 07.07.2020 at the source the table sourting was strange, so that the new files where not on top of the list
#     # while len(l_csv_urls) > 5:
#     #     l_csv_urls.pop()

#     d_csvs_to_fetch = {}

#     # loop over urls to replace outdated files by latest file per day
#     # '/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-25-12-15/download'
#     # '/divi-intensivregister-tagesreport-archiv-csv/divi-intensivregister-2020-06-25-12-15-2/download'
#     for url in l_csv_urls:
#         url = f"https://www.divi.de{url}"
#         # '/divi-intensivregister-tagesreport-archiv-csv/viewdocument/5330/divi-intensivregister-2020-12-21-12-15'
#         filename = re.search(
#             r"/divi-intensivregister-tagesreport-archiv-csv/viewdocument/\d+?/divi-intensivregister-(\d{4}\-\d{2}\-\d{2})[^/]",
#             url,
#         ).group(1)
#         d_csvs_to_fetch[filename] = url
#     del l_csv_urls

#     assert len(d_csvs_to_fetch) > 0, "Error: no files to fetch"
#     for filename, url in d_csvs_to_fetch.items():
#         cachefile = f"data/de-divi/downloaded/{filename}.csv"

#         if not os.path.isfile(cachefile):
#             cont = helper.read_url_or_cachefile(
#                 url=url,
#                 cachefile=cachefile,
#                 request_type="get",
#                 payload={},
#                 cache_max_age=0,
#                 verbose=True,
#             )


def generate_database() -> dict:
    # TODO: use Pandas instead of manuall CVS stuff
    """from 2021-10-29 on Divi publisheds all data in the latest file"""
    d_database = {}
    # d_database_states = {}  # Bundesländer
    d_database_states = {
        "01": {},
        "02": {},
        "03": {},
        "04": {},
        "05": {},
        "06": {},
        "07": {},
        "08": {},
        "09": {},
        "10": {},
        "11": {},
        "12": {},
        "13": {},
        "14": {},
        "15": {},
        "16": {},
        "00": {},
    }
    # 00 = DE-total

    # csv_file = sorted(glob.glob('data/de-divi/downloaded/*.csv'))[-1]
    csv_file = "data/de-divi/downloaded/latest.csv"
    # (filepath, fileName) = os.path.split(csv_file)
    # (fileBaseName, fileExtension) = os.path.splitext(fileName)
    # del filepath, fileName, fileBaseName, fileExtension

    # file 2020-04-24.csv:
    # bundesland,kreis,anzahl_standorte,betten_frei,betten_belegt,faelle_covid_aktuell_im_bundesland
    # file 2020-04-26.csv:
    # gemeindeschluessel,anzahl_meldebereiche,faelle_covid_aktuell,faelle_covid_aktuell_beatmet,anzahl_standorte,betten_frei,betten_belegt,bundesland
    # 2020-04-28.csv
    # gemeindeschluessel,anzahl_meldebereiche,faelle_covid_aktuell,faelle_covid_aktuell_beatmet,anzahl_standorte,betten_frei,betten_belegt,bundesland,daten_stand
    # file 2020-06-28.csv
    # bundesland,gemeindeschluessel,anzahl_meldebereiche,faelle_covid_aktuell,faelle_covid_aktuell_beatmet,anzahl_standorte,betten_frei,betten_belegt,daten_stand
    # file 2021-10-29.csv
    # date,bundesland,gemeindeschluessel,anzahl_standorte,anzahl_meldebereiche,faelle_covid_aktuell,faelle_covid_aktuell_invasiv_beatmet,betten_frei,betten_belegt,betten_belegt_nur_erwachsen,betten_frei_nur_erwachsen

    with open(csv_file, mode="r", encoding="utf-8") as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        for row in csv_reader:
            assert len(row) >= 8, "Error: too few rows found"
            date = row["date"]
            bl_id = row["bundesland"]
            lk_id = row["gemeindeschluessel"]
            d = {
                # "bl_id": row["bundesland"],
                # "lk_id": row["gemeindeschluessel"],
                "Date": date,
                "anzahl_meldebereiche": int(row["anzahl_meldebereiche"]),
                "faelle_covid_aktuell": int(row["faelle_covid_aktuell"]),
                "anzahl_standorte": int(row["anzahl_standorte"]),
                "faelle_covid_aktuell_invasiv_beatmet": int(
                    row["faelle_covid_aktuell_invasiv_beatmet"]
                ),
                "betten_frei": int(float(row["betten_frei"])),
                "betten_belegt": int(float(row["betten_belegt"])),
            }
            # field was renamed in past
            # if "faelle_covid_aktuell_beatmet" in row:
            #     d["faelle_covid_aktuell_beatmet"] = int(
            #         row["faelle_covid_aktuell_beatmet"])
            # elif "faelle_covid_aktuell_invasiv_beatmet" in row:
            #     d["faelle_covid_aktuell_beatmet"] = int(
            #         row["faelle_covid_aktuell_invasiv_beatmet"])

            d["betten_ges"] = d["betten_frei"] + d["betten_belegt"]
            if d["betten_ges"] > 0:
                d["betten_belegt_proz"] = round(
                    100 * d["betten_belegt"] / d["betten_ges"], 1
                )
                d["faelle_covid_aktuell_proz"] = round(
                    100 * d["faelle_covid_aktuell"] / d["betten_ges"], 1
                )
            else:
                d["betten_belegt_proz"] = None
                d["faelle_covid_aktuell_proz"] = None
            if d["faelle_covid_aktuell"] > 0:
                d["faelle_covid_aktuell_beatmet_proz"] = round(
                    100
                    * d["faelle_covid_aktuell_invasiv_beatmet"]
                    / d["faelle_covid_aktuell"],
                    1,
                )
            else:
                d["faelle_covid_aktuell_beatmet_proz"] = 0

            # if "daten_stand" in row:
            #     d["daten_stand"] = row["daten_stand"]
            # else:
            #     d["daten_stand"] = date

            if lk_id not in d_database:
                d_database[lk_id] = []
            d_database[lk_id].append(d)

            # calc de_states_sum
            d2 = dict(d)
            del (
                d2["Date"],
                d2["betten_ges"],
                d2["betten_belegt_proz"],
                d2["faelle_covid_aktuell_proz"],
                d2["faelle_covid_aktuell_beatmet_proz"],
            )
            if date not in d_database_states[bl_id]:
                d_database_states[bl_id][date] = d2
            else:
                for k in d2.keys():
                    d_database_states[bl_id][date][k] += d2[k]
            # 'DE-total'
            if date not in d_database_states["00"]:
                d_database_states["00"][date] = d2
            else:
                for k in d2.keys():
                    d_database_states["00"][date][k] += d2[k]

                # print(d_database_states[bl_id][date])

    helper.write_json(
        "cache/de-divi/de-divi-V3.json", d_database, sort_keys=True, indent=1
    )

    l_lkids = d_database.keys()
    helper.write_json(
        "data/de-divi/lkids.json", sorted(set(l_lkids)), sort_keys=True, indent=1
    )

    d_database_states2 = {}
    for bl_id in d_database_states.keys():
        bl_code = helper.d_BL_code_from_BL_ID[int(bl_id)]
        d_database_states2[bl_code] = []
        for date, d in d_database_states[bl_id].items():
            d["Date"] = date
            # copy from above:
            d["betten_ges"] = d["betten_frei"] + d["betten_belegt"]
            if d["betten_ges"] > 0:
                d["betten_belegt_proz"] = round(
                    100 * d["betten_belegt"] / d["betten_ges"], 1
                )
                d["faelle_covid_aktuell_proz"] = round(
                    100 * d["faelle_covid_aktuell"] / d["betten_ges"], 1
                )
            else:
                d["betten_belegt_proz"] = None
                d["faelle_covid_aktuell_proz"] = None
            if d["faelle_covid_aktuell"] > 0:
                d["faelle_covid_aktuell_beatmet_proz"] = round(
                    100
                    * d["faelle_covid_aktuell_invasiv_beatmet"]
                    / d["faelle_covid_aktuell"],
                    1,
                )
            else:
                d["faelle_covid_aktuell_beatmet_proz"] = 0

            d_database_states2[bl_code].append(d)
    del d_database_states

    helper.write_json(
        "cache/de-divi/de-divi-V3-states.json",
        d_database_states2,
        sort_keys=True,
        indent=1,
    )

    return d_database


# def generate_database_old() -> dict:
#     d_database = {}
#     # d_database_states = {}  # Bundesländer
#     d_database_states = {'01': {}, '02': {}, '03': {}, '04': {}, '05': {}, '06': {}, '07': {
#     }, '08': {}, '09': {}, '10': {}, '11': {}, '12': {}, '13': {}, '14': {}, '15': {}, '16': {}, 'DE-total': {}}
#     for csv_file in sorted(glob.glob('data/de-divi/downloaded/*.csv')):
#         (filepath, fileName) = os.path.split(csv_file)
#         (fileBaseName, fileExtension) = os.path.splitext(fileName)
#         date = fileBaseName
#         del filepath, fileName, fileBaseName, fileExtension

# # file 2020-04-24.csv:
# # bundesland,kreis,anzahl_standorte,betten_frei,betten_belegt,faelle_covid_aktuell_im_bundesland
# # file 2020-04-26.csv:
# # gemeindeschluessel,anzahl_meldebereiche,faelle_covid_aktuell,faelle_covid_aktuell_beatmet,anzahl_standorte,betten_frei,betten_belegt,bundesland
# # 2020-04-28.csv
# # gemeindeschluessel,anzahl_meldebereiche,faelle_covid_aktuell,faelle_covid_aktuell_beatmet,anzahl_standorte,betten_frei,betten_belegt,bundesland,daten_stand
# # file 2020-06-28.csv
# # bundesland,gemeindeschluessel,anzahl_meldebereiche,faelle_covid_aktuell,faelle_covid_aktuell_beatmet,anzahl_standorte,betten_frei,betten_belegt,daten_stand


# # -> skipping file 2020-04-24.csv and 2020-04-25.csv
#        if date in ('2020-04-24', '2020-04-25'):
#             continue

#         with open(csv_file, mode='r', encoding='utf-8') as f:
#             csv_reader = csv.DictReader(f, delimiter=",")
#             for row in csv_reader:
#                 assert len(row) >= 8, "Error: too few rows found"
#                 bl_id = row["bundesland"]
#                 lk_id = row["gemeindeschluessel"]
#                 d = {
#                     # "bl_id": row["bundesland"],
#                     # "lk_id": row["gemeindeschluessel"],
#                     "Date": date,
#                     "anzahl_meldebereiche": int(row["anzahl_meldebereiche"]),
#                     "faelle_covid_aktuell": int(row["faelle_covid_aktuell"]),
#                     "anzahl_standorte": int(row["anzahl_standorte"]),
#                     "betten_frei": int(float(row["betten_frei"])),
#                     "betten_belegt": int(float(row["betten_belegt"]))
#                 }
#                 if "faelle_covid_aktuell_beatmet" in row:
#                     d["faelle_covid_aktuell_beatmet"] = int(
#                         row["faelle_covid_aktuell_beatmet"])
#                 elif "faelle_covid_aktuell_invasiv_beatmet" in row:
#                     d["faelle_covid_aktuell_beatmet"] = int(
#                         row["faelle_covid_aktuell_invasiv_beatmet"])

#                 d["betten_ges"] = d["betten_frei"] + d["betten_belegt"]
#                 if d["betten_ges"] > 0:
#                     d["betten_belegt_proz"] = round(100 *
#                                                     d["betten_belegt"] / d["betten_ges"], 1)
#                     d["faelle_covid_aktuell_proz"] = round(100*d["faelle_covid_aktuell"] /
#                                                            d["betten_ges"], 1)
#                 else:
#                     d["betten_belegt_proz"] = None
#                     d["faelle_covid_aktuell_proz"] = None
#                 if d["faelle_covid_aktuell"] > 0:
#                     d["faelle_covid_aktuell_beatmet_proz"] = round(
#                         100*d["faelle_covid_aktuell_beatmet"] / d["faelle_covid_aktuell"], 1)
#                 else:
#                     d["faelle_covid_aktuell_beatmet_proz"] = 0

#                 # if "daten_stand" in row:
#                 #     d["daten_stand"] = row["daten_stand"]
#                 # else:
#                 #     d["daten_stand"] = date

#                 if lk_id not in d_database:
#                     d_database[lk_id] = []
#                 d_database[lk_id].append(d)

#                 # calc de_states_sum
#                 d2 = dict(d)
#                 del d2['Date'], d2['betten_ges'], d2['betten_belegt_proz'], d2['faelle_covid_aktuell_proz'], d2['faelle_covid_aktuell_beatmet_proz']
#                 if date not in d_database_states[bl_id]:
#                     d_database_states[bl_id][date] = d2
#                 else:
#                     for k in d2.keys():
#                         d_database_states[bl_id][date][k] += d2[k]
#                 # 'DE-total'
#                 if date not in d_database_states['DE-total']:
#                     d_database_states['DE-total'][date] = d2
#                 else:
#                     for k in d2.keys():
#                         d_database_states['DE-total'][date][k] += d2[k]

#                     # print(d_database_states[bl_id][date])

#     helper.write_json('cache/de-divi/de-divi-V3.json',
#                       d_database, sort_keys=True, indent=1)

#     d_database_states2 = {}
#     for bl_id in d_database_states.keys():
#         bl_code = helper.d_BL_code_from_BL_ID[int(bl_id)]
#         d_database_states2[bl_code] = []
#         for date, d in d_database_states[bl_id].items():
#             d['Date'] = date
#             # copy from above:
#             d["betten_ges"] = d["betten_frei"] + d["betten_belegt"]
#             if d["betten_ges"] > 0:
#                 d["betten_belegt_proz"] = round(100 *
#                                                 d["betten_belegt"] / d["betten_ges"], 1)
#                 d["faelle_covid_aktuell_proz"] = round(100*d["faelle_covid_aktuell"] /
#                                                        d["betten_ges"], 1)
#             else:
#                 d["betten_belegt_proz"] = None
#                 d["faelle_covid_aktuell_proz"] = None
#             if d["faelle_covid_aktuell"] > 0:
#                 d["faelle_covid_aktuell_beatmet_proz"] = round(
#                     100*d["faelle_covid_aktuell_beatmet"] / d["faelle_covid_aktuell"], 1)
#             else:
#                 d["faelle_covid_aktuell_beatmet_proz"] = 0

#             d_database_states2[bl_code].append(d)
#     del d_database_states

#     helper.write_json('cache/de-divi/de-divi-V3-states.json',
#                       d_database_states2, sort_keys=True, indent=1)

#     return d_database


def export_tsv(d_database):
    for lk_id, l_time_series in d_database.items():
        fileOut = f"data/de-divi/tsv/{lk_id}"
        with open(fileOut + ".tsv", mode="w", encoding="utf-8", newline="\n") as fh:
            csvwriter = csv.DictWriter(
                fh,
                delimiter="\t",
                extrasaction="ignore",
                fieldnames=[
                    "Date",
                    "betten_ges",
                    "betten_belegt",
                    "betten_belegt_proz",
                    "faelle_covid_aktuell",
                    "faelle_covid_aktuell_proz",
                    "faelle_covid_aktuell_invasiv_beatmet",
                    "faelle_covid_aktuell_beatmet_proz",
                ],
            )
            csvwriter.writeheader()
            for d in l_time_series:
                csvwriter.writerow(d)


# fetch_all_csvs()
fetch_latest_csv()
d_database = generate_database()
export_tsv(d_database)
