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

def HW1_1():
    # 用于输入维度
    n = eval(input('Please input the dimension, if you need visualization please enter 2\n'))
    # 用来输入每一维的长度
    n_size = eval(input('Please input the size of each dimension, seperated by comma\n'))
    assert n == len(n_size), "n and the length of size should be the same"
    # 这里随机生成了这个多维向量的数据,如果是图片的话可以通过load读取数据
    data = np.random.randint(0, 50, size = n_size) # Initialize the data
    print("The data is: \n")
    print(data)            # show the data 

    # 如果是2维的话则进行一个可视化过程
    if n == 2:
        # Histogram visualization
        # prepare the data
        X_size = np.arange(0, n_size[0], step=1)
        Y_size = np.arange(0, n_size[1], step=1)
        xx, yy = np.meshgrid(X_size, Y_size) # set the coordinates
        X, Y = xx.ravel(), yy.ravel()        
        bottom = np.zeros_like(X)            # set the bottom of the histogram
        data = data.ravel()                  # flatten the data
        width = height = 1                   # set the width and height of the histogram
 
        # set the type of the figure
        fig=plt.figure()
        # 因为是二维的坐标，加上值是一个三维的图
        ax=fig.gca(projection='3d')  # set the 3-D coordinates
        ax.bar3d(X, Y, bottom, width, height, data, shade=True)#
        # set the axis
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Value')
        plt.xticks(X_size)
        plt.yticks(Y_size)
        plt.show()
  

def HW1_2():
    def plot(process_flatten, i, ROI):
        # Plot the histogram
        # 直方图可视化
        n, bins, patches = plt.hist(x=process_flatten, bins='auto', alpha=0.7, rwidth=0.85, facecolor='blue')
        plt.grid(axis='y', alpha=0.75)
        x_major_locator=MultipleLocator(1) # Set the interval of axis to 1
        ax=plt.gca()
        ax.xaxis.set_major_locator(x_major_locator)
        plt.xlabel('Grayscale Value')
        plt.ylabel('Frequency')
        title = 'Hist_of_' + str(i) + ':' + str(ROI)
        plt.title(title)
        #plt.show()
        name = title + '.jpg'
        plt.savefig('Hist%s.jpg' %i) # save the figure
        plt.close()

    print('HW1_2 is processing.')
    gray_arr = RGB2Gray('picture.jpg') # load the picture

    # Initialize the ROI
    start = 0
    ROI_size = 10
    data = np.zeros(255)
    # 通过一些参数初始化ROI框
    process = gray_arr[start:start+ROI_size]  
    process_flatten = process.flatten()
    # 画出第一个ROI框
    plot(process_flatten, 0, ROI_size-1)
    
    for i in range(5):
        # 这里的更新我才用了取余的方法，比如说ROI有5行，那么第6行因为6%5=1就应该替换掉第一行的数据
        process[(i + ROI_size + start) % ROI_size] = gray_arr[i + ROI_size + start]  # Every iteration update one row
        process_flatten = process.flatten()
        # 对前5个局部分布直方图进行作图
        plot(process_flatten, i+1, ROI_size+i)


def HW2():
    print('HW2 is processing.')
    def transfer(n):
        # the piecewise linear transformation function
        if 0 <= n < 100:
            return int(0.45 * n)
        elif 100 <= n < 200:
            return int(n - 55)
        else:
            return int(2 * n - 255)
    img = Image.open("./picture.jpg")
    pix = img.load()
    width = img.size[0]
    height = img.size[1]
    new_pic = Image.new("RGB", (width, height))

    for x in range(width):
        for y in range(height):
            r, g, b = pix[x, y]
            r = transfer(r)
            g = transfer(g)
            b = transfer(b)
            # transfer the pixel in different cernel into a new one
            new_pic.putpixel((x, y), (r,g,b))
        time.sleep(0.1)
        end_str = '100%'
        process_bar(x/width, start_str='', end_str=end_str, total_length=15)
    new_pic.show()
    new_pic.save('./new_pic.jpg')

def RGB2Gray(image_name):
    # Convert RGB image to grayscale image
    img = Image.open(image_name)
    gray= img.convert('L')
    grayname = 'Gray_' + image_name
    gray.save(grayname)
    gray_arr = np.array(gray, dtype=np.uint8)
    return gray_arr

def equalization(matrix, vector):
    # The equalization function
    # Matrix means the local ROI matrix, the vector means the vector needed to be updated 
    # Return the vector after update
    # 这是针对某个区域的ROI进行equlization的函数
    max_pixel = matrix.max()
    min_pixel = matrix.min()
    size = matrix.size
    # 这里对灰度值进行了排序
    flatten = np.sort(matrix.flatten())
    width = matrix.shape[0]
    length = matrix.shape[1]
    update_vector = np.zeros((length))
    for y in range(length):
        pixel = matrix[vector, y]
        # 这是主要的equlization函数， 通过flatten(经过排序后的)查找pixel的位置(坐标就是其累积分布函数值)，然后归一化到灰度值的范围之中
        new_pixel = int(np.argwhere(flatten == pixel)[-1]) / size * (max_pixel - min_pixel) + min_pixel
        # esimate the cumulative function
        update_vector[y] = int(new_pixel)
    return update_vector

def HW3():
    # 这里是global equalization, 把整个图片形成的矩阵输入
    grey_arr = RGB2Gray('Zibin.jpg')
    print('HW3_1 is processing.')
    width = grey_arr.shape[0]
    new_pic = np.zeros(grey_arr.shape,dtype = np.int8)

    for i in range(width):
        # Update the whole picture
        # 对图片的每一行进行update
        new_pic[i] = equalization(grey_arr, i)
        time.sleep(0.1)
        end_str = '100%'
        # 进度条
        process_bar(i/width, start_str='', end_str=end_str, total_length=15)
    p_img = Image.fromarray(new_pic, mode='L') # Create the picture from the 2-D array
    p_img.show()
    p_img.save("Equal_Grey.jpg")
    


def HW3_2():

    print('HW3_2 is processing.')
    grey_arr = RGB2Gray('Zibin.jpg')
    grey_width = grey_arr.shape[0]
    # Initialize
    start = 0
    ROI_size = 10
    new_pic = np.zeros(grey_arr.shape,dtype = np.int8)
    matrix = grey_arr[start:ROI_size]
    # 处理最初的ROI
    for i in range(ROI_size):
    
        new_pic[i] = equalization(matrix, i)
    # The first step is to set the ROI and update the vector in ROI
    for i in range(ROI_size, grey_width):
    # 和1_2的方法一样，每次更新一个ROI，更新新进入一行的数据
    # And then we update one vector in one iteration and do the equlization in the vector updated
        matrix[(i % ROI_size)] = grey_arr[i]
        new_pic[i] = equalization(matrix, i % ROI_size)
        time.sleep(0.1)
        end_str = '100%'
        process_bar(i/grey_width, start_str='', end_str=end_str, total_length=15)
    p_img = Image.fromarray(new_pic, mode='L')
    p_img.show()
    p_img.save("Local_Equal_Grey.jpg")
    




if __name__ == "__main__":
    os.chdir(sys.path[0]) # Change the work directory into the file where the python file holds
    # You can comment out the program what you don't need to test
    HW1_1()
    HW1_2()
    HW2()
    HW3()
    HW3_2()