import pandas as pd
import time
import datetime
import os
import random

# 字符串时间转换为时间戳（秒）
def str2time(str):
    return time.mktime(time.strptime(str, "%Y-%m-%d %H:%M:%S"))


# 获取数据的均值
def get_mean(data_list):
    if len(data_list) == 0:
        print(data_list)
    return sum(data_list) / len(data_list)


"""
提取特征项如下：
开始操作到添加购物车的时间（秒）
开始操作到结算之间的行为次数（次）
开始操作到结算之间点击商品详情页的次数（次）
开始操作到结算时间（秒）
file_path: 数据文件路径
save_path: 提取完成后文件保存路径
"""
def get_data(file_path, save_path):
    # 提取完成后的数据
    data_return = {}
    data_csv = pd.read_csv(file_path)
    user_id_list = data_csv["user_id"]
    # 用户ID集合
    user_id_list = user_id_list.drop_duplicates()
    user_id_list = list(user_id_list)
    # 开始操作到加购平均时间集合
    add_cart_time_list = []
    # 开始操作到结算平均时间集合
    purchase_time_list = []
    # 开始操作到结算之间平均行为次数集合
    behaviour_num_list = []
    # 开始操作到计算之间点击商详次数集合
    detail_num_list = []
    for user_id in user_id_list:
        data_list = data_csv[data_csv["user_id"] == user_id]
        data_list = data_list.sort_values(by=["receive_time"], ascending=True)
        event_code_arr = list(data_list["event_code"])
        receive_time_arr = list(data_list["receive_time"].map(str2time))

        # 开始操作到添加购物车的行为
        add_cart_index_arr = [i for i in range(len(event_code_arr)) if event_code_arr[i] in ["app_add_cart_click", "mweb_add_cart_click"]]
        if len(add_cart_index_arr) == 0:
            add_cart_time_list.append(-1)
        else:
            # 存储每一次从开始操作到添加购物车操作之间的时间
            add_cart_time_diff = []
            for i_ in range(len(add_cart_index_arr)):
                index_point = add_cart_index_arr[i_]
                # 添加购物车的时间
                base_data_time = receive_time_arr[index_point]
                curr_data_time = base_data_time
                while index_point > 0:
                    index_point -= 1
                    prev_data_time = receive_time_arr[index_point]
                    if curr_data_time - prev_data_time < 15 * 60:
                        if (event_code_arr[index_point] in ["app_boot", "app_purchase_process", "mweb_payresult_pv"]) or (index_point == 0):
                            add_cart_time_diff.append(base_data_time - prev_data_time)
                            break
                        elif event_code_arr[index_point] in ["app_add_cart_click", "mweb_add_cart_click"]:
                            add_cart_time_diff.append(base_data_time - curr_data_time)
                            break
                        else:
                            curr_data_time = prev_data_time
                            continue
                    else:
                        add_cart_time_diff.append(base_data_time - curr_data_time)
                        break
            # 获取数组中大于0的元素的下标
            add_cart_time_diff_ = [a for a in range(len(add_cart_time_diff)) if add_cart_time_diff[a] > 0]
            if len(add_cart_time_diff_) == 0:
                add_cart_time_list.append(-1)
            else:
                add_cart_time_diff = [add_cart_time_diff[a] for a in add_cart_time_diff_]
                add_cart_time_list.append(round(get_mean(add_cart_time_diff), 2))

        # 开始操作到结算的行为
        purchase_index_arr = [i for i in range(len(event_code_arr)) if event_code_arr[i] in ["app_purchase_process", "mweb_payresult_pv"]]
        if len(purchase_index_arr) == 0:
            purchase_time_list.append(-1)
            behaviour_num_list.append(-1)
            detail_num_list.append(-1)
        else:
            # 存储每一次从开始操作到结算操作之间的时间
            purchase_time_diff = []
            # 存储每一次从开始操作到结算操作之间的行为次数
            purchase_num_diff = []
            # 存储每一次从开始操作到结算操作之间浏览商品详情页的次数
            purchase_detail_diff = [0 for _ in range(len(purchase_index_arr))]
            for i_ in range(len(purchase_index_arr)):
                index_point = purchase_index_arr[i_]
                # 结算的时间
                base_data_time = receive_time_arr[index_point]
                curr_data_time = base_data_time
                i = 0
                while index_point > 0:
                    i += 1
                    index_point -= 1
                    prev_data_time = receive_time_arr[index_point]
                    if event_code_arr[index_point] in ["app_ware_detail_pv", "mweb_detail_pv"]:
                        purchase_detail_diff[i_] += 1
                    if curr_data_time - prev_data_time < 15 * 60:
                        if (event_code_arr[index_point] in ["app_boot", "mweb_home_pv"]) or (index_point == 0):
                            purchase_time_diff.append(base_data_time - prev_data_time)
                            purchase_num_diff.append(i)
                            break
                        elif event_code_arr[index_point] in ["app_purchase_process", "mweb_payresult_pv"]:
                            purchase_time_diff.append(base_data_time - curr_data_time)
                            purchase_num_diff.append(i - 1)
                            break
                        else:
                            curr_data_time = prev_data_time
                            continue
                    else:
                        purchase_time_diff.append(base_data_time - curr_data_time)
                        purchase_num_diff.append(i - 1)
                        break
            # 获取数组中大于0的元素的下标
            purchase_time_diff_ = [a for a in range(len(purchase_time_diff)) if purchase_time_diff[a] > 0]
            if len(purchase_time_diff_) == 0:
                purchase_time_list.append(-1)
                behaviour_num_list.append(-1)
                detail_num_list.append(-1)
            else:
                purchase_time_diff = [purchase_time_diff[a] for a in purchase_time_diff_]
                purchase_num_diff = [purchase_num_diff[a] for a in purchase_time_diff_]
                purchase_detail_diff = [purchase_detail_diff[a] for a in purchase_time_diff_]
                purchase_time_list.append(round(get_mean(purchase_time_diff), 2))
                behaviour_num_list.append(round(get_mean(purchase_num_diff), 2))
                detail_num_list.append(round(get_mean(purchase_detail_diff), 2))

    data_return["user_id"] = user_id_list
    data_return["add_cart_time"] = add_cart_time_list
    data_return["purchase_time"] = purchase_time_list
    data_return["behaviour_num"] = behaviour_num_list
    data_return["detail_num"] = detail_num_list
    df = pd.DataFrame(data_return)
    df.to_csv(save_path, index=False)


