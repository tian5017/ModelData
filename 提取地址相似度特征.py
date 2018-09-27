import Levenshtein as ls
import numpy as np
import pandas as pd

# 计算编辑距离

in_tab = "号楼单元房座层院"
out_tab = "        "
tran_tab = str.maketrans(in_tab, out_tab)

num_dict = {"零": 0, "一": 1, "①": 1, "二": 2, "②": 2, "两": 2, "三": 3, "③": 3, "四": 4, "④": 4, "五": 5, "⑤": 5,
            "六": 6, "⑥": 6, "七": 7, "⑦": 7, "八": 8, "⑧": 8, "九": 9, "⑨": 9, "十": 10, "⑩": 10, "百": 100,
            "千": 1000, "万": 10000, "亿": 100000000}


# 中文数字转为阿拉伯数字，如 五百二十三 --> 523
def chinese2digits(num_chinese):
    result = 0
    tmp = 0
    hnd_mln = 0
    for count in range(len(num_chinese)):
        curr_char = num_chinese[count]
        curr_digit = num_dict.get(curr_char)
        # 亿
        if curr_digit == 10 ** 8:
            result = result + tmp
            result = result * curr_digit
            hnd_mln = hnd_mln * 10 ** 8 + result
            result = 0
            tmp = 0
        # 万
        elif curr_digit == 10 ** 4:
            result = result + tmp
            result = result * curr_digit
            tmp = 0
        # 十, 百, 千
        elif curr_digit >= 10:
            tmp = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp = 0
        # 个
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result
    result = result + tmp
    result = result + hnd_mln
    return result


# 将一个中文句子中的中文数字转换为阿拉伯数字
def chineseNumToArab(in_str):
    in_l = len(in_str)
    out_str = ""
    if in_l == 0:
        return out_str

    has_num_stat = False
    num_str = ""
    for idx in range(in_l):
        if in_str[idx] in list(num_dict.keys()):
            if not has_num_stat:
                has_num_stat = True
            num_str += in_str[idx]
        else:
            if has_num_stat:
                if in_str[idx] in list(num_dict.keys()):
                    num_str += in_str[idx]
                    continue
                else:
                    num_result = str(chinese2digits(num_str))
                    num_str = ""
                    has_num_stat = False
                    out_str += num_result

            out_str += in_str[idx]

    if len(num_str) > 0:
        num_result = str(chinese2digits(num_str))
        out_str += str(num_result)

    return out_str



# 用编辑距离计算两个句子的相似度
def edit_distance_simil(str_1, str_2):
    str_1 = chineseNumToArab(str_1)
    str_2 = chineseNumToArab(str_2)

    # 提取出字符串中的汉字和数字
    str_1_tmp = "".join([x for x in filter(lambda x: x.isalpha() or x.isdigit(), str_1)])
    str_2_tmp = "".join([x for x in filter(lambda x: x.isalpha() or x.isdigit(), str_2)])

    # 去掉没有意义的汉字
    str_1_tmp = str_1_tmp.translate(tran_tab).replace(" ", "")
    str_2_tmp = str_2_tmp.translate(tran_tab).replace(" ", "")

    # 计算编辑距离
    l_dis = ls.distance(str_1_tmp, str_2_tmp)
    # 返回两个句子的相似度
    return 1 - l_dis / max(len(str_1_tmp), len(str_2_tmp))


# 得到一组数据的相似度
# str_list : 包含多个文本的列表
# threshold ： 相似度阈值，默认0.8
# return : 相同地址前缀下，地址相似度超过阈值所占比例
def get_doc_simil(str_list, threshold=0.8):
    result_simil = []
    if len(str_list) == 0:
        return result_simil

    for i in range(len(str_list)):
        tmp_arr = []
        for j in range(len(str_list)):
            tmp_arr.append(edit_distance_simil(str_list[i].strip(), str_list[j].strip()))
        tmp_arr = np.array(tmp_arr)
        tmp_arr_m = tmp_arr[tmp_arr > threshold]
        result_simil.append(round((len(tmp_arr_m) - 1) / len(tmp_arr), 2))

    return result_simil


# 提取地址相似度特征
def get_address_flag():
    file_path = "data/0721-0731/data-0721-0731.csv"
    save_path = "data/0721-0731/result-data-0721-0731.csv"
    df = pd.read_csv(file_path, encoding="GBK")
    address_prefix = df["address_prefix"]
    print(len(address_prefix))
    address_prefix = address_prefix.drop_duplicates()
    address_prefix_list = list(address_prefix)
    print(len(address_prefix_list))
    data_return = {}
    over_order_id_list = []
    over_doc_simil_list = []
    for address_pre in address_prefix_list:
        df_address_tmp = df[df["address_prefix"] == address_pre]
        order_id_tmp = df_address_tmp["id"]
        address_tmp = df_address_tmp["address_prefix"] + df_address_tmp["address_detail"]
        order_id_tmp_list = list(order_id_tmp)
        address_tmp_list = list(address_tmp)
        doc_simil_list = get_doc_simil(address_tmp_list)
        over_order_id_list += order_id_tmp_list
        over_doc_simil_list += doc_simil_list

    data_return["order_id"] = over_order_id_list
    data_return["doc_simil"] = over_doc_simil_list
    df = pd.DataFrame(data_return, columns=["order_id", "doc_simil"])
    df.to_csv(save_path, index=False)
    print("over")



# 将新提取的用户行为特征加入原来数据集（地址相似度）
def data_over():
    df_one = pd.read_csv("data/0721-0731/data-0721-0731-over.csv", encoding="GBK")
    df_two = pd.read_csv("data/0721-0731/doc-simil-0721-0731.csv")

    doc_simil = list(df_two["doc_simil"])
    df_one["doc_simil"] = doc_simil
    df_one.to_csv("data/0721-0731/data-0721-0731-over1.csv", index=False, encoding="GBK")
    print("over")



if __name__ == "__main__":
    # str_list = ["果园西里9甲果园西里9甲5单元201", "果园西里9甲五单元二零一", "果园西里9甲号楼果园西里9甲7单元502",
    #             "果园西里9甲号楼九假五单元201", "果园西里9甲号楼5单元201", "果园西里9甲号楼五单元二零1",
    #             "果园西里9甲号楼5单元201", "果园西里9甲号楼五单元201", "果园西里9甲号楼5单元201"]
    # a = get_doc_simil(str_list)
    # print(a)

    # get_address_flag()
    data_over()