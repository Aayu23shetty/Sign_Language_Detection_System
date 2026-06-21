import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Define paths
data_dir = r"C:/Users/ayush/Desktop/open cv_project/data/train"  # Path to the dataset directory
output_dir = r"C:/Users/ayush/Desktop/open cv_project"  # Output directory for .npy files
image_size = (64, 64)  # Desired image size (height, width)

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Initialize lists to hold images and labels
images = []
labels = []

# Function to load images from a given directory
def load_images_from_directory(directory):
    for label in os.listdir(directory):
        class_dir = os.path.join(directory, label)
        if os.path.isdir(class_dir):
            print(f"Loading images from: {class_dir}")  # Debugging print
            for filename in os.listdir(class_dir):
                if filename.lower().endswith(('.jpg', '.png', '.jpeg')):  # Check for image file formats
                    img_path = os.path.join(class_dir, filename)
                    try:
                        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)  # Read as grayscale
                        if img is None:
                            print(f"Warning: Unable to load image {img_path}")
                            continue
                        img = cv2.resize(img, image_size)  # Resize image
                        images.append(img)
                        labels.append(label)
                    except Exception as e:
                        print(f"Error loading image {img_path}: {e}")

# Load training images
load_images_from_directory(data_dir)

# Check if any images were loaded
if not images:
    print("No images were loaded. Please check the directory structure.")
else:
    # Convert images and labels to numpy arrays
    images = np.array(images, dtype='float32') / 255.0  # Normalize pixel values to [0, 1]
    labels = np.array(labels)

    # Encode labels as integers
    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(labels)  # Convert labels to integer values

    # Split the dataset into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(images, labels, test_size=0.2, random_state=42)

    # Reshape the images for the model input (adding channel dimension)
    X_train = X_train.reshape(-1, image_size[0], image_size[1], 1)
    X_val = X_val.reshape(-1, image_size[0], image_size[1], 1)

    # Save the processed data as .npy files for later use
    np.save(os.path.join(output_dir, 'X_train.npy'), X_train)
    np.save(os.path.join(output_dir, 'y_train.npy'), y_train)
    np.save(os.path.join(output_dir, 'X_val.npy'), X_val)
    np.save(os.path.join(output_dir, 'y_val.npy'), y_val)

    print("Data preprocessing complete.")
    print(f"Training data shape: {X_train.shape}, Training labels shape: {y_train.shape}")
    print(f"Validation data shape: {X_val.shape}, Validation labels shape: {y_val.shape}")

