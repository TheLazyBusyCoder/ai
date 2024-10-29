import numpy as np
import json
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam

# Load the saved model
model = load_model('letter_recognition_model.h5')

# Recompile the model
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Load input data from the JSON file
with open('input.json') as f:
    input_data = json.load(f)

# Prepare lists for training data
new_X_data = []
new_Y_data = []

# Loop through each sample in the input data
for item in input_data:
    array_input = np.array(item['array']).reshape(1, 10, 10, 1)  # Reshape for CNN input
    predicted = model.predict(array_input)
    predicted_class = np.argmax(predicted, axis=-1)
    predicted_letter = chr(predicted_class[0] + ord('A'))  # Assuming labels are A=0, B=1, etc.

    # Check if prediction matches the answer
    if predicted_letter != item['answer']:
        correct_class = ord(item['answer']) - ord('A')

        # Append data for retraining
        new_X_data.append(array_input[0])  # Flattening the input for the new dataset
        new_Y_data.append(np.eye(26)[correct_class])  # One-hot encoding for correct letter

# Convert lists to NumPy arrays for training
if new_X_data:
    new_X_data = np.array(new_X_data)
    new_Y_data = np.array(new_Y_data)

    # Fine-tune the model with the new data
    model.fit(new_X_data, new_Y_data, epochs=1, verbose=1)

# Save the updated model
model.save('letter_recognition_model.h5')

print("Model updated and saved.")
  