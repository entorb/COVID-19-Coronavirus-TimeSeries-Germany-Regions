import pandas as pd
import helper

fileout = "data/de-divi/lk-groups.json"

l_groups = []

d = {
    "id": 1,
    "title": "Fürth und Umland",
    "lkids": ("09563",  # Fürth Stadt
              "09573",  # Fürth Land
              )
}
l_groups.append(d)
d = {
    "id": 2,
    "title": "Erlangen und Umland",
    "lkids": ("09562",  # Erlangen
              "09572",  # ERH
              "09474",  # Forchheim
              # "09575",  # NEA: 48
              )
}
l_groups.append(d)
d = {
    "id": 3,
    "title": "Nürnberg und Umland",
    "lkids": ("09564",  # Nürnberg Stadt
              "09574",  # Nürnberg Land
              "09576",  # Roth
              "09571",  # Ansbach
              )
}
l_groups.append(d)
d = {
    "id": 4,
    "title": "Harburg und Lüneburg",
    "lkids": ("03353",  # Harburg
              "03355",  # LG
              )
}
l_groups.append(d)
d = {
    "id": 5,
    "title": "Dresden und Umland",
    "lkids": ("14612",  # DD
              "14628",  # SS
              "14625",  # Bautzen
              "14627",  # Meißen
              )
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
    f'data/de-divi/downloaded/latest.csv', sep=",")

# select columns
df = df[["date", "gemeindeschluessel",
         "betten_frei", "betten_belegt"]]

df["betten_ges"] = df["betten_frei"] + df["betten_belegt"]

# filter to one date
df = df[df["date"] == "2021-11-13"]

df = df.sort_values(by=['betten_belegt'], ascending=False)

# last row
# df = df.tail(1)
# print(df.head(20))


# display number beds
l_ids = []
for d in l_groups:
    print(f'{d["title"]}')
    for lkid in d["lkids"]:
        df2 = df[df["gemeindeschluessel"] == int(lkid)]
        if len(df2) > 0:
            betten_ges = df2["betten_ges"].iloc[0]
        else:
            betten_ges = 0
        print(f"{lkid} {betten_ges}")
del d, df2, betten_ges
