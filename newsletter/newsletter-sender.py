#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import os
import sqlite3
import json
import hashlib
import random
from datetime import date, timedelta

# TODO

##########################
# Copy of common functions
##########################


def checkRunningOnServer() -> bool:
    if os.path.isdir("/var/www/virtual/entorb/data-web-pages/covid-19"):
        return True
    else:
        return False


def genHash(email: str) -> str:
    s = email + str(random.random())
    return gen_SHA256_string(s)


def gen_SHA256_string(s: str) -> str:
    m = hashlib.sha256()
    m.update(s.encode('ascii'))
    return m.hexdigest()


def db_connect():
    # check I running on entorb.net webserver
    if os.path.isdir("/var/www/virtual/entorb/data-web-pages/covid-19"):
        pathToDb = '/var/www/virtual/entorb/data-web-pages/covid-19/newsletter.db'
    else:
        pathToDb = 'cache/newsletter.db'
    con = sqlite3.connect(pathToDb)
    con.row_factory = sqlite3.Row  # allows for access via row["name"]
    cur = con.cursor()
    return con, cur


def db_updateHash(email) -> str:
    "in DB: update hash of email. returns hash"
    curUpdate = con.cursor()
    h = genHash(email)
    sql = "UPDATE newsletter SET hash = ? WHERE email = ?"
    curUpdate.execute(sql, (h, email))
    con.commit()
    return h


SENDMAIL = "/usr/sbin/sendmail"


def sendmail(to: str, body: str, subject: str, sender: str = 'no-reply@entorb.net'):
    mail = f"To: {to}\nSubject: {subject}\nFrom: {sender}\nContent-Type: text/plain; charset=\"utf-8\"\n\n{body}"
    if checkRunningOnServer():
        p = os.popen(f"{SENDMAIL} -t -i", "w")
        p.write(mail)
        # status = p.close()
        p.close()
    else:
        print(mail)


def format_line(cases_lw_100k: str, cases_lw: str, location: str, slope_arrow: str) -> str:
    return "%6.1f | %5d | %3s | %s\n" % (
        round(cases_lw_100k, 1), cases_lw, slope_arrow, location)


def format_line_only_rel(cases_lw_100k: str, location: str, slope_arrow: str) -> str:
    return "%6.1f           %3s | %s\n" % (round(cases_lw_100k, 1), slope_arrow, location)


# def get_slope_arrow(slope: float) -> str:
#     if slope >= 3:
#         slope_arrow = "↑"
#     elif slope >= 1:
#         slope_arrow = "↗"
#     elif slope > -1:
#         slope_arrow = "→"
#     elif slope > -3:
#         slope_arrow = "↘"
#     else:
#         slope_arrow = "↓"
#     return slope_arrow


def get_slope_text(slope: float) -> str:
    # s = "%+5.1f%%" % slope
    s = "%+3d%%" % slope
    return s


def get_slope_text_from_dict(d: dict) -> str:
    slope = 0
    # if "Slope_Cases_Last_Week_Percent" in d:
    #     slope = d["Slope_Cases_Last_Week_Percent"]
    if "Cases_Last_Week_7Day_Percent" in d:
        slope = d["Cases_Last_Week_7Day_Percent"]
    return get_slope_text(slope)

##########################


# set path variables
pathPrefixOnServer = '/var/www/virtual/entorb/html/COVID-19-coronavirus/'
pathToDataDeDistricts = 'data/de-districts/de-districts-results.json'
pathToDataDeStates = 'data/de-states/de-states-latest.json'
pathToDataCountries = 'data/int/countries-latest-all.json'
if checkRunningOnServer():
    pathToDataDeDistricts = pathPrefixOnServer + pathToDataDeDistricts
    pathToDataDeStates = pathPrefixOnServer + pathToDataDeStates
    pathToDataCountries = pathPrefixOnServer + pathToDataCountries

# connect to DB
con, cur = db_connect()

# load latest data
d_data_DeDistricts = {}
with open(pathToDataDeDistricts, mode='r', encoding='utf-8') as fh:
    d_data_DeDistricts = json.load(fh)

s_date_data_hh = d_data_DeDistricts["02000"]["Date_Latest"]
date_data_hh = date.fromisoformat(s_date_data_hh)
date_yesterday = date.today()-timedelta(days=1)
assert date_data_hh == date_yesterday, f"date data hh: {date_data_hh} != date yesterday {date_yesterday}"
del date_data_hh, date_yesterday

