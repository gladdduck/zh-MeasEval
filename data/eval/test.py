import os


ori_list = os.listdir('text')
new_list = os.listdir('zh-text')

ori_list.sort()
new_list.sort()

for i in range(len(ori_list)):
    if ori_list[i] != new_list[i]:
        print(ori_list[i], new_list[i])
        break
