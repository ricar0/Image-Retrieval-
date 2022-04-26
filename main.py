import pickle

import time
from PCV.localdescriptors import sift
from PCV.imagesearch import vocabulary
from PCV.imagesearch import imagesearch
from PCV.geometry import homography
import sqlite3
import os
import cv2
import tkinter
from tkinter import filedialog
from PIL import Image
import matplotlib.pyplot as plt

def get_imlist(path): #获取所有训练图片
    imlist=[]
    for root, dirs, files, in os.walk(path):
        for file in files:
            fpath = os.path.join(root, file)
            if fpath.endswith('.jpg'):
                imlist.append(fpath)
    return imlist

# imlist = get_imlist('train\\')
#
# nbr_images = len(imlist)

# featlist = [imlist[i][:-3]+'sift' for i in range(nbr_images)] #获取特征列表

# for i in range(nbr_images):
#     sift.process_image(imlist[i], featlist[i])

#生成词汇
# voc = vocabulary.Vocabulary('ukbenchtest')
# voc.train(featlist, 64, 10)
# #
# with open('train/vocabulary.pkl', 'wb') as f:
#     pickle.dump(voc, f)
# print ('vocabulary is:', voc.name, voc.nbr_words)
# print(featlist)

# # 载入词汇
# with open('train/vocabulary.pkl', 'rb') as f:
#     voc = pickle.load(f)
# #
# indx = imagesearch.Indexer('testImaAdd.db',voc)
# indx.create_tables()
# # go through all images, project features on vocabulary and insert
# # 遍历所有的图像，并将它们的特征投影到词汇上
# for i in range(nbr_images):
#     locs,descr = sift.read_features_from_file(featlist[i])
#     indx.add_to_index(imlist[i],descr)
#
# # commit to database
# indx.db_commit()
# #
# con = sqlite3.connect('testImaAdd.db')
# print (con.execute('select count (filename) from imlist').fetchone())
# print (con.execute('select * from imlist').fetchone())

# src = imagesearch.Searcher('testImaAdd.db',voc)

# index of query image and number of results to return
# 查询图像索引和查询返回的图像数

tim, accuracy = [], []
def match_pic(e_entry):
    pic_name = e_entry.get()
    nbr_results = 10
    # 常规查询(按欧式距离对结果排序)
    st = time.time()
    res_reg = [w[1] for w in src.query(pic_name)[:nbr_results]]
    ed = time.time()
    tim.append(ed-st)

    # print(pic_name.split('\\')[-1][:6])
    correct = pic_name.split('\\')[-1][:6]

    # print(correct)
    Acnumber = 0
    carlist = []
    for item in res_reg:#获取匹配图片的车牌号
        carlist.append(imlist[item].split('\\')[-1][:6])
        if correct == imlist[item].split('\\')[-1][:6]:
            Acnumber += 1
        # print(imlist[item][6:][:6])

    accuracy.append(Acnumber/10)
    print("准确度:"+str(Acnumber*10)+"%")

    # 显示查询结果
    # print(res_reg)
    # imagesearch.plot_results(src,res_reg[:8]) #常规查询
    plt.rcParams['font.sans-serif'] = ['SimHei']

    cnt = 1
    for idx in range(nbr_results):
        plt.subplot(3, 4, cnt)
        pic = plt.imread(imlist[res_reg[idx]])
        plt.imshow(pic)
        plt.title(str(carlist[idx]))
        plt.axis('off')
        cnt += 1

    plt.tight_layout()
    plt.show()

def open_file():

    default_dir = r"D:jetbrains/pycharmProjects/pictureMatch/test"
    file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
    file_path = file_path.replace('/', '\\').split('pictureMatch\\')[-1]
    file_path = file_path.replace('test', 'train')

    e.set(file_path)
    # print(e_entry.get())

def show_pic(e_entry):
    file_path = e_entry.get()
    img = cv2.imread(file_path)
    cv2.imshow('选定图片', img)
    cv2.waitKey(0)

def draw():
    Len = len(tim)
    idx = []
    for i in range(Len):
        idx.append(i+1)
    l1 = plt.plot(idx, tim, 'r--', label='运行时间')
    l2 = plt.plot(idx, accuracy, 'g--', label='准确率')
    plt.plot(idx, tim, 'ro-', idx, accuracy, 'g+-')
    plt.legend()
    plt.show()

def windows():
    rt = tkinter.Tk()
    rt.geometry('500x500')  # 窗口的大小
    # rt.withdraw()
    rt.title('图像检索')  # 窗口的标题

    global e
    e = tkinter.StringVar()  # 文本输入框
    e_entry = tkinter.Entry(rt, width=68, textvariable=e)

    #创建button
    b1= tkinter.Button(rt, text='选择图像', width=15,
                   height=2, command=open_file)
    b1.pack()

    b2 = tkinter.Button(rt, text='查看图片', width=15,
                        height=2, command=lambda:show_pic(e_entry))
    b2.pack()

    b3 = tkinter.Button(rt, text='匹配图片', width=15,
                        height=2, command=lambda:match_pic(e_entry))
    b3.pack()

    b4 = tkinter.Button(rt, text='绘图', width=15,
                        height=2, command=draw)
    b4.pack()

    rt.mainloop()

if __name__ == '__main__':
    imlist = get_imlist('train\\')
    nbr_images = len(imlist)
    with open('train/vocabulary.pkl', 'rb') as f:
        voc = pickle.load(f)
    src = imagesearch.Searcher('testImaAdd.db', voc)

    windows()




