# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 15:37:58 2019

@author: rm2-bradburn
"""
from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dense

#Initialising the CNN
classifier = Sequential()

#Convolution - extracting features from the input images - creates feature map
classifier.add(Convolution2D(32, 3, 3, input_shape = (64, 64, 3), activation = 'relu'))

#Pooling - reduces unneeeded info within feature maps - retains important info
classifier.add(MaxPooling2D(pool_size = (2, 2)))

#Flattening - converts matrix to an array so can be input to the neural network
classifier.add(Flatten())

#Full connection - connecting the convolutional network to a neural network
classifier.add(Dense(output_dim = 128, activation = 'relu'))
classifier.add(Dense(output_dim = 1, activation = 'sigmoid'))

#Compiling - compiling the network
classifier.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

# Image data
from keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(
        rescale = 1./255,
        shear_range = 0.2,
        zoom_range = 0.2,
        horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory(
        'dataset/training_set',
        target_size = (64, 64),
        batch_size = 32,
        class_mode = 'binary')

test_set = test_datagen.flow_from_directory(
        'dataset/test_set',
        target_size = (64, 64),
        batch_size = 32,
        class_mode = 'binary')
        
# Training the model
from IPython.display import display
from PIL import Image

classifier.fit_generator(
        training_set,
        steps_per_epoch = 8000,
        epochs = 10,
        validation_data = test_set,
        validation_steps = 800)

import numpy as np
from keras.preprocessing import image
test_image = image.load_img('dog.4931.jpg', target_size = (64, 64))
test_image = image.img_to_array(test_image)
test_image = np.expand_dims(test_image, axis = 0)
result = classifier.predict(test_image)
training_set.class_indices
if result [0][0] >= 0.5:
    prediction = 'dog'
else:
    prediction = 'cat'
print (prediction)


