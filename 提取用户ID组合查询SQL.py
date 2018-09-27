import pandas as pd

# 提取所有的用户ID
def m_test1():
    data = pd.read_csv("data/12345.csv", encoding="GBK")
    webuser_id = data["webuser_id"]
    print(len(webuser_id))

    # 去除重复数据
    user_id_list = webuser_id.drop_duplicates()
    user_id_list = list(user_id_list)
    print(len(user_id_list))

    s = ""
    for i in range(1, len(user_id_list)+1):
        s += str(user_id_list[i-1]) + ","
        if i % 1000 == 0:
            s += "\n"

    with open("sql/aa.txt", "w") as f:
        f.write(s)


# 将用户ID组合到查询SQL中
def m_test2():
    with open("sql/aa.txt", "r") as f:
        list1 = f.readlines()
        l = 0
        for i in range(0, len(list1)):
            list1[i] = list1[i][:-2]

            # 统计每一行包含多少个ID
            aaa = list1[i].split(",")
            l += len(aaa)
            print(len(aaa))

            with open("sql/aa.sql", "a+") as g:
                g.write(str(i+1) + ":SELECT user_id,login_time,created_time FROM dmall_rcs_workbench.user_login_device_info WHERE user_id IN \n")
                g.write("(" + list1[i] + ")\n")
                g.write("ORDER BY user_id")
                g.write("\n\n")

        print("-----------------------------")
        print(l)


if __name__ == "__main__":
    m_test2()
