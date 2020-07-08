function [outputImg] = thin_plate_spline(origin_control, new_control, inputImg)
    % input: original & new control point coord, shape: N*2
    % output: parameters of transformation
    % 获取图像大小、通道数
    [H,W,C] = size(inputImg);
    disp(H);disp(W);
    M = H * W;  % M=图像像素个数
    control_size = size(origin_control);
    N = control_size(1,1); % N=控制点个数
    % 申请空间
    outputImg = zeros(H,W,C);
    
    % 计算参数
    params = get_para(origin_control, new_control);
    
    % 计算outputImg对应的inputImg坐标
    % 生成输入矩阵
    X = zeros(M,2);
    for i=1:M
        X(i,:) = [floor((i-1)/W),mod(i-1,W)];
    end
    S = zeros(M,N);
    for i=1:M
        for j = 1:N
            S(i,j) = sigma(origin_control(j,:),X(i,:));
        end
    end
    O = ones(M,1);
    I = [O,X,S];
    % 计算output对应坐标Y
    Y = I*params;  % Y是M*2维矩阵
    
    % 进行线性插值，将像素填入对应的ouputImg位置
    for i=1:H
        for j=1:W
            outputImg(i,j,:) = linearInterp(inputImg, Y((i-1)*W+j,:));
        end
    end
    
    % print
    print_imgs(inputImg, outputImg)
end 

function [params] = get_para(origin_control, new_control)
    % input: original & new control point coord
    % output: parameters of transformation, in the form of (3+N) * 2
    T = get_T(origin_control);
    % create the RHS vector
    zeros_b = zeros(3,2);
    b = [new_control; zeros_b];
    % compute params [c,a,w]
    params = T \ b;
end

function [T] = get_T(origin_control)
    % this function creates the matrix T which will be used to 
    % compute the params
    sizes = size(origin_control);
    N = sizes(1,1);
    X = origin_control;
    ones_N = ones(N, 1);
    % construct matix S
    S = zeros(N, N);
    for i = 1:N
        for j = 1:N
            x_i = origin_control(i,:);
            x_j = origin_control(j,:);
            S(i,j) = sigma(x_i,x_j);
        end
    end
    % construct T
    T = zeros(N+3, N+3);
    T(1:N,1) = ones_N;
    T(1:N,2:3) = X;
    T(1:N,4:N+3) = S;
    T(N+1,4:N+3) = ones_N.';
    T(N+2:N+3,4:N+3) = X.';
end

function [s_ij] = sigma(x1, x2)
    % input: 2 coords of points
    % ouput: sigma(|x1-x2|)
    r = norm(x1 - x2);
    if r == 0
        s_ij = 0;
    else
        s_ij = r*r*log(r);
    end
end

function print_imgs(inputImg, outputImg)
    % original image
    subplot(1,2,1)
    imshow(inputImg)
    title('Original Image')

    % transformed image
    subplot(1,2,2)
    imshow(outputImg)
    title('Transformed Image')
end