import numpy as np
import datetime
import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers import Rescaling

### PRETRAINING SETTINGS ###
batch_size = 1
image_size = (256, 256) # must be same numbers for both
seed = 0
validation_split = 0.3 # Percentage of total images reserved for validation
epochs = 5

# Grab the images from the "insulators" directory
# and create training and validation datasets out of them.
# This is a binary classification problem, so label_mode is binary
# and there are only two class names.
train_ds, val_ds = tensorflow.keras.utils.image_dataset_from_directory(
    "insulators",
    labels="inferred",
    label_mode="binary",
    class_names=["broken", "unbroken"],
    color_mode="rgb",
    batch_size=batch_size,
    image_size=image_size,
    shuffle=True,
    seed=seed,
    validation_split=validation_split,
    subset="both",
    interpolation="bilinear",
    follow_links=False,
    crop_to_aspect_ratio=False)

# Reserve a subset of the validation dataset for testing our model.
# Currently reserving 2/3 of it for the test dataset.
val_batches = tensorflow.data.experimental.cardinality(val_ds)
test_ds = val_ds.take((2*val_batches) // 3)
val_ds = val_ds.skip((2*val_batches) // 3)

def preprocess_images(dataset, name):
    print("Now preprocessing: ", name)
    rescaling_layer = Rescaling(scale=1.0/255)
    preprocessed_dataset = dataset.map(lambda x, y: (rescaling_layer(x), y))
    return preprocessed_dataset

# Preprocess our image datasets by normalizing them
# (i.e. converting their pixel range of [0-255] to [0-1]).
train_ds_preprocessed = preprocess_images(train_ds, "Training")
val_ds_preprocessed = preprocess_images(val_ds, "Validation")
test_ds_preprocessed = preprocess_images(test_ds, "Testing")

### MODEL ARCHITECTURE ###
# I believe most of our work will focus on changing this section
# in order to achieve better accuracy/optimization for embedded hardware.
# Currently a Sequential model (a stack of layers mapping a single
# input tensor to a single output tensor).
# Feel free to radically change this section's hyperparameters
# (e.g. changing number and/or types of layers/neurons per layer/activations)
#  or even build a entirely new custom architecture
#  using the Keras Functional API.
model = keras.Sequential()
model.add(layers.Dense(32, activation="relu"))
model.add(layers.Dense(32, activation="relu"))
model.add(layers.Flatten())
# needs to be last layer for binary classification problems
model.add(layers.Dense(1, activation="sigmoid"))    

# Compile the model with our chosen loss function and metrics.
# Since this is a binary classification problem,
# "binary_crossentropy" is currently chosen as our function.
model.compile(optimizer="rmsprop",
              loss="binary_crossentropy",
              metrics=["accuracy"])

# Prepare log directory for Tensorboard.
log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tensorflow.keras.callbacks.TensorBoard(log_dir=log_dir,
                                                              histogram_freq=1)
# Start training our model, using our validation dataset for validation.
history = model.fit(train_ds_preprocessed, epochs=epochs,
                    validation_data=val_ds_preprocessed,
                    callbacks=[tensorboard_callback])

# Evaluate our model on its loss and metrics (currently just "accuracy")
# using the test dataset.
loss, acc = model.evaluate(test_ds_preprocessed)  # returns loss and metrics
print()
print("loss: %.2f" % loss)
print("acc: %.2f" % acc)
print()

# Print out a visual comparison of our model's prediction and the actual labels
predictions = (model.predict(test_ds_preprocessed) > 0.5).astype("int32")
labels = np.hstack([y for x, y in test_ds_preprocessed])
mapper = {0: "broken", 1: "unbroken"}
print("Predicted label array:")
print(np.vectorize(mapper.get)(predictions).transpose())
print("Actual label array:")
print(np.vectorize(mapper.get)(labels))
print()

# Request to save our model to a folder.
save_choice = input("Save model to folder? (y/n) ")
if (save_choice == 'y'):
    model.save("broken_or_unbroken_model")
