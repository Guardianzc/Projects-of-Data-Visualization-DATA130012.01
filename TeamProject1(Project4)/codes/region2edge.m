function edgeCoords = region2edge(regionCoords)
%REGION2EDGE    ���������꼯�ϱ�Ϊ�����Ե�㼯��
% ���룺
%   regionCoords    �����ڵ�����꼯�ϣ�N * 2�ľ���
% �����
%   edgeCoords      �����Ե������꼯�ϣ�M * 2�ľ���M << N��

N = size(regionCoords,1);
mask = false(N,1);

% ������һ�ײ�֣�����Ե��
diff = abs(regionCoords(2:end,2) - regionCoords(1:end-1,2) - 1) < eps;
mask(1:end-1) = diff;
mask(2:end) = diff;

% ����һ�к����һ�еı�Ե��
mask(regionCoords(:,2) == regionCoords(1,2)) = true;
mask(regionCoords(:,2) == regionCoords(end,2)) = true;

edgeCoords = regionCoords(mask,:);

end

