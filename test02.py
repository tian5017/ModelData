# 二分查找法
def binary_search(list, item):
    low = 0
    high = len(list) - 1

    i = 0
    while low <= high:
        i += 1
        mid = (low + high) // 2
        guess = list[mid]
        if guess == item:
            return mid, i
        if guess > item:
            high = mid - 1
        else:
            low = mid + 1
    return -1, -1


test_list = [x for x in range(256)]
test_item = 256
a, b = binary_search(test_list, test_item)
if a == -1 and b == -1:
    print(test_item, "在数组中不存在")
else:
    print(test_item, "在数组中的位置索引为：", a, "，总共查找了：", b, "次")