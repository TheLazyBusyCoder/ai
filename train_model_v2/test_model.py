# test_model.py
import numpy as np
from keras.models import load_model

# Load the saved model
model = load_model('letter_recognition_model.h5')

# Function to predict the letter from a 10x10 array
def predict_letter(input_array):
    # Reshape input to match the model's input shape
    input_array = np.array(input_array).reshape(1, 10, 10, 1)  # Shape: (1, 10, 10, 1)
    
    # Make a prediction
    prediction = model.predict(input_array)
    predicted_class = np.argmax(prediction)  # Get the index of the highest probability
    
    return predicted_class

# Read the input from the input.txt file
try:
    with open('input.txt', 'r') as file:
        user_input_str = file.read().strip()  # Read the content and remove any extra spaces/newlines

    # Parse the input string to create a 2D array
    user_input = eval(user_input_str)  # Using eval to convert string to array
    if not (isinstance(user_input, list) and len(user_input) == 10 and all(len(row) == 10 for row in user_input)):
        raise ValueError("Input must be a 10x10 array.")
except Exception as e:
    print(f"Error reading input file: {e}")
    exit()

# Predict the letter
predicted_class = predict_letter(user_input)

# Map the predicted class index back to the corresponding letter
# Assuming labels were encoded as 'A', 'B', ..., 'Z'
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Adjust according to your dataset
predicted_letter = alphabet[predicted_class]

# Print the predicted letter
print(f"The predicted letter is: {predicted_letter}")
