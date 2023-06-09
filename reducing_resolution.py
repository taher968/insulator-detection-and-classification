# Importing required modules
from zipfile import ZipFile
from PIL import Image
from pillow_heif import register_heif_opener
import os

def reducing_resolution():

  # Register the opener for the HEIC image files
  register_heif_opener()

  # Specifying percent of resolution
  picture_resolutions = [5, 10, 25] # Edit this to control the resolution. Start with 5 (low), and increase
  # Specifying the zip file name (e.g. Dataset/BrokenBrown.zip)
  zip_folder_names = ["BrokenBrown.zip", "BrokenWhite.zip", "CrackedWhite.zip", "CrackedWhite2.zip", "UnbrokenBrown.zip", "UnbrokenWhite.zip"] # Add the zip files you want to pull from

  # Iterating through the resolution values
  for resolution in picture_resolutions:
    
    # New directory to save reduced resolution pics to
    new_dir_path = "Dataset/ReducedResolution(" + str(resolution) +"%)"
    os.mkdir(new_dir_path)

    # For each zip_folder being analyzed
    for zip_folder_path in zip_folder_names:
      
      # writing files to a zipfile
      with ZipFile((new_dir_path + "/" + zip_folder_path),'x') as newZip:
        
        # opening the zip file in READ mode
        with ZipFile("Dataset/" + zip_folder_path, 'r') as zip:
          # get the info of all files in the zip
          for info in zip.infolist():
            
            # open the image file for reading
            new_image_name = info.filename.split('/')[-1].replace(".heic", ("at" + str(resolution) + "%.jpg"))
            with zip.open(info.filename) as zipFile:
              with Image.open(zipFile) as pictureFile:
                pictureFile.save(new_dir_path + "/" + new_image_name, quality=resolution)

            # writing each file one by one to the zip
            newZip.write(new_dir_path + "/" + new_image_name)
            os.remove(new_dir_path + "/" + new_image_name) # Comment this line out if you would like to see the images generated and click on them to preview

reducing_resolution()
