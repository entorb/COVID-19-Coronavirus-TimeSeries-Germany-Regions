#!/usr/bin/env python3.10
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions
import datetime
import hashlib
import os
import random
import re
import sqlite3

# import bcrypt

# TODO


##########################
# Copy of common functions
##########################
def checkRunningOnServer() -> bool:
    return os.path.isdir("/var/www/virtual/entorb/data-web-pages/covid-19")


def genHash(email: str) -> str:
    s = email + str(random.random())  # noqa: S311
    return gen_SHA256_string(s)


def updateHash(email) -> str:
    h = genHash(email)
    sql = "UPDATE newsletter SET hash = ? WHERE email = ?"
    cur.execute(sql, (h, email))
    con.commit()
    return h


def gen_SHA256_string(s: str) -> str:
    m = hashlib.sha256()
    m.update(s.encode("ascii"))
    return m.hexdigest()


def insertNewEMail(email: str):
    email = email.lower()  # ensure mail in lower case
    checkValidEMail(email)
    h = genHash(email)
    cur.execute(
        "INSERT INTO newsletter(email, verified, hash, threshold, frequency) VALUES (?,?,?)",
        (email, 1, h, 300, 7),
    )
    con.commit()
    return h


def checkValidEMail(email: str) -> bool:
    # from https://stackoverflow.com/posts/719543/timeline bottom edit
    if not re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        print("Error: invalid email")
        quit()
    return True


##########################


def deleteDB():
    if not checkRunningOnServer() and os.path.isfile(pathToDb):
        os.remove(pathToDb)


def create_table():
    """
    email: text
    verified: unverified -> 0 , verified -> 1
    hash: secred used for admin of that row, updated upon sending of mail
    threshold: value for alter
    regions: list of lk_ids
    frequency: sending frequency, 1= daily, 7=weekly on Sunday
    """
    cur.execute(
        """
      CREATE TABLE newsletter (
          email text,
          verified int,
          hash text,
          threshold int,
          regions text,
          frequency int,
          date_registered date
          )
      """,
    )


def test_select():
    for row in cur.execute("SELECT * FROM newsletter"):
        print(row)
    print(
        "%s rows in the DB table"
        % cur.execute("SELECT count(*) FROM newsletter").fetchone()[0],
    )


# check I running on entorb.net webserver
if checkRunningOnServer():
    pathToDb = "/var/www/virtual/entorb/data-web-pages/covid-19/newsletter.db"
else:
    pathToDb = "cache/newsletter.db"


deleteDB()

con = sqlite3.connect(pathToDb)
cur = con.cursor()

create_table()
cur.execute(
    "INSERT INTO newsletter(email, verified, hash, threshold, regions, frequency, date_registered) VALUES (?,?,?,?,?,?,?)",
    (
        "2tokes@web.de",
        1,
        "36c83758b4174d96dc5b2006d40964c8dd1a39d1a3f4e49885c0af5598936631",
        300,
        "09562,09572,09563,09564,03353,02000,14612",
        1,
        datetime.date.today(),
    ),
)

cur.execute(
    "INSERT INTO newsletter(email, verified, hash, threshold, regions, frequency, date_registered) VALUES (?,?,?,?,?,?,?)",
    (
        "t@entorb.net",
        1,
        "36c83758b4174d96dc5b2006d40964c8dd1a39d1a3f4e49885c0af5598936631",
        300,
        "09562,09572,09563,09564,03353,02000,14612",
        1,
        datetime.date.today(),
    ),
)

cur.execute(
    "INSERT INTO newsletter(email, verified, hash, threshold, regions, frequency, date_registered) VALUES (?,?,?,?,?,?,?)",
    (
        "tokes@web.de",
        1,
        "36c83758b4174d96dc5b2006d40964c8dd1a39d1a3f4e49885c0af5598936631",
        300,
        "09562,09572,09563,09564,03353,02000,14612",
        1,
        datetime.date.today(),
    ),
)

con.commit()
test_select()


cur.close()
con.close()
