import cv2
import numpy as np
import glob
import os
from os import listdir
from os.path import isfile, join
from shutil import move
def make_square(im,imout2):
    d1,d2,d3=im.shape
    
    imout3=imout2
    imout3[0:d1,0:d2,:]=im
    return imout3


oripath=''
savepath=''
clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
onlyfiles = [f for f in listdir(oripath) if isfile(join(oripath, f))]
lenfiles=len(onlyfiles)
for im in range(lenfiles):
    img=cv2.imread(oripath+onlyfiles[im])
    h, w,ch = img.shape
    if h<w:
        img=cv2.resize(img,(299, int(299*h/w)))
    elif h>w:
        img=cv2.resize(img,(int(299*w/h),299 ))
    else:
        img=cv2.resize(img,(299,299 ))
    mask=cv2.imread('mask.jpg')
    img2=make_square(img,mask)
    if img2 is not None:
        img2=cv2.resize(img2,(299,299 ))
        lab = cv2.cvtColor(img2, cv2.COLOR_BGR2LAB)
        lab_planes = cv2.split(lab)
        lab_planes[0] = clahe.apply(lab_planes[0])
        lab = cv2.merge(lab_planes)
        bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        cv2.imwrite(savepath+onlyfiles[im],bgr)
