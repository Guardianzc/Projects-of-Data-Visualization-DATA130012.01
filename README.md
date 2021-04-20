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
* You can see the detail of project [here](./Project1/Project1.py) and my report [here](./Project1/Project1.pdf)
    
**Project2_OTSU**
* 1 Restate the Basic Global Thresholding (BGT) algorithm so that it uses the histogram of an image instead of the image itself. 
* 2 Design an algorithm with the function of locally adaptive thresholding (e.g. based on moving average or local OSTU); implement the algorithm and test it on exemplar image(s).
* 3 编程实现线性插值算法（不能调用某个算法库里面的插值函数），并应用：读出一幅图像，利用线性插值把图片空间分辨率放大N倍，然后保存图片。
* You can see the detail of project [here](./Project2/Project2.py) and my report [here](./Project2/Project2.pdf)

**Project3_Smoothing,Sharpening & Fourier transform**
* 1 编程实现基于空间滤波器的（1）平滑操作、（2）锐化算法算法；并把算法应用与图片上，显示与原图的对比差别。备注：实现的代码不能调用某个算法库里面的函数实现平滑或锐化。
* 2 证明二维变量的离散傅里叶变换的卷积定理即：
f(x,y)*h(x,y) <==> F(u,v)H(u,v)
f(x,y)h(x,y)  <==> F(u,v)*H(u,v)

    其中, * 表示卷积运算。
* 3 编程实现基于课件中频率域滤波5步骤的：（1）低通平滑操作，并把算法应用与图片上，显示原图的频谱图、频域操作结果的频谱图，以及操作结果；（2）频率操作，去除大脑CT体膜Shepp-Logan图像中的条纹。
[freq_testimage_shepplogan.PNG](./Project3/freq_testimage_shepplogan.PNG)

备注：图像的时空-频域变换过程（即离散傅里叶变换和逆变换）可以调用库函数。
* You can see the detail of project [here](./Project3/Project3.py) and my report [here](./Project3/HW3_钟诚_16307110259.pdf)
    
**Project4_Cars**
* This project is a modified version of the Driverless Car assignment written by Chris Piech.
* In this project, I focus on the sensing system, which allows us to track other cars based on noisy sensor readings.(Key words: Bayesian network basics, Emission probabilities, Transition probabilities, Particle filtering)
* You can see the detail of project [here](./Project4_Cars/pj4.pdf) and my report [here](./Project4_Cars/Report.pdf)    

**FinalProject_GOMOKU**
* I do this project with [Ruipu Luo](https://rupertluo.github.io/)
* In this project, we design a fast and effective search algorithm for Gomoku playing.
* We use MCTS and Minimax search with $\alpha$-$\beta$ pruning algorithm for Gomoku and add the threat space algorithm to directly find those high-threat points in order to save search time. The  pruning  algorithm  can  reach  the  chess  power  of pisq7, which won the 24th place in the Gomoku AI Contest 2015.
* You can see the detail of project [here](./FinalProject_GOMOKU/Final_PJ.pdf) and my report [here](./FinalProject_GOMOKU/Alpha_Beta_Pruning_with_Thread_DetectionAlgorithm_for_Gomoku.pdf)
