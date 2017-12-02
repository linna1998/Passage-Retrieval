#encoding=utf-8

from zhcnSegment import *
from fileObject import FileObj
from sentenceSimilarity import SentenceSimilarity
from sentence import Sentence

def ReadFile(articlename, questionname, keywordsname):
    f1 = open(articlename, 'r')
    list_ret = list()
    for f_line in f1.readlines():   
        f_line = f_line.strip('\n')          
        f_line = f_line.split('。')
        for s_str in  f_line:
            if '？' in s_str:
                list_ret.extend(s_str.split('？'))
            elif '！' in s_str:
                list_ret.extend(s_str.split('！'))           
            else:
                list_ret.append(s_str)                              
    f1.close()

    #读入一个问题
    f2 = open(questionname, 'r')    
    for f_line in f2.readlines():      
        f_line = f_line.strip('\n')               
        ques_ret = f_line
    f2.close()

    #读入关键字
    f3 = open(keywordsname, 'r')   
    key_ret = list() 
    for f_line in f3.readlines():   
        f_line = f_line.strip('\n')         
        key_ret.append(f_line)
    f3.close()
    return list_ret, ques_ret, key_ret  

def WriteFile(file, content):
    f = open(file, "w")
    for line in content:
        print(line, file = f)
    return 233333

print("Passage retrieval begins!")
#输入的接口
#question = "阿根廷国家足球队赢得过多少次美洲杯冠军"
#list_keyword = ["阿根廷", "国家", "足球队", "美洲杯", "冠军"]
list_sentence, question, list_keyword = ReadFile('article.txt', 'question.txt', 'keywords.txt')    

#选出包含关键字的句子，放入important_sentence
important_sentence = [] 
for sentence in list_sentence:
    for key in list_keyword:
        if key in sentence:            
            important_sentence.append(sentence)            
            break

#对 important_sentence中的句子，和问题计算相似度

#读入训练集
#TODO: 
#现在的训练集是原来的wiki内容 + 问题 ，后面改一下训练集？
train_sentence = list_sentence
train_sentence.append(question)   
#构造测试集
test_sentence = important_sentence

# 分词工具，基于jieba分词加了一次封装，主要是去除停用词
seg = Seg()

# 训练模型
ss = SentenceSimilarity(seg)
ss.set_sentences(train_sentence)
#ss.TfidfModel()         # tfidf模型
ss.LsiModel()         # lsi模型
#ss.LdaModel()         # lda模型

# 测试与问题的相似度
score_sentence = []   
for i in range(0,len(test_sentence)):
    score = ss.MYsimilarity(question, test_sentence[i])   
    score_sentence.append(score)    

#输出到文件
WriteFile("sentence.txt", important_sentence)
WriteFile("score.txt", score_sentence)

print("Passage retrieval ends!")