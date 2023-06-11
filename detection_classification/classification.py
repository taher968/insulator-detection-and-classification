import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Dense, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.metrics import categorical_crossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
from tensorflow.keras.applications import imagenet_utils
from sklearn.metrics import confusion_matrix
import itertools
import os
import shutil
import random
import matplotlib.pyplot as plt
from IPython.display import Image


# physical_devices = tf.config.experimental.list_physical_devices('GPU')
# print("Num GPUs Available: ", len(physical_devices))
# tf.config.experimental.set_memory_growth(physical_devices[0], True)

# print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))


mobile = tf.keras.applications.mobilenet.MobileNet()

def prepare_image(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array_expanded_dims = np.expand_dims(img_array, axis=0)
    return tf.keras.applications.mobilenet.preprocess_input(img_array_expanded_dims)



def perform_prediction():
    input_folder = 'testing_images/'

    image_files = os.listdir(input_folder)
    for file in image_files:
        #Load image 
        image_path = os.path.join(input_folder, file)
        Image(filename=image_path, width=300,height=200) 
        processed_image = prepare_image(image_path)
        predictions = mobile.predict(processed_image)
        results = imagenet_utils.decode_predictions(predictions)
        print(results)

perform_prediction()

