#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:14:09 2020

@author: Rodrigo
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv

#%% Cria a imagem

img = np.ones((200,200),np.float32) * 255
img[50:150,50:150] = 0

img_diag = img.copy()
    
pt1, pt2, pt3    = (50, 50) , (50, 70) , (70, 50)
pt4, pt5, pt6    = (50, 149), (50, 129), (70, 149)
pt7, pt8, pt9    = (149, 50), (149, 70), (129, 50)
pt10, pt11, pt12 = (149, 149),(149, 129),(129,149)
  
cv.drawContours(img_diag, [np.array( [pt1, pt2, pt3] )], 0, (255,255,255), -1) 
cv.drawContours(img_diag, [np.array( [pt4, pt5, pt6] )], 0, (255,255,255), -1) 
cv.drawContours(img_diag, [np.array( [pt7, pt8, pt9] )], 0, (255,255,255), -1) 
cv.drawContours(img_diag, [np.array( [pt10, pt11, pt12] )], 0, (255,255,255), -1) 

# img= img_diag.copy()
#%% Roberts

h1 = np.array((( 1),
               (-1)), ndmin=2).T

h2 = np.array(((-1),
               ( 1)), ndmin=2).T

h3 = np.array((( 1),
               (-1)), ndmin=2)

h4 = np.array(((1, 0),
               (0,-1)), ndmin=2)

h5 = np.array((( 0,1),
               (-1,0)), ndmin=2)


roberts = [h1,h2,h3,h4,h5]
for idX, h in enumerate(roberts):
    img_h = cv.filter2D(img, -1, h)
    plt.imsave("imgs/img_h" + str(idX+1) + "_0_255.png"  , img_h, cmap='gray', vmin=0, vmax=255)
    plt.imsave("imgs/img_h" + str(idX+1) + "-255_255.png", img_h, cmap='gray', vmin=img_h.min(), vmax=img_h.max())

#%% Prewitt

p1 = np.array(((-1,-1,-1),
               ( 0, 0, 0),
               ( 1, 1, 1)))

p2 = np.array(((-1, 0, 1),
               (-1, 0, 1),
               (-1, 0, 1)))

prewitt = [p1,p2]
for idX, p in enumerate(prewitt):
    img_p = cv.filter2D(img, -1, p)
    plt.imsave("imgs/img_p" + str(idX+1) + "_0_255.png"  , img_p, cmap='gray', vmin=0, vmax=765)
    plt.imsave("imgs/img_p" + str(idX+1) + "-255_255.png", img_p, cmap='gray', vmin=img_p.min(), vmax=img_p.max())

#%% Sobel

s1 = np.array(((-1,-2,-1),
               ( 0, 0, 0),
               ( 1, 2, 1)))

s2 = np.array(((-1, 0, 1),
               (-2, 0, 2),
               (-1, 0, 1)))

s3 = np.array(((-2,-1, 0),
               (-1, 0, 1),
               ( 0, 1, 2)))

s4 = np.array((( 0, 1, 2),
               (-1, 0, 1),
               (-2,-1, 0)))
 
s5 = -1 * s3

s6 = -1 * s4

sobel = [s1,s2,s3,s4,s5,s6]
for idX, s in enumerate(sobel):
    img_s = cv.filter2D(img, -1, s)
    plt.imsave("imgs/img_s" + str(idX+1) + "_0_255.png"  , img_s, cmap='gray', vmin=0, vmax=1020)
    plt.imsave("imgs/img_s" + str(idX+1) + "-255_255.png", img_s, cmap='gray', vmin=766, vmax=img_s.max())

#%% Gradiente

g1 = np.array((( 0,-1, 0),
               (-1, 4,-1),
               ( 0,-1, 0)))

g2 = np.array(((-1,-1,-1),
               (-1, 8,-1),
               (-1,-1,-1)))


grad = [g1,g2]
for idX, g in enumerate(grad):
    img_g = cv.filter2D(img_diag, -1, g)
    plt.imsave("imgs/img_g" + str(idX+1) + "_0_255.png"  , img_g, cmap='gray', vmin=0, vmax=255)
    plt.imsave("imgs/img_g" + str(idX+1) + "-255_255.png", img_g, cmap='gray', vmin=img_s.min(), vmax=img_s.max())

#%%
# Cria uma bordinha nas extremidades
img[0 ,:] = 0
img[-1,:] = 0
img[:, 0] = 0
img[:,-1] = 0

img_diag[0 ,:] = 0
img_diag[-1,:] = 0
img_diag[:, 0] = 0
img_diag[:,-1] = 0

plt.imsave("imgs/img.png"  , img  , cmap='gray', vmin=0, vmax=255)
plt.imsave("imgs/img_g.png", img_diag, cmap='gray', vmin=0, vmax=255)



