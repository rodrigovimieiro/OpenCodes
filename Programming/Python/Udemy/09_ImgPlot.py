"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================
"""
import matplotlib.pyplot as plt
from tensorflow.python import keras


#%%


(x_train, y_train), (_,_) = keras.datasets.mnist.load_data()

print(x_train.shape)
print(y_train.shape)

im = x_train[0,:,:]
im_label = y_train[0]

print(im.shape)

plt.title("Label: %d" % im_label)
plt.imshow(im,'gray')





