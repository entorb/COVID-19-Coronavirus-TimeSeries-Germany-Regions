# from
# https://raw.githubusercontent.com/ythlev/covid-19/master/run.py

# Created by Chang Chia-huan
import argparse
import pathlib
import json
import csv
import io
import urllib.request
import urllib.parse
import math
import statistics
import datetime

parser = argparse.ArgumentParser(
    description="This script generates svg maps for the COVID-19 outbreak for select places")
parser.add_argument(
    "-p", "--place", help="Name of place to generate; by default, maps for select places are generated")
args = vars(parser.parse_args())

with open((pathlib.Path() / "meta").with_suffix(".json"), newline="", encoding="utf-8") as file:
    meta = json.loads(file.read())

if args["place"] != None:
    places = [args["place"]]
else:
    places = meta["places"]

with open((pathlib.Path() / "population").with_suffix(".json"), newline="", encoding="utf-8-sig") as file:
    population = json.loads(file.read())

for place in places:
    main = {}
    for area in population[place]:
        main[area] = {
            "population": population[place][area],
            "cases": 0
        }
    unused = 0
    if place == "Taiwan":
        with urllib.request.urlopen("https://od.cdc.gov.tw/eic/Age_County_Gender_19Cov.json") as response:
            cases = json.loads(response.read())
        for row in cases:
            main[row["縣市"]]["cases"] += int(row["確定病例數"])
        date = datetime.date.today()
    elif place == "UK" or place == "England" or place == "London":
        date, text = 0, ""
        import xml.etree.ElementTree as ET
        with urllib.request.urlopen("https://publicdashacc.blob.core.windows.net/publicdata?restype=container&comp=list") as response:
            root = ET.fromstring(response.read())
        for name in root.iter("Name"):
            if name.text.find("data_") > -1 and int(name.text[5:13]) > date:
                date = int(name.text[5:13])
                text = name.text

        with urllib.request.urlopen("https://c19pub.azureedge.net/" + text) as response:
            data = json.loads(response.read())
        if place == "UK":
            for sub_data in [data["countries"], data["regions"]]:
                for k, v in sub_data.items():
                    if k == "E92000001":
                        unused += 1
                    else:
                        main[k]["cases"] = v["totalCases"]["value"]
        else:
            for k, v in data["utlas"].items():
                if k in main:
                    main[k]["cases"] = v["totalCases"]["value"]
                else:
                    unused += 1
                    if args["place"] != None or unused < 9:
                        print(k, v["totalCases"]["value"])
        date = datetime.datetime.fromisoformat(
            data["lastUpdatedAt"].rstrip("Z"))
    elif place == "Czechia":
        with urllib.request.urlopen("https://api.apify.com/v2/key-value-stores/K373S4uCFR9W1K8ei/records/LATEST?disableRedirect=true") as response:
            data = json.loads(response.read())
        for row in data["infectedByRegion"]:
            if row["name"] in main:
                main[row["name"]]["cases"] = row["value"]
            else:
                unused += 1
                if args["place"] != None or unused < 9:
                    print(row["name"])
        date = datetime.datetime.fromisoformat(
            data["lastUpdatedAtSource"].rstrip("Z"))
    elif place == "Japan":
        with urllib.request.urlopen("https://www.stopcovid19.jp/data/covid19japan.json") as response:
            data = json.loads(response.read())
        for row in data["area"]:
            main[row["name"]]["cases"] = int(row["npatients"])
        if data["lastUpdate"] != "--":
            date = datetime.datetime.fromisoformat(data["lastUpdate"])
        else:
            date = datetime.date.today()
            print("No date available for Japan; current date used")
    else:
        if place in meta["query_list"]:
            queries = meta["query_list"][place]
        else:
            queries = [place]
        try:
            for query in queries:
                url = "https://services{}.arcgis.com/{}/arcgis/rest/services/{}/FeatureServer/{}/".format(
                    meta["query"][query][0][0],
                    meta["query"][query][0][1],
                    urllib.parse.quote(meta["query"][query][0][2]),
                    meta["query"][query][0][3],
                )
                url1 = url + "?f=pjson"
                with urllib.request.urlopen(url1) as response:
                    date = json.loads(response.read())[
                        "editingInfo"]["lastEditDate"] / 1000
                    date = datetime.datetime.fromtimestamp(
                        date, tz=datetime.timezone.utc)
                url2 = url + "query?where={}%3E0&outFields={},{},{}&returnGeometry=false&returnExceededLimitFeatures=true&f=pjson".format(
                    meta["query"][query][0][4],
                    meta["query"][query][1][0],
                    urllib.parse.quote(meta["query"][query][1][1]),
                    meta["query"][query][1][2]
                )
                with urllib.request.urlopen(url2) as response:
                    if place == "US":
                        start = 255
                    else:
                        start = 0
                    for item in json.loads(response.read())["features"][start:]:
                        id = str(item["attributes"]
                                 [meta["query"][query][1][0]]).lstrip("0")
                        if id in main:
                            main[id]["cases"] = int(
                                item["attributes"][meta["query"][query][1][1]])
                            if meta["query"][query][1][2] != "":
                                main[id]["population"] = int(
                                    item["attributes"][meta["query"][query][1][2]])
                        elif id not in [None, "None", "NA"] and item["attributes"][meta["query"][query][1][1]] != None:
                            unused += 1
                            if args["place"] != None or unused < 9:
                                print(id, item["attributes"]
                                      [meta["query"][query][1][1]])
        except:
            print("Error fetching data for", place)
            continue

    if place in meta["10000"]:
        unit = 10000
    else:
        unit = 1000000

    values = []
    for area in main:
        if main[area]["population"] > 0:
            main[area]["pcapita"] = main[area]["cases"] / \
                main[area]["population"] * unit
            values.append(main[area]["pcapita"])
        else:
            print("Population for", area, "not found")

    q = statistics.quantiles(values, n=100, method="inclusive")
    step = math.sqrt(statistics.mean(values) - q[0]) / 3

    threshold = [0, 0, 0, 0, 0, 0]
    for i in range(1, 6):
        threshold[i] = math.pow(i * step, 2) + q[0]

    with open((pathlib.Path() / "template" / place).with_suffix(".svg"), "r", newline="", encoding="utf-8") as file_in:
        with open((pathlib.Path() / "results" / place).with_suffix(".svg"), "w", newline="", encoding="utf-8") as file_out:
            if threshold[5] >= 10000:
                num = "{:_.0f}"
            elif threshold[1] >= 10:
                num = "{:.0f}"
            else:
                num = "{:.2f}"

            for row in file_in:
                written = False
                for area in main:
                    if row.find('id="{}"'.format(area)) > -1:
                        i = 0
                        while i < 5:
                            if main[area]["pcapita"] >= threshold[i + 1]:
                                i += 1
                            else:
                                break
                        file_out.write(row.replace('id="{}"'.format(
                            area), 'style="fill:{}"'.format(meta["colour"][i])))
                        written = True
                        break
                if written == False:
                    if row.find('>Date') > -1:
                        file_out.write(row.replace(
                            'Date', date.strftime("%F")))
                    elif row.find('>level') > -1:
                        for i in range(6):
                            if row.find('level{}'.format(i)) > -1:
                                if i == 0:
                                    file_out.write(row.replace('level{}'.format(
                                        i), "&lt; " + num.format(threshold[1]).replace("_", "&#8201;")))
                                else:
                                    file_out.write(row.replace('level{}'.format(
                                        i), "≥ " + num.format(threshold[i]).replace("_", "&#8201;")))
                    else:
                        file_out.write(row)

    cases = []
    for area in main:
        cases.append(main[area]["cases"])
    print("{}: {} cases total in {} areas; {} figures unused".format(
        place, sum(cases), len(cases), unused))
