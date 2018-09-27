# -*- coding: utf-8 -*-
import gensim
import jieba


def m_1(model):
    # 得到相似词和相似程度
    result = model.most_similar("罗亚")
    print("罗亚的近义词有：")
    for word in result:
        print(word[0], word[1])

    # # 得到一组词中最无关的词
    # print("--------------------------------------")
    # list4 = ["汽车", "火车", "飞机", "北京"]
    # print(model.doesnt_match(list4))
    #
    # # 得到两组词的相似度
    # print("--------------------------------------")
    # list1 = ["警察", "生活", "无聊"]
    # list2 = ["警员", "快乐"]
    # list3 = ["电力"]
    # list_sim1 = model.n_similarity(list1, list2)
    # print(list_sim1)
    # list_sim2 = model.n_similarity(list2, list3)
    # print(list_sim2)


def m_2(model):
    # 得到两组词的相似度
    print("--------------------------------------")
    list1 = ['北京市', '昌平区', '华龙', '苑', '北', '里', '二', '号', '楼', '二', '单元', '五', '零', '一']
    list2 = ['北京市', '昌平区', '华龙', '苑', '北', '里', '一', '号', '楼', '四', '单元']
    list_sim1 = model.n_similarity(list1, list2)
    print(list_sim1)


# 将字符串中的阿拉伯数字转换为汉字数字
# 去掉停用词
def num2word(str):
    s = ""
    numerals_tmp1 = {0: "零", 1: "一", 2: "二", 3: "三", 4: "四", 5: "五", 6: "六", 7: "七", 8: "八", 9: "九"}
    numerals_tmp2 = {"〇": "零", "A": "一", "B": "二", "C": "三", "D": "四", "E": "五", "F": "六", "G": "七", "H": "八", "I": "九", "J": "一零",
                     "K": "一一", "L": "一二", "M": "一三", "N": "一四", "O": "一五", "P": "一六", "Q": "一七", "R": "一八", "S": "一九", "T": "二零",
                     "U": "二一", "V": "二二", "W": "二三", "X": "二四", "Y": "二五", "Z": "二六"}
    stop_words = "-,，.。、/、()（） "
    for i in str:
        if i in stop_words:
            pass
        else:
            if i.isdigit():
                s += numerals_tmp1[int(i)]
            elif i in list(numerals_tmp2.keys()):
                s += numerals_tmp2[i]
            else:
                s += i

    return s


def m_3(model):
    print("--------------------------------------")
    s1 = "北京市 朝阳区 芍药居北里210号楼 2669"
    s2 = "北京市 朝阳区 芍药居北里210号楼 2778"
    s1 = num2word(s1)
    s2 = num2word(s2)
    sl_1 = jieba.lcut(s1, HMM=False)
    print(sl_1)
    sl_2 = jieba.lcut(s2, HMM=False)
    print(sl_2)

    sl_diff = model.n_similarity(sl_1, sl_2)
    print(sl_diff)



if __name__ == "__main__":
    # 加载模型
    # model = None
    model = gensim.models.KeyedVectors.load_word2vec_format("model/test.bin", binary=True)
    m_1(model)

