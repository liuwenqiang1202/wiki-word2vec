# coding:utf-8
import re
import gensim
import jieba.analyse

print('主程序开始...')

print('读取word2vec...')
word2vec = gensim.models.Word2Vec.load('wiki.model')
print('读取word2vec结束！')

print('读取停用词...')
stopwords = []
for word in open('stopwords.txt', 'r', encoding='utf-8'):
    if word.strip():
        stopwords.append(word.strip())
jieba.analyse.set_stop_words('stopwords.txt')
print(stopwords)
print('停用词读取结束！')

print('读取正向词...')
positives = []
for word in open('positive.txt', 'r', encoding='utf-8'):
    if word.strip():
        positives.append(word.strip())
print(positives)
print('正向词读取结束！')

print('读取负向词...')
negatives = []
for word in open('negative.txt', 'r', encoding='utf-8'):
    if word.strip():
        negatives.append(word.strip())
print(negatives)
print('负向词读取结束！')

print('加载自定义词库...')
jieba.load_userdict('dict.txt')
print('自定义词库加载结束！')

print('关键词抽取...')
title = '天津武清的三星工厂疑似发生火灾'
content = '昨天，位于天津武清的三星工厂冒出滚滚浓烟，疑似发生火灾。\n三星方面回应称，目前已确认发生火灾的工厂为天津三星视界有限公司，初步推断是堆放废弃物的地方着火。\n昨天早上，有网友拍摄视频爆料位于天津武清的三星工厂冒出滚滚浓烟，疑似发生火灾。随后，天津消防武清支队发布公告称，起火的是三星视界有限公司，起火物质为生产车间内锂电池及部分半成品，现场已经报灭，无人员伤亡。不过这一消息随后被删除。三星方面表示，“锂电池起火”这一说法并不准确，初步推断是堆放废弃物的地方着火，具体原因和损失还在调查之中。消防称三星工厂内锂电池起火网友爆料的视频及图片显示，昨天早上，位于天津市武清区的三星工厂内冒出滚滚浓烟，数公里外的居民楼可见浓烟。视频中有网友介绍称，此前有过一波大的浓烟，后来减弱，不过随后浓烟又增大。由于网友多是远距离拍摄，因此从视频中无法确定火势及具体起火点。\n昨天下午15时许，天津市武清公安局公安消防支队证实了起火位置是位于天津市武清区开发区庆龄大道的三星视界有限公司的生产车间。武清消防支队称，起火物质是车间内锂电池及部分半成品。武清消防支队表示，起火时间为2月8日早上6时许，截止到昨天下午15时，现场已经报灭，正在组织排烟，无人员伤亡。此次火灾武清消防支队共出动19部消防车及110余名消防官兵前往现场处置。昨天晚间，天津市公安局武清分局发布消息，称2017年2月8日6时17分许，坐落于武清区的天津三星视界有限公司一废弃品仓库发生火灾。接到报警后，公安消防和属地武清分局警力迅速赶到现场，展开处置工作。7时55分火被扑灭，无人员伤亡，起火原因正在调查中。'
keywords = jieba.analyse.textrank(content, topK=10, withWeight=True, allowPOS=('nt', 'ns', 'n', 'vn', 'v'))
print(keywords)
print('关键词抽取结束！')

print('分句处理...')
contents = re.split(u'。|\n', content)
contents = filter(lambda s: (s if s != '' else None), contents)
contents = list(contents)
print(contents)
print('分句处理结束！')

print('停用词去除...')
contents.append(title)
results = []
for content in contents:
    seg = jieba.cut(content)
    results.append([])
    for c in seg:
        if c.strip() != '' and c not in stopwords:
            results[-1].append(c)
contents = results[:-1]
title = results[-1]
print(contents)
print('停用词去除结束！')

print('关键句抽取...')
sims = []
for i in range(len(contents)):
    content = contents[i]
    content_sim = 0
    for word in content:
        max_sim = 0
        for keyword in keywords:
            try:
                temp_sim = word2vec.similarity(word, keyword[0])
                if temp_sim > max_sim:
                    max_sim = temp_sim
                content_sim += max_sim * float(keyword[1])
            except:
                continue
    sims.append([content_sim / len(content), content])
sims.sort(key=(lambda x: x[0]), reverse=True)
key_contents = [title, sims[0][1], sims[1][1]]
print(key_contents)
print('关键句抽取结束！')

print('倾向性判断...')
orientations = []
for content in key_contents:
    pos_num = 0
    pos_value = 0
    neg_num = 0
    neg_value = 0
    for word in content:
        neg = 0
        pos = 0
        for positive in positives:
            try:
                temp = word2vec.similarity(word, positive)
                if temp > pos:
                    pos = temp
            except:
                continue
        for negative in negatives:
            try:
                temp = word2vec.similarity(word, negative)
                if temp > neg:
                    neg = temp
            except:
                continue
        if pos > neg and pos > 0.5:
            pos_num += 1
            pos_value += pos
        if neg > pos and neg > 0.5:
            neg_num += 1
            neg_value += neg
    pos_ave = (pos_value / pos_num) if pos_num != 0 else 0
    neg_ave = (neg_value / neg_num) if neg_num != 0 else 0
    orientations.append(pos_ave if pos_ave > neg_ave else -neg_ave)
print(orientations)
pos_num = 0
pos_sum = 0
neg_num = 0
neg_sum = 0
for orientation in orientations:
    if orientation > 0:
        pos_num += 1
        pos_sum += orientation
    else:
        neg_num += 1
        neg_sum += orientation
pos_orientation = pos_sum / pos_num if pos_num != 0 else 0
neg_orientation = neg_sum / neg_num if neg_num != 0 else 0
print('%lf' % (pos_orientation if pos_orientation > -neg_orientation else neg_orientation))
print('倾向性判断结束!')
