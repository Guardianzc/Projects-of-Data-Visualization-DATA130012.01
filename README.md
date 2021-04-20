# Projects-of-Data-Visualization-DATA130012.01
This is a report including all projects in my 2020 Spring Data Visualization course (DATA130008.01) in [DATA130012.01](https://sds.fudan.edu.cn/)  of [Fudan University](https://www.fudan.edu.cn/) .

## Project
   * [Project1_Histograms](./Project1)
   * [Project2_OTSU](./Project2)
   * [Project3_Smoothing,Sharpening & Fourier transform](./Project3)
   * [Project4_(Team Project1) Image_transform](./TeamProject1(Project4))
   * [Project5_Gray2RGB](./Project5)
   * [Project6_VTK](./Project6)
   
## Details
**Project1_Histograms**
* 1 (1) implement n-dimensional joint histogram and test the code on two-dimensional data; plot the results. (2) implement computation of local histograms of an image using the efficient update of local histogram method introduced in local histogram processing.
* 2 Implement a piecewise linear transformation function (below figure) for image contrast stretching. The code should read in an image; for intensity of all pixels, use the function to compute new intensity values; and finally output/ save the image with new intensity values.
* 3 Implement the algorithm of local histogram equalization: (1) first implement histogram equalization algorithm, and then (2) implement the local histogram equalization using efficient computation of local histogram. Please test your code on images and show the results in your report.
* You can see the detail of code [here](./Project1/Project1.py) and my report [here](./Project1/Project1.pdf)
    
**Project2_OTSU**
* 1 Restate the Basic Global Thresholding (BGT) algorithm so that it uses the histogram of an image instead of the image itself. 
* 2 Design an algorithm with the function of locally adaptive thresholding (e.g. based on moving average or local OSTU); implement the algorithm and test it on exemplar image(s).
* 3 编程实现线性插值算法（不能调用某个算法库里面的插值函数），并应用：读出一幅图像，利用线性插值把图片空间分辨率放大N倍，然后保存图片。
* You can see the detail of code [here](./Project2/Project2.py) and my report [here](./Project2/Project2.pdf)

**Project3_Smoothing,Sharpening & Fourier transform**
* 1 编程实现基于空间滤波器的（1）平滑操作、（2）锐化算法算法；并把算法应用与图片上，显示与原图的对比差别。备注：实现的代码不能调用某个算法库里面的函数实现平滑或锐化。
* 2 证明二维变量的离散傅里叶变换的卷积定理即：

f(x,y)*h(x,y) <==> F(u,v)H(u,v)

f(x,y)h(x,y)  <==> F(u,v)*H(u,v)

    其中, * 表示卷积运算。
* 3 编程实现基于课件中频率域滤波5步骤的：（1）低通平滑操作，并把算法应用与图片上，显示原图的频谱图、频域操作结果的频谱图，以及操作结果；（2）频率操作，去除大脑CT体膜Shepp-Logan图像中的条纹。
[freq_testimage_shepplogan.PNG](./Project3/freq_testimage_shepplogan.PNG)

备注：图像的时空-频域变换过程（即离散傅里叶变换和逆变换）可以调用库函数。
* You can see the detail of code [here](./Project3/Project3.py) and my report [here](./Project3/HW3_钟诚_16307110259.pdf)
    
**Project4_(Team Project1) Image_transform**
* I do this project with [Allan Zhang](https://github.com/zhangyilang) and [Lulu Zhou](https://github.com/doris-lessing)
* 1）实现基于局部仿射的形变算法，（2）实现基于反向的图像变换算法，从而实现人脸到狒狒脸的图像变换。作业的基本算法内容参考课堂上讲解和课件。可以参考其他有关的学术资料改进效果（optional），但不能只使用其他的算法而没有实现题目要求的两个基本方法
* You can see the detail of code [here](./TeamProject1(Project4)/codes) and my report [here](./TeamProject1(Project4)/report.pdf)    

**Project5_Gray2RGB**
* 1 设计灰度向彩色（伪彩）变换的算法、实现代码并用图片进行测试。
* 2 请使用世界各国GDP总量数据（从http://www.gapminder.org网站下载；或从elearning下载），(1) 用折线、散点做一个完整可视化图，显示世界各国20年的GDP数值；(2) 使用地图做图，显示世界各国GDP在20年来的动态变化。建议选择显示至少超过5个国家的数据。
* 3 请使用地震数据（从http://www.r-project.org下载叫quakes数据；或从elearning下载），使用地图可视化的方法对数据进行可视化，展现地震的地点。
* You can see the detail of code [here](./Project5/Project5.py) and my report [here](./Project5/Report.pdf)

**Project6_Gray2RGB**
* 1 阅读了解VTK（[VTK - The Visualization Toolkit](https://www.vtk.org)），学习某个编程环境下调用VTK库进行可视化。
* 2 调用可视化渲染引擎库（如VTK），实现三维体数据完整的渲染过程（如光照模型，颜色设置等）。需要实现的渲染过程包括：(1) 等值面渲染，(2) 体渲染。请自己找一个体数据进行测试和结果展示。提交作业需要对使用数据进行说明，并提交源数据（或数据下载的网上链接）。
* 3 请设计一个方法消除等值面渲染结果中的碎片化的面单元，如下图所示，并使用数据进行测试并且展示可视化结果。心脏CT图像：[image_lr.nii.gz](./Project6/image/image_lr.nii.gz)
* You can see the detail of code [here](./Project6/VTKtest.py) and my report [here](./Project6/Report.pdf)
