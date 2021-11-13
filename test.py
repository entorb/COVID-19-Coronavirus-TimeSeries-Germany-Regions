import datetime as dt
import pandas as pd
import helper


# df = pd.read_csv(
#     f'data/de-districts/de-district_timeseries-02000.tsv', sep="\t")
# df = helper.pandas_set_date_index(df)

# df = df["Cases_New"]


# print(df.tail())


df_divi_latest = pd.read_csv(
    f'data/de-divi/downloaded/latest.csv', sep=",")

print(df_divi_latest.tail())
