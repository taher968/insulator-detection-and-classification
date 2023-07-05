# Creating the Dataset

First a set of images are taken and their resolution is decreased to a particular resolution (216 x 216 in this case), this is done using the `reduce_resolution.py` script 

The Dataset is then annotated using the VoTT tool with an 80/20 training and validation split and exported using the Pascal VOC format

In the export format, two files are generated `insulator_train.txt` and `insulator_validation.txt` which contains the name of images belonging to each set

The XML's and Images are present in the same folder, to separate them we using the `transfer.py` script to create two new directories `Images` and `XML` 

Each of these directories contain `Training/` and `Validation/` folders representing the specific datasets

We then combine the information from all the XML's to two csv each for Training and Validation using the `xml_to_csv.py` script

# Training and Testing the Model

The steps to train and test our model are listed in `Insulator_Disc_Detector.ipynb` notebook

To test our model we transfer some images into the `Testing\` folder which the model uses for testing it's localisation and detection model


# Cropping and Transfering Positive Images

TODO