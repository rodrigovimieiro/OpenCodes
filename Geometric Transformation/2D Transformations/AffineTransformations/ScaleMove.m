% Affine Transformations
% 07/2017
% Rodrigo Vimieiro

%%
close all;clear all;clc


%2D Triangle
Object = [1 2 2 3 3 3
          0 1 0 2 1 0];
      
plot(Object(1,1:end),Object(2,1:end),'r*')
hold on

%Origin
plot(0,0,'b.','MarkerSize',30)

% Homogeneous Coordinates for the point
Object = [Object;1 1 1 1 1 1];


s1 = 2;
s2 = 2;
xt = 2;
yt = 2;

%Scale and Move Matrix (Homogeneous Coordinates)
AffineTranfM = [s1 0 xt 
                0 s2 yt
                0  0 1];
   
%Affine transformation
Result = AffineTranfM * Object;

%Showing results
plot(Result(1,1:end),Result(2,1:end),'g*')
axis([-1 10 -1 10])
title('Affine Transf. (Scale&Move)');
xlabel('x')
ylabel('y')
legend('Original','Origem','Final')
grid on
  
  