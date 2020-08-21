#!/usr/local/bin/python3.6

import os
import sqlite3
import json
import hashlib
import random
from datetime import date

# TODO

##########################
# Copy of common functions
##########################


def checkRunningOnServer() -> bool:
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
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
    if os.path.isdir("/home/entorb/data-web-pages/covid-19"):
        pathToDb = '/home/entorb/data-web-pages/covid-19/newsletter.db'
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


SENDMAIL = "/usr/lib/sendmail"


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
    return "%5.1f / %4d %s   : %s\n" % (
        round(cases_lw_100k, 1), cases_lw, slope_arrow, location)


def format_line2(cases_lw_100k: str, location: str) -> str:
    return "%5.1f            : %s\n" % (round(cases_lw_100k, 1), location)


def get_slope_arrow(slope: float) -> str:
    if slope > 1:
        slope_arrow = "↑"
    elif slope > 0.5:
        slope_arrow = "↗"
    elif slope >= -0.5:
        slope_arrow = "→"
    elif slope >= -1:
        slope_arrow = "↘"
    else:
        slope_arrow = "↓"
    return slope_arrow

##########################


# set path variables
if checkRunningOnServer():
    pathToData = '/home/entorb/html/COVID-19-coronavirus/data/de-districts/de-districts-results.json'
else:
    pathToData = 'data/de-districts/de-districts-results.json'

# connect to DB
con, cur = db_connect()

# load latest data
d_districts_latest = {}
with open(pathToData, mode='r', encoding='utf-8') as fh:
    d_districts_latest = json.load(fh)
dataDate = d_districts_latest["02000"]["Date_Latest"]

d_id_cases_lw_100k = {}
# sum up German values
cases_DE_last_week = 0
for lk_id, d in d_districts_latest.items():
    cases_DE_last_week += d["Cases_Last_Week"]
    d_id_cases_lw_100k[lk_id] = d["Cases_Last_Week_Per_100000"]
    d["Slope_Cases_Arrow"] = get_slope_arrow(d["Slope_Cases_New_Per_Million"])
cases_DE_last_week_100k = cases_DE_last_week / 83.019200 / 10

# find worst districts
l_worst_lk_ids = []
for lk_id, value in sorted(d_id_cases_lw_100k.items(), key=lambda item: item[1], reverse=True):
    l_worst_lk_ids.append(lk_id)
del d_id_cases_lw_100k, lk_id
s_worst_lk = ""
number_worst = 5
count = 0
for lk_id in l_worst_lk_ids:
    count += 1
    d = d_districts_latest[lk_id]
    s_worst_lk += format_line(
        cases_lw_100k=d["Cases_Last_Week_Per_100000"],
        cases_lw=d["Cases_Last_Week"],
        location=f"{d['LK_Name']} ({d['LK_Typ']} in {d['BL_Code']})",
        slope_arrow=d["Slope_Cases_Arrow"]
    )
    if count == number_worst:
        break
del lk_id, count

# loop over subscriptions
for row in cur.execute("SELECT email, verified, hash, threshold, regions, frequency, date_registered FROM newsletter WHERE verified = 1 AND regions IS NOT NULL"):
    mailBody = ""
    # for debugging: only send to me
    # if row["email"] != "my-email-address":
    #     continue
    # mailBody += "HINWEIS: Dies ist ein Nachversand, da mir ein Fehler unterlaufen ist, der dazu führte, dass die heutige E-Mail veraltete Daten (Datenstand: 2020-07-06) enthielt. Ich bitte die Umstände zu entschuldigen. \nLG Torben\n\n\n"

    mailTo = row["email"]
    s_this_regions = row["regions"]
    l_this_regions = row["regions"].split(',')

    # for sorting by value
    d_this_regions_cases_100k = {}
    for lk_id in l_this_regions:
        d_this_regions_cases_100k[lk_id] = d_districts_latest[lk_id]["Cases_Last_Week_Per_100000"]

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
        #        mailBody += f"Versandgrund: \n\n"
        # table header
        mailBody += "Infektionen      : Landkreis\n"
        mailBody += "Rel.¹ / Absolut²\n"
        # table body
        for lk_id, value in sorted(d_this_regions_cases_100k.items(), key=lambda item: item[1], reverse=True):
            d = d_districts_latest[lk_id]
            mailBody += format_line(
                cases_lw_100k=d["Cases_Last_Week_Per_100000"],
                cases_lw=d["Cases_Last_Week"],
                location=f"{d['LK_Name']} ({d['LK_Typ']} in {d['BL_Code']})",
                slope_arrow=d["Slope_Cases_Arrow"]
            )
        mailBody += format_line2(cases_DE_last_week_100k, "Deutschland")
        # flop 10
        mailBody += "Top 5\n" + s_worst_lk

        # table footer
        mailBody += f"Datenstand: {dataDate}\n"
        mailBody += "Einheiten: Neu-Infektionen letzte Woche, ¹relativ pro 100.000 Einwohner / ²absolut\n"
        mailBody += f"\nZeitverlauf Deiner ausgewählten Landkreise: https://entorb.net/COVID-19-coronavirus/?yAxis=Cases_Last_Week_Per_100000&DeDistricts={s_this_regions}&Sort=Sort_by_last_value#DeDistrictChart\n"

        # create a new hash
        # add management link including new hash
        h = db_updateHash(mailTo)
        mailBody += f"\nAbmelden/Einstellungen ändern: https://entorb.net/COVID-19-coronavirus/newsletter-frontend.html?hash={h}\n"

        mailBody += "\nNeu anmelden: https://entorb.net/COVID-19-coronavirus/newsletter-register.html\n"

        mailBody += f"\nentorb's Coronavirus Auswertungen: https://entorb.net/COVID-19-coronavirus/\n"

        sendmail(to=mailTo, body=mailBody,
                 subject=f"[COVID-19 Landkreis Benachrichtigung] - {reason_for_sending}")
