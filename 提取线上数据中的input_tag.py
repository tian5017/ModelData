import pandas as pd
import json


df = pd.read_csv("data/online-data-0824-0916-new.csv", encoding="GBK")
input_tag = list(df["input_tag"])
login_order_time_list = []
for aa in input_tag:
    d = json.loads(aa)
    login_order_time_list.append(d["login_order_time"])

df["login_order_time"] = login_order_time_list
df.to_csv("data/online-data-0824-0916-new1.csv", encoding="GBK", index=False)
print("over")

