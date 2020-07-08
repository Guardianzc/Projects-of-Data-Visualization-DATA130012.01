function [transform] = form_transform(shape_A, shape_goal, origin, map, style)
if style == 1
    % 形成二维坐标（,3）——(x,y,1)，然后求逆，这里是正方形框，故有四个参数
    for i = 1:2
        %锟斤拷一锟斤拷
        origin(i) = origin(i) - shape_A(1)/2;
        map(i) = map(i) - shape_goal(1)/2;
    end
    for i = 3:4
        origin(i) = origin(i) - shape_A(2)/2;
        map(i) = map(i) - shape_goal(2)/2;    
    end
    % 锟轿成撅拷锟斤拷然锟斤拷锟斤拷A
    origin_matrix = [origin(1),origin(3),1; origin(1),origin(4),1; origin(2),origin(3),1; origin(2),origin(4),1]';
    map_matrix = [map(1),map(3),1; map(1),map(4),1; map(2),map(3),1; map(2),map(4),1]';
    % origin = transform * transmap
end

if style == 2
    for i = 1:2
        %归一化
        origin(i) = origin(i) - shape_A(1)/2;
        map(i) = map(i) - shape_goal(1)/2;
    end
    for i = 3:5
        origin(i) = origin(i) - shape_A(2)/2;
        map(i) = map(i) - shape_goal(2)/2;    
    end
    %同样的，这里是5个点（三角形）的情况
    origin_matrix = [origin(1),origin(4),1; origin(2),origin(3),1; origin(2),origin(4),1; origin(2),origin(5),1]';
    map_matrix = [map(1), map(4), 1; map(2), map(3), 1;map(2), map(4), 1;map(2), map(5), 1;]'; 
end

if style == 3
    for i = 1:3
        %归一化
        origin(i) = origin(i) - shape_A(1)/2;
        map(i) = map(i) - shape_goal(1)/2;
    end
    for i = 4:6
        origin(i) = origin(i) - shape_A(2)/2;
        map(i) = map(i) - shape_goal(2)/2;    
    end 
    origin_matrix = [origin(1),origin(5),1; origin(2),origin(4),1; origin(2),origin(5),1; origin(2),origin(6),1; origin(3),origin(5),1]';
    map_matrix = [map(1), map(5), 1; map(2), map(4), 1;map(2), map(5), 1;map(2), map(6), 1;map(3), map(5), 1;]'; 
end
    transform = origin_matrix * pinv(map_matrix);
end