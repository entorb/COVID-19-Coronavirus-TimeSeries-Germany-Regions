#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
This is my test playground and template for new scripts
"""

__author__ = "Dr. Torben Menke"
__email__ = "https://entorb.net"
__license__ = "GPL"

# Built-in/Generic Imports
import datetime as dt

# Further Modules
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# My Helper Functions
import helper

# Set German date format for plots: Okt instead of Oct
import locale

locale.setlocale(locale.LC_ALL, "de_DE.UTF-8")
