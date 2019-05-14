# coding:utf-8
import re

print('主程序执行开始...')

input_file_name = 'wiki.cn.simple.separate.txt'
output_file_name = 'wiki.txt'
input_file = open(input_file_name, 'r', encoding='utf-8')
output_file = open(output_file_name, 'w', encoding='utf-8')

print('开始读入数据文件...')
lines = input_file.readlines()
print('读入数据文件结束！')

print('正则程序执行开始...')
count = 1
cn_reg = '^[\u4e00-\u9fa5]+$'

for line in lines:
    line_list = line.split('\n')[0].split(' ')
    line_list_new = []
    for word in line_list:
        if re.search(cn_reg, word):
            line_list_new.append(word)
    # print(line_list_new)
    output_file.write(' '.join(line_list_new) + '\n')
    count += 1
    if count % 10000 == 0:
        print('目前已正则%d条数据' % count)
print('正则程序执行结束！')

print('主程序执行结束！')
