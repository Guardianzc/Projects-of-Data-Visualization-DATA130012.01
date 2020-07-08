function data_interp = linearInterp(img,coord)
%LINEARINTERP   图像线性插值
% 输入：
%   img         单通道/多通道图像矩阵（MATLAB copy-on-write特性导致并不会发生值传递）
%   coord       需要插值的坐标向量，长度与图像维度匹配
% 输出：
%   data_interp 插值后得到的数据点

%% 初始化
% 维度匹配检查
if (length(coord) ~= 2)
    error('Dimension error!');
end
[H,W,C] = size(img);

% 申请空间
data_interp = zeros(1,1,C);

%% 线性插值
coord(1) = min(max(1,coord(1)),H);  % 处理第一维越界
coord(2) = min(max(1,coord(2)),W);  % 处理第二维越界
coord_fl = floor(coord);            % 坐标向下取整，确定下界
dist = coord - coord_fl;            % 计算距离
w1 = [1-dist(1),dist(1)];           % 第一维权重
w2 = [1-dist(2),dist(2)];           % 第二维权重

% 判断坐标点是否为整数，简化计算
if abs(coord_fl - coord) < eps              % 两个维度均为整数，无需插值
    data_interp = img(coord(1),coord(2),:);
elseif abs(coord_fl(1) - coord(1)) < eps    % 第一维为整数
    data_interp = w2 * reshape(img(coord(1),coord_fl(2):coord_fl(2)+1,:),[2,C]);
elseif abs(coord_fl(2) - coord(2)) < eps    % 第二维为整数
    data_interp = w1 * reshape(img(coord_fl(1):coord_fl(1)+1,coord(2),:),[2,C]);
else                                        % 两个维度均为小数
    m = img(coord_fl(1):coord_fl(1)+1,coord_fl(2):coord_fl(2)+1,:);
    for ch = 1:C
        data_interp(ch) = w1 * m(:,:,ch) * w2';
    end
end

end
