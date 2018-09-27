import pandas as pd


# 将文档按照某一列排序
def date_time_sort():
    # 排序列所在的文档
    file_path1 = "data/online-data-0824-0916.csv"
    # 需要排序的文档
    file_path2 = "data/train-online-data-0824-0916-time.csv"

    df1 = pd.read_csv(file_path1, encoding="GBK")
    print(len(df1))
    df2 = pd.read_csv(file_path2, encoding="GBK", index_col="order_id")
    print(len(df2))
    order_id_list = list(df1["id"])
    df2 = df2.reindex(order_id_list)
    df2.to_csv("data/train-online-data-0824-0916-time-sort.csv", encoding="GBK", index=True)
    print("over")


# 将新提取的用户行为特征加入原来数据集（登陆到下单时间特征）
def data_set_add_col():
    df_one = pd.read_csv("data/0817-0820/data-rcs-0817-0820-2-model.csv", encoding="GBK")
    df_two = pd.read_csv("data/0817-0820/data-rcs-0817-0820-2-flag-over.csv")
    flag = list(df_two["flag"])
    df_one["new_rcs_flag"] = flag
    df_one.to_csv("data/0817-0820/data-rcs-0817-0820-2-model-over.csv", index=False, encoding="GBK")
    print("over")



if __name__ == "__main__":
    date_time_sort()