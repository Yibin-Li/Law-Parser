import csv
from pyhanlp import *
import pickle
import pandas as pd
import time
from jpype import *
import pickle


filename = 'OGI2016_noduplicate_winloss.csv'
#filename = '/Users/wuxiaohan/Desktop/UCSC_database_project/data/test_data.csv'
pos_list = ['an','g','gb','gbc','gc','gg','gi','gm','gp','i','j','l','n','nb',\
            'nba','nbc','nbp','nf','ng','nh','nhd','nhm','ni','nic','nis','nit'\
            'nl','nm','nmc','nn','nnd','nnt','nt','ntc','nto','nz','vn']
stopword = ['原告','被告','汉族','判决书','判决','法院','当事人','审判长','审判员',\
            '人民陪审员','代理审判员','书记员','对方','当事人','人数','副本','案件'\
            '被告方','代表人','终字','原被告','。案','上诉人','确认','法>']

##read file
texts = pd.read_csv(filename)
ids = list(texts['id'])
category = list(texts['category'])
facts = list(texts['facts'])
# with open(filename) as csvfile:
#     reader = csv.reader(csvfile)
#     next(reader)
#     ids=[]
#     facts = []
#     for item in reader:
#         ids.append(item[0])
#         facts.append(item[19])
#     csvfile.close()


##remove spaces tab \n
def cleaning(files):
    for i in range(len(files)):
        files[i] = files[i].replace(' ','').replace('　','').replace('\n','')
    return files

facts = cleaning(facts)
print('cleaning done')

# """ 演示用户词典的动态增删
    # TO-DO:
    # DoubleArrayTrie分词
    # 首字哈希之后二分的trie树分词
    # >>> text = "攻城狮逆袭单身狗，迎娶白富美，走上人生巅峰"
    # >>> demo_custom_dictionary(text)
    # [攻城/vi, 狮/ng, 逆袭/nz, 单身/n, 狗/n, ，/w, 迎娶/v, 白富美/nr, ，/w, 走上/v, 人生/n, 巅峰/n]
    # [攻城狮/nz, 逆袭/nz, 单身狗/nz, ，/w, 迎娶/v, 白富美/nz, ，/w, 走上/v, 人生/n, 巅峰/n]
    # """
    #print(HanLP.segment(text))

    # CustomDictionary.insert(newphrase, "nz 1024")  # 动态增加
    #CustomDictionary.insert("白富美", "nz 1024")  # 强行插入
    #CustomDictionary.remove("攻城狮") # 删除词语（注释掉试试）
    #CustomDictionary.add("单身狗", "nz 1024 n 1")
    #CustomDictionary.remove("单身狗")  # 删除词语（注释掉试试）
    #CustomDictionary.remove("白富美")  # 删除词语（注释掉试试）
    #print(CustomDictionary.get("单身狗"))

# CustomDictionary.insert("审判委员会", "nz 1024") #其他名词

# """ NLP分词，更精准的中文分词、词性标注与命名实体识别
#         标注集请查阅 https://github.com/hankcs/HanLP/blob/master/data/dictionary/other/TagPKU98.csv
#         或者干脆调用 Sentence#translateLabels() 转为中文
#     #>>> demo_NLP_segment()
#     [我/r, 新造/v, 一个/m, 词/n, 叫/v, 幻想乡/ns, 你/r, 能/v, 识别/v, 并/c, 正确/ad, 标注/v, 词性/n, 吗/y, ？/w]
#     我/代词 的/助词 希望/名词 是/动词 希望/动词 张晚霞/人名 的/助词 背影/名词 被/介词 晚霞/名词 映/动词 红/形容词
#     支援/v 臺灣/ns 正體/n 香港/ns 繁體/n ：/w [微软/nt 公司/n]/nt 於/p 1975年/t 由/p 比爾·蓋茲/n 和/c 保羅·艾倫/nr 創立/v 。/w
#     """
# print(NLPTokenizer.segment("我新造一个词叫幻想乡你能识别并正确标注词性吗？"))  # “正确”是副形词。
# 注意观察下面两个“希望”的词性、两个“晚霞”的词性
# print(NLPTokenizer.analyze("我的希望是希望张晚霞的背影被晚霞映红").translateLabels())
# print(NLPTokenizer.analyze("支援臺灣正體香港繁體：微软公司於1975年由比爾·蓋茲和保羅·艾倫創立。"))
start = time.clock()

# Run segmentation in JVM
startJVM(getDefaultJVMPath(), "-ea", "-Djava.class.path=/anaconda3/lib/python3.7/site-packages/pyhanlp/static/hanlp-portable-1.6.0.jar")
NLPTokenizer = JClass("com.hankcs.hanlp.tokenizer.NLPTokenizer")
segmentedText = []
segmentedPOS = []
for i in range(len(facts)):
# for i in range(10):
    textSegments = []
    posSegments = []
    for segment in NLPTokenizer.segment(facts[i]):
        # split on the last occurence of '/'
        word, pos = str(segment).rsplit('/',1)
        textSegments.append(word)
        posSegments.append(pos)
    segmentedText.append(textSegments)
    segmentedPOS.append(posSegments)
    if i%100 == 0:
        print(i,'files done, time used:{}'.format(time.clock()-start))
print('segmentation done')
shutdownJVM()
# Shutdown JVM

d = {'id': ids, 'segmentedText': segmentedText, 'segmentedPOS':segmentedPOS, 'category':category}
out_list = pd.DataFrame(data=d)
out_list.to_pickle('All_OGI_segmented_facts.pickle')

# out_list.to_csv('All_OGI_segmented_facts.csv')

# out_list = []
# for item in segmented:
#     noun_list = []
#     for file in item:
#         if str(file.nature) in pos_list and len(file.word) > 1 and file.word not in stopword:
#             noun_list.append(file.word)
#     out_list.append(noun_list)
# print('Selected nouns, remove stopwords')
#
# all_stems = sum(out_list, [])
# stems_once = set(stem for stem in set(all_stems) if all_stems.count(stem) < 5)
# texts = [[stem for stem in text if stem not in stems_once] for text in out_list]
# print(texts[0])
# filehandler = open("/Users/wuxiaohan/Desktop/2019SpringRaWork/All_OGI/All_OGI_segmented","wb")
# pickle.dump(out_list,filehandler)
# filehandler.close()

# test=''
# for item in res:
#     test = test+item
# print(HanLP.extractPhrase(test,20))
# print(CustomDictionary.get("审判委员会"))
