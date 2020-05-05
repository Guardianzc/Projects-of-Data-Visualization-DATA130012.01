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
import re

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

def convolution(region, filter):
    '''
    region -- the origin picture
    filter -- the convolution filter 
    '''
    padding = np.zeros((np.shape(region)[0] + 1, np.shape(region)[1] + 1))
    width, height = np.shape(region)
    for i in range(1, width+1):
        for j in range(1, height+1):
            padding[i,j] = region[i-1, j-1]
    
    new = np.zeros((width, height))
    convwidth, convheight = np.shape(filter)
    # convolutional operation
    for i in range(1, width+1):
        time.sleep(0.1)
        end_str = '100%'
        # 进度条
        process_bar(i/width, start_str='', end_str=end_str, total_length=15)
        for j in range(1, height+1):
            convsum = 0
            for s in range(convwidth):
                for t in range(convheight):
                    convsum += filter[s,t] * padding[i-s+int(s/2), j-t+int(t/2)] 
            new[i-1, j-1] = int(convsum)
    # form a new picture
    new = region - new
    im = Image.fromarray(new)
    im = im.convert('L')
    im.show()
    im.save('Sharpening.png')

def GLPF(img, D):
    # size of filter
    width, height = np.shape(img)[1], np.shape(img)[0]
    u = range(width)
    v = range(height)
    u, v = np.meshgrid(u, v)
    #  Gaussian operation
    low_pass_filter = np.sqrt( (u - width/2)**2 + (v - height/2)**2) 
    G = np.exp((-1 * low_pass_filter**2) / (2 * D ** 2 ))
    return np.clip(G, 0, 1)

def Bandreject_filters(img):
    width, height = np.shape(img)[0], np.shape(img)[1]
    B_filters = np.zeros((width,height))
    # try different filters
    #B_filters[img < 9] = 1
    B_filters[310:400,:] = 1
    B_filters[:, 310:400] = 1
    #B_filters[:,300:400] = 1
    return B_filters

def fft(img):
    # for fast fourier transformation 
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    show_fshift = np.log(np.abs(fshift))
    # show the Spectrogram
    plt.imshow(show_fshift, 'gray'), plt.title('Fourier Image')
    plt.show()
    # Different filters in 3.1 and 3.2
    '''
    GLPF_filter = GLPF(img, 40)
    img_GLPF = GLPF_filter * fshift
    show_img_GLPF = np.log(np.abs(img_GLPF))
    plt.imshow(show_img_GLPF, 'gray'), plt.title('Filtered Image')
    '''
    B_filter = Bandreject_filters(show_fshift)
    img_B = B_filter * fshift
    show_img_B = np.log(np.abs(img_B))
    plt.imshow(show_img_B, 'gray'), plt.title('Filtered Image')
    plt.show()
    # for IDFT and form a new picture
    img_ifftshifted = np.fft.ifftshift(img_B)
    img_ifft = np.fft.ifft2(img_ifftshifted)
    img_real = np.abs(np.real(img_ifft))
    img_new = np.clip(img_real,0,255)
    plt.imshow(img_new, 'gray'), plt.title('New Image')
    plt.show()

if __name__ == "__main__":
    os.chdir(sys.path[0])
    
    gray_arr = RGB2Gray('zibin.jpg')
    smoothing = np.array([[1/9,1/9,1/9],[1/9,1/9,1/9],[1/9,1/9,1/9]])
    sharpening = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    convolution(gray_arr, sharpening)
    
    '''
    photo_arr = RGB2Gray('pic.jpg')
    fft(photo_arr)
    ''''''
    freq_arr = RGB2Gray('freq_testimage_shepplogan.PNG')
    fft(freq_arr)
    '''
