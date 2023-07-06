# Importing required modules
import os
import cv2
import imgaug.augmenters as iaa
import numpy as np
import shutil
from zipfile import ZipFile
from PIL import Image
from pillow_heif import register_heif_opener

def augment_image(input_file, output_folder, augmentation_factor, zipFile):

  # Initialize image augmentation sequence
  seq = iaa.Sequential([
    # iaa.Fliplr(0.5),  # Horizontal flip with a 50% chance
    # iaa.Affine(rotate=(-45, 45)),  # Rotation between -45 to 45 degrees
    iaa.Multiply((0.8, 1.2)),  # Multiply image with random values between 0.8 and 1.2
    iaa.ContrastNormalization((0.8, 1.2)),  # Apply contrast normalization
    iaa.AdditiveGaussianNoise(scale=(0, 0.05 * 255)),  # Add Gaussian noise
    iaa.GaussianBlur(sigma=(0, 1.0))  # Apply Gaussian blur
    # Add more augmentations as needed
  ])

    
  if input_file.lower().endswith('.heic'):
    image = Image.open(input_file)
    if image.mode != "RGB":
      image = image.convert("RGB")
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
  else:
    image = cv2.imread(input_file)
  
  if image is None:
    print(f"Failed to load image: {input_file}")

  # Perform augmentation multiple times
  for i in range(augmentation_factor):
    augmented_image = seq(image=image)

    # Generate new filename
    filename, extension = os.path.splitext(input_file)
    new_filename = f"{filename}_augmented_{i+1}{extension}"

    # Save augmented image to the new file
    cv2.imwrite(new_filename, augmented_image)
    zipFile.write(new_filename)
    os.remove(new_filename)

  print(f"Augmented {input_file} {augmentation_factor} times.")

  print("Image augmentation completed.")

def reducing_resolution():

  # Register the opener for the HEIC image files
  register_heif_opener()

  # Set percent of resolution
  picture_resolutions = [5, 10, 25] # Edit this to control the resolution. Start with 5 (low), and increase
  # Set the zip file names (e.g. Dataset/BrokenBrown.zip)
  zip_folder_names = ["BrokenBrown.zip", "BrokenWhite.zip", "CrackedWhite.zip", "CrackedWhite2.zip", "UnbrokenBrown.zip", "UnbrokenWhite.zip"] 
  # Set the number of times to augment each image
  augmentation_factor = 10

  # Create New directory to save reduced and augmented images in if it doesn't exist, if it does delete
  new_dir_path = "Dataset/AlteredImages"
  if os.path.exists(new_dir_path):
    shutil.rmtree(new_dir_path)
  os.mkdir(new_dir_path)

  # Iterating through the resolution values
  for zip_folder_path in zip_folder_names:
    
    # writing files to a zipfile
    with ZipFile(os.path.join(new_dir_path, zip_folder_path),'x') as newZip:

      # For each zip_folder being analyzed
      for resolution in picture_resolutions:
    
        # opening the zip file in READ mode
        with ZipFile(os.path.join("Dataset", zip_folder_path),'r') as zip:
          # get the info of all files in the zip
          for info in zip.infolist():
            # open the image file for reading
            new_image_name = info.filename.split('/')[-1].replace(".heic", f"at{resolution}%.jpg")
            with zip.open(info.filename) as zipFile:
              with Image.open(zipFile) as pictureFile:
                # Actual point of quality reduction
                new_file_path = os.path.join(new_dir_path, new_image_name)
                pictureFile.save(new_file_path, quality=resolution)
                augment_image(new_file_path, new_dir_path, augmentation_factor, newZip)

            # writing each file one by one to the zip
            newZip.write(new_file_path)
            os.remove(new_file_path) # Comment this line out if you would like to see the images generated and click on them to preview

reducing_resolution()
