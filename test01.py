import pandas as pd

df = pd.DataFrame({"id": [1001, 1002, 1003, 1004, 1005, 1006],
                   "date": pd.date_range('20130102', periods=6),
                   "city": ['Beijing ', 'SH', ' guangzhou ', 'Shenzhen', 'shanghai', 'BEIJING '],
                   "age": [23, 44, 54, 32, 34, 32],
                   "price": [1200, 0, 2133, 5433, 0, 4432]}, columns=['id', 'date', 'city', 'category', 'age', 'price'])

df = df.fillna(value="10")
print(df)
df.to_csv("abc.csv")
