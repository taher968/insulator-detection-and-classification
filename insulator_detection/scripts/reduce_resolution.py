import os
from PIL import Image

# Folder path containing the images
folder_path = 'images/'

# New resolution
new_width = 216
new_height = 216

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.jpg') or filename.endswith('.png'):  # Adjust file extensions as needed
        # Open the image
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path)

        # Resize the image
        resized_image = image.resize((new_width, new_height))

        # Save the resized image (overwrite the original image)
        resized_image.save(image_path)
        print('Image resized successfully')