def get_yestoday(mytime):
    t1 = datetime.datetime.strptime(mytime, "%Y-%m-%d %H:%M:%S")
    t2 = datetime.timedelta(days=-1)
    t3 = t1 + t2
    my_yes_time = t3.strftime('%Y-%m-%d %H:%M:%S')
    return my_yes_time


def diff_date(time1, time2):
    t1 = datetime.datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
    t2 = datetime.datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")
    return (t2 - t1).seconds


"""
提取特征项如下：
搜索到添加购物车的时间（秒）
搜索到下单的时间（秒）
搜索到下单之间点击商品详情页的次数（次）
file_path: 数据文件路径
save_path: 提取完成后文件保存路径
"""
data_path = "./data/test/ip-hn-rrl-over.csv"
data_file_df = pd.read_csv(data_path)
def get_data_new(file_path, save_path):
    # 提取完成后的数据
    data_return = {}
    data_csv = pd.read_csv(file_path)
    user_id_list = data_csv["user_id"]
    # 用户ID集合
    user_id_list = user_id_list.drop_duplicates()
    user_id_list = list(user_id_list)
    # 搜索到加购时间
    sou_cart_time_list = []
    # 搜索到下单时间
    sou_order_time_list = []
    # 搜索到下单之间点击商品详情页的次数
    sou_order_num_list = []
    if int(8416373) in user_id_list:
        user_id_list.remove(int(8416373))
    if int(738304) in user_id_list:
        user_id_list.remove(int(738304))
    for user_id in user_id_list:
        curr_user_data = data_file_df.loc[data_file_df.loc[:, "user_id"] == user_id, :]
        curr_user_data = curr_user_data.sort_values(by=["created"], ascending=True)
        curr_created = curr_user_data["created"].values[0]
        curr_created = curr_created.replace("/", "-")
        curr_yestoday = get_yestoday(curr_created)

        data_list = data_csv[data_csv["user_id"] == user_id]
        data_list = data_list.sort_values(by=["receive_time"], ascending=True)
        data_list_tmp1 = data_list.loc[(data_list["receive_time"] <= curr_created) & (data_list["receive_time"] >= curr_yestoday), :]
        data_list_tmp2 = data_list_tmp1.reset_index(drop=True)

        # 开始操作到添加购物车的行为
        add_cart_index = -1
        for i in range(len(data_list_tmp2)-1, 0, -1):
            if data_list_tmp2.loc[i, "event_code"] in ["app_add_cart_click", "mweb_add_cart_click"]:
                if (i - 1 >= 0) and (data_list_tmp2.loc[i - 1, "event_code"] in ["app_add_cart_click", "mweb_add_cart_click"]):
                    continue
                else:
                    add_cart_index = i
                    break
        if int(add_cart_index) >= 1 and int(add_cart_index) < len(data_list_tmp2):
            index_point1 = add_cart_index
            # 添加购物车的时间
            base_data_time1 = data_list_tmp2.loc[add_cart_index, "receive_time"]
            curr_data_time1 = base_data_time1
            sou_cart_time = -1
            # 从添加购物车的行为开始往前查找搜索行为
            while index_point1 > 0:
                index_point1 -= 1
                prev_data_time1 = data_list_tmp2.loc[index_point1, "receive_time"]
                diff_time1 = diff_date(prev_data_time1, curr_data_time1)
                if diff_time1 < 15 * 60:
                    if data_list_tmp2.loc[index_point1, "event_code"] in ["app_search_click"]:
                        sou_cart_time = diff_date(prev_data_time1, base_data_time1)
                        sou_cart_time_list.append(sou_cart_time)
                        break
                    else:
                        curr_data_time1 = prev_data_time1
                        continue
                else:
                    sou_cart_time = diff_date(curr_data_time1, base_data_time1)
                    sou_cart_time_list.append(sou_cart_time)
                    break
            if sou_cart_time == -1:
                sou_cart_time_list.append(-1)
        else:
            sou_cart_time_list.append(-1)

        # 开始操作到下单的行为
        index_point2 = len(data_list_tmp2) - 1
        curr_data_time2 = curr_created
        sou_order_time = -1
        # 从添加购物车的行为开始往前查找搜索行为
        while index_point2 > 0:
            index_point2 -= 1
            prev_data_time2 = data_list_tmp2.loc[index_point2, "receive_time"]
            diff_time2 = diff_date(prev_data_time2, curr_data_time2)
            if diff_time2 < 15 * 60:
                if data_list_tmp2.loc[index_point2, "event_code"] in ["app_search_click"]:
                    sou_order_time = diff_date(prev_data_time2, curr_created)
                    sou_order_time_list.append(sou_order_time)
                    break
                else:
                    curr_data_time2 = prev_data_time2
                    continue
            else:
                sou_order_time = diff_date(curr_data_time2, curr_created)
                sou_order_time_list.append(sou_order_time)
                break
        if sou_order_time == -1:
            sou_order_time_list.append(-1)

        sou_order_num_list.append(len(data_list_tmp2) - 1 - index_point2)

    data_return["user_id"] = user_id_list
    data_return["sou_cart_time"] = sou_cart_time_list
    data_return["sou_order_time"] = sou_order_time_list
    data_return["sou_order_num"] = sou_order_num_list
    df = pd.DataFrame(data_return)
    df.to_csv(save_path, index=False)




