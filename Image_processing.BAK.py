"""






"""

import os
import glob
import cv2
import numpy as np
import copy
from matplotlib import pyplot as plt

"""
def histogram_equalize(img):
    b, g, r = cv2.split(img)
    red = cv2.equalizeHist(r)
    green = cv2.equalizeHist(g)
    blue = cv2.equalizeHist(b)
    return cv2.merge((blue, green, red))

os.chdir('/home/zhewei/Zhewei/CamVid/val/')
for files in glob.glob('*.png'):
    print (files)
    img = cv2.imread(files)
    img = histogram_equalize(img)

    #img_yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)
    ## equalize the histogram of the Y channel
    #img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

    ## convert the YUV image back to RGB format
    #img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    #cv2.imshow('Color input image', img)
    #cv2.imshow('Histogram equalized', img_output)
    #cv2.waitKey(0)



    #blur = cv2.GaussianBlur(img, (5,5), 0)
    #Half_size = cv2.resize(blur, (0,0), fx=0.5, fy=0.5)
    #blur2 = cv2.GaussianBlur(Half_size, (5,5), 0)
    #Quarter_size = cv2.resize(blur2, (0,0), fx=0.5, fy=0.5)
    #print img.shape
    #print Quarter_size.shape
    cv2.imwrite('/home/zhewei/Zhewei/CamVid/val_EB/'+files, img)

"""


"""
# for ground truth, the label is from 0 to 11, But it has 10 classes for total
os.chdir('/home/zhewei/Zhewei/CamVid_MultiScale/valannot/')
for files in glob.glob('*.png'):
    img = cv2.imread(files, cv2.IMREAD_GRAYSCALE)
    #tmp = copy.deepcopy(img)
    all_pixel = list()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            all_pixel.append(img[i,j])
            #tmp[i,j] = img[i,j]*10

    class_list = list(set(all_pixel))
    # to visualize the image
    #cv2.imwrite('contrast.png', tmp)

    for classNO, classPixel in enumerate(class_list):
        tmp = copy.deepcopy(img)
        for i in range(tmp.shape[0]):
            for j in range(tmp.shape[1]):
                if img[i,j] != classPixel:
                    tmp[i,j] = 0
                else:
                    tmp[i,j] = 255

        # gaussian twice to get 1/4 size
        blur = cv2.GaussianBlur(tmp, (5,5), 0)
        Half_size = cv2.resize(blur, (0,0), fx=0.5, fy=0.5)
        blur2 = cv2.GaussianBlur(Half_size, (5,5), 0)
        Quarter_size = cv2.resize(blur2, (0,0), fx=0.5, fy=0.5)
        Quarter_size = Quarter_size.reshape((1,Quarter_size.shape[0], Quarter_size.shape[1]))
        if classNO == 0:
            stack_img = Quarter_size
        else:
            stack_img = np.concatenate((stack_img, Quarter_size), axis=0)


    # go back to grey image
    final_img = np.zeros((stack_img.shape[1], stack_img.shape[2]),dtype=np.int)
    for i_s in range(stack_img.shape[1]):
        for j_s in range(stack_img.shape[2]):
            tmp_array = stack_img[:,i_s,j_s]
            max_index = np.argmax(tmp_array)
            final_img[i_s, j_s] = class_list[max_index]
            #print tmp_array
            
    cv2.imwrite('/home/zhewei/Zhewei/CamVid_MultiScale/valannot_small/'+files, final_img)
    #cv2.imwrite('final.png', final_img)
    print files

"""


"""
os.chdir ('/home/zhewei/Zhewei/CamVid_MultiScale/test/')
for files in glob.glob('*.png'):
    print (files)
    img = cv2.imread(files)
    print (img.shape)
    norm_img = copy.deepcopy(img)

    blur = cv2.GaussianBlur(norm_img, (5,5), 0)
    Half_size = cv2.resize(blur, (0,0), fx=0.5, fy=0.5)
    blur2 = cv2.GaussianBlur(Half_size, (5,5), 0)
    Quarter_size = cv2.resize(blur2, (0,0), fx=0.5, fy=0.5)

    norm_img = cv2.normalize(Quarter_size, dst=norm_img, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    norm_img = np.uint8(norm_img*255)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4,4))
    cl1 = clahe.apply(norm_img[:,:,0])
    cl2 = clahe.apply(norm_img[:,:,1])
    cl3 = clahe.apply(norm_img[:,:,2])
    cl = cv2.merge((cl1, cl2, cl3))
    #cv2.imshow('result', cl)
    #cv2.imshow('origin', img)
    #cv2.waitKey(0)
    #print (a)
    cv2.imwrite('/home/zhewei/Zhewei/CamVid_MultiScale/test_small/'+files, cl)
"""


os.chdir ('/home/zhewei/Zhewei/CamVid_MultiScale/trainannot/')
for files in glob.glob('*.png'):
    print (files)
    img = cv2.imread(files,0)
    #tmp = copy.deepcopy(img)
    print (img.shape)
    all_pixel = list()
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            all_pixel.append(img[i,j])
            #tmp[i,j] = img[i,j]*10

    class_list = list(set(all_pixel))
    for classNO, classPixel in enumerate(class_list):
        tmp = copy.deepcopy(img)
        for i in range(tmp.shape[0]):
            for j in range(tmp.shape[1]):
                if img[i,j] != classPixel:
                    tmp[i,j] = 0
                else:
                    tmp[i,j] = 255

        blur = cv2.GaussianBlur(tmp, (5,5), 0)
        Half_size = cv2.resize(blur, (0,0), fx=0.5, fy=0.5)
        blur2 = cv2.GaussianBlur(Half_size, (5,5), 0)
        Quarter_size = cv2.resize(blur2, (0,0), fx=0.5, fy=0.5)

        norm_img = cv2.normalize(Quarter_size, dst=tmp, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
        norm_img = np.uint8(norm_img*255)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4,4))
        cl1 = clahe.apply(norm_img)
        cl1 = cl1.reshape((1, cl1.shape[0], cl1.shape[1]))
        if classNO == 0:
            stack_img = cl1
        else:
            stack_img = np.concatenate((stack_img, cl1), axis=0)


    # go back to grey image
    final_img = np.zeros((stack_img.shape[1], stack_img.shape[2]),dtype=np.int)
    for i_s in range(stack_img.shape[1]):
        for j_s in range(stack_img.shape[2]):
            tmp_array = stack_img[:,i_s,j_s]
            max_index = np.argmax(tmp_array)
            final_img[i_s, j_s] = class_list[max_index]
            #print tmp_array
    #cv2.imshow('result', final_img)
    #cv2.waitKey(0)
    #cv2.imwrite('final.png', final_img)
    #print (a)
    cv2.imwrite('/home/zhewei/Zhewei/CamVid_MultiScale/trainannot_small/'+files, final_img)
    
