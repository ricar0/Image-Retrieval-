import pickle

import time
import random
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from PCV.localdescriptors import sift
from PCV.imagesearch import vocabulary
from PCV.imagesearch import imagesearch
import sqlite3
import os
import cv2
import tkinter
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

map = {}

def resize(w_box, h_box, pil_image):

  w, h = pil_image.size
  f1 = 1.0*w_box/w # 1.0 forces float division in Python2
  f2 = 1.0*h_box/h
  factor = min([f1, f2])
  width = int(w*factor)
  height = int(h*factor)
  return pil_image.resize((width, height), Image.ANTIALIAS)

def get_imlist(path): #获取所有训练图片
    imlist=[]
    for root, dirs, files, in os.walk(path):
        for file in files:
            map[file[:6:]]=len(files)
            fpath = os.path.join(root, file)
            if fpath.endswith('.jpg'):
                imlist.append(fpath)

    return imlist

tim, accuracy, recall, fpr = [], [], [], []

def match_pic(e_entry,rt):
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
    recall.append(Acnumber/map[correct])
    fpr.append((10-Acnumber)/(len(imlist)-map[correct]))
    #设置字体
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.title('正确车牌:' + correct + "  " + "准确度:" + str(accuracy), verticalalignment="bottom")
    cnt = 1
    fig = plt.figure(figsize=(10, 4), dpi=70)  # 图像比例
    f_plot = fig.add_subplot(341)  # 划分区域
    canvas_spice = FigureCanvasTkAgg(fig, rt)
    canvas_spice.get_tk_widget().place(x=300, y=350)  # 放置位置
    f_plot.clear()  # 刷新

    for idx in range(nbr_results):
        plt.subplot(3, 4, cnt)
        pic = plt.imread(imlist[res_reg[idx]])
        plt.imshow(pic)
        plt.title(str(carlist[idx]))
        plt.axis('off')
        cnt += 1
    #
    plt.tight_layout()
    canvas_spice.draw()

def match_pic2(pic_name):
    nbr_results = 10
    st = time.time()
    res_reg = [w[1] for w in src.query(pic_name)[:nbr_results]]
    ed = time.time()
    tim.append(ed-st)

    correct = pic_name.split('\\')[-1][:6]
    # print(correct)
    Acnumber = 0
    carlist = []
    for item in res_reg:#获取匹配图片的车牌号
        item -= 1
        carlist.append(imlist[item].split('\\')[-1][:6])
        if correct == imlist[item].split('\\')[-1][:6]:
            Acnumber += 1

    accuracy.append(Acnumber/10)
    recall.append(Acnumber/map[correct])
    fpr.append((10-Acnumber)/(len(imlist)-map[correct]))

def open_file(label_img):
    default_dir = r"D:jetbrains/pycharmProjects/pictureMatch/test"
    file_path = filedialog.askopenfilename(title=u'选择文件', initialdir=(os.path.expanduser(default_dir)))
    file_path = file_path.replace('/', '\\').split('pictureMatch\\')[-1]
    file_path = file_path.replace('test', 'train')

    newImage = Image.open(file_path)
    newImage = resize(200,200,newImage)
    img = ImageTk.PhotoImage(image=newImage)
    label_img.configure(image=img)
    label_img.image = img

    e.set(file_path)

def draw1(rt):
    # Len = len(tim)
    # idx = []
    # for i in range(Len):
    #     idx.append(i+1)
    # l1 = plt.plot(idx, tim, 'r--', label='运行时间(s)')
    # l2 = plt.plot(idx, accuracy, 'g--', label='准确率')
    # l3 = plt.plot(idx, recall, 'b--', label='召回率')
    # plt.plot(idx, tim, 'ro-', idx, accuracy, 'g+-', idx, recall, 'bo-')
    # plt.legend()
    # plt.show()
    accuracy.clear()
    tim.clear()
    recall.clear()
    label = list(range(1, 21))
    for i in range(1, 21):
        rnd = random.randint(0, len(imlist))
        match_pic2(imlist[rnd])

    fig = plt.figure(figsize=(10, 4), dpi=70)  # 图像比例
    f_plot = fig.add_subplot(111)  # 划分区域
    canvas_spice = FigureCanvasTkAgg(fig, rt)
    canvas_spice.get_tk_widget().place(x=300, y=20)  # 放置位置

    plt.rcParams['font.sans-serif'] = 'SimHei'  # 全局字体
    f_plot.clear()  # 刷新

    plt.subplot(131)
    plt.xlabel('次数')
    plt.ylabel('精确度(100%)')
    plt.plot(label, accuracy, 'b')
    plt.grid(True)  # 网格

    plt.subplot(132)
    plt.xlabel('次数')
    plt.ylabel('耗时(s)')
    plt.plot(label, tim, 'g')
    plt.grid(True)  # 网格

    plt.subplot(133)
    plt.xlabel('次数')
    plt.ylabel('召回率')
    plt.plot(label, recall, 'r')
    plt.grid(True)  # 网格

    canvas_spice.draw()

def draw2():

    plt.plot(fpr, recall, 'r--', label='运行时间(s)')
    plt.show()

def windows():
    rt = tkinter.Tk()
    rt.geometry('1000x800')  # 窗口的大小
    # rt.withdraw()
    rt.title('图像检索')  # 窗口的标题

    global e
    e = tkinter.StringVar()  # 文本输入框
    e_entry = tkinter.Entry(rt, width=68, textvariable=e)

    img = ImageTk.PhotoImage(file='init.jpg')
    label_img = tkinter.Label(rt, image=img)

    #创建button

    b1= tkinter.Button(rt, text='选择图像', width=15,
                   height=2, command=lambda:open_file(label_img))
    b1.place(x=100,y=10)

    label_img.place(x=50,y=80,height=210, width=210)

    b3 = tkinter.Button(rt, text='匹配图片', width=15,
                        height=2, command=lambda:match_pic(e_entry,rt))
    b3.place(x=100,y=300)

    b4 = tkinter.Button(rt, text='运行时间、精确度、召回率', width=20,
                        height=2, command=lambda:draw1(rt))
    b4.place(x=80,y=350)

    b5 = tkinter.Button(rt, text='roc曲线', width=15,
                        height=2, command=draw2)
    b5.place(x=100,y=400)

    rt.mainloop()

if __name__ == '__main__':
    # imlist = get_imlist('train\\')
    # nbr_images = len(imlist)
    # featlist = [imlist[i][:-3]+'sift' for i in range(nbr_images)] #获取特征列表
    #
    # for i in range(nbr_images):
    #     sift.process_image(imlist[i], featlist[i]) #前四个分别是位置、尺度、方向 后面128维方向向量
    #
    # # 生成词汇
    # voc = vocabulary.Vocabulary('ukbenchtest')
    # voc.train(featlist, 1024, 10)
    # #
    # with open('train/vocabulary.pkl', 'wb') as f:
    #     pickle.dump(voc, f)
    # print ('vocabulary is:', voc.name, voc.nbr_words)
    # print(featlist)
    #
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

    # index of query image and number of results to return
    # 查询图像索引和查询返回的图像数

    imlist = get_imlist('train\\')
    nbr_images = len(imlist)
    featlist = [imlist[i][:-3] + 'sift' for i in range(nbr_images)]  # 获取特征列表

    with open('train/vocabulary.pkl', 'rb') as f:
        voc = pickle.load(f)
    src = imagesearch.Searcher('testImaAdd.db', voc)

    locs, descr = sift.read_features_from_file(featlist[0])

    windows()




