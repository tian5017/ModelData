import pandas as pd
import util_online as util
import decimal
from timeit import Timer
import time

# 重写round方法，精确计算四舍五入
def round(v, k):
    acc = "." + "".join([str(0) for _ in range(k)])
    return float(decimal.Decimal(decimal.Decimal(str(v)).quantize(decimal.Decimal(acc), rounding=decimal.ROUND_HALF_UP)))

MODEL_N1 = 4.0
MODEL_N2 = 3.0


# 提取数据
# data : 原始数据集
# train_data_list : 提取特征之后的数据集
def dt_extract_data(data, train_data_list):
    baijiaxing_txt = pd.read_csv("data/baijiaxing.txt", sep=",", encoding="GBK")
    baijiaxing = baijiaxing_txt.columns.values
    for i in range(len(data)):
        print(i)
        # ----------------------提取优惠比例----------------------
        train_data_list.loc[i, "coupon_radio"] = round(data.loc[i, "use_coupon"] / data.loc[i, "total_price"], 2)
        # ----------------------提取促销比例----------------------
        train_data_list.loc[i, "promotion_radio"] = round(data.loc[i, "promotion_price"] / data.loc[i, "total_price"], 2)
        # ----------------------提取实际付款比例----------------------
        train_data_list.loc[i, "realpay_radio"] = round((data.loc[i, "total_price"] - data.loc[i, "use_coupon"] - data.loc[i, "promotion_price"]) / data.loc[i, "total_price"], 2)
        # ----------------------提取登陆到下单的时间----------------------
        train_data_list.loc[i, "login_order_time"] = data.loc[i, "login_order_time"]
        # 当前地址前缀
        curr_address_prefix = data.loc[i, "address_prefix"]
        # 当前地址详情
        curr_address_detail = data.loc[i, "address_detail"]
        # 和当前地址前缀有相同前缀的所有数据
        curr_brfore_data = data.loc[:i] # 从第1条到当前数据
        curr_tmp_data_tmp = curr_brfore_data[curr_brfore_data["address_prefix"] == curr_address_prefix]
        # 从当前时间开始，往前推7天的时间
        create_time = data.loc[i, "created"] # 下单时间
        # 7天之前到现在时间段内的所有数据
        curr_tmp_data = util.get_7_day_to_now(curr_tmp_data_tmp, create_time)
        # ----------------------提取(前缀 + 详细地址）相似度----------------------
        same_address_prefix_list = list(curr_tmp_data["address_prefix"] + curr_tmp_data["address_detail"])
        train_data_list.loc[i, "doc_simil"] = util.get_doc_simil_one(same_address_prefix_list, curr_address_prefix + curr_address_detail)
        # ----------------------提取实付运费比例----------------------
        total_freight_fee = data.loc[i, "total_freight_fee"]
        discount_freight_fee = data.loc[i, "discount_freight_fee"]
        if total_freight_fee == 0 or (total_freight_fee - discount_freight_fee) < 0:
            train_data_list.loc[i, "real_freight_fee"] = 0
        else:
            train_data_list.loc[i, "real_freight_fee"] = (total_freight_fee - discount_freight_fee) / total_freight_fee
        # ----------------判断姓是否在百家姓内 / 判断名字的长度是否是2到3个字 / 判断姓和名是否相同----------------
        name = data.loc[i, "name"]
        if name[0] in baijiaxing:
            train_data_list.loc[i, "xingconfidence"] = 1
        else:
            train_data_list.loc[i, "xingconfidence"] = 0
        if len(name) == 2 or len(name) == 3:
            train_data_list.loc[i, "nameconfidence"] = 1
        else:
            train_data_list.loc[i, "nameconfidence"] = 0
        if len(name) > 1 and name[1] != name[0]:
            train_data_list.loc[i, "xingmingxiangdeng"] = 1
        else:
            train_data_list.loc[i, "xingmingxiangdeng"] = 0
        # -----------------------提取溢价率--------------------------
        order_price = data.loc[i, "order_price"]
        train_data_list.loc[i, "price_ratio"] = round((order_price - 1999.0) / 1999.0, 9)
        # ---------------------------提取相同地址前缀相同IP比例--------------------------
        # 当前IP
        ip_address = data.loc[i, "user_ip"]
        # 相同地址前缀下和当前IP相同的IP的数目
        same_addressprefix_same_ip_num = list(curr_tmp_data["user_ip"].values).count(ip_address)
        if same_addressprefix_same_ip_num < MODEL_N1:
            train_data_list.loc[i, "sameaddressprefix_sameIP_ratio"] = 0.0
        else:
            train_data_list.loc[i, "sameaddressprefix_sameIP_ratio"] = round(float((same_addressprefix_same_ip_num - MODEL_N1) / (float(len(curr_tmp_data)) - MODEL_N2)), 9)
        # ----------------------------提取详细地址中数字的相似度--------------------------
        # 当前详细地址
        address_detail = data.loc[i, "address_detail"]
        address_detail = util.chineseNumToArab(address_detail)
        # 相同地址前缀下的详细地址
        same_address_prefix_detail = list(curr_tmp_data["address_detail"].values)
        # 将句子中的中文数字转换为阿拉伯数字
        same_address_prefix_detail = [util.chineseNumToArab(tmp) for tmp in same_address_prefix_detail]
        # 提取出详细地址中的数字
        same_address_prefix_detail_num = [x for x in ["".join(list(filter(lambda x: x.isdigit(), tmp))) for tmp in same_address_prefix_detail]]
        same_address_prefix_detail_num = list(filter(None, same_address_prefix_detail_num))
        address_detail_num = "".join(list(filter(lambda x: x.isdigit(), address_detail)))
        train_data_list.loc[i, "sameaddressprefix_similardetail"] = util.get_doc_simil_one(same_address_prefix_detail_num, address_detail_num)
        # -----------------------------提取详细地址中汉字的相似度--------------------------
        # 提取出详细地址中的汉字
        same_address_prefix_detail_word = [x for x in ["".join(list(filter(lambda x: x.isalpha(), tmp))) for tmp in same_address_prefix_detail]]
        same_address_prefix_detail_word = list(filter(None, same_address_prefix_detail_word))
        address_detail_word = "".join(list(filter(lambda x: x.isalpha(), address_detail)))
        train_data_list.loc[i, "sameaddressprefix_detail_zhongwen"] = util.get_doc_simil_one(same_address_prefix_detail_word, address_detail_word)
        # -----------------------------相同地址前缀下不同用户比例---------------------------
        sameaddress_user_num = len(set(list(curr_tmp_data["webuser_id"].values)))
        if float(sameaddress_user_num) < MODEL_N1:
            sameaddressprefix_userratio = 0.0
        else:
            sameaddressprefix_userratio = round((float(sameaddress_user_num) - MODEL_N1) / (float(len(curr_tmp_data)) - MODEL_N2), 9)
        train_data_list.loc[i, "sameaddressprefix_userratio"] = sameaddressprefix_userratio
        # -----------------------------相同地址前缀下相同收货人姓名比例--------------------------------
        # 相同地址前缀下的收货人姓名
        same_address_prefix_name = list(curr_tmp_data["name"].values)
        train_data_list.loc[i, "same_address_prefix_name"] = util.same_data_num(same_address_prefix_name, name)
        # -----------------------------相同地址前缀下相同收货人手机号数量--------------------------------
        phone = data.loc[i, "phone"]
        # 相同地址前缀下的收货人手机号码
        same_address_prefix_phone = list(curr_tmp_data["phone"].values)
        train_data_list.loc[i, "same_address_prefix_phone"] = util.same_data_num(same_address_prefix_phone, phone)
        # -----------------------------相同地址前缀下相同设备号数量--------------------------------
        deviceid = data.loc[i, "deviceid"]
        # 相同地址前缀下的设备号
        same_address_prefix_deviceid = list(curr_tmp_data["deviceid"].values)
        train_data_list.loc[i, "same_address_prefix_deviceid"] = util.same_data_num(same_address_prefix_deviceid, deviceid)
        # -----------------------------------提取注册来源---------------------------------------
        register_src = data.loc[i, "register_src"]
        if register_src in (2, 3, 4, 9):
            train_data_list.loc[i, "register"] = 1
        else:
            train_data_list.loc[i, "register"] = 0
        # ---------------------------提取截断地址前缀后相同地址前缀下地址详情的相似度--------------------------
        # 当前地址前缀(截断)
        address_prefix_new = data.loc[i, "address_prefix_new"]
        # 当前地址详情(截断)
        address_detail_new = data.loc[i, "address_detail_new"]
        # 和当前地址前缀(截断)有相同前缀的所有数据
        curr_tmp_data_tmp_new = curr_brfore_data[curr_brfore_data["address_prefix_new"] == address_prefix_new]
        # 7天之前到现在时间段内的所有数据
        curr_tmp_data_new = util.get_7_day_to_now(curr_tmp_data_tmp_new, create_time)
        # 相同地址前缀(截断)下的详细地址
        same_address_prefix_new_detail = list(curr_tmp_data_new["address_detail_new"].values)
        train_data_list.loc[i, "sameaddressprefix_new_samedetail"] = util.get_doc_simil_one(same_address_prefix_new_detail, address_detail_new)
        # ---------------------------组合特征--------------------------
        # sameaddressprefix_userratio+sameaddressprefix_new_samedetail
        train_data_list.loc[i, "sameaddressprefix_userratio+sameaddressprefix_new_samedetail"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] + train_data_list.loc[i, "sameaddressprefix_new_samedetail"], 9)
        # sameaddressprefix_userratio+sameaddressprefix_similardetail
        train_data_list.loc[i, "sameaddressprefix_userratio+sameaddressprefix_similardetail"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] + train_data_list.loc[i, "sameaddressprefix_similardetail"], 9)
        # sameaddressprefix_userratio+same_address_prefix_name
        train_data_list.loc[i, "sameaddressprefix_userratio+same_address_prefix_name"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] + train_data_list.loc[i, "same_address_prefix_name"], 9)

        # sameaddressprefix_new_samedetail-sameaddressprefix_detail_zhongwen
        train_data_list.loc[i, "sameaddressprefix_new_samedetail-sameaddressprefix_detail_zhongwen"] = round(train_data_list.loc[i, "sameaddressprefix_new_samedetail"] - train_data_list.loc[i, "sameaddressprefix_detail_zhongwen"], 9)
        # sameaddressprefix_userratio+doc_simil
        train_data_list.loc[i, "sameaddressprefix_userratio+doc_simil"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] + train_data_list.loc[i, "doc_simil"], 9)
        # sameaddressprefix_userratio/price_ratio
        if train_data_list.loc[i, "price_ratio"] != 0:
            train_data_list.loc[i, "sameaddressprefix_userratio/price_ratio"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] / train_data_list.loc[i, "price_ratio"], 9)
        else:
            train_data_list.loc[i, "sameaddressprefix_userratio/price_ratio"] = 0.0
        # price_ratio+login_order_time
        train_data_list.loc[i, "price_ratio+login_order_time"] = round(train_data_list.loc[i, "price_ratio"] + train_data_list.loc[i, "login_order_time"], 9)
        # sameaddressprefix_userratio+coupon_radio
        train_data_list.loc[i, "sameaddressprefix_userratio+coupon_radio"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] + train_data_list.loc[i, "coupon_radio"], 9)
        # sameaddressprefix_userratio*same_address_prefix_name
        train_data_list.loc[i, "sameaddressprefix_userratio*same_address_prefix_name"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] * train_data_list.loc[i, "same_address_prefix_name"], 9)
        # sameaddressprefix_new_samedetail/doc_simil
        if train_data_list.loc[i, "doc_simil"] != 0:
            train_data_list.loc[i, "sameaddressprefix_new_samedetail/doc_simil"] = round(train_data_list.loc[i, "sameaddressprefix_new_samedetail"] / train_data_list.loc[i, "doc_simil"], 9)
        else:
            train_data_list.loc[i, "sameaddressprefix_new_samedetail/doc_simil"] = 0.0
        # sameaddressprefix_new_samedetail-doc_simil
        train_data_list.loc[i, "sameaddressprefix_new_samedetail-doc_simil"] = round(train_data_list.loc[i, "sameaddressprefix_new_samedetail"] - train_data_list.loc[i, "doc_simil"], 9)
        # sameaddressprefix_new_samedetail-sameaddressprefix_sameIP_ratio
        train_data_list.loc[i, "sameaddressprefix_new_samedetail-sameaddressprefix_sameIP_ratio"] = round(train_data_list.loc[i, "sameaddressprefix_new_samedetail"] - train_data_list.loc[i, "sameaddressprefix_sameIP_ratio"], 9)
        # sameaddressprefix_userratio-login_order_time
        train_data_list.loc[i, "sameaddressprefix_userratio-login_order_time"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] - train_data_list.loc[i, "login_order_time"], 9)
        # sameaddressprefix_userratio-sameaddressprefix_similardetail
        train_data_list.loc[i, "sameaddressprefix_userratio-sameaddressprefix_similardetail"] = round(train_data_list.loc[i, "sameaddressprefix_userratio"] - train_data_list.loc[i, "sameaddressprefix_similardetail"], 9)
        # sameaddressprefix_similardetail+login_order_time
        train_data_list.loc[i, "sameaddressprefix_similardetail+login_order_time"] = round(train_data_list.loc[i, "sameaddressprefix_similardetail"] + train_data_list.loc[i, "login_order_time"], 9)
        # sameaddressprefix_similardetail-doc_simil
        train_data_list.loc[i, "sameaddressprefix_similardetail-doc_simil"] = round(train_data_list.loc[i, "sameaddressprefix_similardetail"] - train_data_list.loc[i, "doc_simil"], 9)
        # price_ratio+sameaddressprefix_detail_zhongwen
        train_data_list.loc[i, "price_ratio+sameaddressprefix_detail_zhongwen"] = round(train_data_list.loc[i, "price_ratio"] + train_data_list.loc[i, "sameaddressprefix_detail_zhongwen"], 9)
        # price_ratio+coupon_radio
        train_data_list.loc[i, "price_ratio+coupon_radio"] = round(train_data_list.loc[i, "price_ratio"] + train_data_list.loc[i, "coupon_radio"], 9)
        # sameaddressprefix_similardetail+same_address_prefix_name
        train_data_list.loc[i, "sameaddressprefix_similardetail+same_address_prefix_name"] = round(train_data_list.loc[i, "sameaddressprefix_similardetail"] + train_data_list.loc[i, "same_address_prefix_name"], 9)
        # coupon_radio/sameaddressprefix_sameIP_ratio
        if train_data_list.loc[i, "sameaddressprefix_sameIP_ratio"] != 0:
            train_data_list.loc[i, "coupon_radio/sameaddressprefix_sameIP_ratio"] = round(train_data_list.loc[i, "coupon_radio"] / train_data_list.loc[i, "sameaddressprefix_sameIP_ratio"], 9)
        else:
            train_data_list.loc[i, "coupon_radio/sameaddressprefix_sameIP_ratio"] = 0.0

    return train_data_list



def main():
    base_data = pd.read_csv("data/test/20181019-D1-over.csv", encoding="GBK")
    # 按照时间顺序排序
    data = base_data.sort_values(by=["created", "address_prefix"])

    train_data_list = pd.DataFrame()
    train_data_list["order_id"] = data["id"]
    train_data_list["rcs_flag"] = data["rcs_flag"]
    # train_data_list["result"] = data["result"]
    # train_data_list["new_flag"] = data["new_flag"]

    # 提取特征
    train_data_list = dt_extract_data(data, train_data_list)

    # 特征提取完成后，在按照原来的输入顺序进行排序
    base_order_id_list = list(base_data["id"])
    train_data_list["order_id"] = train_data_list["order_id"].astype("category")
    train_data_list["order_id"].cat.reorder_categories(base_order_id_list, inplace=True)
    train_data_list.sort_values("order_id", inplace=True)
    train_data_list.to_csv("data/test/20181019-D1-train.csv", index=False)
    print("over")


if __name__ == "__main__":
    exc_time = Timer("main()", "from __main__ import main").timeit(1)
    print("run times:", exc_time)