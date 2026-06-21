


import os
import numpy as np
import cv2

minValue = 200
image_size = (100, 100)  # Adjust the size if needed

# Function to preprocess and save images
def preprocess_and_save_images(input_dir, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop over each class folder in the input directory
    for label in os.listdir(input_dir):
        class_dir = os.path.join(input_dir, label)
        
        # Create corresponding class folder in the output directory
        output_class_dir = os.path.join(output_dir, label)
        if not os.path.exists(output_class_dir):
            os.makedirs(output_class_dir)

        # Process each image in the class folder
        for filename in os.listdir(class_dir):
            if filename.endswith('.jpg') or filename.endswith('.png'):
                img_path = os.path.join(class_dir, filename)
                img = cv2.imread(img_path)

                if img is None:
                    print(f"Error: Image at {img_path} not found.")
                    continue

                # Convert the image to grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Apply Gaussian blur
                blur = cv2.GaussianBlur(gray, (5, 5), 2)

                # Apply adaptive thresholding
                th3 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

                # Apply Otsu's thresholding
                ret, processed_img = cv2.threshold(th3, minValue, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

                # Resize the image if needed
                processed_img = cv2.resize(processed_img, image_size)

                # Save the processed image in the output directory
                output_img_path = os.path.join(output_class_dir, filename)
                cv2.imwrite(output_img_path, processed_img)

                print(f"Processed and saved: {output_img_path}")

# Example usage
input_directory = r"C:/Users/ayush/Desktop/open cv_project/data/train"  # Path to your train folder
output_directory = r"C:/Users/ayush/Desktop/open cv_project/processed"  # Output folder to save processed images

# Preprocess and save all images
preprocess_and_save_images(input_directory, output_directory)

print("Processing complete.")