d_data_DeStates = {}
with open(pathToDataDeStates, mode='r', encoding='utf-8') as fh:
    d_data_DeStates = json.load(fh)

d_data_Countries = {}
with open(pathToDataCountries, mode='r', encoding='utf-8') as fh:
    # convert list to dict
    l = json.load(fh)
    for d in l:
        code = d['Code']
        del d['Code']
        d_data_Countries[code] = d
del code, fh, l, d

# Ranking of worst Landkreise
d_id_cases_DeDistricts = {}
for id, d in d_data_DeDistricts.items():
    # handling of missing disticts from API response
    if id not in d_data_DeDistricts or "Cases_Last_Week_Per_Million" not in d:
        # print(id, d)
        continue
    d_id_cases_DeDistricts[id] = d["Cases_Last_Week_Per_Million"]/10
    d["Slope"] = get_slope_text_from_dict(d)
l_worst_lk_ids = []
for id, value in sorted(d_id_cases_DeDistricts.items(), key=lambda item: item[1], reverse=True):
    l_worst_lk_ids.append(id)
del d_id_cases_DeDistricts, id

# Ranking of worst Bundesländer
d_id_cases_DeStates = {}
for id, d in d_data_DeStates.items():
    if id == 'DE-total':
        cases_DE_last_week_100k = d["Cases_Last_Week_Per_Million"]/10
        slope_DE = get_slope_text_from_dict(d)

    else:
        d_id_cases_DeStates[id] = d["Cases_Last_Week_Per_Million"]/10
        d["Slope"] = get_slope_text_from_dict(d)
l_worst_bl_ids = []
for id, value in sorted(d_id_cases_DeStates.items(), key=lambda item: item[1], reverse=True):
    l_worst_bl_ids.append(id)
del d_id_cases_DeStates, id

# Ranking of worst Countries
d_id_cases_Countries = {}
for id, d in d_data_Countries.items():
    d_id_cases_Countries[id] = d["Cases_Last_Week_Per_Million"]/10
    d["Slope"] = get_slope_text_from_dict(d)
l_worst_country_ids = []
for id, value in sorted(d_id_cases_Countries.items(), key=lambda item: item[1], reverse=True):
    l_worst_country_ids.append(id)
del d_id_cases_Countries, id


# string snippet of worst DeDistricts
s_worst_lk = ""
max_lines = 10
count = 0
for id in l_worst_lk_ids:
    count += 1
    d = d_data_DeDistricts[id]
    s_worst_lk += format_line(
        cases_lw_100k=d["Cases_Last_Week_Per_Million"]/10,
        cases_lw=d["Cases_Last_Week"],
        location=f"{d['LK_Name']} ({d['LK_Typ']} in {d['BL_Code']})",
        slope_arrow=d["Slope"]
    )
    if count == max_lines:
        break

# string snippet of worst Bundesländer
s_worst_bl = ""
for id in l_worst_bl_ids:
    d = d_data_DeStates[id]
    s_worst_bl += format_line(
        cases_lw_100k=d["Cases_Last_Week_Per_Million"]/10,
        cases_lw=d["Cases_Last_Week"],
        location=f"{d['State']}",
        slope_arrow=d["Slope"]
    )

# string snippet of worst Countries
s_worst_countries = ""
max_lines = 30
count = 0
for id in l_worst_country_ids:
    count += 1
    d = d_data_Countries[id]
    s_worst_countries += format_line_only_rel(
        cases_lw_100k=d["Cases_Last_Week_Per_Million"]/10,
        location=f"{d['Country']}",
        slope_arrow=d["Slope"]
    )
    if count == max_lines:
        break


