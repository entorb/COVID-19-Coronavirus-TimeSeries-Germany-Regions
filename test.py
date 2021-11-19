import datetime as dt
import pandas as pd
import helper


# df = pd.read_csv(
#     f'data/de-districts/de-district_timeseries-02000.tsv', sep="\t")
# df = helper.pandas_set_date_index(df)

# df = df["Cases_New"]


# print(df.tail())


df_divi_latest = pd.read_csv(f"data/de-divi/downloaded/latest.csv", sep=",")

print(df_divi_latest.tail())


l1 = range(1, 16 + 1)
l2 = ["de-states"] * len(l1)
l3 = [df_divi_latest] * len(l1)
print(list(zip(l1, l2, l3)))
