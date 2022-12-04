#!/usr/bin/env python3.10
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions
import json
import os
import sqlite3

# import datetime


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

# Maintenance
# cur.execute("ALTER TABLE newsletter ADD date_registered date")
# cur.execute("UPDATE newsletter set date_registered  = ?",
#             (datetime.date.today(),))
# con.commit()

# threshold: per Million to per 100k
# cur.execute("UPDATE newsletter SET threshold = 30 WHERE threshold = 300")
# con.commit()

# cur.execute("DELETE FROM newsletter WHERE email = 'soll@weg.de'")
# con.commit()


print("=== List of Users ===")
print("%-20s %1s %3s %1s" % ("email", "v", "t", "f"))
sql = "SELECT email, verified, hash, threshold, regions, frequency, date_registered FROM newsletter ORDER BY date_registered ASC"
d_region_counter = {}
count_rows = 0
for row in cur.execute(sql):
    print(
        "%-20s %1s %3s %1s %s\n %-45s\n %-64s"
        % (
            row["email"],
            row["verified"],
            row["threshold"],
            row["frequency"],
            row["date_registered"],
            row["regions"],
            row["hash"],
        ),
    )
    if row["verified"] == 1 and row["regions"] is not None:
        count_rows += 1
        l_this_regions = row["regions"].split(",")
        for region in l_this_regions:
            if region not in d_region_counter:
                d_region_counter[region] = 1
            else:
                d_region_counter[region] += 1

print("")
print("=== Landkreis-Ranking ===")
print("id    : Anz : Landkreis")
for my_id, value in sorted(
    d_region_counter.items(),
    key=lambda item: item[1],
    reverse=True,
):
    if value <= 2:
        break
    print(f"{my_id} : %3d : {d_districts_latest[my_id]['Landkreis']}" % value)

print(f"{count_rows} Abonnenten")
cur.close()
con.close()
