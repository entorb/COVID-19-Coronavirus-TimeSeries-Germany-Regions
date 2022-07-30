#!/usr/bin/env python3.9
# by Dr. Torben Menke https://entorb.net
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions

"""
Creates groups of ICU locations
"""

# Further Modules
import pandas as pd

# My Helper Functions
import helper

fileout = "data/de-divi/lk-groups.json"

l_groups = []

# lk_ids:
# Gemeingeschlüssel, siehe
# https://github.com/entorb/COVID-19-Coronavirus-German-Regions/blob/master/data/de-districts/mapping_landkreis_ID_name.json

d = {
    "id": 1,
    "title": "Fürth und Umland",
    "lk_ids": (
        "09563",  # Fürth Stadt
        "09573",  # Fürth Land
    ),
}
l_groups.append(d)
d = {
    "id": 2,
    "title": "Erlangen und Umland",
    "lk_ids": (
        "09562",  # Erlangen
        "09572",  # ERH
        "09474",  # Forchheim
        # "09575",  # NEA: 48
    ),
}
l_groups.append(d)
d = {
    "id": 3,
    "title": "Nürnberg und Umland",
    "lk_ids": (
        "09564",  # Nürnberg Stadt
        "09574",  # Nürnberg Land
        "09576",  # Roth
        "09571",  # Ansbach
    ),
}
l_groups.append(d)
d = {
    "id": 4,
    "title": "Harburg und Lüneburg",
    "lk_ids": (
        "03353",  # Harburg
        "03355",  # LG
    ),
}
l_groups.append(d)
d = {
    "id": 5,
    "title": "Dresden Krankenhauscluster",
    "lk_ids": (
        "14612",  # DD
        "14628",  # SS-OE
        "14625",  # Bautzen
        "14627",  # Meißen
        "14626",  # Görlitz
    ),
}
l_groups.append(d)
d = {
    "id": 6,
    "title": "Leipzig Krankenhauscluster",
    "lk_ids": (
        "14713",  # L
        "14729",  # L Land
        "14730",  # Nordsachsen
        "14627",  # Meißen
        "14626",  # Görlitz
    ),
}
l_groups.append(d)
d = {
    "id": 7,
    "title": "Chemnitz Krankenhauscluster",
    "lk_ids": (
        "14511",  # Chemnitz
        "14522",  # Mittelsachsen
        "14524",  # Zwickau
        "14521",  # Erzgebirgskreis
        "14523",  # Vogtlandkreis
    ),
}
l_groups.append(d)


# assert id unique
l_ids = []
for d in l_groups:
    print(d["title"])
    print(d["id"])
    assert d["id"] not in l_ids, f'{d["title"]} has non-unique id: {d["id"]}'
    l_ids.append(d["id"])

helper.write_json(fileout, d=l_groups)


df = pd.read_csv(
    f"data/de-divi/downloaded/latest.csv",
    sep=",",
    usecols=["date", "gemeindeschluessel", "betten_frei", "betten_belegt"],
)

df["betten_ges"] = df["betten_frei"] + df["betten_belegt"]

# filter to one date
df = df[df["date"] == "2021-11-13"]

df = df.sort_values(by=["betten_belegt"], ascending=False)

# last row
# df = df.tail(1)
# print(df.head(20))


# display number beds
l_ids = []
for d in l_groups:
    print(f'{d["title"]}')
    for lkid in d["lk_ids"]:
        df2 = df[df["gemeindeschluessel"] == int(lkid)]
        if len(df2) > 0:
            betten_ges = df2["betten_ges"].iloc[0]
        else:
            betten_ges = 0
        print(f"{lkid} {betten_ges}")
del d, df2, betten_ges
