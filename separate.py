# coding:utf-8
import jieba

print('主程序执行开始...')

input_file_name = 'wiki.cn.simple.txt'
output_file_name = 'wiki.cn.simple.separate.txt'
input_file = open(input_file_name, 'r', encoding='utf-8')
output_file = open(output_file_name, 'w', encoding='utf-8')

print('开始读入数据文件...')
lines = input_file.readlines()
print('读入数据文件结束！')

print('分词程序执行开始...')
count = 1
for line in lines:
    # jieba分词的结果是一个list，需要拼接，但是jieba把空格回车都当成一个字符处理
    output_file.write(' '.join(jieba.cut(line.split('\n')[0].replace(' ', ''))) + '\n')
    count += 1
    if count % 10000 == 0:
        print('目前已分词%d条数据' % count)
print('分词程序执行结束！')

print('主程序执行结束！')
