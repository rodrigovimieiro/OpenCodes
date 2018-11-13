clear;close all; clc;

save = 0;

% Calculate number of angular projections
deg = 1;
thetas = 0:deg:180-deg;

% Make the Phantom Image
% imageResolution = 256;
% phantomImg = phantom(imageResolution);
% phantomImg = double(phantomImg - min(phantomImg(:))); % set min of image to zero

phantomImg =imread('phantomImg.bmp');

Sinogram = radon(phantomImg);

% Radon
Sinogram_0deg  = radon(phantomImg,0);
Sinogram_90deg  = radon(phantomImg,90);
Sinogram_45deg = radon(phantomImg,45);
Sinogram_135deg = radon(phantomImg,135);

% Make sensor projections image
if(save==1)
    imwrite(mat2gray(repmat(Sinogram_0deg,1,10)),'Sinogram_0deg.png')
    imwrite(mat2gray(repmat(Sinogram_90deg,1,10)),'Sinogram_90deg.png')
    imwrite(mat2gray(repmat(Sinogram_45deg,1,10)),'Sinogram_45deg.png')
    imwrite(mat2gray(repmat(Sinogram_135deg,1,10)),'Sinogram_135deg.png')
end

% make the IRadon for each proj
phantomImg_res0 = iradon([Sinogram_0deg Sinogram_0deg],[0 0])./2;
phantomImg_res90 = iradon([Sinogram_90deg Sinogram_90deg],[90 90])./2;
phantomImg_res45 = iradon([Sinogram_45deg Sinogram_45deg],[45 45])./2;
phantomImg_res135 = iradon([Sinogram_135deg Sinogram_135deg],[135 135])./2;

if(save==1)
    imwrite(mat2gray(phantomImg_res0),'iRadon_0deg.png')
    imwrite(mat2gray(phantomImg_res90),'iRadon_90deg.png')
    imwrite(mat2gray(phantomImg_res45),'iRadon_45deg.png')
    imwrite(mat2gray(phantomImg_res135),'iRadon_135deg.png')
end
      
result_final = mat2gray(phantomImg_res0 + phantomImg_res90 + phantomImg_res45 + phantomImg_res135); 
result_final_all = mat2gray(iradon(Sinogram,thetas,'linear','none'));
 
if(save==1)
    imwrite(result_parcial,'Backprojection_parcial.png')
    imwrite(result_final,'Backprojection_final.png')
    imwrite(result_final_all,'Backprojection_final_all.png')
end

