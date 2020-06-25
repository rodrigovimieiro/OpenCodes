#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:09:22 2020

@author: Rodrigo

source: https://www.pyimagesearch.com/2020/04/20/detect-and-remove-duplicate-images-from-a-dataset-for-deep-learning/
"""

import pathlib
import numpy as np
import cv2
import os

#%%
def dhash(image, hashSize=8):
    # convert the image to grayscale and resize the grayscale image,
    # adding a single column (width) so we can compute the horizontal
    # gradient
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hashSize + 1, hashSize))

    # compute the (relative) horizontal gradient between adjacent
    # column pixels
    diff = resized[:, 1:] > resized[:, :-1]

    # convert the difference image to a hash and return it
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def calcHash(paths, file_indicator = "image"):
    
    hashes = {}
    
    # loop over our image paths
    for path in paths:
        
          if file_indicator == "image":
              # load the input image and compute the hash
              image = cv2.imread(path)
          else:
              vs = cv2.VideoCapture(path)
              
              # grab the current frame
              image = vs.read()[100]
              
          h = dhash(image)
    
          # grab all image paths with that hash, add the current image
          # path to it, and store the list back in the hashes dictionary
          p = hashes.get(h, [])
          p.append(path)
          hashes[h] = p
    
    return hashes

def removeDuplicated(hashes, file_indicator = "image", remove_flag = False):  
      
    count_duplicate = 0
    
    # loop over the image hashes
    for (h, hashedPaths) in hashes.items():
         # check to see if there is more than one image with the same hash
         if len(hashedPaths) > 1:
            # check to see if this is a dry run
            if remove_flag == False:
                 # initialize a montage to store all images with the same
                 # hash
                 montage = None
    
                 # loop over all image paths with the same hash
                 for p in hashedPaths:
                    # load the input image and resize it to a fixed width
                    # and height
                    if file_indicator == "image":
                        # load the input image and compute the hash
                        image = cv2.imread(p)
                    else:
                        vs = cv2.VideoCapture(p)
                      
                        # grab the current frame
                        image = vs.read()[100]
                        
                    image = cv2.resize(image, (150, 150))
    
                    # if our montage is None, initialize it
                    if montage is None:
                         montage = image
    
                    # otherwise, horizontally stack the images
                    else:
                         montage = np.hstack([montage, image])
    
                 # show the montage for the hash
                 print("[INFO] hash: {}".format(h))
                 cv2.imshow("Montage", montage)
                 cv2.waitKey(0)
                 count_duplicate += 1
                 print(hashedPaths)
    
            # otherwise, we'll be removing the duplicate images
            else:
                 # loop over all image paths with the same hash *except*
                 # for the first image in the list (since we want to keep
                 # one, and only one, of the duplicate images)
                 for p in hashedPaths[1:]:
                    os.remove(p)
                    
    return count_duplicate


#%%
rootDir2Read = pathlib.Path("/Volumes/RodrigoHD/USA")

remove_flag = -1

#%%

paths = list(rootDir2Read.glob('**/*'))

video_files, img_files = 0,0

imagePaths = []
videoPaths = []

for path in paths:
    if path.is_dir():
        continue
    else:  
        extension = str(path).split('.')[-1].lower()
        if extension == 'jpeg' or extension == 'png' or extension == 'jpg':
            imagePaths.append(str(path))
            img_files += 1
            
        elif extension == 'mp4' or extension == 'mov':
            videoPaths.append(str(path))
            video_files += 1            
        
        elif extension == 'lrv' or extension == 'thm' or extension == 'lvix' or extension == 'ini':
            os.remove(str(path))
        
        elif extension == 'ds_store' or extension == 'db':
            continue
                      
        else:
            print(extension)
                    
print("[INFO] We have {} video files and {} images file. Total of:{}".format(video_files,img_files,img_files+video_files))
        
#%%

# calcHashAndRemoveDuplicated(imagePaths, file_indicator = 0, remove_flag = False) 
 
# hashes = calcHash(imagePaths, file_indicator = "image")
# removeDuplicated(hashes, file_indicator = "image", remove_flag = False)

hashes = calcHash(videoPaths, file_indicator = "video")
removeDuplicated(hashes, file_indicator = "video", remove_flag = False)
    




