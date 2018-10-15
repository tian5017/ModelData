import pandas as pd
import numpy as np


# max-min归一算法
def normal_data(flag, data):
    if flag:
        # 结果映射到[0, 1]
        return [round((float(i) - min(data)) / float(max(data) - min(data)), 2) for i in data]
    else:
        # 结果映射到[-1, 1]
        return [round((float(i) - np.mean(data)) / float(max(data) - min(data)), 2) for i in data]


# z-score标准化算法
def z_score(data):
    data_mean = np.mean(data)
    ss = sum([(i - data_mean) ** 2 for i in data]) / len(data)
    return [(i - data_mean) / ss for i in data]



# 将数据中大于阈值的时间归一化处理
def m_test1():
    df = pd.read_csv("data/0914-1011/login-time-0914-1011-tmp3.csv")
    ixs = df[df["login_order_time"] >= 200000].index

    for ix in list(ixs):
        df.loc[ix, "login_order_time"] = 200000

    df.to_csv("data/0914-1011/login-time-0914-1011-tmp4.csv", index=False)
    print("over")


# 数据归一化处理(max-min方式)
def m_test2():
    df = pd.read_csv("data/0914-1011/login-time-0914-1011-tmp4.csv")
    login_order_time = list(df["login_order_time"])

    login_order_time = normal_data(True, login_order_time)
    df["login_order_time"] = login_order_time

    df.to_csv("data/0914-1011/login-time-0914-1011-over.csv", index=False)
    print("over")



if __name__ == "__main__":
    m_test2()
