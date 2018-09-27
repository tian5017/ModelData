# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 16:13:25 2018
@author: dmall
"""
import pandas as pd
import re
raw = pd.read_csv(u"D:\\dataset\\0723\\0711-0720新人劵地址排序-汇总.csv",encoding="gb18030")
#raw1 = pd.read_csv(u"D:\\dataset\\0716\\data-0621-0710(增加5维特征).csv",encoding="gb18030")
#raw2 = pd.read_csv(u"D:\\dataset\\0711\\data-0705-0710.csv",encoding="gb18030")
head = raw.columns.values
baijiaxing_txt = pd.read_csv('D:\\dataset\\0518\\5-21\\baijiaxing.txt', sep=',',encoding="gb18030")
baijiaxing = baijiaxing_txt.columns.values
print (head)

data0514 = raw
#data0514 = data0514.append(raw2.loc[raw2['dt'] == 20180709], ignore_index=True)

#data0514 = pd.DataFrame(columns = head)
#data0516 = pd.DataFrame(columns = head)

'''
data0514 = data0514.append(raw.loc[raw['dt'] == 20180514], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180515], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180516], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180517], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180518], ignore_index=True)


data0514 = data0514.append(raw.loc[raw['dt'] == 20180621], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180622], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180623], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180624], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180625], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180626], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180627], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180628], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180629], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180630], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180701], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180702], ignore_index=True)

data0514 = data0514.append(raw.loc[raw['dt'] == 20180703], ignore_index=True)
data0514 = data0514.append(raw.loc[raw['dt'] == 20180704], ignore_index=True)
#data0514 = data0514.append(raw2.loc[raw2['dt'] == 20180709], ignore_index=True)
'''


h,w = data0514.shape 


data0514['real_freight_fee']=float(0.0)
data0514['price_ratio']=float(0.0)
#data0514['coupon_radio']=float(1.0)
data0514['xingconfidence']=0
data0514['nameconfidence']=0
data0514['xingmingxiangdeng']=0
data0514['sameaddressprefix']=0
data0514['sameaddressprefix_sameprice']=0.0
data0514['sameaddressprefix_sameIP']=0.0
data0514['sameaddressprefix_sameprice_ratio']=0.0
data0514['sameaddressprefix_sameIP_ratio']=0.0
data0514['register']=0
data0514['sameaddressprefix_similardetail']=0.0
data0514['sameaddressprefix_distinctuser']=0
data0514['sameaddressprefix_userratio'] = 0.0
# data0514['address_detail_zhongwen']=''
data0514['sameaddressprefix_detail_zhongwen'] = 0.0

############################################### 详细地址转关键数字
unit_name=data0514['address_detail']
common_used_numerals_tmp = {u'零': 0, u'一': 1, u'二': 2, u'两': 2, u'三': 3, u'四': 4, u'五': 5, u'六': 6, u'七': 7, u'八': 8, u'九': 9,  
                            u'十': 10, u'百': 100, u'千': 1000, u'万': 10000, u'亿': 100000000}  
common_used_numerals = {}  
for key in common_used_numerals_tmp:  
    common_used_numerals[key] = common_used_numerals_tmp[key]  
  
  
def chinese2digits(uchars_chinese):  
    total = 0  
    r = 1  # 表示单位：个十百千...  
    for i in range(len(uchars_chinese) - 1, -1, -1):  
        val = common_used_numerals.get(uchars_chinese[i])  
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类  
            if val > r:  
                r = val  
                total = total + val  
            else:  
                r = r * val  
                # total =total + r * x  
        elif val >= 10:  
            if val > r:  
                r = val  
            else:  
                r = r * val  
        else:  
            total = total + r * val  
    return total  
  
  
num_str_start_symbol = [u'一', u'二', u'两', u'三', u'四', u'五', u'六', u'七', u'八', u'九',  
                        u'十']  
more_num_str_symbol = [u'零', u'一', u'二', u'两', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'百', u'千', u'万', u'亿']  
  
def changeChineseNumToArab(oriStr):  
    lenStr = len(oriStr);  
    aProStr = ''  
    if lenStr == 0:  
        return aProStr;  
  
    hasNumStart = False;  
    numberStr = ''  
    for idx in range(lenStr):  
        if oriStr[idx] in num_str_start_symbol:  
            if not hasNumStart:  
                hasNumStart = True;  
  
            numberStr += oriStr[idx]  
        else:  
            if hasNumStart:  
                if oriStr[idx] in more_num_str_symbol:  
                    numberStr += oriStr[idx]  
                    continue  
                else:  
                    numResult = str(chinese2digits(numberStr))  
                    numberStr = ''  
                    hasNumStart = False;  
                    aProStr += numResult  
  
            aProStr += oriStr[idx]  
            pass  
  
    if len(numberStr) > 0:  
        resultNum = chinese2digits(numberStr)  
        aProStr += str(resultNum)  
  
    return aProStr  

for i in range(h):
    testStr = unit_name.at[i]
    unit_name.at[i] = changeChineseNumToArab(testStr)
    df0 = unit_name.at[i]
    df1 = df0.encode('gbk')  
    df2 = filter(str.isdigit, df1)
    unit_name.at[i] = df2
    ss=''
    for w in df0:
       if  w>= u'\u4e00' and w<=u'\u9fa5':
           ss+=w
    ss = re.sub("[号+楼+单+元+座+层+院]+".decode("utf8"), "".decode("utf8"),ss)
    data0514.at[i,'address_detail_zhongwen'] = ss


data0514['unit_name'] = unit_name
data0514['unit_name1']=data0514['unit_name']  
data0514.loc[data0514['unit_name'] =='','unit_name1']='empty'  

#################################################################

################################################### 编辑距离

def normal_leven(str1, str2):
      len_str1 = len(str1) + 1
      len_str2 = len(str2) + 1
      #create matrix
      matrix = [0 for n in range(len_str1 * len_str2)]
      #init x axis
      for i in range(len_str1):
          matrix[i] = i
      #init y axis
      for j in range(0, len(matrix), len_str1):
          if j % len_str1 == 0:
              matrix[j] = j // len_str1
          
      for i in range(1, len_str1):
          for j in range(1, len_str2):
              if str1[i-1] == str2[j-1]:
                  cost = 0
              else:
                  cost = 1
              matrix[j*len_str1+i] = min(matrix[(j-1)*len_str1+i]+1,
                                          matrix[j*len_str1+(i-1)]+1,
                                          matrix[(j-1)*len_str1+(i-1)] + cost)
          
      return matrix[-1]

##########################################################


newdata = data0514.values
address_prefix = list(data0514['address_prefix'].values)
heads = data0514.columns.values
sameaddress_dataframe = pd.DataFrame(columns = heads)

for i in range(h):
    
    if data0514.at[i,'register_src'] in (2,3,4,9):                                               #########  转化用户注册来源
        data0514.at[i,'register'] = 1
        
    address_str = data0514.at[i,'address_prefix']                                                #########  同一地址前缀下单量
    data0514.at[i,'sameaddressprefix'] = address_prefix.count(address_str)
    
    price = data0514.at[i,'total_price']
    IP_address = data0514.at[i,'user_ip']
    
    sameaddress_dataframe = sameaddress_dataframe.append(data0514.loc[data0514['address_prefix'] == address_str])
    sameaddress_price = list(sameaddress_dataframe['total_price'].values)
    sameaddress_IP = list(sameaddress_dataframe['user_ip'].values)
    data0514.at[i,'sameaddressprefix_sameprice'] = (sameaddress_price.count(price)-1.0)/float(data0514.at[i,'sameaddressprefix'])
    data0514.at[i,'sameaddressprefix_sameIP'] = sameaddress_IP.count(IP_address)
    data0514.at[i,'sameaddressprefix_sameprice_ratio']=(float(data0514.at[i,'sameaddressprefix_sameprice'])-1.0)/float(data0514.at[i,'sameaddressprefix'])
    data0514.at[i,'sameaddressprefix_sameIP_ratio']=(float(data0514.at[i,'sameaddressprefix_sameIP'])-1.0)/float(data0514.at[i,'sameaddressprefix'])
    
    
    
    
    hh,ww = sameaddress_dataframe.shape                                                         ############  详细地址提取数字相似性计算
    sameaddress_detail = list(sameaddress_dataframe['unit_name1'].values)
    if data0514.at[i,'unit_name1'] != 'empty':
        str1 = data0514.at[i,'unit_name1']
        count = 0.0
        for ii in range(hh):
            str2 = sameaddress_detail[ii]
            bianjidistance = normal_leven(str1,str2)
            similarity = 1 - float(bianjidistance)/max(len(str1),len(str2))
            if similarity >= 0.8:
                count = count + 1
        data0514.at[i,'sameaddressprefix_similardetail'] = (count-1)/float(data0514.at[i,'sameaddressprefix'])
    else:
        data0514.at[i,'sameaddressprefix_similardetail'] = 0
    
    sameaddress_detail_zhongwen = list(sameaddress_dataframe['address_detail_zhongwen'].values)     ############  详细地址中文相似性计算
    if data0514.at[i,'address_detail_zhongwen'] != '':
        str3 = data0514.at[i,'address_detail_zhongwen']
        count1 = 0.0
        for iii in range(hh):
            str4 = sameaddress_detail_zhongwen[iii]
            bianjidistance = normal_leven(str3,str4)
            similarity = 1 - float(bianjidistance)/max(len(str3),len(str4))
            if similarity >= 0.8:
                count1 = count1 + 1
        data0514.at[i,'sameaddressprefix_detail_zhongwen'] = (count1-1)/float(data0514.at[i,'sameaddressprefix'])
    else:
        data0514.at[i,'sameaddressprefix_detail_zhongwen'] = 0
            
    
        
    sameaddress_user = len(set(list(sameaddress_dataframe['webuser_id'])))                      ############  相同地址前缀用户数
    data0514.at[i,'sameaddressprefix_distinctuser'] =  sameaddress_user         
    data0514.at[i,'sameaddressprefix_userratio'] = (float(data0514.at[i,'sameaddressprefix_distinctuser'])-1.0)/float(data0514.at[i,'sameaddressprefix'])
    

    sameaddress_dataframe.drop(sameaddress_dataframe.index,inplace=True)
    
    
    
    
    strname = data0514.at[i,'name']                                                              #########  姓名编码
    if strname[0] in baijiaxing:
        data0514.at[i,'xingconfidence']=1
        if len(strname) ==2 or len(strname) ==3:
            data0514.at[i,'nameconfidence']=1
            if strname[1] != strname[0]:
                data0514.at[i,'xingmingxiangdeng']=1
    
    
    if newdata[i,2]==2:
        data0514.at[i,'my_flag']=0                                                               #########  将疑似项归为 0
    
    
    if newdata[i,9]!=0:
        data0514.at[i,'real_freight_fee']=(float(newdata[i,9])-float(newdata[i,10]))/float(newdata[i,9])      ###添加实际运费占比列
    
    data0514.at[i,'price_ratio']=(float(newdata[i,8])-1999)/1999                                ###添加订单金额超过最低19.99的比例
    #if newdata[i,8]!=0:
        #data0514.at[i,'coupon_radio']=(float(newdata[i,5])/(float(newdata[i,6])-float(newdata[i,7])))

del data0514['catagory_id']

head1 = data0514.columns.values
train = pd.DataFrame(columns = head1)
test = pd.DataFrame(columns = head1)

'''
train = train.append(data0514.loc[data0514['dt'] == 20180514], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180515], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180516], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180517], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180518], ignore_index=True)


train = train.append(data0514.loc[data0514['dt'] == 20180621], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180622], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180623], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180624], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180625], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180626], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180627], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180628], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180629], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180630], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180701], ignore_index=True)
train = train.append(data0514.loc[data0514['dt'] == 20180702], ignore_index=True)

test = test.append(data0514.loc[data0514['dt'] == 20180703], ignore_index=True)
test = test.append(data0514.loc[data0514['dt'] == 20180704], ignore_index=True)




train.drop(['dt','id','coupon_code','validdays','address_prefix','address_detail','phone','name','deviceid','webuser_id','user_ip','register_src','birthday','id_type',
               'id_no','longitude','latitude','sameaddressprefix','use_coupon','total_price','promotion_price',
               'order_price','total_freight_fee','discount_freight_fee','ware_num','ware_weight','sku_cnt','sameaddressprefix_sameIP',
               'sameaddressprefix_sameprice','unit_name','unit_name1','sameaddressprefix_distinctuser','sameaddressprefix_sameprice_ratio',
               'address_detail_zhongwen','sameaddressprefix_detail_zhongwen'],axis=1,inplace=True)

test.drop(['dt','id','coupon_code','validdays','address_prefix','address_detail','phone','name','deviceid','webuser_id','user_ip','register_src','birthday','id_type',
               'id_no','longitude','latitude','sameaddressprefix','use_coupon','total_price','promotion_price',
               'order_price','total_freight_fee','discount_freight_fee','ware_num','ware_weight','sku_cnt','sameaddressprefix_sameIP',
               'sameaddressprefix_sameprice','unit_name','unit_name1','sameaddressprefix_distinctuser','sameaddressprefix_sameprice_ratio',
               'address_detail_zhongwen','sameaddressprefix_detail_zhongwen'],axis=1,inplace=True)
    
train.to_csv("D:\\dataset\\0718\\test\\0621-0702.csv")
test.to_csv("D:\\dataset\\0718\\test\\0703-0704.csv")
'''

data0514.drop(['dt','id','coupon_code','validdays','address_prefix','address_detail','phone','name','deviceid','webuser_id','user_ip','register_src','birthday','id_type',
               'id_no','longitude','latitude','sameaddressprefix','use_coupon','total_price','promotion_price',
               'order_price','total_freight_fee','discount_freight_fee','ware_num','ware_weight','sku_cnt','sameaddressprefix_sameIP',
               'sameaddressprefix_sameprice','unit_name','unit_name1','sameaddressprefix_distinctuser','sameaddressprefix_sameprice_ratio',
               'address_detail_zhongwen','model_result','model_coupon_type','input_tag','output_tag','order_create_time'],axis=1,inplace=True)
    
data0514.to_csv(u"D:\\dataset\\0726\\0711-0720送入模型数据new.csv")



