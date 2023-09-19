import tensorflow as tf
from tensorflow import keras

mnist = keras.datasets.mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Normalize the pixel value to be between 0 and 1
train_images, test_images = train_images / 255.0, test_images / 255.0

# Create a basic nural network with chatGPT
# Creates the model and each layer in the model
model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),  # First layer is a flattened out picture of 28 * 28 pixels
    keras.layers.Dense(128, activation='relu'),  # # Hidden layer with ReLU activation
    keras.layers.Dropout(0.2),
    keras.layers.Dense(64, activation='relu'),  # Additional hidden layer
    keras.layers.Dropout(0.2),  # Dropout for regularization
    keras.layers.Dense(10)  # Output layer of the digit
])

# Compile the model
model.compile(
    optimizer='adam',  # Popular optimization algorythm to update the weights
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),  # decides how the predictions are compared
    # to the actual labels during training
    metrics=['accuracy'])  # what metrics to monitor during training

# Train the model
model.fit(train_images, train_labels, epochs=10)

# Evaluate how good the model is
test_loss, test_acc = model.evaluate(test_images, test_labels, verbose=2)
print(f'\nTest accuracy: {test_acc * 100:.2f}%')

# Make predictions - running the trained model
predictions = model.predict(test_images)

# Save the trained model to a file
model.save("handwritten_recognition_model.keras")
