#!/usr/bin/env python3.10
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions
import datetime
import json
import os
import sqlite3


# Print necessary headers.
print("Content-Type: text/html; charset=UTF-8")
print()


##########################
# Copy of common functions
##########################
def checkRunningOnServer() -> bool:
    return os.path.isdir("/var/www/virtual/entorb/data-web-pages/covid-19")


def db_connect():
    "connect to sqlite DB"
    # check I running on entorb.net webserver
    if os.path.isdir("/var/www/virtual/entorb/data-web-pages/covid-19"):
        pathToDb = "/var/www/virtual/entorb/data-web-pages/covid-19/newsletter.db"
    else:
        pathToDb = "cache/newsletter.db"
    con = sqlite3.connect(pathToDb)
    con.row_factory = sqlite3.Row  # allows for access via row["name"]
    cur = con.cursor()
    return con, cur


##########################


print(
    """<!doctype html>
<html lang="de">

<head>
  <title>COVID-19 Landkreis Benachrichtigung - Stats</title>
  <meta charset="utf-8">
  <meta name="author" content="Dr. Torben Menke">
  <link rel="stylesheet" href="/style.css" />
</head>

<body>
""",
)


# set path variables
if checkRunningOnServer():
    pathToData = "/var/www/virtual/entorb/html/COVID-19-coronavirus/data/de-districts/de-districts-results.json"
else:
    pathToData = "data/de-districts/de-districts-results.json"

# load latest data
d_districts_latest = {}
with open(pathToData, encoding="utf-8") as fh:
    d_districts_latest = json.load(fh)

con, cur = db_connect()
sql = "SELECT date_registered, regions FROM newsletter WHERE regions IS NOT NULL"
d_counter_region = {}
d_counter_date = {}
d_counter_week = {}
count_rows = 0
for row in cur.execute(sql):
    count_rows += 1
    l_this_regions = row["regions"].split(",")
    for region in l_this_regions:
        if region not in d_counter_region:
            d_counter_region[region] = 1
        else:
            d_counter_region[region] += 1
    date = datetime.datetime.strptime(row["date_registered"], "%Y-%m-%d")
    week = date.strftime("%Y-%V")
    if date not in d_counter_date:
        d_counter_date[date] = 1
    else:
        d_counter_date[date] += 1
    if week not in d_counter_week:
        d_counter_week[week] = 1
    else:
        d_counter_week[week] += 1

cur.close()
con.close()

print(f"<h2>{count_rows} Abonnenten</h2>")


print("<h2>Landkreis-Ranking</h2>")
print('<table border="1">')
print("<tr><th>Anzahl</th><th>Landkreis</th></tr>")
# print("Anz : Landkreis")
for my_id, value in sorted(
    d_counter_region.items(),
    key=lambda item: item[1],
    reverse=True,
):
    if value < 5:
        break
    lk_name = (
        d_districts_latest[my_id]["Landkreis"]
        .encode("ascii", "xmlcharrefreplace")
        .decode()
    )
    # lk_name = lk_name.replace("ö", "&ouml;")
    # print(f"%3d : {d_districts_latest[id]['Landkreis']}" % value)
    print(f"<tr><td>{value}</td><td>{lk_name}</td></tr>")
print("</table>")

print("<h2>Anmeldungen</h2>")
print('<table border="1">')
print("<tr><th>Woche</th><th>Neue Abonnenten</th></tr>")
# print("Anz : Landkreis")
for week, value in sorted(d_counter_week.items(), reverse=True):
    # print(f"%3d : {d_districts_latest[id]['Landkreis']}" % value)
    print(f"<tr><td>{week}</td><td>{value}</td></tr>")
print("</table>")


print("</body>\n</html>")
