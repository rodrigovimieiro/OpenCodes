%% Author: Rodrigo de Barros Vimieiro
% Date: April, 2018
% rodrigo.vimieiro@gmail.com
% =========================================================================
%{
% -------------------------------------------------------------------------
%                 evalASF(volume,roi,bg,sliceInFocus)
% -------------------------------------------------------------------------
%     DESCRIPTION:
%  
%     INPUT:
% 
%     - 
% 
%     OUTPUT:
% 
%     - .
% 
%     Reference: Jiang Hsieh's book (second edition)
% 
%     -----------------------------------------------------------------------
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
%% ASF Code
function [slicesEvals,asf] = evalASF(volume,roi,bg,sliceInFocus)

sliceGap = 5;
slicesEvals = sliceInFocus-sliceGap:sliceInFocus+sliceGap;

numROI = size(roi.ii,2);

for n=1:numROI
    
    iiR = roi.ii{n};
    jjR = roi.jj{n};
    iiB = bg.ii{n};
    jjB = bg.jj{n}; 
    
    denoInFocus = mean(mean(volume(iiR,jjR,sliceInFocus))) - mean(mean(volume(iiB,jjB,sliceInFocus)));

    for zInd=1:numel(slicesEvals) 

        sliceOutFocus =  slicesEvals(zInd);
        
        numOutFocus = mean(mean(volume(iiR,jjR,sliceOutFocus))) - mean(mean(volume(iiB,jjB,sliceOutFocus)));
        asf(n,zInd) = numOutFocus / denoInFocus;

    end
end

asf = mean(asf,1);

end