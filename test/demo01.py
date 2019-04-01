import pandas as pd


train = pd.read_csv("./data/test.tsv", sep="\t", header=0, index_col="test_id")

# 1、将缺失值作为一个层次
def step1():
    train["category_name"] = train["category_name"].fillna("missing").astype("category")
    train["brand_name"] = train["brand_name"].fillna("missing").astype("category")
    train["item_condition_id"] = train["item_condition_id"].astype("category")
    print(train.head(5))




if __name__ == "__main__":
    step1()


