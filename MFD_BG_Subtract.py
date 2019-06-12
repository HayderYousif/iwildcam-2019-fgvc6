import cv2
import numpy as np
import glob
import os
from os import listdir
from os.path import isfile, join

def imclahe(img,clahe):
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    lab_planes = cv2.split(lab)
    lab_planes[0] = clahe.apply(lab_planes[0])
    lab = cv2.merge(lab_planes)
    bgr = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    return bgr
def hogmat(gray_image):
    winSize = (16,16)
    blockSize = (16,16)
    blockStride = (8,8)
    cellSize = (8,8)
    nbins = 36
    derivAperture = 1
    winSigma = 4.
    histogramNormType = 0
    L2HysThreshold = 2.0000000000000001e-01
    gammaCorrection = 0
    nlevels = 64
    hog = cv2.HOGDescriptor(winSize,blockSize,blockStride,cellSize,nbins,derivAperture,winSigma,
                        histogramNormType,L2HysThreshold,gammaCorrection,nlevels)
    #hog = cv2.HOGDescriptor((16,16),(16,16),(16,16),(8,8),36)
    data=[ [ 0 for i in range(36) ] for j in range(736) ]
    i=0;
    for blocky in range(0, 368, 16):
        for blockx in range(0, 512, 16):
            img2 = gray_image[blocky: blocky + 16,blockx: blockx + 16]
            h2=hog.compute(img2)
            data1 = np.array( h2 )
            data [i][:]=np.transpose(data1)
            i=i+1;
    return data

def make_square(im):
    d1,d2,d3=im.shape
    d=max(d1,d2)
    #imout=[ [ 0 for i in range(d) ] for j in range(d) for j in range(3)]
    imout=np.zeros((d,d,3),np.uint8)
    imout[:,:,0]=[ [ 0 for i in range(d) ] for j in range(d)]
    imout[:,:,1]=[ [ 255 for i in range(d) ] for j in range(d)]
    imout[:,:,2]=[ [ 0 for i in range(d) ] for j in range(d)]
    imout[0:d1,0:d2,:]=im
    return imout
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%% Build BG Image Function %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
def bgmodel(data,lenfiles):
    pairs=int(lenfiles*(lenfiles-1)/2)
    if lenfiles>2:
        bghog=[ [ 0 for i in range(36) ] for j in range(736) ]
        diff=[ [ 0 for i in range(736) ] for j in range(pairs) ]
        imind=[0 for i in range(pairs)]
        first=0
        if lenfiles>15:
            last=14
            diff=[ [ 0 for i in range(736) ] for j in range(int(15*14/2)) ]
            imind=[0 for i in range(int(15*14/2))]
        else:
            last=lenfiles-1
        cou=-1

        for aa in range(first,last):
            for conse in range(first,last):
                cou=cou+1
                imind[cou]=first
                blkind=0
                for blky in range(0, 23):
                    for blkx in range(0, 32):
                        diff[cou][blkind]=np.sum(np.absolute(np.subtract(data[first][:][blkind], data[first+1][:][blkind])))
                        blkind=blkind+1
                
            first=first+1
        blkind=0
        mindisind=np.argmin(diff, axis=0)
        #print(imind)
        for blky in range(0, 23):
            for blkx in range(0, 32):
                bghog[blkind]=data[imind[mindisind[blkind]]][:][blkind]
                #print(imind[mindisind[blkind]])
                blkind=blkind+1
    return bghog        
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%% Extract HOG for all images %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
RESIZED_IMAGE_COLS=512
RESIZED_IMAGE_ROWS=368
oripath=""
foldernames= os.listdir (oripath)
savepath=''
lenfolders=len(foldernames)
clahe = cv2.createCLAHE(clipLimit=2.0,tileGridSize=(8,8))
for fd in range( lenfolders):
    #os.makedirs(savepath+foldernames[fd])
    onlyfiles = [f for f in listdir(oripath+foldernames[fd]) if isfile(join(oripath+foldernames[fd], f))]
    lenfiles=len(onlyfiles)
    imgori=cv2.imread(oripath+foldernames[fd]+"\\"+onlyfiles[0])
    ROIheight,ROIwidth,channels=imgori.shape
    #ROIheight=ROIheight
    print(fd)

    data=[  0 for k in range(lenfiles) for i in range(36)  for j in range(736) ]
    if lenfiles>2:
        for im in range(0, lenfiles):        
            img=cv2.imread(oripath+foldernames[fd]+"\\"+onlyfiles[im])#'d16395s8i1.JPG'
            h, w,ch = img.shape
            img=img[32:h, 0:w]
            img=cv2.resize(img,(512, 368))
            #img = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
            gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #gray_image=img[:,:,0]+img[:,:,1]+img[:,:,2]
            gray_image = cv2.GaussianBlur(gray_image,(13,13),5.7)
            data[im]=hogmat(gray_image)

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%% Bounding Boxes %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  
        bghog=bgmodel(data,lenfiles)
        for im in range(0, lenfiles):
            imgori=cv2.imread(oripath+foldernames[fd]+"\\"+onlyfiles[im])
            #print(im)
            img = np.zeros([23,32],dtype=np.uint8)
            blkind=0
            for blky in range(0, 23):
                for blkx in range(0, 32):
                    diff=(np.sum(np.absolute(np.subtract(data[im][:][blkind], bghog[blkind][:]))))
                    blkind=blkind+1
                    #print((diff))
                    if diff>6.1:
                        img[blky][blkx]=1
            #img=cv2.medianBlur(img,3)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
            img = cv2.morphologyEx(img,cv2.MORPH_CLOSE,kernel)
            #img=cv2.floodFill(img,'holes')
            nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(img)
            x=stats[1:,cv2.CC_STAT_LEFT]
            y=stats[1:,cv2.CC_STAT_TOP]
            w=stats[1:,cv2.CC_STAT_WIDTH]
            h=stats[1:,cv2.CC_STAT_HEIGHT]
            x2 = (x) * 16 * (ROIwidth-32) / RESIZED_IMAGE_COLS+32
            y2 = (y) * 16 * (ROIheight) / RESIZED_IMAGE_ROWS
            w2 = (w) * 16 * ROIwidth / RESIZED_IMAGE_COLS
            h2 = h * 16 * (ROIheight) /RESIZED_IMAGE_ROWS 
            areas = np.multiply(w2,h2)
            ind=0
            #print('//////////////////////////')
            for xx in range(0,len(x2)):
                #print(int(x2[xx]),int(y2[xx]),int(w2[xx]),int(h2[xx]))
                if areas[xx]>2000:
                    ind=ind+1
                    cropped=imgori[int(y2[xx]):int(y2[xx])+int(h2[xx]),int(x2[xx]):(int(x2[xx])+int(w2[xx]))]
                    cv2.imwrite(savepath+onlyfiles[im].replace('.jpg','')+'_'+str(ind)+'.jpg',cropped)
                    
    else:
        for im in range(0, lenfiles):
            cropped=cv2.imread(oripath+foldernames[fd]+"\\"+onlyfiles[im])#'d16395s8i1.JPG'
            cv2.imwrite(savepath+onlyfiles[im],cropped)
