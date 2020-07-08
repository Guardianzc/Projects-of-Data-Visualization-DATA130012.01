function data_interp = linearInterp(img,coord)
%LINEARINTERP   ͼ�����Բ�ֵ
% ���룺
%   img         ��ͨ��/��ͨ��ͼ�����MATLAB copy-on-write���Ե��²����ᷢ��ֵ���ݣ�
%   coord       ��Ҫ��ֵ������������������ͼ��ά��ƥ��
% �����
%   data_interp ��ֵ��õ������ݵ�

%% ��ʼ��
% ά��ƥ����
if (length(coord) ~= 2)
    error('Dimension error!');
end
[H,W,C] = size(img);

% ����ռ�
data_interp = zeros(1,1,C);

%% ���Բ�ֵ
coord(1) = min(max(1,coord(1)),H);  % �����һάԽ��
coord(2) = min(max(1,coord(2)),W);  % ����ڶ�άԽ��
coord_fl = floor(coord);            % ��������ȡ����ȷ���½�
dist = coord - coord_fl;            % �������
w1 = [1-dist(1),dist(1)];           % ��һάȨ��
w2 = [1-dist(2),dist(2)];           % �ڶ�άȨ��

% �ж�������Ƿ�Ϊ�������򻯼���
if abs(coord_fl - coord) < eps              % ����ά�Ⱦ�Ϊ�����������ֵ
    data_interp = img(coord(1),coord(2),:);
elseif abs(coord_fl(1) - coord(1)) < eps    % ��һάΪ����
    data_interp = w2 * reshape(img(coord(1),coord_fl(2):coord_fl(2)+1,:),[2,C]);
elseif abs(coord_fl(2) - coord(2)) < eps    % �ڶ�άΪ����
    data_interp = w1 * reshape(img(coord_fl(1):coord_fl(1)+1,coord(2),:),[2,C]);
else                                        % ����ά�Ⱦ�ΪС��
    m = img(coord_fl(1):coord_fl(1)+1,coord_fl(2):coord_fl(2)+1,:);
    for ch = 1:C
        data_interp(ch) = w1 * m(:,:,ch) * w2';
    end
end

end
