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

xt = 4;
yt = 4;
%Translation Matrix (Homogeneous Coordinates)
AffineTranfM = [1 0 xt 
                0 1 yt
                0 0 1];
   
%Affine transformation
Result = AffineTranfM * Object;

%Showing results
plot(Result(1,1:end),Result(2,1:end),'g*')
axis([-1 10 -1 10])
title('Affine Transf. (Translation)');
grid on
  
  