%% Author: Rodrigo de Barros Vimieiro
% Date: September -th, 2017
% rodrigo.vimieiro@gmail.com
% =========================================================================
%{
Counter-clockwise rotation around axis with positive angles
%}
% =========================================================================
%% 3D Rotation Matrix Code
function [Xr,Yr,Zr] = rot3d(X,Y,Z, teta, eixo)

[m,n] = size(Z);

Xr = zeros(m,n);
Yr = Xr;
Zr = Xr;

M = ones(4,numel(Z));

k=1;
for i=1:1:m
    for j=1:1:n
        M(1,k) = X(i,j);
        M(2,k) = Y(i,j); 
        M(3,k) = Z(i,j); 
        k=k+1;
    end
end

switch eixo
    case 'x'
        % Rotation matrix 3D around X axis
        mRotate = [  1       0           0      0
                     0   cos(teta)  -sin(teta)  0
                     0   sin(teta)   cos(teta)  0
                     0       0           0      1];
    case 'y'
        % Rotation matrix 3D around Y axis
        mRotate = [ cos(teta)   0  sin(teta)   0
                     0          1       0      0
                   -sin(teta)   0  cos(teta)   0
                     0          0       0      1];
    case 'z'
        % Rotation matrix 3D around Z axis
        mRotate = [ cos(teta)   -sin(teta)   0  0
                    sin(teta)    cos(teta)   0  0
                       0            0        1  0
                       0            0        0  1];       
end
Mrotated = (mRotate*M);

k=1;
for i=1:1:m
    for j=1:1:n
        Xr(i,j) = Mrotated(1,k);
        Yr(i,j) = Mrotated(2,k);
        Zr(i,j) = Mrotated(3,k);
        k=k+1;
    end
end

end