import pandas as pd
import os


# 将新提取的多个特征数据文件合并为一个文件
def m_test1():
    fs = os.listdir("data/0711-0720/login_time")
    for i in range(len(fs)):
        print(fs[i])
        file_path = "data/0711-0720/login_time/" + fs[i]
        fr_lines = open(file_path, "r", encoding="utf-8").readlines()
        print(len(fr_lines))
        a = 1
        if i == 0:
            a = 0
        with open("data/0711-0720/login-time-0711-0720.csv", "a+", encoding="utf-8") as aa:
            for x in range(a, len(fr_lines)):
                aa.write(fr_lines[x])
    print("合并完毕")
    # df = pd.read_csv("result.csv")
    # data_list = df.drop_duplicates()
    # data_list.to_csv("result_data.csv", index=False)
    # print("去重完毕")



# 将新提取的用户行为特征加入原来数据集（用户行为特征）
def m_test2():
    df_one = pd.read_csv("./data/test/test.csv", encoding="GBK")
    df_two = pd.read_csv("./data/test/event-test-over.csv")
    add_cart_time = []
    behaviour_num = []
    detail_num = []
    purchase_time = []
    for i in range(len(df_one)):
        user_id = df_one.loc[i, "webuser_id"]
        print(str(i) + ", " + str(user_id))
        two_data = df_two[df_two["user_id"] == float(user_id)]
        if len(two_data) == 0:
            add_cart_time.append(-1)
            behaviour_num.append(-1)
            detail_num.append(-1)
            purchase_time.append(-1)
        else:
            add_cart_time.append(two_data["add_cart_time"].values[0])
            behaviour_num.append(two_data["behaviour_num"].values[0])
            detail_num.append(two_data["detail_num"].values[0])
            purchase_time.append(two_data["purchase_time"].values[0])

    df_one["add_cart_time"] = add_cart_time
    df_one["behaviour_num"] = behaviour_num
    df_one["detail_num"] = detail_num
    df_one["purchase_time"] = purchase_time
    df_one.to_csv("./data/test/test-order.csv", index=False)
    print("over")


# 将新提取的用户行为特征加入原来数据集（登陆到下单时间特征）
def m_test3():
    df_one = pd.read_csv("data/test/MJ-1017-1018.csv", encoding="GBK")
    df_two = pd.read_csv("data/test/MJ-LT-1017-1018-over.csv")
    login_order_time = []
    for i in range(len(df_one)):
        order_id = df_one.loc[i, "id"]
        print(str(i) + ", " + str(order_id))
        two_data = df_two[df_two["order_id"] == float(order_id)]
        login_order_time.append(two_data["login_order_time"].values[0])

    df_one["login_order_time"] = login_order_time
    df_one.to_csv("data/test/MJ-1017-1018-over.csv", index=False, encoding="GBK")
    print("over")



if __name__ == "__main__":
    m_test2()
