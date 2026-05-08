# -*- coding:utf-8 -*-
import pandas as pd
import jieba

#基于BosonNLP情感词典计算情感值
def getscore(text):
    global key, score, stopwords
    #删除停用词
    for x in stopwords:
        if x in text:
            text = text.strip(x)
    # jieba分词
    segs = jieba.lcut(text,cut_all = False) #返回list
    # 计算得分
    score_list = []
    for x in segs:
        if x in key:
            score_list.append(score[key.index(x)])
    return sum(score_list)


if __name__=='__main__':
    #载入词典
    BosonNLP_dict = pd.read_table(r"BosonNLP_dict\BosonNLP_sentiment_score.txt", sep=" ", names=['key', 'score'])
    key = BosonNLP_dict['key'].values.tolist()
    score = BosonNLP_dict['score'].values.tolist()
    #载入停用词
    stopwords = open(r"BosonNLP_dict\baidu_stopwords.txt", 'r', encoding = 'utf-8').read().split('\n')
    #载入文本
    df = pd.read_excel("test_data/99.xlsx")
    df['情感得分'] = ''
    df['情感倾向'] = ''

    #计算情感值并标记
    for i in range(len(df)):
        print(df.loc[i, '评论'])
        text_score = getscore(df.loc[i, '评论'])
        print("情感值：", round(text_score, 5))
        df.loc[i, '情感得分'] = round(text_score, 5)
        if text_score<0:
            print('机器标注情感倾向：消极\n')
            df.loc[i, '情感倾向'] = '消极'
        else:
            print('机器标注情感倾向：积极\n')
            df.loc[i, '情感倾向'] = '积极'

    #写出分析结果
    df.to_excel("result_data/情感分析结果.xlsx")
