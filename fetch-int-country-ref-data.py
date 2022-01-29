#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
fetches a ref table of country data from geonames.org
is based on https://raw.githubusercontent.com/lorey/list-of-l_countries/master/generator.py
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import codecs
import urllib
import csv

# My Helper Functions
import helper

# header row:
# ISO	ISO3	ISO-Numeric	fips	Country	Capital	Area(in sq km)	Population	Continent	tld	CurrencyCode	CurrencyName	Phone	Postal Code Format	Postal Code Regex	Languages	geonameid	neighbours	EquivalentFipsCode

file_JSON = "data/ref_country_database.json"
file_CSV = "data/ref_country_database.tsv"


url = "http://download.geonames.org/export/dump/countryInfo.txt"
stream = urllib.request.urlopen(url)
reader = codecs.getreader("utf-8")
reader = csv.reader(reader(stream), delimiter="\t")
del url, stream

# split comment rows and data rows
comment_rows = []
non_comment_rows = []
for row in reader:
    if row[0][0] == "#":
        comment_rows.append(row)
    else:
        non_comment_rows.append(row)
del reader, row

# search for table headers
header_row = ["", ""]  # Dummy entry
while header_row[0] != "#ISO":
    header_row = comment_rows.pop()
del comment_rows
header_row[0] = "ISO"  # remove comment space

d_country_ref_data = {}
for row in non_comment_rows:
    d = {}

    # read files from csv and map them to dict
    for i in range(0, len(row)):
        col_title = header_row[i]
        col = row[i]
        d[col_title] = col

    # add missing keys as None
    for col_title in header_row:
        if col_title not in d:
            d[col_title] = None
    country_name = d["Country"]
    del d["Country"]

    d_country_ref_data[country_name] = d
assert len(non_comment_rows) == len(d_country_ref_data.keys())
del row, non_comment_rows, d, country_name, col_title, col


for country_name in d_country_ref_data:
    d_country_ref_data[country_name]["Population"] = int(
        d_country_ref_data[country_name]["Population"]
    )
    d_country_ref_data[country_name]["geonameid"] = int(
        d_country_ref_data[country_name]["geonameid"]
    )
    d_country_ref_data[country_name]["ISO-Numeric"] = int(
        d_country_ref_data[country_name]["ISO-Numeric"]
    )
    d_country_ref_data[country_name]["Area(in sq km)"] = float(
        d_country_ref_data[country_name]["Area(in sq km)"]
    )


if d_country_ref_data["Eritrea"]["Population"] == 0:
    d_country_ref_data["Eritrea"]["Population"] = 5750433

# export as json
helper.write_json(file_JSON, d_country_ref_data)

# export as csv

l = []
for country_name in sorted(d_country_ref_data.keys()):
    d = d_country_ref_data[country_name]
    d["Country"] = country_name
    l.append(d)
del d

keys = header_row
with open(file_CSV, mode="w", encoding="utf-8", newline="\n") as file:
    dict_writer = csv.DictWriter(file, keys, delimiter="\t")
    dict_writer.writeheader()
    dict_writer.writerows(l)
