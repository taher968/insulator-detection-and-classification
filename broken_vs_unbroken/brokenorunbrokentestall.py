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

# Create testing dataset of all images
test_all_ds = tensorflow.keras.utils.image_dataset_from_directory(
    "insulators",
    labels="inferred",
    label_mode="binary",
    class_names=["broken", "unbroken"],
    color_mode="rgb",
    batch_size=batch_size,
    image_size=image_size,
    shuffle=True,
    seed=seed,
    interpolation="bilinear",
    follow_links=False,
    crop_to_aspect_ratio=False)


def preprocess_images(dataset, name):
    print("Now preprocessing: ", name)
    rescaling_layer = Rescaling(scale=1.0/255)
    preprocessed_dataset = dataset.map(lambda x, y: (rescaling_layer(x), y))
    return preprocessed_dataset

# Preprocess our image dataset by normalizing it
# (i.e. converting their pixel range of [0-255] to [0-1]).
test_all_ds_preprocessed = preprocess_images(test_all_ds, "Testing (All)")

# Load the existing model.
model = keras.models.load_model("broken_or_unbroken_model")

# Evaluate our model on its loss and metrics (currently just "accuracy")
# using the test dataset.
loss, acc = model.evaluate(test_all_ds_preprocessed)  # returns loss and metrics
print()
print("loss: %.2f" % loss)
print("acc: %.2f" % acc)
print()

# Print out a visual comparison of our model's prediction and the actual labels
predictions = (model.predict(test_all_ds_preprocessed) > 0.5).astype("int32")
labels = np.hstack([y for x, y in test_all_ds_preprocessed])
mapper = {0: "broken", 1: "unbroken"}
print("Predicted label array:")
print(np.vectorize(mapper.get)(predictions).transpose())
print("Actual label array:")
print(np.vectorize(mapper.get)(labels))
print()
