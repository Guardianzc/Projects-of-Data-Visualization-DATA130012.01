function [transMap] = form_transMap(shape, goal_control, style)
    % 这里生成transmap, 
	% goal_control :目标图控制点, 类型为cell
	% shape: 目标图大小
    transMap = zeros(shape(1:2));
    
    for i = 1:size(goal_control,2)
        if style{i} == 1
            % 矩形
            transMap(goal_control{i}(1):goal_control{i}(2), goal_control{i}(3):goal_control{i}(4)) = i;
        end
        if style{i} == 4
            % 梯形
            Trapezoid = goal_control{i};
            for j = Trapezoid(1):Trapezoid(2)
            transMap(j, fix(Trapezoid(3) - (Trapezoid(3)-Trapezoid(5)) / (Trapezoid(2)-Trapezoid(1)) * (j-Trapezoid(1))) : fix((Trapezoid(6)-Trapezoid(4)) / (Trapezoid(2)-Trapezoid(1)) * (j-Trapezoid(1)) + Trapezoid(4))) = i;
            end
		end
		
		if style{i} == 2
		    % 三角形
			Tri = goal_control{i};
			for j = Tri(1):Tri(2)
			    transMap(j, fix(Tri(4) - (Tri(4)-Tri(3)) / (Tri(2)-Tri(1)) * (j-Tri(1))) : fix((Tri(5)-Tri(4)) / (Tri(2)-Tri(1)) * (j-Tri(1)) + Tri(4))) = i;
			end
		end
		
		if style{i} == 3
		    diamond = goal_control{i};
			for j = diamond(1):diamond(2)
			    transMap(j, fix(diamond(5) - (diamond(5)-diamond(4)) / (diamond(2)-diamond(1)) * (j-diamond(1))) : fix((diamond(6)-diamond(5)) / (diamond(2)-diamond(1)) * (j-diamond(1)) + diamond(5))) = i;
			end
			for j = diamond(2):diamond(3)
			    transMap(j, fix(diamond(4) + (diamond(5)-diamond(4)) / (diamond(3)-diamond(2)) * (j-diamond(2))) : fix(diamond(6) - (diamond(6)-diamond(5)) / (diamond(3)-diamond(2)) * (j-diamond(2)) )) = i;
			end			
			
    end
end