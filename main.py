# @author: Ishman Mann
# @date: 13/10/2022
# 
# @description:
#   Classification model for CIFAR-10 dataset using a CNN in TensorFlow
#
# @references:
#   https://www.youtube.com/watch?v=tPYj3fFJGjk&t=3961s&ab_channel=freeCodeCamp.org
#   https://github.com/UWARG/computer-vision-python/blob/main/README.md#naming-and-typing-conventions

#------------------------------------------------------------------------------------------------------------------------------------------------------------

# Imports

import matplotlib.pyplot as plt
import numpy as np

from sklearn import model_selection

import tensorflow as tf
from tensorflow import keras
import tensorflow_datasets as tfds

from keras import datasets, layers, models

#------------------------------------------------------------------------------------------------------------------------------------------------------------
# Loading the dataset

# as_supervised=True yeilds (x, y) tuples instead of a dictionary
(datasetTrain, datasetTest), datasetInfo = tfds.load('cifar10', split = ['train', 'test'], 
                                                      shuffle_files=True, as_supervised=True, with_info=True)




#------------------------------------------------------------------------------------------------------------------------------------------------------------
# Data preprocessing and augmentation

dataRescaling = keras.Sequential([layers.Rescaling(1.0/255)]) 
# no resizing necessary since all images are 32 x 32 pixels

dataAugmention = keras.Sequential([
  layers.RandomFlip("horizontal_and_vertical"),
  layers.RandomRotation(0.2)






  # **need to add more transformations here
  # **consider adding custom transformations
  # **reference https://www.tensorflow.org/tutorials/images/data_augmentation
])


def prepare_data(dataset, batchSize=32, training=False, numAugmentations=1, shuffleBuffer=1000):

  # rescale all datasets
  dataset = dataset.map(lambda x, y: (dataRescaling(x) , y),
                        num_parallel_calls=tf.data.AUTOTUNE) # AUTOTUNE means dynamically tuned based on available CPU
  
  if (training):

    # desired numAugmentations are made and concatenated to original dataset
    if (numAugmentations > 0):
      augmentation = dataset.repeat(count=numAugmentations)
      augmentation = augmentation.map(lambda x, y: (dataAugmention(x, training=True)),
                                      num_parallel_calls=tf.data.AUTOTUNE)
      dataset = dataset.concatenate(augmentation)

    # shuffle and batch dataset
    dataset = dataset.shuffle(shuffle_buffer=shuffleBuffer)
    dataset = dataset.batch(batchSize)
  
  else:

    # batch dataset
    dataset = dataset.batch(batchSize)

  # prefetch to overlap dataset preprocessing and model excecution -> faster run time
  # (not using dataset.cache().prefetch, incase dataset is too large for cache storage) 
  return dataset.prefetch(buffer_size=tf.data.AUTOTUNE)


  


# Will run augmentation seperate to model creation for efficiency