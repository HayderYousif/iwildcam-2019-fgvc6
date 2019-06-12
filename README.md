# iwildcam-2019-fgvc6
Classifying Camera trap images from based on sequence-level decision. First, using our background modeling, we developed a scheme to generate candidate object regions or object proposals in the spatiotemporal domain. Second, we overcome the problem of noisy foregound regions by dentifying the best temporal subset of object proposals after data preprocessing and oversampling. Our preprocessing and oversampling are the enabling steps to provide the DCNN model with more distictive images and to mimic the camera trap image challenges. Third, we aggregate and fuse the features of these selected object proposals for efficient sequence-level animal species classification. Finally, each frame within a given sequence is labeled with either the sequence-level animal class or empty based on the features of the region proposals of that frame.


# Region proposals
We use our backgound subtration to generate the region proposals. For the training, we use the IoU between the foreground region and the provided bounding box annotations
> MFD_BG_Subtract.py


# Image Preprocessing
We notice that, in night-time camera trap images, the lighting varies significantly between regions with the center regions being significantly brighter than surrounding regions. To address this issue, we use the contrast-adaptive histogram equalization (CLAHE) method to pre-process our images.
> Image_preprocessing.py # You need "mask.png" file to run this code


# Data balancing
We increase the number of training samples of the classes with less 100 images (e.g., wolf, elk, mountain_lion,...) from both camera trap and iNaturalist by changing the contrast and brightness of the RGB and the grayscale versions. 
> Image_oversampling.py


# Training
We train Inceptionv3, ResNet152, and InceptionResnetv2 DCNN models with  pytorch using the region proposals from our background subtraction. We collected bounding box annotations from iNaturalist images 2017/2018 of the missing classes (9 classes) of the provided camera trap training images.


# Testing
There are different ways other than the next steps to find the image-level class:

A) Pytorch part:
We save the test patch (region proposal) ID, prediction class, and softmax features (23-length vector) from each DCNN model similar to:
> testpatches.csv

B) Matlab Part:
1- Each sequence should have a folder containing it's patches similar to:
> testseq.txt

2- Image-level prediction for each model can be obtained:
> Test_images_prediction.m

3- The majority voting from the three DCNN models can be applied for better results using "mode" Matlab command.

#Citation
@article{yousif2019dynamic,
title={Dynamic Programming Selection of  Object Proposals  for  Sequence-Level Animal Species Classification in the Wild},
author={Yousif, Hayder and Kays, Roland and He, Zhihai},
journal={IEEE Transactions on Circuits and Systems for Video Technology},
year={2019},
publisher={IEEE}
}
@article{yousif2018object,
  title={Object detection from dynamic scene using joint background modeling and fast deep learning classification},
  author={Yousif, Hayder and Yuan, Jianhe and Kays, Roland and He, Zhihai},
  journal={Journal of Visual Communication and Image Representation},
  volume={55},
  pages={802--815},
  year={2018},
  publisher={Elsevier}
}



