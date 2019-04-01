import pandas as pd


# 将商品信息加入原数据集
def m_test1():
    df_one = pd.read_csv("./data/xian-rrl-1125-1205-ip.csv")
    df_two = pd.read_csv("./data/ware-xian-rrl.csv")
    ware_id_list = []
    ware_num_list = []
    ware_price_list = []
    ware_promotion_list = []
    for i in range(len(df_one)):
        order_id = df_one.loc[i, "order_id"]
        print(str(i) + ", " + str(order_id))
        two_data = df_two[df_two["order_id"] == order_id]
        ware_id_list.append(two_data["ware_id_list"].values[0])
        ware_num_list.append(two_data["ware_num_list"].values[0])
        ware_price_list.append(two_data["ware_price_list"].values[0])
        ware_promotion_list.append(two_data["ware_promotion_list"].values[0])

    df_one["ware_id_list"] = ware_id_list
    df_one["ware_num_list"] = ware_num_list
    df_one["ware_price_list"] = ware_price_list
    df_one["ware_promotion_list"] = ware_promotion_list
    df_one.to_csv("./data/xian-rrl-1125-1205-ware0.csv", index=False)
    print("over")


# 处理商品信息-取出每个订单中，金额最大的商品
def m_test2():
    df = pd.read_csv("./data/xian-rrl-1125-1205-ware0.csv")
    ware_id_list = []
    ware_num_list = []
    ware_price_list = []
    ware_promotion_list = []
    for i in range(len(df)):
        print(df.loc[i, "order_id"])
        ware_id_arr = df.loc[i, "ware_id_list"].split("|")
        ware_num_arr = df.loc[i, "ware_num_list"].split("|")
        ware_price_arr = df.loc[i, "ware_price_list"].split("|")
        ware_promotion_arr = df.loc[i, "ware_promotion_list"].split("|")
        max_price = str(max([int(x) for x in ware_price_arr]))
        max_price_idx = ware_price_arr.index(max_price)
        ware_id_list.append(ware_id_arr[max_price_idx])
        ware_num_list.append(ware_num_arr[max_price_idx])
        ware_price_list.append(max_price)
        ware_promotion_list.append(ware_promotion_arr[max_price_idx])
    df["ware_id_list"] = ware_id_list
    df["ware_num_list"] = ware_num_list
    df["ware_price_list"] = ware_price_list
    df["ware_promotion_list"] = ware_promotion_list
    df.to_csv("./data/xian-rrl-1125-1205-ware1.csv", index=False)
    print("over")


# 处理商品信息-取出每个订单中，优惠金额最大的商品
def m_test3():
    df = pd.read_csv("./data/xian-rrl-1125-1205-ware0.csv")
    ware_id_list = []
    ware_num_list = []
    ware_price_list = []
    ware_promotion_list = []
    for i in range(len(df)):
        print(df.loc[i, "order_id"])
        ware_id_arr = df.loc[i, "ware_id_list"].split("|")
        ware_num_arr = df.loc[i, "ware_num_list"].split("|")
        ware_price_arr = df.loc[i, "ware_price_list"].split("|")
        ware_promotion_arr = df.loc[i, "ware_promotion_list"].split("|")
        max_price = str(max([int(x) for x in ware_promotion_arr]))
        max_price_idx = ware_promotion_arr.index(max_price)
        ware_id_list.append(ware_id_arr[max_price_idx])
        ware_num_list.append(ware_num_arr[max_price_idx])
        ware_price_list.append(ware_price_arr[max_price_idx])
        ware_promotion_list.append(max_price)
    df["ware_id_list"] = ware_id_list
    df["ware_num_list"] = ware_num_list
    df["ware_price_list"] = ware_price_list
    df["ware_promotion_list"] = ware_promotion_list
    df.to_csv("./data/xian-rrl-1125-1205-ware2.csv", index=False)
    print("over")


if __name__ == "__main__":
    m_test1()
    m_test3()