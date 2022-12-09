#!/bin/bash
echo Date Int-Countries: $(tail -1 data/int/countries-latest-selected.tsv | cut -f2)
echo Date DE-States: $(tail -1 data/de-states/de-states-latest.tsv | cut -f5)
echo Date DE-Erlangen: $(tail -1 data/de-districts/de-district_timeseries-09562.tsv | cut -f2)
