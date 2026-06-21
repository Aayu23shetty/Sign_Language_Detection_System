import tensorflow as tf
import cv2
import numpy as np

# Load the trained model
model = tf.keras.models.load_model(r"C:/Users/ayush/Downloads/open cv_project/sign_model.keras")

# Load and preprocess a new image
def preprocess_image(image_path):
    img = cv2.imread(image_path)
    img = cv2.resize(img, (100, 100))  # Resize to match training size
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Path to a new image
new_image_path = r"C:/Users/ayush/Downloads/open cv_project/processed/0/1.jpg"
preprocessed_image = preprocess_image(new_image_path)

# Make a prediction
predictions = model.predict(preprocessed_image)
predicted_class = np.argmax(predictions, axis=1)
print(f"Predicted class: {predicted_class[0]}")






















