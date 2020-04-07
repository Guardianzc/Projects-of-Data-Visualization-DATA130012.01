import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import os
import sys
from collections import Counter
from matplotlib.pyplot import MultipleLocator

def process_bar(percent, start_str='', end_str='', total_length=0):
    # print the process bar
    # 这是一个用来显示进度条的函数，因为很多图片在处理时的时间都比较长
    bar = ''.join(["\033[31m%s\033[0m"%'-'] * int(percent * total_length)) + '>'
    bar = '\r' + start_str + bar.ljust(total_length) + ' {:0>4.1f}%|'.format(percent*100) + end_str
    print(bar, end='', flush=True)

def RGB2Gray(image_name):
    # Convert RGB image to grayscale image
    img = Image.open(image_name)
    gray= img.convert('L')
    grayname = 'Gray_' + image_name
    gray.save(grayname)
    gray_arr = np.array(gray, dtype=np.uint8)
    return gray_arr

def OTSU(img):
    '''
    img: the image need to be processed by OTSU
    output: a numpy array with 0,1 , shows the value of new picture
    '''
    # find the shape of img
    width, height = img.shape
    # find the maximun and minimun pixel value of image
    max_value = img.max()
    min_value = img.min()
    # store the best threshold value
    max_threshold = 0
    max_loca = 0
    # Total number of pixels
    total = width * height
    
    for i in range(min_value, max_value):
        small = []
        big = []
        for j in range(width):
            for k in range(height):
                if img[j,k] <= i:
                    # Divide the image into 2 classes
                    small.append(img[j,k])
                else:
                    big.append(img[j,k])
        # Frqency
        w_s = len(small)/total
        w_b = len(big)/total
        # Mean of each classes
        mean_s = sum(small) / (total*w_s)
        mean_b = sum(big) / (total*w_b)
        # Calculate the between class variance
        sigma_bet = w_s * w_b * (mean_s - mean_b) ** 2
        if sigma_bet > max_loca:
            max_loca = sigma_bet
            max_threshold = i
    # Plot the binary image
    new_img = np.zeros(img.shape)
    for i in range(width):
        for j in range(height):
            if img[i,j] > max_threshold:
                new_img[i,j] = 1
    return new_img


def Q3():
    print('Question 3 is processing.')
    img = RGB2Gray("Q3picture1.png")
    # Find the shape of the image
    width, height = img.shape
    # Create the new image
    threshold_img = np.zeros(img.shape)
    # Create the local subimage and using OTSU to calculate the Binarization Image 
    for i in range(0,width,50):
        for j in range(0,height,50):
            # Update
            threshold_img[i:i+50, j:j+50] = OTSU(img[i:i+50, j:j+50])
        time.sleep(0.1)
        end_str = '100%'
        # 进度条
        process_bar(i/width, start_str='', end_str=end_str, total_length=15)
    # Show the Binarization Image by the color of black and white
    threshold_img *= 255
    im = Image.fromarray(threshold_img)
    im = im.convert('L')
    im.show()
    im.save('Q3.png')


def Interpolation(new_img, img, n):
    '''
    new_img: array to store the new image, shape = (img.shape * n)
    img: the image need to interpolation
    n : How many times the sharpness needs to rise
    '''
    width, height = new_img.shape
    width_old, height_old = img.shape
    for i in range(width):
        for j in range(height):
            i_old = i / n
            j_old = j / n
            # Calculate the distance
            x1 = int(i_old)
            y1 = int(j_old)
            x2 = int(min(i_old + 1, width_old-1))
            y2 = int(min(j_old + 1, height_old-1))
            # Locate the four points that needed in interpolation
            p1, p2, p3, p4 = img[x1,y1], img[x1,y2], img[x2,y1], img[x2,y2]
            # the distances in interpolation
            u = i_old - x1
            v = j_old - y1
            # the new value
            value = p1 * (1-u) * (1-v) + p2 * (1-u) * v + p3 * u * (1-v) + p4 * u * v
            new_img[i,j] = value
        time.sleep(0.1)
        end_str = '100%'
        # 进度条
        process_bar(i/width, start_str='', end_str=end_str, total_length=15)
    return new_img


def MedianFilter(img, dst, k = 3):
    # 中值滤波器(在后续实验中已弃用)
    height, width = img.shape
    height = int(height/k)
    width = int(width/k)
    edge = int((k-1)/2)
    if height - 1 - edge <= edge or width - 1 - edge <= edge:
        print("The parameter k is to large.")
        return None
    new_arr = np.zeros((height, width), dtype = "uint8")
    for i in range(height):
        for j in range(width):
            '''
            if i <= edge - 1 or i >= height - 1 - edge or j <= edge - 1 or j >= height - edge - 1:
                new_arr[i, j] = img[i, j]
            else:
                new_arr[i, j] = np.median(img[i - edge:i + edge + 1, j - edge:j + edge + 1])
            '''
            new_arr[i,j] = img[i*2, j*2]
        time.sleep(0.1)
        end_str = '100%'
        # 进度条
        process_bar(i/height, start_str='', end_str=end_str, total_length=15)
    new_img = Image.fromarray(new_arr)
    new_img.save(dst)
    return new_arr
 
def Q4(n):
    print('Question 4 is processing.')
    '''
    img_arr = RGB2Gray("Q4.jpg")
    dst = 'Q4MedianFilter.png'
    img = MedianFilter(img_arr, dst, k = 2)
    '''
    img = RGB2Gray("Q4.jpg")
    width, height = img.shape
    new_img = np.zeros((width*n, height*n))
    new_img = Interpolation(new_img, img, n)
    # Show the new image
    im = Image.fromarray(new_img)
    im = im.convert('L')
    im.show()
    im.save('Q4.png')

    

if __name__ == "__main__":
    os.chdir(sys.path[0])
    Q3()
    Q4(2)
    pass


