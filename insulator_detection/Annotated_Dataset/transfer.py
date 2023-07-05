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

# Read training file list from 'insulator_train.txt'
with open('insulator_train.txt', 'r') as insulator_file:
    insulator_train_file_list = [os.path.splitext(line.strip())[0] for line in insulator_file.readlines()]

# Read training file list from 'non-insulator_train.txt'
with open('non-insulator_train.txt', 'r') as non_insulator_file:
    non_insulator_train_file_list = [os.path.splitext(line.strip())[0] for line in non_insulator_file.readlines()]

# Combine both lists into train_file_list
train_file_list = insulator_train_file_list + non_insulator_train_file_list

# Read validation file list
with open('insulator_val.txt', 'r') as file:
    insulator_val_file_list = [os.path.splitext(line.strip())[0] for line in file.readlines()]

with open('non-insulator_val.txt', 'r') as file:
    non_insulator_val_file_list = [os.path.splitext(line.strip())[0] for line in file.readlines()]

val_file_list = insulator_val_file_list + non_insulator_val_file_list


# Transfer training files
transfer_files(source_image_dir, source_xml_dir, dest_train_image_dir, dest_train_xml_dir, dest_val_image_dir, dest_val_xml_dir, train_file_list)

# Transfer validation files
transfer_files(source_image_dir, source_xml_dir, dest_train_image_dir, dest_train_xml_dir, dest_val_image_dir, dest_val_xml_dir, val_file_list)