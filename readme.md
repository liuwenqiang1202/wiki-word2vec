之前做过一些自然语言处理的工作，主要是根据一些企业在互联网上的相关新闻进行分析，对其倾向性进行判断，最终目的是辅助国内某单位更好地对其管辖的企业进行监管工作。现在总结整理一下。这篇文章主要对**词向量训练阶段**进行阐述。（所有代码见我的Github）

---

## 数据获取
使用的语料库是wiki百科的中文语料库，下载地址：https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2。另外，提供百度网盘下载链接：https://pan.baidu.com/s/1eLkybiYOE_aVxsN0pALATg，提取码为：hmtn。

下载之后如下图（PyCharm截图），大小为1.16GB。

![zhwiki-latest-pages-articles.xml.bz2](https://upload-images.jianshu.io/upload_images/11579422-186c2888dab99f7c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

## 将xml格式数据转为txt
因为原始文件是xml格式，并且是压缩文件，所以做了一步数据解压并进行格式转换的工作。
具体使用了gensim库中的维基百科处理类WikiCorpus，该类中的get_texts方法原文件中的文章转化为一个数组，其中每一个元素对应着原文件中的一篇文章。然后通过for循环便可以将其中的每一篇文章读出，然后进行保存。

![xml2txt.py](https://upload-images.jianshu.io/upload_images/11579422-2eea76b4928478ae.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
# coding; utf-8
"""
这个代码是将从网络上下载的xml格式的wiki百科训练语料转为txt格式
wiki百科训练语料
    链接：https://pan.baidu.com/s/1eLkybiYOE_aVxsN0pALATg
    密码：hmtn
"""

from gensim.corpora import WikiCorpus

if __name__ == '__main__':

    print('主程序开始...')

    input_file_name = 'zhwiki-latest-pages-articles.xml.bz2'
    output_file_name = 'wiki.cn.txt'
    print('开始读入wiki数据...')
    input_file = WikiCorpus(input_file_name, lemmatize=False, dictionary={})
    print('wiki数据读入完成！')
    output_file = open(output_file_name, 'w', encoding="utf-8")

    print('处理程序开始...')
    count = 0
    for text in input_file.get_texts():
        output_file.write(' '.join(text) + '\n')
        count = count + 1
        if count % 10000 == 0:
            print('目前已处理%d条数据' % count)
    print('处理程序结束！')

    output_file.close()
    print('主程序结束！')
```

结果文件截图：

![wiki.cn.txt](https://upload-images.jianshu.io/upload_images/11579422-a67e13e691a2a5c8.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![xml2txt-result](https://upload-images.jianshu.io/upload_images/11579422-8b06a73f3adf188e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

## 繁体转为简体
为了方便后期处理，接下来对上面的结果进行简体化处理，将所有的繁体全部转化为简体。在这里，使用了另外一个库zhconv。对上面结果的每一行调用convert函数即可。

![tradition2simple.py](https://upload-images.jianshu.io/upload_images/11579422-a2affe683a8998df.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
# coding:utf-8
import zhconv

print('主程序执行开始...')

input_file_name = 'wiki.cn.txt'
output_file_name = 'wiki.cn.simple.txt'
input_file = open(input_file_name, 'r', encoding='utf-8')
output_file = open(output_file_name, 'w', encoding='utf-8')

print('开始读入繁体文件...')
lines = input_file.readlines()
print('读入繁体文件结束！')

print('转换程序执行开始...')
count = 1
for line in lines:
    output_file.write(zhconv.convert(line, 'zh-hans'))
    count += 1
    if count % 10000 == 0:
        print('目前已转换%d条数据' % count)
print('转换程序执行结束！')

print('主程序执行结束！')
```

结果截图：

![wiki.cn.simple.txt](https://upload-images.jianshu.io/upload_images/11579422-95fcddafa5a4be48.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![tradition2simple-result](https://upload-images.jianshu.io/upload_images/11579422-15e69c3d38423539.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

## 分词
对于中文来说，分词是必须要经过的一步处理，下面就需要进行分词操作。在这里使用了大名鼎鼎的jieba库。调用其中的cut方法即可。

![separate.py](https://upload-images.jianshu.io/upload_images/11579422-e16d06c115bb039e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
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
```

结果截图：

![wiki.cn.simple.seprate.txt](https://upload-images.jianshu.io/upload_images/11579422-ff07ff6f7ba8775b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![separate-result](https://upload-images.jianshu.io/upload_images/11579422-cfd18e1ef400d9d9.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

## 去除非中文词
可以看到，经过上面的处理之后，现在的结果已经差不多了，但是还存在着一些非中文词，所以下一步便将这些词去除。具体做法是通过正则表达式判断每一个词是不是符合汉字开头、汉字结尾、中间全是汉字，即“**^[\u4e00-\u9fa5]+$**”。

![remove.py](https://upload-images.jianshu.io/upload_images/11579422-04fd2508db80f17d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
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

print('分词程序执行开始...')
count = 1
cn_reg = '^[\u4e00-\u9fa5]+$'

for line in lines:
    line_list = line.split('\n')[0].split(' ')
    line_list_new = []
    for word in line_list:
        if re.search(cn_reg, word):
            line_list_new.append(word)
    print(line_list_new)
    output_file.write(' '.join(line_list_new) + '\n')
    count += 1
    if count % 10000 == 0:
        print('目前已分词%d条数据' % count)
print('分词程序执行结束！')

print('主程序执行结束！')
```

结果截图：

![wiki.txt](https://upload-images.jianshu.io/upload_images/11579422-989b5cf02ee59995.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

![remove-result](https://upload-images.jianshu.io/upload_images/11579422-3e6ebef3f9b15d46.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

## 词向量训练
上面的工作主要是对wiki语料库进行数据预处理，接下来才真正的词向量训练。

![word2vec.py](https://upload-images.jianshu.io/upload_images/11579422-976b344b74ec1836.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

```
# coding:utf-8
import multiprocessing
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence

if __name__ == "__main__":
    print('主程序开始执行...')

    input_file_name = 'wiki.txt'
    model_file_name = 'wiki.model'

    print('转换过程开始...')
    model = Word2Vec(LineSentence(input_file_name),
                     size=400,  # 词向量长度为400
                     window=5,
                     min_count=5,
                     workers=multiprocessing.cpu_count())
    print('转换过程结束！')

    print('开始保存模型...')
    model.save(model_file_name)
    print('模型保存结束！')

    print('主程序执行结束！')
```

也是使用了gensim库，通过其中的Word2Vec类进行了模型训练，并将最终的词向量保存起来。

![wiki.model](https://upload-images.jianshu.io/upload_images/11579422-fd2532d8da28f433.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

---

> **参考文献：**
> [1]. wiki中文语料库, https://dumps.wikimedia.org/zhwiki/latest/zhwiki-latest-pages-articles.xml.bz2.
> [2]. 使用 word2vec 训练wiki中英文语料库, https://www.jianshu.com/p/05800a28c5e4.
> [3]. 中英文维基百科语料上的Word2Vec实验, http://www.52nlp.cn/%E4%B8%AD%E8%8B%B1%E6%96%87%E7%BB%B4%E5%9F%BA%E7%99%BE%E7%A7%91%E8%AF%AD%E6%96%99%E4%B8%8A%E7%9A%84word2vec%E5%AE%9E%E9%AA%8C.

---

> 作者原创，如需转载及其他问题请邮箱联系：lwqiang_chn@163.com。
> 个人网站：https://www.myqiang.top。
> GitHub：https://github.com/liuwenqiang1202。