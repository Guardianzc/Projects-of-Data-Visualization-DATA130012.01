function edgeCoords = region2edge(regionCoords)
%REGION2EDGE    将区域坐标集合变为区域边缘点集合
% 输入：
%   regionCoords    区域内点的坐标集合，N * 2的矩阵
% 输出：
%   edgeCoords      区域边缘点的坐标集合，M * 2的矩阵（M << N）

N = size(regionCoords,1);
mask = false(N,1);

% 纵坐标一阶差分，检测边缘点
diff = abs(regionCoords(2:end,2) - regionCoords(1:end-1,2) - 1) < eps;
mask(1:end-1) = diff;
mask(2:end) = diff;

% 检测第一列和最后一列的边缘点
mask(regionCoords(:,2) == regionCoords(1,2)) = true;
mask(regionCoords(:,2) == regionCoords(end,2)) = true;

edgeCoords = regionCoords(mask,:);

end

