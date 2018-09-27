import pandas as pd
import time
import os

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
开始操作到结算时间（秒）
开始操作到结算之间的行为次数（次）
开始操作到结算之间点击商品详情页的次数（次）
file_path : 数据文件路径
save_path : 提取完成后文件保存路径
"""
def get_data(file_path, save_path):
    # 提取完成后返回的数据
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
        add_cart_index_arr = [i for i in range(len(event_code_arr)) if event_code_arr[i] == "app_add_cart_click"]
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
                    if curr_data_time - prev_data_time < 60 * 60:
                        if (event_code_arr[index_point] in ["app_boot", "app_purchase_process"]) or (index_point == 0):
                            add_cart_time_diff.append(base_data_time - prev_data_time)
                            break
                        elif event_code_arr[index_point] == "app_add_cart_click":
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
        purchase_index_arr = [i for i in range(len(event_code_arr)) if event_code_arr[i] == "app_purchase_process"]
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
                    if event_code_arr[index_point] == "app_ware_detail_pv":
                        purchase_detail_diff[i_] += 1
                    if curr_data_time - prev_data_time < 60 * 60:
                        if (event_code_arr[index_point] in ["app_boot"]) or (index_point == 0):
                            purchase_time_diff.append(base_data_time - prev_data_time)
                            purchase_num_diff.append(i)
                            break
                        elif event_code_arr[index_point] == "app_purchase_process":
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



if __name__ == "__main__":
    # file_path = "data/1000.csv"
    # get_data(file_path)

    fs = os.listdir("data/0621-0710")
    for f in fs:
        file_path = "data/0621-0710/" + f
        save_path = "result/a" + f
        get_data(file_path, save_path)