# 提取所有的用户ID
def get_user_ids():
    data = pd.read_csv("./data/test/data-1125-over.csv")
    webuser_id = data["a.webuser_id"]
    print(len(webuser_id))
    # 去除重复数据
    user_id_list = webuser_id.drop_duplicates()
    user_id_list = list(user_id_list)
    print(len(user_id_list))
    s = ""
    for i in range(1, len(user_id_list)+1):
        s += str(user_id_list[i-1]) + ","
        if i % 500 == 0:
            s = s[:-1]
            s += "\n"
    with open("./data/test/20181126-1.txt", "w") as f:
        s = s[:-1]
        f.write(s)



# 将新提取的多个特征数据文件合并为一个文件
def data_file_merge():
    fs = os.listdir("./data/test/event_out")
    for i in range(len(fs)):
        print(fs[i])
        file_path = "./data/test/event_out/" + fs[i]
        fr_lines = open(file_path, "r", encoding="utf-8").readlines()
        print(len(fr_lines))
        a = 1
        if i == 0:
            a = 0
        with open("./data/test/event-hn-rrl.csv", "a+", encoding="utf-8") as aa:
            for x in range(a, len(fr_lines)):
                aa.write(fr_lines[x])
    print("合并完毕")



# 将新提取的用户行为特征加入原来数据集（用户行为特征）
def event_in_data():
    df_one = pd.read_csv("./data/test/1114-false.csv")
    df_two = pd.read_csv("./data/test/1114-event-false-over.csv")
    add_cart_time = []
    behaviour_num = []
    detail_num = []
    purchase_time = []
    for i in range(len(df_one)):
        # 此处webuser_id需要查看原数据文件中的字段名，需要与原字段名保持一致
        user_id = df_one.loc[i, "用户ID"]
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
    df_one.to_csv("./data/test/1114-false-over.csv", index=False)
    print("over")



