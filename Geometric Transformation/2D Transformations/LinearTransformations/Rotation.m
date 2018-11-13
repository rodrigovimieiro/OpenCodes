% Linear Transformations
% 07/2017
% Rodrigo Vimieiro

%%
close all;clear all;clc


%Cubo
Object = [  2    3   2   3
          -0.5 -0.5 0.5 0.5];
      
plot(Object(1,1:end),Object(2,1:end),'r*')
hold on

%Origin
plot(0,0,'b.','MarkerSize',30)

%% Rotation Matrix Counter-Clockwise
teta = 45;
LinearTranfM = [cosd(teta) -sind(teta)
                sind(teta)  cosd(teta)];
   
%Linear transformation
Result = LinearTranfM * Object;

%Showing results
plot(Result(1,1:end),Result(2,1:end),'g*')

%% Rotation Matrix Clockwise
teta = 45;
LinearTranfM = [ cosd(teta) sind(teta)
                -sind(teta) cosd(teta)];
   
%Linear transformation
Result = LinearTranfM * Object;

%Showing results
plot(Result(1,1:end),Result(2,1:end),'m*')
axis([-3 10 -3 10])
title('L.T. Rotation Counter-Clockwise');
grid on
  
  