import numpy as np
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam  # Import the Adam optimizer

# Load the saved model
model = load_model('letter_recognition_model.h5')

# Recompile the model with the original optimizer settings (use the same settings as used during training)
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Load the input data from the JSON file
with open('input.json') as f:
    input_data = json.load(f)

# Convert the loaded array into a NumPy array
array_input = np.array(input_data['array']).reshape(1, 10, 10, 1)  # Reshape for CNN input

# Make prediction
prediction = model.predict(array_input)
predicted_class = np.argmax(prediction, axis=-1)
predicted_letter = chr(predicted_class[0] + ord('A'))  # Assuming labels are A=0, B=1, etc.

print(f"The predicted letter is: {predicted_letter}")

# Get user feedback
feedback = input("Is this prediction correct? Type '1' for yes or '0' for no: ")

if feedback == '0':
    correct_letter = input("Please enter the correct letter: ").upper()
    # Convert correct letter to one-hot encoding
    correct_class = ord(correct_letter) - ord('A')

    # Prepare new data for training
    new_X_data = np.array(array_input)  # Same input
    new_Y_data = np.zeros((1, 26))  # Assuming 26 letters (A-Z)
    new_Y_data[0][correct_class] = 1  # One-hot encoding for correct letter

    # Fine-tune the model with new data
    model.fit(new_X_data, new_Y_data, epochs=1, verbose=1)

# Save the updated model
model.save('letter_recognition_model.h5')

print("Model updated and saved.")
