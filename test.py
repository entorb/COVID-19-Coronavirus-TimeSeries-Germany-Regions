import datetime as dt
import pandas as pd
import helper


# df = pd.read_csv(
#     f'data/de-districts/de-district_timeseries-02000.tsv', sep="\t")
# df = helper.pandas_set_date_index(df)

# df = df["Cases_New"]


# print(df.tail())


# df = pd.read_csv(f"data/de-divi/downloaded/latest.csv", sep=",")
# idx = df.index[-1] + 1
# print(idx)

# df.loc[300000] = 123


# print(df.tail())


# l1 = range(1, 16 + 1)
# l2 = ["de-states"] * len(l1)
# l3 = [df_divi_latest] * len(l1)
# print(list(zip(l1, l2, l3)))


for row in range(16, 10 - 1, -1):
    print(row)
