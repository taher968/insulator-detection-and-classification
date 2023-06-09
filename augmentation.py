import os
import cv2
import imgaug.augmenters as iaa
from PIL import Image
from pillow_heif import register_heif_opener
import numpy as np

register_heif_opener()


def augment_images(input_folder, output_folder, augmentation_factor):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

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

    # Iterate over images in the input folder
    image_files = os.listdir(input_folder)
    for file in image_files:
        # Load image
        image_path = os.path.join(input_folder, file)
        
        if file.lower().endswith('.heic'):
            image = Image.open(image_path)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        else:
            image = cv2.imread(image_path)
        
        if image is None:
            print(f"Failed to load image: {file}")
            continue

        # Perform augmentation multiple times
        for i in range(augmentation_factor):
            augmented_image = seq(image=image)

            # Generate new filename
            filename, extension = os.path.splitext(file)
            new_filename = f"{filename}_augmented_{i+1}{extension}"

            # Save augmented image to output folder
            output_path = os.path.join(output_folder, new_filename)
            cv2.imwrite(output_path, augmented_image)

        print(f"Augmented {file} {augmentation_factor} times.")

    print("Image augmentation completed.")


# Set input and output folder paths
input_folder = "images/"
output_folder = "augmented_images/"

# Set the number of times to augment each image
augmentation_factor = 3

# Perform image augmentation
augment_images(input_folder, output_folder, augmentation_factor)