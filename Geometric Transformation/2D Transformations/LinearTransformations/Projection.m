% Linear Transformations
% 07/2017
% Rodrigo Vimieiro

%%
close all;clear all;clc


%Triangle
Object = [1 2 2 3 3 3
          1 2 1 3 2 1];
      
plot(Object(1,1:end),Object(2,1:end),'r*')
hold on

%Origin
plot(0,0,'b.','MarkerSize',30)

%% Orthographic Projection Matrix -> X
LinearTranfM = [1 0
                0 0];
   
%Linear transformation
Result = LinearTranfM * Object;

%Showing results
plot(Result(1,1:end),Result(2,1:end),'g*')


%% Orthographic Projection Matrix -> Y
LinearTranfM = [0 0
                0 1];
   
%Linear transformation
Result = LinearTranfM * Object;

%Showing results
plot(Result(1,1:end),Result(2,1:end),'m*')
axis([-1 10 -1 10])
title('L.T. Orthographic Projection X&Y');
grid on
  
  