%% Author: Rodrigo de Barros Vimieiro
% Date: July, 2018
% rodrigo.vimieiro@gmail.com
% =========================================================================
%{
% -------------------------------------------------------------------------
%                 
% -------------------------------------------------------------------------
%     DESCRIPTION:
% 
%     Reference: Three-Dimensional Digital Tomosynthesis - Yulia Levakhina (2014)
% 
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
%% 2-D Distance Driven Code
clear; clc;

global draw;
draw = 0;

%% Geometry Definitions

% Geometry
geo.DSD = 100000;%70;       % Distance from source to detector (mm)
geo.DSO =  99700;%50;       % Distance from source to iso-center
geo.pSize = 1;              % Square pixel size (mm)
geo.dSize = 0.5;            % Square detector size (mm)

geo.nPix = 256;%20;         % Number of pixels elements (Row and Col)
geo.nDet = 1024;%50;        % Number of detector elements

% Angle
deg = 1;
geo.theta = deg2rad(0:deg:360-deg);

% Iso-center
geo.isoX = 0;
geo.isoY = 0;

% Make the Phantom Image
phantomImg = phantom(geo.nPix ,geo.nPix );
phantomImg = mat2gray(phantomImg); % set min of image to zero

% Projection
sinogram = projection(phantomImg,geo);

% Back-projection
image = backprojection(sinogram,geo);

%% Projection
function sinogram = projection(phantom,geo)

global draw;

DSD = geo.DSD;      
DSO = geo.DSO;      
pSize = geo.pSize;    
dSize = geo.dSize;    
nPix = geo.nPix;       
nDet = geo.nDet;     
theta = geo.theta; 

% Detector boundaries
detX = (-(nDet/2):(nDet/2)) .* dSize;
detY = (-(DSD-DSO)-(dSize/2)) .* ones(1,nDet+1);

% Pixel boundaries
[pixelX,pixelY]=meshgrid(-(nPix/2):(nPix/2));
pixelX = pixelX .* pSize;
pixelY = flipud(pixelY - pSize/2);

% Tube
tubeX = 0;     
tubeY = DSO;    

% Iso-center
isoX = geo.isoX;
isoY = geo.isoY;

sinogram = zeros(size(theta,2),nDet);

% For each projection
for proj=1:size(theta,2)
    
    angle = theta(proj);
       
    % Tubre rotation
    rtubeX = ( (tubeX - isoX )*cos(angle) - (tubeY - isoY )*sin(angle) ) + isoX;
    rtubeY = ( (tubeX - isoX )*sin(angle) + (tubeY - isoY )*cos(angle) ) + isoY;

    % Detector rotation
    rdetX = ( (detX - isoX ).*cos(angle) - (detY - isoY ).*sin(angle) ) + isoX;
    rdetY = ( (detX - isoX ).*sin(angle) + (detY - isoY ).*cos(angle) ) + isoY;
    
    if(draw)
        drawGeo(rtubeX,rtubeY,pixelX,pixelY,rdetX,rdetY)
    end    
    
    % Define angle case and which axis it it project boundaries
    % Case 1 
    if(((angle>=0)&&(angle<=pi/4))||(angle>=7*pi/4))       
        axisXCase = 1;   % Map on X axis
        angleCase = 1;
        c1=0;c2=1;
    else
        % Case 2
        if((angle>pi/4)&&(angle<3*pi/4))
            axisXCase = 0;   % Map on Y axis
            angleCase = 2;
            c1=0;c2=1;
        else
            % Case 3
            if(((angle>=3*pi/4)&&(angle<=5*pi/4)))
                axisXCase = 1;   % Map on X axis
                angleCase = 3;
                c1=0;c2=-1;
            else
            % Case 4
                axisXCase = 0;   % Map on Y axis
                angleCase = 4;
                c1=0;c2=-1;
            end
        end
    end
    
    % Mapping boundaries into a commum axis
    if(axisXCase)
        detm = mapp2x(rtubeX,rtubeY,rdetX,rdetY);
        pixm = mapp2x(rtubeX,rtubeY,pixelX,pixelY);
        img = phantom;
    else
        detm = mapp2y(rtubeX,rtubeY,rdetX,rdetY);
        pixm = fliplr(mapp2y(rtubeX,rtubeY,pixelX,pixelY)');
        img = fliplr(phantom');
    end
    
               
    center_det = floor((nDet+1)/2+1);
    if(axisXCase) 
        % X-Ray pixel intersection calculation
        L = abs(pSize/cos(angle)); % This account for parallel-beam
        % Correction for fan-beam
        for n=1:nDet
            L1(n)=sqrt((rtubeX-detm(center_det)).^2+(rtubeY-0).^2)...
            /sqrt((rtubeX-detm(n)).^2+(rtubeY-0).^2);
        end
    else
        % X-Ray pixel intersection calculation
        L = abs(pSize/sin(angle)); % This account for parallel-beam
        % Correction for fan-beam
        for n=1:nDet
            L1(n)=sqrt((rtubeX-0).^2+(rtubeY-detm(center_det)).^2)...
            /sqrt((rtubeX-0).^2+(rtubeY-detm(n)).^2);
        end           
    end     
    L = L./L1;
    
    pixIstart = 1;
    pixIinc = 1;
    if((angleCase == 1)||(angleCase == 2))
        detIstart = 1;
        detIinc = 1;
    else
        detIstart = nDet+1;
        detIinc = -1;
    end

    
    deltaDetm = detm(detIstart+detIinc)- detm(detIstart); % Mapped detector length
    deltaPixm = pixm(1,2)- pixm(1,1);   % Mapped pixel length
    
    sinoTmp = zeros(1,nDet);
    
    % For each row
    for row=1:nPix
        
        rowm = pixm(row,:); % Get first mapped row from image.
        
        detInd = detIstart;
        pixInd = pixIstart;            
        
        % Find first detector overlap maped with pixel maped (Case 1)
        if(detm(detInd)-rowm(pixIstart)<-deltaDetm)
            while((detm(detInd)-rowm(pixIstart)<-deltaDetm))            
                detInd = detInd + detIinc;            
            end
        else
        % Find first pixel overlap maped with detector maped (Case 2)           
            if(detm(detIstart)-rowm(pixInd)>deltaPixm)
                while(detm(detIstart)-rowm(pixInd)>deltaPixm)            
                    pixInd = pixInd + pixIinc;            
                end
            end
        end
        
%         deltaD = detm(detInd)-rowm(pixIstart);        
%         % Find first detector overlap maped with pixel maped (Case 1)
%         if(deltaD<0)
%             while((deltaD<0)&&(abs(deltaD)>deltaDetm)) 
%                 deltaD = detm(detInd)-rowm(pixIstart);
%                 detInd = detInd + 1;            
%             end
%             detInd = detInd - 1;
%         else           
%             while((deltaD>0)&&(abs(deltaD)>deltaPixm))
%                 deltaD = detm(detIstart)-rowm(pixInd);
%                 pixInd = pixInd + 1;            
%             end
%             pixInd = pixInd - 1;
%         end

        % Get the left coordinate of the first overlap
        % Try the following lines for a better understanding
        % % ---------------------------------------------------------------
        % %   plot(detm,zeros(1,size(detm,2)),'r.','MarkerSize',6)
        % %   hold on
        % %   plot(pixm(1,:),zeros(1,size(pixm,2)),'b.','MarkerSize',6)
        % %   hold off
        % %   legend('Detector Boundaries','Pixel Boundaries')
        % % ---------------------------------------------------------------
        if( detm(detInd) < rowm(pixInd) )
            moving_left_boundary = rowm(pixInd);            
        else
            moving_left_boundary = detm(detInd);
        end
               
        % Loop over intersections
        while((detInd<=nDet)&&(pixInd<=nPix)&&(detInd>=0))
            % Case A, when you jump to the next detector boundarie but stay
            % in the same pixel
            if(detm(detInd+c2)<=rowm(pixInd+1))
                overLap = detm(detInd+c2)- moving_left_boundary; % Overlap Calculation
                sinoTmp(detInd) = sinoTmp(detInd) + overLap * img(row,pixInd) / deltaDetm;
                detInd = detInd + detIinc;
                moving_left_boundary = detm(detInd + c1);
            else
            % Case B, when you jump to the next pixel boundarie but stay 
            % in the same detector
                overLap = rowm(pixInd+1)- moving_left_boundary; % Overlap Calculation
                sinoTmp(detInd) = sinoTmp(detInd) + overLap * img(row,pixInd) / deltaDetm;
                pixInd = pixInd + pixIinc;
                moving_left_boundary = rowm(pixInd);
            end
        end % Overlap loop                             
    end % Row loop 
    
    sinogram(proj,:) = sinoTmp .* L;
    
end % Projection loop

end

%% Backprojection
function reconImg = backprojection(sinogram,geo)

global draw;

DSD = geo.DSD;      
DSO = geo.DSO;      
pSize = geo.pSize;    
dSize = geo.dSize;    
nPix = geo.nPix;       
nDet = geo.nDet;     
theta = geo.theta; 

% Detector boundaries
detX = (-(nDet/2):(nDet/2)) .* dSize;
detY = (-(DSD-DSO)-(dSize/2)) .* ones(1,nDet+1);

% Pixel boundaries
[pixelX,pixelY]=meshgrid(-(nPix/2):(nPix/2));
pixelX = pixelX .* pSize;
pixelY = flipud(pixelY - pSize/2);

% Tube
tubeX = 0;     
tubeY = DSO;    

% Iso-center
isoX = geo.isoX;
isoY = geo.isoY;

reconImg = zeros(nPix,nPix);
reconImgTmp = reconImg;

% For each projection
for proj=1:size(theta,2)
    
    angle = theta(proj);
       
    % Tubre rotation
    rtubeX = ( (tubeX - isoX )*cos(angle) - (tubeY - isoY )*sin(angle) ) + isoX;
    rtubeY = ( (tubeX - isoX )*sin(angle) + (tubeY - isoY )*cos(angle) ) + isoX;

    % Detector rotation
    rdetX = ( (detX - isoX ).*cos(angle) - (detY - isoY ).*sin(angle) ) + isoX;
    rdetY = ( (detX - isoX ).*sin(angle) + (detY - isoY ).*cos(angle) ) + isoX;
    
    if(draw)
        drawGeo(rtubeX,rtubeY,pixelX,pixelY,rdetX,rdetY)
    end    
    
    % Define angle case and which axis it it project boundaries
    % Case 1 
    if(((angle>=0)&&(angle<=pi/4))||(angle>=7*pi/4))       
        axisXCase = 1;   % Map on X axis
        angleCase = 1;
        c1=0;c2=1;
    else
        % Case 2
        if((angle>pi/4)&&(angle<3*pi/4))
            axisXCase = 0;   % Map on Y axis
            angleCase = 2;
            c1=0;c2=1;
        else
            % Case 3
            if(((angle>=3*pi/4)&&(angle<=5*pi/4)))
                axisXCase = 1;   % Map on X axis
                angleCase = 3;
                c1=0;c2=-1;
            else
            % Case 4
                axisXCase = 0;   % Map on Y axis
                angleCase = 4;
                c1=0;c2=-1;
            end
        end
    end
    
    % Mapping boundaries into a commum axis
    if(axisXCase)
        detm = mapp2x(rtubeX,rtubeY,rdetX,rdetY);
        pixm = mapp2x(rtubeX,rtubeY,pixelX,pixelY);
    else
        detm = mapp2y(rtubeX,rtubeY,rdetX,rdetY);
        pixm = fliplr(mapp2y(rtubeX,rtubeY,pixelX,pixelY)');
    end
    
               
    center_det = floor((nPix+1)/2+1);
    if(axisXCase) 
        % X-Ray pixel intersection calculation
        L = abs(pSize/cos(angle)); % This account for parallel-beam
        % Correction for fan-beam
        for n=1:nPix
            L1(n)=sqrt((rtubeX-pixm(center_det)).^2+(rtubeY-0).^2)...
            /sqrt((rtubeX-pixm(n)).^2+(rtubeY-0).^2);
        end
    else
        % X-Ray pixel intersection calculation
        L = abs(pSize/sin(angle)); % This account for parallel-beam
        % Correction for fan-beam
        for n=1:nPix
            L1(n)=sqrt((rtubeX-0).^2+(rtubeY-pixm(center_det)).^2)...
            /sqrt((rtubeX-0).^2+(rtubeY-pixm(n)).^2);
        end           
    end     
    L = L./L1;
    
    pixIstart = 1;
    pixIinc = 1;
    if((angleCase == 1)||(angleCase == 2))
        detIstart = 1;
        detIinc = 1;
    else
        detIstart = nDet+1;
        detIinc = -1;
    end

    
    deltaDetm = detm(detIstart+detIinc)- detm(detIstart); % Mapped detector length
    deltaPixm = pixm(1,2)- pixm(1,1);   % Mapped pixel length    
    
    % For each row
    for row=1:nPix
        
        reconTmp = zeros(1,nPix);
        
        rowm = pixm(row,:); % Get first mapped row from image.
        
        detInd = detIstart;
        pixInd = pixIstart;            
        
        % Find first detector overlap maped with pixel maped (Case 1)
        if(detm(detInd)-rowm(pixIstart)<-deltaDetm)
            while((detm(detInd)-rowm(pixIstart)<-deltaDetm))            
                detInd = detInd + detIinc;            
            end
        else
        % Find first pixel overlap maped with detector maped (Case 2)           
            if(detm(detIstart)-rowm(pixInd)>deltaPixm)
                while(detm(detIstart)-rowm(pixInd)>deltaPixm)            
                    pixInd = pixInd + pixIinc;            
                end
            end
        end
        
        % Get the left coordinate of the first overlap
        % Try the following lines for a better understanding
        % % ---------------------------------------------------------------
        % %   plot(detm,zeros(1,size(detm,2)),'r.','MarkerSize',6)
        % %   hold on
        % %   plot(pixm(1,:),zeros(1,size(pixm,2)),'b.','MarkerSize',6)
        % %   hold off
        % %   legend('Detector Boundaries','Pixel Boundaries')
        % % ---------------------------------------------------------------
        if( detm(detInd) < rowm(pixInd) )
            moving_left_boundary = rowm(pixInd);            
        else
            moving_left_boundary = detm(detInd);
        end
               
        % Loop over intersections
        while((detInd<=nDet)&&(pixInd<=nPix)&&(detInd>=0))
            % Case A, when you jump to the next detector boundarie but stay
            % in the same pixel
            if(detm(detInd+c2)<=rowm(pixInd+1))
                overLap = detm(detInd+c2)- moving_left_boundary; % Overlap Calculation
                reconTmp(pixInd) =  reconTmp(pixInd) + overLap * sinogram(proj,detInd) / deltaDetm;
                detInd = detInd + detIinc;
                moving_left_boundary = detm(detInd + c1);
            else
            % Case B, when you jump to the next pixel boundarie but stay 
            % in the same detector
                overLap = rowm(pixInd+1)- moving_left_boundary; % Overlap Calculation
                reconTmp(pixInd) =  reconTmp(pixInd) + overLap * sinogram(proj,detInd) / deltaDetm;
                pixInd = pixInd + pixIinc;
                moving_left_boundary = rowm(pixInd + c1);
            end
        end % Overlap loop
        reconImgTmp(row,:) = reconTmp .* L;
    end % Row loop 
    
    if((angleCase == 1)||(angleCase == 3))
        reconImg = reconImg + reconImgTmp; 
    else
        reconImg = reconImg + fliplr(reconImgTmp)';
    end
   
        
end % Projection loop
reconImg = reconImg ./ proj;
end

%% Map Y
% Function that map detector or pixel bounderies onto Y axis
function [y] = mapp2y(x1,y1,x2,y2)
    y=y1-x1.*(y1-y2)./(x1-x2);
end

%% Map X
% Function that map detector or pixel bounderies onto X axis
function [x] = mapp2x(x1,y1,x2,y2)
    x=-(y1).*(x1-x2)./(y1-y2)+x1;
end

%% Draw 2D
% Function to draw geometry
function drawGeo(tubeX,tubeY,pixelX,pixelY,detX,detY)
    plot(tubeX,tubeY,'*')
    hold on
    plot([detX(1),detX(end)],[detY(1),detY(end)])
    vetX = [pixelX(1,1),pixelX(end,1),pixelX(end,end),pixelX(1,end)];
    vetY = [pixelY(1,1),pixelY(end,1),pixelY(end,end),pixelY(1,end)];
    patch(vetX,vetY,[0,0,0,0],'FaceColor','none','EdgeColor','black','linewidth',2,'LineStyle','--')
end

