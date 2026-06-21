import os
import numpy as np
import cv2
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pickle

# Path to the main processed folder
data_dir = r"C:/Users/ayush/Downloads/open cv_project/processed"
# Initialize lists to store images and labels
X = []
y = []

# Create a mapping of label names to integers
label_mapping = {label: idx for idx, label in enumerate(os.listdir(data_dir))}
print("Label Mapping:", label_mapping)

# Iterate over each subfolder in the data directory
for label in os.listdir(data_dir):
    label_path = os.path.join(data_dir, label)
    if os.path.isdir(label_path):  # Check if it is a folder
        for image_file in os.listdir(label_path):
            image_path = os.path.join(label_path, image_file)
            # Read the image using OpenCV
            img = cv2.imread(image_path)
            if img is not None:
                # Resize image to a fixed size (e.g., 100x100)
                img = cv2.resize(img, (100, 100))
                X.append(img)
                y.append(label_mapping[label])  # Convert label to its mapped integer value

# Convert lists to numpy arrays
X = np.array(X, dtype=np.float32) / 255.0  # Normalize pixel values to [0, 1]
y = np.array(y, dtype=np.int64)

# Split the dataset into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the CNN model
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3)),  # Adjust input image shape to 100x100
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(len(label_mapping), activation='softmax')  # Number of classes
])

# Compile the model
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',  # Use this loss function for integer labels
              metrics=['accuracy'])

# Training the model
history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_val, y_val))

# Evaluate the model on the validation data
val_loss, val_accuracy = model.evaluate(X_val, y_val)
print(f'Validation Loss: {val_loss:.4f}, Validation Accuracy: {val_accuracy:.4f}')

# Save the model
model.save(r"C:/Users/ayush/Downloads/open cv_project/sign_model.keras")


