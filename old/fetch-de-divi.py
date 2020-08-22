#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
https://www.divi.de/register/kartenansicht

https://diviexchange.z6.web.core.windows.net/report.html

https://docs.python-guide.org/scenarios/scrape/

https://towardsdatascience.com/web-scraping-html-tables-with-python-c9baba21059

"""

import glob
import os.path
import json
# from lxml.cssselect import CSSSelector
from lxml import html
import requests
import csv
# pip install cssselect
# page = requests.get(
#     'https://web.archive.org/web/20200331201117/https://diviexchange.z6.web.core.windows.net/report.html')


def read_from_url(url: str) -> str:
    page = requests.get(url)
    return page.content


def read_from_file(filename: str) -> str:
    with open(filename, mode='r', encoding='utf-8') as fh:
        cont = fh.read()
    return cont


def extract_table(content: str) -> dict:

    tree = html.fromstring(content)
    del content

    l_column_names = []
    thead_trs = tree.xpath('//*/thead/tr')
    tr0 = thead_trs[0]
    assert len(tr0) == 15
    for i in range(len(tr0)):
        th = tr0[i]
        if i == 0:
            text = "Bundesland"
        else:
            text = th.text_content()
        l_column_names.append(text)
    del thead_trs, tr0, i, th, text

    l_column_names.pop(0)  # remove first column Bundesland

    # ensure the columns have not been shifted
    assert l_column_names[0] == 'ICU low care (frei)'
    l_column_names[0] = 'ICU low free'
    assert l_column_names[1] == 'ICU low care (belegt)'
    l_column_names[1] = 'ICU low occupied'
    assert l_column_names[2] == 'ICU low care in 24 h (Anzahl)'
    l_column_names[2] = 'ICU low in 24h'
    assert l_column_names[3] == 'ICU high care (frei)'
    l_column_names[3] = 'ICU high free'
    assert l_column_names[4] == 'ICU high care (belegt)'
    l_column_names[4] = 'ICU high occupied'
    assert l_column_names[5] == 'ICU high care in 24 h (Anzahl)'
    l_column_names[5] = 'ICU high in 24h'
    assert l_column_names[6] == 'ICU ECMO (frei)'
    l_column_names[6] = 'ICU ECMO free'
    assert l_column_names[7] == 'ICU ECMO (belegt)'
    l_column_names[7] = 'ICU ECMO occupied'
    assert l_column_names[8] == 'ICU ECMO care in 24 h (Anzahl)'
    l_column_names[8] = 'ICU ECMO in 24h'
    assert l_column_names[9] == 'Anzahl ECMO-FÃ¤lle pro Jahr'
    l_column_names[9] = 'ECMO cases per year'
    assert l_column_names[10] == 'COVID-19 aktuell in Behandlung'
    l_column_names[10] = 'COVID-19 in treatment'
    assert l_column_names[11] == 'COVID-19 genesen'
    l_column_names[11] = 'COVID-19 recovered'
    assert l_column_names[12] == 'COVID-19 beatmet'
    l_column_names[12] = 'COVID-19 ventilated'
    assert l_column_names[13] == 'COVID-19 verstorben'
    l_column_names[13] = 'COVID-19 died'

    tbody_trs = tree.xpath('//*/tbody/tr')
    del tree

    i = 0
    l_rows = []
    for tr in tbody_trs:
        l_columns = []
        if len(tr) != 15:
            continue
        assert len(tr) == 15, f"length = {len(tr)}"
        i += 1
        for td in tr:
            l_columns.append(td.text_content())
        l_rows.append(list(l_columns))
    del tbody_trs, l_columns, i, tr, td

    assert len(l_rows) == 16  # 16 Bundesländer
    d = {}

    for row in l_rows:
        bundesland = row.pop(0)
        if bundesland == 'NRW':
            bundesland = 'NW'
        # convert numbers to int
        row = [int(v) for v in row]
        d2 = {}
        for i in range(len(row)):
            d2[l_column_names[i]] = row[i]
        d2['ICU low occupied percent'] = round(
            100 * d2['ICU low occupied'] / (d2['ICU low free'] + d2['ICU low occupied']), 1)
        d2['ICU high occupied percent'] = round(
            100 * d2['ICU high occupied'] / (d2['ICU high free'] + d2['ICU high occupied']), 1)

        d2['ICU ECMO occupied percent'] = round(
            100 * d2['ICU ECMO occupied'] / (d2['ICU ECMO free'] + d2['ICU ECMO occupied']), 1)
        d[bundesland] = d2
    del row, bundesland, d2, i
    return d


# d_all_dates = {}
l_all_dates = []

for fileIn in sorted(glob.glob('cache/divi/*.html')):
    print(fileIn)
    # fileIn = 'data-divi/divi-2020-03-31.html'
    # (fileBaseName, fileExtension) = os.path.splitext(fileIn)
    # content = read_from_url('https://diviexchange.z6.web.core.windows.net/report.html')

    import re
    myPattern = 'divi-(.*)\.html$'
    myRegExp = re.compile(myPattern)
    myMatch = myRegExp.search(fileIn)
    assert myMatch != None, f"date not found in: \n{fileIn}"
    datum = myMatch.group(1)

    fileOut = f'data/de-divi/de-divi-{datum}.json'

    content = read_from_file(fileIn)
    d_divi_table = extract_table(content)

    # file_out = f'data-divi'
    with open(fileOut, mode='w', encoding='utf-8', newline='\n') as fh:
        json.dump(d_divi_table, fh, ensure_ascii=False)
    d = {'Date': datum, 'Data': d_divi_table}
    l_all_dates.append(d)


# file_out = f'data-divi'
with open('data/de-divi/de-divi-all.json', mode='w', encoding='utf-8', newline='\n') as fh:
    json.dump(l_all_dates, fh, ensure_ascii=False)

for BL_ID in sorted(l_all_dates[-1]['Data'].keys()):
    with open(f'data/de-divi/de-divi-{BL_ID}.tsv', mode='w', encoding='utf-8', newline='\n') as fh:
        csvwriter = csv.writer(fh, delimiter="\t")
        l = (
            '# Date',
            'ICU low occupied percent',
            'ICU high occupied percent',
            'ICU ECMO occupied percent'
        )
        csvwriter.writerow(l)

        # # TODO:
        for entry in l_all_dates:
            l = (
                entry['Date'],
                entry['Data'][BL_ID]['ICU low occupied percent'],
                entry['Data'][BL_ID]['ICU high occupied percent'],
                entry['Data'][BL_ID]['ICU ECMO occupied percent']
            )

            csvwriter.writerow(l)
