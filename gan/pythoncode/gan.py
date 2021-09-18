import keras
from keras import layers
from keras.preprocessing import image
import numpy as np
import cv2
import os

from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession

config = ConfigProto()
config.gpu_options.allow_growth = True
session = InteractiveSession(config = config)

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

def generator(height, width, channels, latentDim):
    generator_input = keras.Input(shape=(latentDim,))
    map = layers.Dense(128*64*64)(generator_input)

    layer0 = layers.LeakyReLU()(map)
    layerReshape0 = layers.Reshape((64, 64, 128))(layer0)

    layerConv0 = layers.Conv2D(256, 5, padding="same")(layerReshape0)
    layer1 = layers.LeakyReLU()(layerConv0)

    layerConvTransposed = layers.Conv2DTranspose(256, 4, strides=2, padding="same")(layer1)
    layer2 = layers.LeakyReLU()(layerConvTransposed)

    layerConv1 = layers.Conv2D(256, 5, padding="same")(layer2)
    layer3 = layers.LeakyReLU()(layerConv1)

    layerConv2 = layers.Conv2D(256, 5, padding="same")(layer3)
    layer4 = layers.LeakyReLU()(layerConv2)


    layer5 = layers.Conv2D(channels, 7, activation="tanh", padding="same")(layer4)
    generator = keras.models.Model(generator_input, layer5)
    generator.summary()
    

def discriminator(height, width, channels):
    discriminator_input = layers.Input(shape=(height, width, channels))
    layerConv0 = layers.Conv2D(128, 3)(discriminator_input)
    layer0 = layers.LeakyReLU()(layerConv0)

    layerConv1 = layers.Conv2D(128, 4, strides=2)(layer0)
    layer1 = layers.LeakyReLU()(layerConv1)

    layerConv2 = layers.Conv2D(128, 4, strides=2)(layer1)
    layer2 = layers.LeakyReLU()(layerConv2)

    layerConv3 = layers.Conv2D(128, 4, strides=2)(layer2)
    layer3 = layers.LeakyReLU()(layerConv3)

    flattenedLayer = layers.Flatten()(layer3)

    droppedOutLayers = layers.Dropout(0.4)(flattenedLayer)

    denseLayer = layers.Dense(1, activation="sigmoid")(droppedOutLayers)

    discriminator = keras.models.Model(discriminator_input, denseLayer)
    discriminator.summary()