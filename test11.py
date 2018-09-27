import os


fs = os.listdir("data/test")
for i in range(len(fs)):
    print(fs[i])
    file_path = "data/test/" + fs[i]
    fr_lines = open(file_path, "r", encoding="utf-8").readlines()
    print(len(fr_lines))
    a = 1
    if i == 0:
        a = 0
    with open("data/abcde.csv", "a+", encoding="utf-8") as aa:
        for x in range(a, len(fr_lines)):
            aa.write(fr_lines[x])
print("合并完毕")
