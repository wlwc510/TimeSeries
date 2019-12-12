import jieba
import os
import json

# text = "我来到北京清华大学"
# seg_list = jieba.cut(text, cut_all=True)
# print("[全模式]: ", "/ ".join(seg_list))
#
# # 精确模式
# seg_list = jieba.cut(text, cut_all=False)
# print("[精确模式]: ", "/ ".join(seg_list))
#
# # 默认是精确模式
# seg_list = jieba.cut(text)
# print("[默认模式]: ", "/ ".join(seg_list))
#
# # 新词识别 “杭研”并没有在词典中,但是也被Viterbi算法识别出来了
# seg_list = jieba.cut("他来到了网易杭研大厦")
# print("[新词识别]: ", "/ ".join(seg_list))
#
# # 搜索引擎模式
# seg_list = jieba.cut_for_search(text)
# print("[搜索引擎模式]: ", "/ ".join(seg_list))

#获得文档内容
rootdir=["D:/publications/preparing/00blockchain/区块链政策整理140个"]

rootdirCate=[]

c = []
# cdir=[]

for i in rootdir:  # 定义函数，查找所有文件

    for parent, dirnames, filenames in os.walk(i):

        for dirname in dirnames:

            rootdirCate.append(os.path.join(parent, dirname))

for j in rootdirCate:  # 定义函数，查找所有文件

    cate=[]

    for parent, dirnames, filenames in os.walk(j):

        for filename in filenames:

            if filename.endswith(".txt"):

                cate.append(os.path.join(parent, filename))

        print(str(cate))

    c.append(cate)

txt=[]

for onec in c:

    txtone=""

    for loc in onec:

        try:

            with open(loc, "r") as f:

                cu=f.read()

                # cu=cu.replace("\n","")

                cu=cu.replace(" ","")

                txtone+=cu

                # print(cu)

                f.close()

        except:

            print("出错")
    # 加上换行
    # txtone+="\n"

    txt.append(txtone)

print("应该总共有30行",str(len(txt)))

# data=open("D:/publications/preparing/00blockchain/data/policydata.txt", 'w+')
#
# print(txt,file=data)
#
# data.close()

dataraw=open("D:/publications/preparing/00blockchain/data/policydata.txt", 'w+')

print(txt,file=dataraw)

dataraw.close()

datalines=open("D:/publications/preparing/00blockchain/data/policydatalines.txt", 'w')

# print(txt,file=datalines)
#
# data.close()

c_list=[]

for txti in txt:

    seg_list = jieba.cut(txti)

    # print("[新词识别]: ", "/ ".join(seg_list))

    c_list.append(" ".join(seg_list))

print("也应该有30行", str(len(c_list)))

datalines.writelines(c_list)

datalines.close()

