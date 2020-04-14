#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 16:15:08 2020

@author: Rodrigo
"""

# USAGE
# python detect_faces.py --image rooster.jpg --prototxt deploy.prototxt.txt --model res10_300x300_ssd_iter_140000.caffemodel

# import the necessary packages
import numpy as np
import matplotlib.pyplot as plt
import cv2

path_img = "galera.png"
path_prototxt = "deploy.prototxt.txt"
path_model = "res10_300x300_ssd_iter_140000.caffemodel"
confidence_input = 0.5

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# 	help="path to input image")
# ap.add_argument("-p", "--prototxt", required=True,
# 	help="path to Caffe 'deploy' prototxt file")
# ap.add_argument("-m", "--model", required=True,
# 	help="path to Caffe pre-trained model")
# ap.add_argument("-c", "--confidence", type=float, default=0.5,
# 	help="minimum probability to filter weak detections")
# args = vars(ap.parse_args())


img_plt = plt.imread(path_img)
img_plt = np.uint8(255 * img_plt)
image_bgr = cv2.merge([img_plt[:,:,2],img_plt[:,:,1],img_plt[:,:,0]])

# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(path_prototxt, path_model)

# load the input image and construct an input blob for the image
# by resizing to a fixed 300x300 pixels and then normalizing it
# image = cv2.imread(path_img)
(h, w) = image_bgr.shape[:2]
blob = cv2.dnn.blobFromImage(cv2.resize(image_bgr, (300, 300)), 1.0,
 	(300, 300), (104.0, 177.0, 123.0))

# pass the blob through the network and obtain the detections and
# predictions
print("[INFO] computing object detections...")
net.setInput(blob)
detections = net.forward()

# loop over the detections
for i in range(0, detections.shape[2]):
 	# extract the confidence (i.e., probability) associated with the
 	# prediction
 	confidence = detections[0, 0, i, 2]

 	# filter out weak detections by ensuring the `confidence` is
 	# greater than the minimum confidence
 	if confidence > confidence_input:
		# compute the (x, y)-coordinates of the bounding box for the
		# object
         box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
         (startX, startY, endX, endY) = box.astype("int")
         # draw the bounding box of the face along with the associated
         # probability
         text = "{:.2f}%".format(confidence * 100)
         y = startY - 10 if startY - 10 > 10 else startY + 10
         cv2.rectangle(image_bgr, (startX, startY), (endX, endY),
   			(0, 0, 255), 2)
         cv2.putText(image_bgr, text, (startX, y),
   			cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

# show the output image
b,g,r = cv2.split(image_bgr)     # get b,g,r
image_rgb = cv2.merge([r,g,b]) # switch it to rgb
plt.imshow(image_rgb)