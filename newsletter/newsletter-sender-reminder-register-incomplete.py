#!/usr/bin/python3.8
# -*- coding: utf-8 -*-

import os
import sqlite3
import json
import hashlib
import random
from datetime import date
from datetime import datetime

##########################
# Copy of common functions
##########################


def checkRunningOnServer() -> bool:
    if os.path.isdir("/var/www/virtual/entorb/data-web-pages/covid-19"):
        return True
    else:
        return False


def db_connect():
    # check I running on entorb.net webserver
    if os.path.isdir("/var/www/virtual/entorb/data-web-pages/covid-19"):
        pathToDb = "/var/www/virtual/entorb/data-web-pages/covid-19/newsletter.db"
    else:
        pathToDb = "cache/newsletter.db"
    con = sqlite3.connect(pathToDb)
    con.row_factory = sqlite3.Row  # allows for access via row["name"]
    cur = con.cursor()
    return con, cur


# SENDMAIL = "/usr/sbin/sendmail"


# def sendmail(to: str, body: str, subject: str, sender: str = 'no-reply@entorb.net'):
#     mail = f"To: {to}\nSubject: {subject}\nFrom: {sender}\nContent-Type: text/plain; charset=\"utf-8\"\n\n{body}"
#     if checkRunningOnServer():
#         p = os.popen(f"{SENDMAIL} -t -i", "w")
#         p.write(mail)
#         # status = p.close()
#         p.close()
#     else:
#         print(mail)


def sendmail(
    to: str,
    body: str,
    subject: str = "[COVID-19 Landkreis Benachrichtigung]",
    sender: str = "no-reply@entorb.net",
):

    if checkRunningOnServer():
        # V1: via SENDMAIL
        # SENDMAIL = "/usr/sbin/sendmail"
        # mail = f"To: {to}\nSubject: {subject}\nFrom: {sender}\nContent-Type: text/plain; charset=\"utf-8\"\n\n{body}"
        # # p = os.popen(f"{SENDMAIL} -t -i", "w")
        # p.write(mail)
        # # status = p.close()
        # p.close()

        # V2: via my Mailer Daemon
        insertNewEMail(send_to=to, subject=subject, body=body, send_from=sender)

    else:
        print(f"To: {to}\nSubject: {subject}\nFrom: {sender}\n{body}")


def insertNewEMail(
    send_to: str,
    subject: str,
    body: str,
    send_from: str = "no-reply@entorb.net",
    send_cc: str = "",
    send_bcc: str = "",
):
    # This is a copy from mailer-daemon/insert.py
    import sqlite3

    PATH = "/var/www/virtual/entorb/mail-daemon/outbox.db"

    # ensureValidEMail(send_to) # uncommented, because send_to might contain the name as well

    con = sqlite3.connect(PATH)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO outbox(send_to, subject, body, send_from, send_cc, send_bcc, date_created, date_sent) VALUES (?,?,?,?,?,?,CURRENT_TIMESTAMP, NULL)",
        (send_to, subject, body, send_from, send_cc, send_bcc),
    )
    con.commit()
    cur.close()
    con.close()


##########################


# set path variables
if checkRunningOnServer():
    pathToData = "/var/www/virtual/entorb/html/COVID-19-coronavirus/data/de-districts/de-districts-results.json"
else:
    pathToData = "data/de-districts/de-districts-results.json"

# connect to DB
con, cur = db_connect()

# loop over subscriptions
date_now = datetime.now()
for row in cur.execute(
    "SELECT email, verified, hash, threshold, regions, frequency, date_registered FROM newsletter WHERE (verified = 0) or (verified = 1 AND regions IS NULL) ORDER BY date_registered DESC"
):
    date_registered = datetime.strptime(row["date_registered"], "%Y-%m-%d")
    days_since = (date_now - date_registered).days

    # skip recent subscriptions
    if days_since < 3:
        continue
    # delete old and forgotten ones
    if days_since > 60:
        print(f"deleted old entry", row["email"])
        cur.execute("DELETE FROM newsletter WHERE email = ?", (row["email"],))
        con.commit()
        continue

    reason_for_sending = "Erinnerung die Anmeldung abzuschließen"
    h = row["hash"]
    print(row["email"], row["verified"], row["regions"], row["date_registered"])

    mailBody = f"Hallo {row['email']},\n\ndies ist eine Erinnerung daran, dass Du Dich für meine COVID-19 Landkreisbenachrichtigung eingetragen hast, diese Anmeldung aber noch nicht abgeschlossen ist. Du hast nun folgende Möglichkeiten:\n"

    mailBody += f"\n1. Anmeldung abschließen und interessante Landkreise auswählen: https://entorb.net/COVID-19-coronavirus/newsletter-frontend.html?action=verify&hash={h}\n"

    mailBody += f"\n2. Abmelden: https://entorb.net/COVID-19-coronavirus/newsletter-frontend.html?action=unsubscribe&hash={h}\n"

    mailBody += f"\n3. Diese E-Mail ignorieren und in einer Woche eine erneute Erinnerung zu bekommen ;-)\n"

    mailBody += f"\nBleib gesund\nTorben"

    sendmail(
        to=row["email"],
        body=mailBody,
        subject=f"[COVID-19 Landkreis Benachrichtigung] - {reason_for_sending}",
    )
