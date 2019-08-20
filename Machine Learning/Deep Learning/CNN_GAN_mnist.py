"""
Author: Rodrigo de Barros Vimieiro
Date: August, 2019
rodrigo.vimieiro@gmail.com
=========================================================================

    DESCRIPTION:

    REFERENCE:
    https://medium.com/datadriveninvestor/generative-adversarial-network-gan-using-keras-ce1c05cfdfd3  
    https://towardsdatascience.com/gan-by-example-using-keras-on-tensorflow-backend-1a6d515a60d0
        

    Department of Electrical and Computer Engineering, 
    São Carlos School of Engineering, 
    University of São Paulo, 
    São Carlos, Brazil.

    ---------------------------------------------------------------------
    Copyright (C) <2018>  <Rodrigo de Barros Vimieiro>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.    
 

=========================================================================
"""

#%%

import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

from tensorflow.python import keras
from tensorflow.python.keras.models import Model,Sequential
from tensorflow.python.keras.layers import Dense, Flatten, Conv2D, Dropout, Activation, BatchNormalization, Reshape, UpSampling2D, Conv2DTranspose,Input, LeakyReLU
from tensorflow.python.keras.optimizers import RMSprop

from tqdm import tqdm

#%%
def data_preprocess(x_train, y_train, x_test, y_test, param):
    
    # Converts a class vector (integers) to binary class matrix.  
    y_train_out = tf.keras.utils.to_categorical(y_train,param['num_classes'],dtype='uint8')
    y_test_out = tf.keras.utils.to_categorical(y_test,param['num_classes'],dtype='uint8')
    
    # Normalize data
    x_train_out =  x_train / 255
    x_test_out =  x_test / 255
    
    # Reshape data to 4 dimensions
    x_train_out = x_train_out.reshape(param['num_images_train'], param['img_rows'], param['img_cols'], 1)
    x_test_out = x_test_out.reshape(param['num_images_test'], param['img_rows'], param['img_cols'], 1)
    
    return (x_train_out, y_train_out), (x_test_out, y_test_out)
