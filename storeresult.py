import cv2
import numpy as np
import tensorflow as tf
from datetime import datetime

# Load the trained model
model = tf.keras.models.load_model(r"C:/Users/ayush/Downloads/open cv_project/sign_model.keras")

# Define the label mapping for your classes
inverse_label_mapping = {
    0: '0', 1: '1', 2: '2', 3: 'A', 4: 'B', 5: 'C',
    6: 'D', 7: 'E', 8: 'f', 9: 'G', 10: 'H', 11: 'I'
}

# Function to preprocess the image
def preprocess_image(frame):
    img = cv2.resize(frame, (100, 100))  # Resize to match training size
    img = img / 255.0  # Normalize pixel values
    img = np.expand_dims(img, axis=0)  # Add batch dimension
    return img

# Initialize video capture and variables for logging
cap = cv2.VideoCapture(0)
last_prediction = None  # Track last unique prediction

# Open a log file to save unique predictions
with open("predictions_log.txt", "a") as log_file:
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Exit if there is an error

        preprocessed_frame = preprocess_image(frame)

        # Make a prediction
        predictions = model.predict(preprocessed_frame)
        predicted_class = np.argmax(predictions, axis=1)[0]
        confidence = np.max(predictions) * 100

        # Check if the predicted class exists in the mapping
        if predicted_class in inverse_label_mapping:
            label = inverse_label_mapping[predicted_class]
        else:
            label = "Unknown class"

        # Display prediction on the frame
        cv2.putText(frame, f'Predicted: {label} ({confidence:.2f}%)', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Live Prediction', frame)

        # Log only if confidence > 8% and prediction is new
        if confidence > 8 and last_prediction != predicted_class:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_file.write(f"{timestamp}: Predicted {label} with {confidence:.2f}% confidence\n")
            log_file.flush()  # Immediately write to the file
            last_prediction = predicted_class  # Update the last prediction

        # Exit on pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()