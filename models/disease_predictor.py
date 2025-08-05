# models/disease_predictor.py
import numpy as np
from PIL import Image
# from tensorflow.keras.models import load_model # Keep this commented if you don't have a model
from langchain.tools import tool
import os

# A placeholder list of class names.
CLASS_NAMES = ['Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Late_blight', 'Corn_(maize)___Common_rust_'] # Add other classes as needed

@tool
def analyze_plant_image(image_file_path: str) -> str:
    """
    Analyzes an image of a plant leaf from a given file path to identify diseases.
    Use this tool when the user has uploaded an image and wants to know what is wrong with their plant.
    The input MUST be a string containing the full file path to the image, e.g., 'temp/uploaded_image.png'.
    """
    if not isinstance(image_file_path, str) or not os.path.exists(image_file_path):
        return "Error: Invalid or non-existent file path provided. Please ensure the file was saved correctly."

    try:
        # --- Real model prediction logic ---
        # In a real scenario, you would uncomment the following:
        # model = load_model('assets/plant_disease_model.h5')
        # img = Image.open(image_file_path).resize((256, 256))
        # img_array = np.array(img)
        # img_array = np.expand_dims(img_array, axis=0)
        # predictions = model.predict(img_array)
        # predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
        # confidence = np.max(predictions[0])
        # result = f"Detected: {predicted_class} with {confidence*100:.2f}% confidence."
        # --- End of real logic ---

        # --- Placeholder logic for now ---
        # This simulates a successful prediction since we don't have the trained model file.
        # It checks the filename to guess what was uploaded for a better simulation.
        if 'strawberry' in image_file_path.lower() or 'oip' in image_file_path.lower():
             result = "Simulated Result: The image shows classic signs of Strawberry Leaf Scorch, a common fungal disease."
        elif 'corn' in image_file_path.lower():
             result = "Simulated Result: The image shows signs of Common Rust on the corn leaf."
        else:
             result = "Simulated Result: Disease identified from image."
        # --- End of placeholder logic ---

        # Clean up the temporary file after processing
        os.remove(image_file_path)

        return result
    except Exception as e:
        return f"An error occurred during image analysis: {e}"