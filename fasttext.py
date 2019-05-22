# coding:utf-8
import multiprocessing
from gensim.models import FastText
from gensim.models.word2vec import LineSentence

if __name__ == "__main__":
    print('主程序开始执行...')

    input_file_name = 'wiki.txt'
    model_file_name = 'wiki.model.fasttext'

    print('转换过程开始...')
    model = FastText(LineSentence(input_file_name),
                     size=100,  # 词向量长度为100
                     window=5,
                     min_count=5,
                     workers=multiprocessing.cpu_count())
    print('转换过程结束！')

    print('开始保存模型...')
    model.save(model_file_name)
    print('模型保存结束！')

    print('主程序执行结束！')
