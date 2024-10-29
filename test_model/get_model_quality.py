import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

# Load the saved model
model = load_model('letter_recognition_model.h5')

# Load validation data from JSON file
with open('validation_data.json') as f:
    validation_data = json.load(f)

# Prepare input and output arrays for evaluation
X_test = []
y_test = []

# Process each sample in the validation data
for item in validation_data:
    array_input = np.array(item['array']).reshape(10, 10, 1)  # Reshape for CNN input
    X_test.append(array_input)
    label_index = ord(item['answer']) - ord('A')  # Convert letter to class index (A=0, B=1, ...)
    y_test.append(label_index)

# Convert lists to NumPy arrays for Keras
X_test = np.array(X_test)
y_test = to_categorical(np.array(y_test), num_classes=26)  # One-hot encode the labels

# Evaluate the model on the validation data
loss, accuracy = model.evaluate(X_test, y_test, verbose=1)

# Print the evaluation results
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print(f"Model Loss: {loss:.4f}")
