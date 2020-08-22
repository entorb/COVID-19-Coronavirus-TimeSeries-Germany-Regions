#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Joins 2 files
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import math
import csv

f1 = "data/int/countries-latest-selected.tsv"
f2 = "data/int/countries-gnuplot-fit.tsv"

f_out = 'data/int/countries-joined_selected_and_gnuplot_fit.tsv'
l1 = []
l2 = []


def split_lines(l: list) -> list:
    """splits list l of strings containing tabs into list of lists"""
    for i in range(len(l)):
        line = l[i]
        line = line.strip()  # trim spaces / linebreaks
        columns = line.split("\t")
        l[i] = columns
    return l


with open(f1, mode='r', encoding='utf-8') as fh1:
    l1 = fh1.readlines()
l1 = split_lines(l1)

with open(f2, mode='r', encoding='utf-8') as fh2:
    l2 = fh2.readlines()
l2 = split_lines(l2)

# asserts
assert len(l1) == len(l2), "E: input files differ in length"
for i in range(len(l1)):
    assert l1[i][0] == l2[i][0], "E: input files countries do not match: " + \
        l1[i][0] + " != " + l2[i][0]

deaths_per_million_of_IT = 0
for line in l1:
    if line[0] == 'Italy':
        deaths_per_million_of_IT = float(line[5])
        break

assert deaths_per_million_of_IT != 0

num_cols_l1 = len(l1[0])
num_cols_l2 = len(l2[0])

l_out = []
for i in range(len(l1)):
    l = list(l1[i])
    l.extend(l2[i][1:])
    if i == 0:  # header row
        l.append("Days till deaths/pop of Italy")
    else:  # data rows
        this_deaths_per_million = float(l1[i][5])
        duplications_till_level_of_IT = math.log(deaths_per_million_of_IT /
                                                 this_deaths_per_million)/math.log(2)
        doubling_time = float(l2[i][5])
        days = duplications_till_level_of_IT * doubling_time
        # print(l1[i][0] + " " + str(days))
        l.append("%.1f" % (days))
    l_out.append(list(l))


with open(f_out, mode='w', encoding='utf-8', newline='\n') as f:
    csvwriter = csv.writer(f, delimiter="\t")
    for line in l_out:
        csvwriter.writerow(line)
