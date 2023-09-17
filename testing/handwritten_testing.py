import numpy as np
import tensorflow as tf
from PIL import Image

# Load the saved model
loaded_model = tf.keras.models.load_model("handwritten_recognition_model.keras")

# Load the image
image_path = "handwritten_images/3.jpg"
image = Image.open(image_path)

# Resize the image to 28x28 pixels
image = image.resize((28, 28))

# Convert the image to grayscale
image = image.convert("L")

# Normalize pixel values to [0, 1]
image = np.array(image).astype(float)
image_array = np.array(image) / 255.0

# Make a prediction
prediction = loaded_model.predict(np.expand_dims(image_array, axis=0))

# Extract the predicted label (digit)
predicted_label = np.argmax(prediction)

print(f"Predicted Digit: {predicted_label}")
