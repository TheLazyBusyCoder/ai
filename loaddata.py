import json
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from keras.utils import to_categorical

def load_data(letter_data_dir):
    data = []
    labels = []
    for filename in os.listdir(letter_data_dir):
        if filename.endswith('.json'):
            letter = filename[0]  # Extract the letter from the filename (e.g., 'S' from 'S.json')
            with open(os.path.join(letter_data_dir, filename)) as f:
                letter_data = json.load(f)
                # Convert to NumPy array and flatten if necessary
                for letter_example in letter_data:
                    data.append(np.array(letter_example))
                    labels.append(letter)  # Append the corresponding label
    return np.array(data), np.array(labels)

# Example usage
data, labels = load_data('./letter_data')

# Normalize the data (already binary, but converting to float for future use)
data = data.astype('float32')

# Reshape data to add a channel dimension (10, 10, 1)
data = data.reshape(-1, 10, 10, 1)  # Now it will have shape (number_of_samples, 10, 10, 1)

# Encode labels to integers
label_encoder = LabelEncoder()
encoded_labels = label_encoder.fit_transform(labels)

# Convert integer labels to one-hot encoding
categorical_labels = to_categorical(encoded_labels)

# Save the data and labels as .npy files
np.save('X_data.npy', data)  # Save the processed data
np.save('y_labels.npy', categorical_labels)  # Save the encoded labels