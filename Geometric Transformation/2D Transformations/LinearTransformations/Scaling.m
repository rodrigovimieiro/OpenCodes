% Linear Transformations
% 07/2017
% Rodrigo Vimieiro

%%
close all;clear all;clc


%Cubo
Object = [2 3 2 3
          1 1 0 0];
      
plot(Object(1,1:end),Object(2,1:end),'r*')
hold on

%Origin
plot(0,0,'b.','MarkerSize',30)

%Scaling Matrix
sFx = 2;
sFy = 2;
LinearTranfM = [sFx 0
                0 sFy];
   
%Linear transformation
Result = LinearTranfM * Object;

%Showing results
plot(Result(1,1:end),Result(2,1:end),'g*')
axis([-1 10 -1 10])
title('L.T. Scaling');
grid on
  
  