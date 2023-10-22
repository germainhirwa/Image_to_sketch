import cv2
import urllib.request
import numpy as np
import os

def create_pencil_sketch(input_source, output_folder, output_name):
    # Read the input image
    if input_source.startswith('http'):
        # If the input is a URL, download the image
        response = urllib.request.urlopen(input_source)
        image_array = np.asarray(bytearray(response.read()), dtype=np.uint8)
        image = cv2.imdecode(image_array, -1)
    else:
        # If the input is a local file path, read the image
        image = cv2.imread(input_source)

    # Check if the image was loaded successfully
    if image is None:
        print("Error: Unable to load the image.")
        return

    # Convert the BGR image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_image = 255 - gray_image

    # Apply Gaussian blur to the inverted image
    blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)

    # Invert the blurred image
    inverted_blurred = 255 - blurred

    # Create the pencil sketch by dividing the grayscale image by the inverted blurred image
    pencil_sketch = cv2.divide(gray_image, inverted_blurred, scale=256.0)

    # Specify the output file path
    output_path = os.path.join(output_folder, f"{output_name}.png")

    # Save the pencil sketch
    cv2.imwrite(output_path, pencil_sketch)

    print(f"Pencil sketch saved as {output_path}")

# Input source options (URL, local file path, or drag and drop)
input_source = input("Enter the URL or file path of the photo (or drag and drop the photo): ")

# Specify the name for the output photo (without extension)
output_name = input("Enter the desired name for the output photo (without extension): ")

# Specify the folder where the output photo should be saved (or press Enter for default)
output_folder = input("Enter the folder path to save the output photo (or press Enter for default): ")

# If the user didn't specify an output folder, use the Downloads folder
if not output_folder:
    output_folder = os.path.expanduser("~/Downloads")

# Call the create_pencil_sketch function with the input source, output folder, and output name
create_pencil_sketch(input_source, output_folder, output_name)
