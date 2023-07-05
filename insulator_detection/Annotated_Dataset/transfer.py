import os
import shutil

def transfer_files(source_image_dir, source_xml_dir, dest_train_image_dir, dest_train_xml_dir, dest_val_image_dir, dest_val_xml_dir, file_list):
    for filename in file_list:

        # Get the file paths
        image_file = os.path.join(source_image_dir, filename + '.jpg')
        xml_file = os.path.join(source_xml_dir, filename + '.xml')
        
        # Transfer image file
        if filename in train_file_list:
            os.makedirs(dest_train_image_dir, exist_ok=True)
            dest_image_file = os.path.join(dest_train_image_dir, filename + '.jpg')
        else:
            os.makedirs(dest_val_image_dir, exist_ok=True)
            dest_image_file = os.path.join(dest_val_image_dir, filename + '.jpg')
        
        shutil.copyfile(image_file, dest_image_file)
        
        # Transfer XML file
        if filename in train_file_list:
            os.makedirs(dest_train_xml_dir, exist_ok=True)
            dest_xml_file = os.path.join(dest_train_xml_dir, filename + '.xml')
        else:
            os.makedirs(dest_val_xml_dir, exist_ok=True)
            dest_xml_file = os.path.join(dest_val_xml_dir, filename + '.xml')
        
        shutil.copyfile(xml_file, dest_xml_file)

# Source directories
source_image_dir = 'JPEGImages'
source_xml_dir = 'Annotations'

# Destination directories for training files
dest_train_image_dir = 'Images/Training'
dest_train_xml_dir = 'XML/Training'

# Destination directories for validation files
dest_val_image_dir = 'Images/Validation'
dest_val_xml_dir = 'XML/Validation'

# Read training file list
with open('insulator_train.txt', 'r') as file:
    train_file_list = [os.path.splitext(line.strip())[0] for line in file.readlines()]

# Read validation file list
with open('insulator_val.txt', 'r') as file:
    val_file_list = [os.path.splitext(line.strip())[0] for line in file.readlines()]

# Transfer training files
transfer_files(source_image_dir, source_xml_dir, dest_train_image_dir, dest_train_xml_dir, dest_val_image_dir, dest_val_xml_dir, train_file_list)

# Transfer validation files
transfer_files(source_image_dir, source_xml_dir, dest_train_image_dir, dest_train_xml_dir, dest_val_image_dir, dest_val_xml_dir, val_file_list)