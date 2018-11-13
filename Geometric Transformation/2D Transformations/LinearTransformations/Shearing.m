% Linear Transformations
% 07/2017
% Rodrigo Vimieiro

%%
close all;clear all;clc

% Paralelogram Vertical
Object = [1 1 1 2 2 2
          0 1 2 0 1 2];
      
plot(Object(1,1:end),Object(2,1:end),'r*')
hold on

% Origin
plot(0,0,'b.','MarkerSize',30)

% Shearing Matrix -> X
sF = 2;
LinearTranfM = [1 sF
                0 1];
   
%Linear transformation
Result = LinearTranfM * Object;

% Showing results
plot(Result(1,1:end),Result(2,1:end),'g*')
axis([-1 10 -1 10])
title('L.T. Shearing X Direction');
grid on

%%

% Paralelogram Horizontal
Object = [1 2 3 1 2 3
          0 0 0 1 1 1];

figure
plot(Object(1,1:end),Object(2,1:end),'r*')
hold on

% Origin
plot(0,0,'b.','MarkerSize',30)

% Shearing Matrix -> Y
sF = 2;
LinearTranfM = [ 1 0
                sF 1];
   
%Linear transformation
Result = LinearTranfM * Object;

% Showing results
plot(Result(1,1:end),Result(2,1:end),'g*')
axis([-1 10 -1 10])
title('L.T. Shearing Y Direction');
grid on


  
  