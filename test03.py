import time

a = "2018/06/25 0:00:18.0"
b = "2018/06/25 0:00:40.0"
a = a[0:-2]
b = b[0:-2]

# 转换为本地时间
a1 = time.strptime(a, "%Y/%m/%d %H:%M:%S")
b1 = time.strptime(b, "%Y/%m/%d %H:%M:%S")

print(a)
print(a1)
print(b)
print(b1)

# 转换为时间戳
a2 = time.mktime(a1)
b2 = time.mktime(b1)

c = a2 + ((b2 - a2) / 2)
c1 = time.localtime(c)
print(c)
print(c1)

c2 = time.strftime("%Y/%m/%d %H:%M:%S", c1)
print(c2)
