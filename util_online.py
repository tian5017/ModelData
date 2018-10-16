import Levenshtein as ls
import numpy as np
import pandas as pd
import decimal
import time
import datetime

# 重写round方法，精确计算四舍五入
def round(v, k):
    acc = "." + "".join([str(0) for _ in range(k)])
    return float(decimal.Decimal(decimal.Decimal(str(v)).quantize(decimal.Decimal(acc), rounding=decimal.ROUND_HALF_UP)))


# 计算编辑距离
in_tab = "号楼单元房座层院"
out_tab = "        "
tran_tab = str.maketrans(in_tab, out_tab)

num_dict = {"零": 0, "O": 0, "o": 0, "一": 1, "①": 1, "I": 1, "i": 1, "二": 2, "②": 2, "两": 2, "三": 3, "③": 3, "四": 4, "④": 4, "五": 5, "⑤": 5,
            "六": 6, "⑥": 6, "七": 7, "⑦": 7, "八": 8, "⑧": 8, "九": 9, "⑨": 9, "十": 10, "⑩": 10, "百": 100,
            "千": 1000, "万": 10000, "亿": 100000000}


MODEL_N1 = 4.0
MODEL_N2 = 3.0

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
    num_str_start_symbol = ['一', '①', '二', '②', '两', '三', '③', '四', '④', '五', '⑤', '六', '⑥', '七', '⑦', '八', '⑧', '九', '⑨', '十', '⑩']
    in_l = len(in_str)
    out_str = ""
    if in_l == 0:
        return out_str

    has_num_stat = False
    num_str = ""
    for idx in range(in_l):
        if in_str[idx] in list(num_str_start_symbol):
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

    tmp_extend_symbol = {'O': '0', 'o': '0', 'I': '1', 'i': '1'}
    out_list = []
    if len(out_str) > 0:
        for out_char in out_str:
            if out_char in tmp_extend_symbol.keys():
                out_list.append(tmp_extend_symbol[out_char])
            else:
                out_list.append(out_char)

    return "".join(out_list)



# 用编辑距离计算两个句子的相似度
def edit_distance_simil(str_1, str_2):
    # 句子中的中文数字转换为阿拉伯数字
    str_1 = chineseNumToArab(str_1)
    str_2 = chineseNumToArab(str_2)

    # 提取出字符串中的汉字、字母和数字
    str_1_tmp = "".join([x for x in filter(lambda x: x.isalpha() or x.isdigit(), str_1)])
    str_2_tmp = "".join([x for x in filter(lambda x: x.isalpha() or x.isdigit(), str_2)])

    # 去掉没有意义的汉字
    str_1_tmp = str_1_tmp.translate(tran_tab).replace(" ", "")
    str_2_tmp = str_2_tmp.translate(tran_tab).replace(" ", "")

    # 计算编辑距离
    l_dis = ls.distance(str_1_tmp, str_2_tmp)
    if max(len(str_1_tmp), len(str_2_tmp)) == 0:
        return 0
    # 返回两个句子的相似度
    return 1.0 - l_dis / max(len(str_1_tmp), len(str_2_tmp))


# 计算一个句子在一个句子列表中的相似度
# str_list : 包含多个文本的列表
# str_one : 计算相似度的句子
# threshold ： 相似度阈值，默认0.8
# return : 相同地址前缀下，地址相似度超过阈值所占比例
def get_doc_simil_one(str_list, str_one, threshold=0.8):
    result_simil = 0.0
    if len(str_list) > 0 and str_one != "":
        tmp_arr = []
        for i in range(len(str_list)):
            tmp_arr.append(edit_distance_simil(str_list[i].strip(), str_one.strip()))

        tmp_arr = np.array(tmp_arr)
        tmp_arr_m = tmp_arr[tmp_arr >= threshold]
        if len(tmp_arr_m) >= MODEL_N1:
            result_simil = round((len(tmp_arr_m) - MODEL_N1) / (len(tmp_arr) - MODEL_N2), 2)

    return result_simil


# 计算data_list中和str_item相等的元素比例
# 计算公式：（data_list中与str_item相等的元素个数 - 1） / 10
def same_data_num(data_list, str_item):
    df = pd.DataFrame(data_list, columns=["tmp"])
    return (len(df[df["tmp"] == str_item]) - 1.0) / 10.0



# 获取从当天算起，7天之前的日期
def get_7_days_before(data):
    if isinstance(data, str):
        data_str = data.split(" ")[0]
        date_1 = time.strptime(data_str, "%Y/%m/%d")
        date_2 = datetime.datetime(date_1[0], date_1[1], date_1[2])
        date_3 = str(date_2 + datetime.timedelta(days=-6))
        date_3 = time.strptime(date_3, "%Y-%m-%d %H:%M:%S")
        time_stamp = time.mktime(date_3)
        return time_stamp


# 找出list中从create_time之前7天到create_time之间的所有数据
def get_7_day_to_now(list_data, create_time):
    time_stamp = get_7_days_before(create_time)
    for i in list_data.index:
        tmp_data = list_data.loc[i]
        tmp_data_time = tmp_data["created"]
        tmp_data_time_str = time.strptime(tmp_data_time, "%Y/%m/%d %H:%M")
        tmp_data_time_stamp = time.mktime(tmp_data_time_str)
        if tmp_data_time_stamp < time_stamp:
            list_data.drop(index=[i], inplace=True)
    return list_data



# 数据中的地址前缀遇到数字或者括号，进行截断，截断部分合并到详细地址，生成新的数据文件
def address_cut():
    tmp_arr = ["(", "（", "[", "【"]
    data = pd.read_csv("data/12345/abcde-over.csv", encoding="GBK")
    for i in range(len(data)):
        address_prefix = data.loc[i, "address_prefix"]
        address_detail = data.loc[i, "address_detail"]
        address_prefix_new = ""
        address_detail_new = ""
        for j in range(len(address_prefix)):
            if address_prefix[j].isdigit() or (address_prefix[j] in tmp_arr):
                address_prefix_new = address_prefix[:j]
                address_detail_new = address_prefix[j:] + address_detail
                break
        if address_prefix_new == "":
            address_prefix_new = address_prefix
        if address_detail_new == "":
            address_detail_new = address_detail

        data.loc[i, "address_prefix_new"] = address_prefix_new
        data.loc[i, "address_detail_new"] = address_detail_new
    data.to_csv("data/12345/abcde-new.csv", encoding="GBK", index=False)
    print("over")



if __name__ == "__main__":
    pass