#%%
def create_discriminator():
    # Create the Discriminator network structure
    discriminator = Sequential()
    
    discriminator.add(Conv2D(64, kernel_size=(5, 5),
                     strides=2,
                     activation=LeakyReLU(alpha=0.2),
                     padding='same',
                     input_shape=(param['img_rows'], param['img_cols'], 1)))
    discriminator.add(Dropout(0.4))
    discriminator.add(Conv2D(128, kernel_size=(5, 5),
                     strides=2,
                     activation=LeakyReLU(alpha=0.2),
                     padding='same',))
    discriminator.add(Dropout(0.4))
    discriminator.add(Conv2D(256, kernel_size=(5, 5),
                     strides=2,
                     activation=LeakyReLU(alpha=0.2),
                     padding='same',))
    discriminator.add(Dropout(0.4))
    discriminator.add(Conv2D(256, kernel_size=(5, 5),
                     strides=2,
                     activation=LeakyReLU(alpha=0.2),
                     padding='same',))
    discriminator.add(Dropout(0.4))
    
    discriminator.add(Flatten())
    discriminator.add(Dense(1, activation='sigmoid'))
    
    # Compile it
    discriminator.compile(optimizer=RMSprop(lr=0.0008, clipvalue=1.0, decay=6e-8), 
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
    
    discriminator.summary() 
    
    return discriminator

def create_generator():
    # Create the Generator network structure
    generator = Sequential()
    
    generator.add(Dense(12544, input_dim=100))
    generator.add(BatchNormalization(momentum=0.9))
    generator.add(Activation('relu'))
    generator.add(Reshape((7, 7, 256)))
    generator.add(Dropout(0.4))
    
    generator.add(UpSampling2D())
    generator.add(Conv2DTranspose(int(128), 5, padding='same'))
    generator.add(BatchNormalization(momentum=0.9))
    generator.add(Activation('relu'))
    generator.add(UpSampling2D())
    generator.add(Conv2DTranspose(int(64), 5, padding='same'))
    generator.add(BatchNormalization(momentum=0.9))
    generator.add(Activation('relu'))
    generator.add(Conv2DTranspose(int(32), 5, padding='same'))
    generator.add(BatchNormalization(momentum=0.9))
    generator.add(Activation('relu'))
    
    
    generator.add(Conv2DTranspose(1, 5, padding='same'))
    generator.add(Activation('sigmoid'))
    
    generator.compile(optimizer=RMSprop(lr=0.0004, clipvalue=1.0, decay=3e-8), 
                          loss='binary_crossentropy',
                          metrics=['accuracy'])
    
    generator.summary()
    
    return generator


#%%
def plot_generated_images(epoch, generator, examples=100, dim=(10,10), figsize=(10,10)):
    noise= np.random.normal(loc=0, scale=1, size=[examples, 100])
    generated_images = generator.predict(noise)
    generated_images = generated_images.reshape(100,28,28)
    plt.figure(figsize=figsize)
    for i in range(generated_images.shape[0]):
        plt.subplot(dim[0], dim[1], i+1)
        plt.imshow(generated_images[i],'gray')
        plt.axis('off')
    plt.tight_layout()
    #plt.savefig('gan_generated_image %d.png' %epoch)

#%%  
def data_show(x_test,y_test,prediction,nimages):
    
    nrandom = np.random.choice(prediction.shape[0],nimages)
    
    figure = plt.figure(figsize=(14, 6))
    
    for k, nrand in enumerate(nrandom):
        subplot = figure.add_subplot(3, 5, k + 1, xticks=[], yticks=[])
            
        subplot.imshow(np.squeeze(x_test[nrand])) 
    
    return 
    
#%% **************************** Main Code ************************************

(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()


# Create a dictionary with general parameters
param = {'num_classes': len(np.unique(y_train)),
         'img_rows': x_train.shape[1],
         'img_cols': x_train.shape[2],
         'num_images_train': x_train.shape[0],
         'num_images_test': x_test.shape[0]
         }

# Pre-process function
(x_train, y_train), (x_test, y_test) = data_preprocess(x_train,y_train,x_test,y_test,param)


discriminator = create_discriminator()
generator = create_generator()

discriminator.trainable=False
gan_input = Input(shape=(100,))
x = generator(gan_input)
gan_output= discriminator(x)
gan= Model(inputs=gan_input, outputs=gan_output)
gan.compile(loss='binary_crossentropy', optimizer='adam')

gan.summary()


batch_size = 128;
epochs = 40    

for e in range(1,epochs+1 ):
    print("Epoch %d" %e)
    for _ in tqdm(range(batch_size)):
        #generate  random noise as an input  to  initialize the  generator
        noise= np.random.normal(0,1, [batch_size, 100])
        
        # Generate fake MNIST images from noised input
        generated_images = generator.predict(noise)
        
        # Get a random set of  real images
        image_batch =x_train[np.random.randint(low=0,high=x_train.shape[0],size=batch_size)]
        
        #Construct different batches of  real and fake data 
        X= np.concatenate([image_batch, generated_images])
        
        # Labels for generated and real data
        y_dis=np.zeros(2*batch_size)
        y_dis[:batch_size]=0.9
        
        #Pre train discriminator on  fake and real data  before starting the gan. 
        discriminator.trainable=True
        discriminator.train_on_batch(X, y_dis)
        
        #Tricking the noised input of the Generator as real data
        noise= np.random.normal(0,1, [batch_size, 100])
        y_gen = np.ones(batch_size)
        
        # During the training of gan, 
        # the weights of discriminator should be fixed. 
        #We can enforce that by setting the trainable flag
        discriminator.trainable=False
        
        #training  the GAN by alternating the training of the Discriminator 
        #and training the chained GAN model with Discriminator’s weights freezed.
        gan.train_on_batch(noise, y_gen)
        
    if e == 1 or e % 20 == 0:
       
        plot_generated_images(e, generator)

  


#%%