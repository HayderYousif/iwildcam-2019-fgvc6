
import cv2
import numpy as np
import os
from os import listdir
from os.path import isfile, join
########## This function has been built based on stackoverflow codes
def apply_brightness_contrast(input_img, brightness = 0, contrast = 0):

    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow)/255
        gamma_b = shadow

        buf = cv2.addWeighted(input_img, alpha_b, input_img, 0, gamma_b)
    else:
        buf = input_img.copy()

    if contrast != 0:
        f = 131*(contrast + 127)/(127*(131-contrast))
        alpha_c = f
        gamma_c = 127*(1-f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

s = 299
blist = [0, -127, 127,   0,  0, 64] # list of brightness values
clist = [0,    0,   0, -64, 20, 20] # list of contrast values
oripath=''
foldernames= os.listdir (oripath)
savepath=''
lenfolders=len(foldernames)

for fd in range(lenfolders):
   # os.makedirs(savepath+foldernames[fd])
    onlyfiles = [f for f in listdir(oripath+foldernames[fd]) if isfile(join(oripath+foldernames[fd], f))]
    lenfiles=len(onlyfiles)
    for im in range(0, lenfiles):        
            img=cv2.imread(oripath+foldernames[fd]+"\\"+onlyfiles[im])
            img = cv2.resize(img, (s,s), 0, 0, cv2.INTER_AREA)
            cv2.imwrite(savepath+foldernames[fd]+'\\'+onlyfiles[im], img)
            for i, b in enumerate(blist):
                c = clist[i]
                out = apply_brightness_contrast(img, b, c)
                gray_image = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY)
                backtorgb = cv2.cvtColor(gray_image,cv2.COLOR_GRAY2BGR)
                cv2.imwrite(savepath+foldernames[fd]+'\\'+onlyfiles[im].replace('.jpg','_')+str(i)+'.jpg', out)
                cv2.imwrite(savepath+foldernames[fd]+'\\'+onlyfiles[im].replace('.jpg','_')+str(i)+'_g.jpg', backtorgb)

