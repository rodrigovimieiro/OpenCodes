%% Author: Rodrigo de Barros Vimieiro
% Date: October, 2018
% rodrigo.vimieiro@gmail.com
% =========================================================================
%{
% -------------------------------------------------------------------------
%                 
% -------------------------------------------------------------------------
%     DESCRIPTION:
% 
%     Reference: 
%     - Branchless Distance Driven Projection and Backprojection,
%     Samit Basu and Bruno De Man (2006)
%     ---------------------------------------------------------------------
%     Copyright (C) <2018>  <Rodrigo de Barros Vimieiro>
% 
%     This program is free software: you can redistribute it and/or modify
%     it under the terms of the GNU General Public License as published by
%     the Free Software Foundation, either version 3 of the License, or
%     (at your option) any later version.
% 
%     This program is distributed in the hope that it will be useful,
%     but WITHOUT ANY WARRANTY; without even the implied warranty of
%     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
%     GNU General Public License for more details.
% 
%     You should have received a copy of the GNU General Public License
%     along with this program.  If not, see <http://www.gnu.org/licenses/>.
%}
% =========================================================================
%% Branchless Distance Driven Paper 

clc; clear;close all

% Pixel boundaries
p_i = 1:5:105;

% Number of pixels
n_p = size(p_i,2)-1;

% Value of pixels
p_v = rand(1,n_p) - 0.5;



% p(x) function
p_x = 0;
figure,hold on
for xi=1:size(p_i,2)
    for i=1:n_p    
        p_x = p_x + p_v(i) * rect( (p_i(xi) -(( p_i(i+1)+ p_i(i) )/2)) / (p_i(i+1)- p_i(i)) );
    end
    plot(p_i(xi),p_x,'*r')
    p_x = 0;
end
stem(p_i(2:end),p_v,'b.')

% P(x) function   -> Integral of p(x)
P_x = 0;
figure,hold on

pj = 5; %size(p_i,2)
pj_i = pj;
 for pj_i=2:pj
    for i=1:pj-1    
        P_x = P_x + p_v(i) * (p_i(i+1)- p_i(i)) * ramp( (p_i(pj_i) -(( p_i(i+1)+ p_i(i) )/2)) / (p_i(i+1)- p_i(i)) );
        rampV(pj_i,i) = ramp( (p_i(pj_i) -(( p_i(i+1)+ p_i(i) )/2)) / (p_i(i+1)- p_i(i)) );
    end
    plot(p_i(pj_i),P_x,'*r')
    P_x = 0;
 end




function y = rect(x)

y = (x>=-0.5) && (x<0.5);

end

function y = ramp(x)

if(x<-0.5)
    y = 0;
elseif((x>=-0.5) && (x<0.5))
    y = x+0.5;
else
    y=1;
end

end