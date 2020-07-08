function [outputImg] = localAffine_inv(inputImg,transform,transMap,varargin)
%LOCALAFFINE_INV    局部仿射变换（反向图变换），将目标图坐标映射到输入图坐标，
%                   用输入图插值后的像素填充目标图中相应的位置
% 输入：
%   ·inputImg	输入单通道/多通道图像矩阵
%   ·transform	元胞向量，元胞的每个元素为每个区域对应的 3 * 3 反向仿射变换矩阵;
%                变换以图片中心为原点
%   ·transMap   目标图中每个像素点需要进行的反向仿射变换；0表示变换区域外的点，
%                大于0的数字k表示该区域需要进行transform{k}的仿射变换
%   ·varargin   包含以下字段的默认参数
%       - 'dist_e'      根据距离计算权值时的指数，默认为1
%       - 'visualize'   布尔型参数，是否进行可视化；默认为true
% 输出：
%   ·outputImg  经过局部仿射变换（反向图变换）的图像

%% 初始化
% 输入参数解析
p = inputParser;                                    % 解析器实例
p.addRequired('img',@(x)ismatrix(x)||ndims(x)==3)   % 单通道/多通道图像矩阵
p.addRequired('transform',@(x)iscell(x))            % 元胞向量
p.addRequired('transMap',@(x)ismatrix(x))           % 二维矩阵
p.addParameter('dist_e',1,@(x)isscalar(x));         % 标量
p.addParameter('visualize',true,@(x)islogical(x));  % 布尔参数
p.parse(inputImg,transform,transMap,varargin{:});   % 解析

% 获取图像大小、通道数
[H,W,C] = size(inputImg);
% 申请空间
outputImg = zeros(H,W,C);

% 生成中心化坐标矩阵
coord = zeros([H,W,2]);     
coord(:,:,1) = repmat((1:H)'-H/2,[1,W]);
coord(:,:,2) = repmat((1:W)-W/2,[H,1]);
transMap = repmat(transMap,[1,1,2]);    % 将transMap维度与coord统一，方便操作

%% 计算局部区域内的仿射变换
numTrans = numel(transform);            % 仿射变换的种类数
inRegionCoord = cell(1,numTrans);       % 各局部区域的坐标集合
for t = 1:numTrans
    inRegionCoord{t} = reshape(coord(transMap == t),[],2)'; % 需要第t种变换的目标图像素的坐标
    numCoord = size(inRegionCoord{t},2);                    % 坐标的数量
    transCoord = transform{t} * [inRegionCoord{t};ones(1,numCoord)];    % 仿射变换
    transCoord = transCoord(1:2,:);                         % 去掉最后一行的1
    for i = 1:numCoord
        dst = num2cell(inRegionCoord{t}(:,i) + [H/2;W/2]);  % 需要填充的坐标
        outputImg(dst{:},:) = linearInterp(inputImg,transCoord(:,i)+[H/2;W/2]); % 填充
    end
end

%% 计算局部区域外的加权仿射变换
offRegionCoord = reshape(coord(transMap == 0),1,[],2);  % 局部区域外的坐标集合，增加一维方便矩阵计算
numCoord = size(offRegionCoord,2);                      % 区域外点的个数

% 计算区域外的点到每个区域的最小距离
dist_power = zeros(numTrans,numCoord);              % 申请空间
for t = 1:numTrans
    inRegionEdge = region2edge(inRegionCoord{t}');  % 局部区域的边缘点
    inRegionEdge = reshape(inRegionEdge,[],1,2);
    dist_tmp = repmat(offRegionCoord,[size(inRegionEdge,1),1,1]) - ...
        repmat(inRegionEdge,[1,numCoord,1]);               % 计算距离
    dist_tmp = sum(dist_tmp.^2,3) .^ (1 / 2 * p.Results.dist_e);    % 距离的指数
    dist_power(t,:) = 1 ./ (min(dist_tmp,[],1) - 1 + eps);  % 区域外的点到该区域的最短距离-1（的倒数）
end

% 根据距离计算加权仿射变换
offRegionCoord = reshape(offRegionCoord,[],2)';     % 去掉之前增加的维度
transCoord = zeros(2,numCoord);                     % 初始化
for t = 1:numTrans
    tmpCoord = transform{t} * [offRegionCoord;ones(1,numCoord)];        % 仿射变换
    weight = dist_power(t,:) ./ sum(dist_power,1);                      % 计算权重
    transCoord = transCoord + tmpCoord(1:2,:) .* repmat(weight,[2,1]);  % 去掉最后一行的1，按权重求和
end

% 根据反向变换后的坐标进行填充
for i = 1:numCoord
    dst = num2cell(offRegionCoord(:,i) + [H/2;W/2]);                        % 需要填充的坐标
    outputImg(dst{:},:) = linearInterp(inputImg,transCoord(:,i)+[H/2;W/2]); % 填充
end

%% 可视化
if p.Results.visualize
    % 原图
    subplot(1,2,1)
    imshow(inputImg)
    title('Original Image')
    
    % 基于反向局部仿射变换后的图片
    subplot(1,2,2)
    imshow(outputImg)
    title('Transformed Image')
end

end

