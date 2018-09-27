import pandas as pd
import time
import os

# 字符串时间转换为时间戳（秒）
def str2time(str):
    return time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S"))


"""
统计两次操作的最大间隔时间
file_path : 数据文件路径
"""
def get_data(file_path):
    data_csv = pd.read_csv(file_path)
    user_id_list = data_csv["user_id"]
    # 用户ID集合
    user_id_list = user_id_list.drop_duplicates()
    user_id_list = list(user_id_list)
    # 开始操作到加购平均时间集合
    diff_time_list = []

    for user_id in user_id_list:
        data_list = data_csv[data_csv["user_id"] == user_id]
        data_list = data_list.sort_values(by=["receive_time"], ascending=True)
        receive_time_arr = list(data_list["receive_time"].map(str2time))

        temp_time_list = []
        for i in range(len(receive_time_arr) - 1):
            temp_time_list.append(receive_time_arr[i + 1] - receive_time_arr[i])

        diff_time_list.append(max(temp_time_list))

    print(diff_time_list)
    return sum(diff_time_list) / len(diff_time_list)




if __name__ == "__main__":
    # file_path = "test/test3.csv"
    # get_data(file_path)

    fs = os.listdir("data")
    t = []
    for f in fs:
        file_path = "data/" + f
        t.append(get_data(file_path))

    print("----------------------------------------")
    print(t)
    print(sum(t) / len(t))


