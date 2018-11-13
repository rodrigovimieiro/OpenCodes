% Linear Transformations
% 07/2017
% Rodrigo Vimieiro

%%
close all;clear all;clc

%Triangle
Object = [2 3 3 4 4 4
          0 1 0 2 1 0];
      
plot(Object(1,1:end),Object(2,1:end),'r*')
hold on

%Origin
plot(0,0,'b.','MarkerSize',30)

%Reflection Matrix
LinearTranfM = [0 1
                1 0];
   
%Linear transformation
Result = LinearTranfM * Object;

%Showing results
plot(Result(1,1:end),Result(2,1:end),'g*')
axis([-1 10 -1 10])
title('L.T. Reflection');
grid on
  
  