import pandas as pd
import time
import os


# 字符串时间转换为时间戳（秒）
def str2time(str):
    if "/" in str:
        return time.mktime(time.strptime(str, "%Y/%m/%d %H:%M"))
    else:
        return time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S"))


# 将新提取的多个特征数据文件合并为一个文件
def m_test0():
    fs = os.listdir("data/0818-0821/login")
    df = None
    for i in range(len(fs)):
        print(fs[i])
        file_path = "data/0818-0821/login/" + fs[i]
        tmp_df = pd.read_csv(file_path)
        print(len(tmp_df))
        if i == 0:
            df = tmp_df
        else:
            df = pd.concat([df, tmp_df], axis=0)
    df.to_csv("data/0818-0821/login-time-0818-0821.csv", index=False)
    print(len(df))
    print("合并完毕")


# 使用后一列的数据填充缺失值
def m_test1():
    df = pd.read_csv("data/12345/login-time-abcde.csv")
    # 使用后一列的数据填充此列缺失值
    df = df.fillna(method="bfill", axis=1)
    df.to_csv("data/12345/login-time-abcde-tmp1.csv", index=False)
    print("over")


# 提取新特征（注册/登录到下单的时间）
def m_test2():
    df_one = pd.read_csv("data/12345/abcde.csv", encoding="GBK")
    df_two = pd.read_csv("data/12345/login-time-abcde-tmp1.csv")
    return_time = []
    for i in range(len(df_one)):
        user_id = df_one.loc[i]["webuser_id"]
        order_create_time = df_one.loc[i]["created"]
        order_create_time = str2time(order_create_time)

        temp_data = df_two[df_two["user_id"] == user_id]
        temp_data = temp_data.sort_values(by=["created_time"], ascending=True)
        temp_data_arr = list(temp_data["created_time"].map(str2time))
        if len(temp_data_arr) > 0:
            diff_time_arr = []
            for temp_time in temp_data_arr:
                diff_time_arr.append(order_create_time - temp_time)
            diff_time_arr = [i for i in diff_time_arr if i > 0]
            if len(diff_time_arr) > 0:
                return_time.append(min(diff_time_arr))
            else:
                return_time.append(-1)
        else:
            return_time.append(-1)

    data_return = {}
    data_return["order_id"] = list(df_one["id"])
    data_return["user_id"] = list(df_one["webuser_id"])
    data_return["login_order_time"] = return_time
    df = pd.DataFrame(data_return)
    df.to_csv("data/12345/login-time-abcde-tmp2.csv", index=False)
    print("over")


# 提取登录到下单时间为-1的数据，然后计算平均值，进行填充
def m_test3():
    df = pd.read_csv("data/12345/login-time-abcde-tmp2.csv")
    temp_data = df[df["login_order_time"] == -1]
    print(len(temp_data))

    a20 = df[df["login_order_time"] > 0]
    a21 = list(a20["login_order_time"])
    a22 = sum(a21) / len(a21)
    print(a22)

    temp_order_id_arr = list(temp_data["order_id"])
    for temp_order_id in temp_order_id_arr:
        ix = df[df["order_id"] == temp_order_id].index[0]
        df.loc[ix, "login_order_time"] = a22

    df.to_csv("data/12345/login-time-abcde-tmp3.csv", index=False)




if __name__ == "__main__":
    m_test3()