# loop over subscriptions
for row in cur.execute("SELECT email, verified, hash, threshold, regions, frequency, date_registered FROM newsletter WHERE verified = 1 AND regions IS NOT NULL"):
    mailBody = ""
    # for debugging: only send to me
    # if row["email"] != "my-email-address":
    #     continue
    mailBody += """HINWEIS: Aufgrund der aktuellen Lage habe ich eine "Prognose für Intensivstations Bettenbedarf" erstellt. Gerne an Krankenhäuser weitergeben, vielleicht hilft es für deren Planung.
    https://entorb.net/COVID-19-coronavirus/#DeStatesIcuForecast
    LG Torben\n\n\n"""

    mailTo = row["email"]
    s_this_regions = row["regions"]
    l_this_regions = row["regions"].split(',')
    # 16056 Eisenach was merged with 16063: LK Wartburgkreis
    # see https://www.eisenach.de/rathaus/fusion-der-stadt-eisenach
    if "16056" in l_this_regions:
        l_this_regions.remove("16056")

    # for sorting by value
    d_this_regions_cases_100k = {}
    for lk_id in l_this_regions:
        d_this_regions_cases_100k[lk_id] = d_data_DeDistricts[lk_id]["Cases_Last_Week_Per_Million"]/10

    toSend = False
    reason_for_sending = ""
    # check if notification is due, based on threshold and frequency
    # daily sending
    if row["threshold"] <= max(d_this_regions_cases_100k.values()):
        toSend = True
        reason_for_sending = "Grenzwert überschritten"
    elif row["frequency"] == 1:
        toSend = True
        reason_for_sending = "Täglicher Versand"
    elif row["frequency"] == 7 and date.today().isoweekday() == 7:
        toSend = True
        reason_for_sending = "Sonntäglicher Versand"

    if toSend:
        # mailBody += f"Hinweis: Die Landkreisdaten stammen vom RKI und werden dort um 0:00 Uhr veröffentlicht. Die Gesundheitsämter sind teilweise schneller in der Aktualisierung ihrer Zahlen, daher findet man unterschiedliche Zahlen in unterschiedlichen Quellen.\n\n"
        # table header
        mailBody += "Infektionen      : Ort\n"
        mailBody += "Rel.¹ | Absolut² | Änderung³\n"
        mailBody += "Deine Landkreisauswahl\n"
        # table body
        for lk_id, value in sorted(d_this_regions_cases_100k.items(), key=lambda item: item[1], reverse=True):
            d = d_data_DeDistricts[lk_id]
            if "Slope" not in d:  # handling of missing disticts from API response
                continue
            mailBody += format_line(
                cases_lw_100k=d["Cases_Last_Week_Per_Million"]/10,
                cases_lw=d["Cases_Last_Week"],
                location=f"{d['LK_Name']} ({d['LK_Typ']} in {d['BL_Code']})",
                slope_arrow=d["Slope"]
            )

        mailBody += "\nTop 10 Landkreise\n" + s_worst_lk

        mailBody += f"Datenstand Landkreisdaten: {s_date_data_hh}\n"

        mailBody += f"Hinweis: Die Landkreisdaten stammen vom RKI und werden dort um 0:00 Uhr veröffentlicht. Die Gesundheitsämter sind teilweise schneller in der Aktualisierung ihrer Zahlen, daher findet man unterschiedliche Zahlen in unterschiedlichen Quellen.\n"

        mailBody += "\nBundesländer\n" + s_worst_bl

        mailBody += "\nDeutschland gemittelt\n" + format_line_only_rel(cases_DE_last_week_100k,
                                                                       "Deutschland", slope_DE)
        mailBody += "\nLänder der Welt\n" + s_worst_countries

        # table footer
        mailBody += "Einheiten: Neu-Infektionen letzte Woche, ¹relativ pro 100.000 Einwohner, ²absolut, ³7-Tages Differenz\n"
        mailBody += f"\nZeitverlauf Deiner ausgewählten Landkreise: https://entorb.net/COVID-19-coronavirus/?yAxis=Cases_Last_Week_Per_100000&DeDistricts={s_this_regions}&Sort=Sort_by_last_value#DeDistrictChart\n"

        # create a new hash
        # add management link including new hash
        h = db_updateHash(mailTo)
        mailBody += f"\nAbmelden/Einstellungen ändern: https://entorb.net/COVID-19-coronavirus/newsletter-frontend.html?hash={h}\n"

        mailBody += "\nNeu anmelden: https://entorb.net/COVID-19-coronavirus/newsletter-register.html\n"

        mailBody += f"\nAlle Auswertungen: https://entorb.net/COVID-19-coronavirus/\n"

        sendmail(to=mailTo, body=mailBody,
                 subject=f"[COVID-19 Landkreis Benachrichtigung] - {reason_for_sending}")
