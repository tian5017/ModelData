import jieba
import jieba.analyse as ans
import nltk
import numpy as np


def t_1():
    seg_list = jieba.cut("今天天气很不错,今天天气很差")
    seg_list = [i for i in seg_list]

    print(seg_list)

    cfd = nltk.FreqDist(seg_list)
    print(dict(cfd))
    print(list(cfd.values()))

def t_2():
    aa = []
    bb = []
    s = "我来到北京清华大学"
    for x, w in ans.extract_tags(s, withWeight=True):
        aa.append(x + "  " + str(w))
    print(aa)

    for x, w in ans.textrank(s, withWeight=True):
        bb.append(x + "  " + str(w))
    print("----------------------------")
    print(bb)


def t_3():
    s1 = "北京市昌平区华龙苑北里2号楼二单元501"
    s2 = "北京市昌平区华龙苑北里1号楼4单元"

    sl_1 = jieba.cut(s1)
    sl_1 = [i for i in sl_1]
    cfd_1 = nltk.FreqDist(sl_1)
    # 词频向量
    w_arr_1 = list(cfd_1.values())
    sl_2 = jieba.cut(s2)
    sl_2 = [i for i in sl_2]
    cfd_2 = nltk.FreqDist(sl_2)
    # 词频向量
    w_arr_2 = list(cfd_2.values())

    m_k = max(len(w_arr_1), len(w_arr_2))
    if len(w_arr_1) < m_k:
        for i in range(m_k - len(w_arr_1)):
            w_arr_1.append(0)
    if len(w_arr_2) < m_k:
        for i in range(m_k - len(w_arr_2)):
            w_arr_2.append(0)

    w_arr_1 = np.array(w_arr_1)
    w_arr_2 = np.array(w_arr_2)
    print(w_arr_1)
    print(w_arr_2)

    num = float(np.dot(w_arr_1.T, w_arr_2))
    denom = np.linalg.norm(w_arr_1) * np.linalg.norm(w_arr_2)
    # 余弦相似度
    cos = num / denom
    # 归一化
    sim = 0.5 + 0.5 * cos
    print(sim)



if __name__ == "__main__":
    t_3()

