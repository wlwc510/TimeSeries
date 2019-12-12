import os
import os.path
from win32com import client as wc

c = []

rootdir = ["D:/publications/preparing/00blockchain/区块链政策整理140个"]  # 以该路径为实验


def txt(j, c):

    try:
        word = wc.Dispatch('Word.Application')

        print(str(c[j]))

        doc = word.Documents.Open(c[j])

        newname = c[j][:-5] + "(translate txt)"

        doc.SaveAs(newname, 4)

        doc.Close()

        word.Quit()

        os.remove(c[j])

        print("完成")

    except:

        print("出错")


def wordt(c):  # 定义函数，进行筛选

    for j in range(0, len(c)):

        if c[j][-5:] == ".docx" or c[j][-4:] == ".doc":  # 寻找docx文件


            txt(j, c)  #

        else:
            pass


for i in rootdir:  # 定义函数，查找所有文件

    for parent, dirnames, filenames in os.walk(i):

        for filename in filenames:

            if filename.endswith(".docx") or filename.endswith(".doc"):

                c.append(os.path.join(parent, filename))
            # print(str(os.path.join(parent, filename)))

wordt(c)