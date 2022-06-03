from PIL import Image
from numpy import *
from pylab import *
import os

def process_image(imagename,resultname,params="--edge-thresh 10 --peak-thresh 5"):
    """ Process an image and save the results in a file. """

    if imagename[-3:] != 'pgm':
        # create a pgm file
        im = Image.open(imagename).convert('L')  #.convert('L') 将RGB图像转为灰度模式，灰度值范围[0,255]
        im.save('tmp.pgm')                       #将灰度值图像信息保存在.pgm文件中
        imagename = 'tmp.pgm'

    cmmd = str(r"D:\Google\vlfeat-0.9.20-bin\vlfeat-0.9.20\bin\win64\sift.exe "+imagename+" --output="+resultname+
                " "+params)
    os.system(cmmd)                              #执行sift可执行程序，生成resultname(test.sift)文件
    print('processed', imagename, 'to', resultname)


def read_features_from_file(filename):
    """ Read feature properties and return in matrix form. """

    f = loadtxt(filename)
    return f[:,:4],f[:,4:] # feature locations, descriptors

