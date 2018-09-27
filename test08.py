import pandas as pd
import os

def get_data():
    fs = os.listdir("result")
    s = 0
    for f in fs:
        file_path = "result/" + f

        data_csv = pd.read_csv(file_path)
        user_id_list = data_csv["user_id"]
        user_id_list = list(user_id_list)

        s += len(user_id_list)
        print(len(user_id_list))
    print("-------------------------------")
    print(s)




if __name__ == "__main__":
    get_data()


