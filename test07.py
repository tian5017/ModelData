import pandas as pd
import os

# 统计user_id数量
def get_data():
    fs = os.listdir("result/data-0621-0710")
    s = 0
    for f in fs:
        file_path = "data/" + f

        data_csv = pd.read_csv(file_path)
        user_id_list = data_csv["user_id"]
        # 用户ID集合
        user_id_list = user_id_list.drop_duplicates()
        user_id_list = list(user_id_list)

        s += len(user_id_list)
        print(len(user_id_list))
    print("-------------------------------")
    print(s)


# 统计user_id数量
def get_data2():
    file_path = "result/0621-0710/result_data-0621-0710.csv"
    data_csv = pd.read_csv(file_path)
    user_id_list = data_csv["user_id"]
    print(len(user_id_list))
    # 用户ID集合
    user_id_list = user_id_list.drop_duplicates()
    user_id_list = list(user_id_list)
    print(len(user_id_list))
    print("-------------------------------")


# 去除重复数据
def get_data3():
    file_path = "result/0621-0710/result_data-0621-0710.csv"
    data_csv = pd.read_csv(file_path)
    print(len(data_csv))
    data_csv = data_csv.drop_duplicates(["user_id"])
    print(len(data_csv))
    data_csv.to_csv("result/0621-0710/result_data-0621-0710-over.csv", index=False)




if __name__ == "__main__":
    get_data3()