# 将新提取的用户行为特征加入原来数据集（新用户行为特征）
def event_in_data_new():
    df_one = pd.read_csv("./data/test/ip-hn-rrl-over.csv")
    df_two = pd.read_csv("./data/test/event-hn-rrl.csv")
    sou_cart_time = []
    sou_order_time = []
    sou_order_num = []
    for i in range(len(df_one)):
        # 此处webuser_id需要查看原数据文件中的字段名，需要与原字段名保持一致
        user_id = df_one.loc[i, "user_id"]
        print(str(i) + ", " + str(user_id))
        two_data = df_two[df_two["user_id"].astype(str) == str(user_id)]
        if len(two_data) == 0:
            sou_cart_time.append(-1)
            sou_order_time.append(-1)
            sou_order_num.append(-1)
        else:
            sou_cart_time.append(two_data["sou_cart_time"].values[0])
            sou_order_time.append(two_data["sou_order_time"].values[0])
            sou_order_num.append(two_data["sou_order_num"].values[0])

    df_one["sou_cart_time"] = sou_cart_time
    df_one["sou_order_time"] = sou_order_time
    df_one["sou_order_num"] = sou_order_num
    df_one.to_csv("./data/test/ip-hn-rrl-event.csv", index=False)
    print("over")


# 随机选取非刷单用户的用户ID
def get_user_ids_by_nomal():
    # 选取的用户ID的数量
    num = 1500
    data = pd.read_csv("./data/test/data-1109-1111.csv", encoding="GBK")
    user_id_list = list(data[data["result"] == 0]["webuser_id"])
    data_set = set()
    while len(data_set) < num:
        ran = random.randint(1, len(user_id_list) - 2)
        data_set.add(user_id_list[ran])
    print(len(data_set))
    data_list = list(data_set)
    s = ""
    for i in range(1, len(data_list)+1):
        s += str(data_list[i-1]) + ","
        if i % 200 == 0:
            s = s[:-1]
            s += "\n"
    with open("./data/test/20181115-aa.txt", "w") as f:
        s = s[:-1]
        f.write(s)



# 提取行为数据（old）
def get_event_data_old():
    fs = os.listdir("./data/test/event")
    for i in range(len(fs)):
        print(fs[i])
        file_path = "./data/test/event/" + fs[i]
        save_path = "./data/test/event_out/" + fs[i]
        get_data(file_path, save_path)



# 提取行为数据（new）
def get_event_data_new():
    fs = os.listdir("./data/test/event")
    for i in range(len(fs)):
        print(fs[i])
        file_path = "./data/test/event/" + fs[i]
        save_path = "./data/test/event_out/" + fs[i]
        get_data_new(file_path, save_path)



if __name__ == "__main__":
    # 0、随机提取非刷单数据用户ID
    # get_user_ids_by_nomal()
    # 1、提取刷单数据所有用户ID
    # get_user_ids()
    # 2、用第一步提取的user_id到hive中查询用户行为数据
    # 查询SQL：SELECT user_id,event_code,event_name,receive_time from dmall_dm_userprofile.events WHERE cast(user_id AS bigint) in () and dt>='20180101'
    # 3、提取用户行为数据（四维）
    # get_event_data_old()
    # 4、如果查询的行为数据文件有多个，要先对单个文件提取行为数据，最后合并行为数据文件
    # data_file_merge()
    # 5、将提取的用户行为数据加入原数据集
    # event_in_data()

    # 提取用户行为数据（新）
    # get_event_data_new()
    # get_data_new("./data/test/event/event-11.csv", "./data/test/event_out/event-11.csv")

    # 将提取的用户行为数据加入原数据集（新）
    event_in_data_new()
