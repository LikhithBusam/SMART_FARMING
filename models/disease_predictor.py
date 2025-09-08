# # # models/disease_predictor.py
# # import numpy as np
# # from PIL import Image
# # # from tensorflow.keras.models import load_model # Keep this commented if you don't have a model
# # from langchain.tools import tool
# # import os

# # # A placeholder list of class names.
# # CLASS_NAMES = ['Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Late_blight', 'Corn_(maize)___Common_rust_'] # Add other classes as needed

# # @tool
# # def analyze_plant_image(image_file_path: str) -> str:
# #     """
# #     Analyzes an image of a plant leaf from a given file path to identify diseases.
# #     Use this tool when the user has uploaded an image and wants to know what is wrong with their plant.
# #     The input MUST be a string containing the full file path to the image, e.g., 'temp/uploaded_image.png'.
# #     """
# #     if not isinstance(image_file_path, str) or not os.path.exists(image_file_path):
# #         return "Error: Invalid or non-existent file path provided. Please ensure the file was saved correctly."

# #     try:
# #         # --- Real model prediction logic ---
# #         # In a real scenario, you would uncomment the following:
# #         # model = load_model('assets/plant_disease_model.h5')
# #         # img = Image.open(image_file_path).resize((256, 256))
# #         # img_array = np.array(img)
# #         # img_array = np.expand_dims(img_array, axis=0)
# #         # predictions = model.predict(img_array)
# #         # predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
# #         # confidence = np.max(predictions[0])
# #         # result = f"Detected: {predicted_class} with {confidence*100:.2f}% confidence."
# #         # --- End of real logic ---

# #         # --- Placeholder logic for now ---
# #         # This simulates a successful prediction since we don't have the trained model file.
# #         # It checks the filename to guess what was uploaded for a better simulation.
# #         if 'strawberry' in image_file_path.lower() or 'oip' in image_file_path.lower():
# #              result = "Simulated Result: The image shows classic signs of Strawberry Leaf Scorch, a common fungal disease."
# #         elif 'corn' in image_file_path.lower():
# #              result = "Simulated Result: The image shows signs of Common Rust on the corn leaf."
# #         else:
# #              result = "Simulated Result: Disease identified from image."
# #         # --- End of placeholder logic ---

# #         # Clean up the temporary file after processing
# #         os.remove(image_file_path)

# #         return result
# #     except Exception as e:
# #         return f"An error occurred during image analysis: {e}"





# # models/disease_predictor.py
# import numpy as np
# from PIL import Image
# # from tensorflow.keras.models import load_model # Keep this commented if you don't have a model
# from langchain.tools import tool
# import os

# # A placeholder list of class names.
# CLASS_NAMES = ['Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Late_blight', 'Corn_(maize)___Common_rust_'] # Add other classes as needed

# # Disease recommendations mapping
# DISEASE_RECOMMENDATIONS = {
#     'Strawberry___Leaf_scorch': 'Apply fungicides like copper-based sprays. Ensure proper watering and avoid overhead irrigation. Remove affected leaves.',
#     'Strawberry___healthy': 'Plant appears healthy! Continue regular care and monitoring.',
#     'Tomato___Late_blight': 'Apply fungicides like Chlorothalonil or Copper-based sprays. Improve air circulation and avoid watering leaves directly.',
#     'Corn_(maize)___Common_rust_': 'Apply fungicides if severe. Consider resistant varieties for future planting. Ensure proper spacing for air circulation.',
#     'Unknown': 'Unable to identify specific disease. Consider consulting a local agricultural extension office or plant pathologist.'
# }

# @tool
# def analyze_plant_image(image_file_path: str) -> dict:
#     """
#     Analyzes an image of a plant leaf from a given file path to identify diseases.
#     Use this tool when the user has uploaded an image and wants to know what is wrong with their plant.
#     The input MUST be a string containing the full file path to the image, e.g., 'temp/uploaded_image.png'.
#     Returns a dictionary with 'disease' and 'recommendations' keys.
#     """
#     if not isinstance(image_file_path, str) or not os.path.exists(image_file_path):
#         return {
#             "disease": "Error", 
#             "recommendations": "Invalid or non-existent file path provided. Please ensure the file was saved correctly."
#         }

#     try:
#         # --- Real model prediction logic ---
#         # In a real scenario, you would uncomment the following:
#         # model = load_model('assets/plant_disease_model.h5')
#         # img = Image.open(image_file_path).resize((256, 256))
#         # img_array = np.array(img)
#         # img_array = np.expand_dims(img_array, axis=0)
#         # predictions = model.predict(img_array)
#         # predicted_class = CLASS_NAMES[np.argmax(predictions[0])]
#         # confidence = np.max(predictions[0])
#         # --- End of real logic ---

#         # --- Placeholder logic for now ---
#         # This simulates a successful prediction since we don't have the trained model file.
#         # It checks the filename to guess what was uploaded for a better simulation.
#         if 'strawberry' in image_file_path.lower() or 'oip' in image_file_path.lower():
#             predicted_disease = "Strawberry___Leaf_scorch"
#         elif 'corn' in image_file_path.lower():
#             predicted_disease = "Corn_(maize)___Common_rust_"
#         elif 'tomato' in image_file_path.lower():
#             predicted_disease = "Tomato___Late_blight"
#         else:
#             predicted_disease = "Unknown"
#         # --- End of placeholder logic ---

#         # Get recommendations for the predicted disease
#         recommendations = DISEASE_RECOMMENDATIONS.get(predicted_disease, DISEASE_RECOMMENDATIONS['Unknown'])

#         # Clean up the temporary file after processing
#         try:
#             os.remove(image_file_path)
#         except OSError:
#             pass  # File might have already been deleted

#         return {
#             "disease": predicted_disease,
#             "recommendations": recommendations
#         }

#     except Exception as e:
#         return {
#             "disease": "Error",
#             "recommendations": f"An error occurred during image analysis: {e}"
#         }



import numpy as np
from PIL import Image, ImageStat
import base64
import io
import cv2
from sklearn.cluster import KMeans
from scipy import stats
from langchain.tools import tool

@tool
def analyze_plant_image(image_data: str) -> dict:
    """
    Dynamically analyzes an uploaded plant leaf image to identify diseases.
    Uses computer vision techniques to detect anomalies, discoloration, and patterns
    that may indicate plant diseases.
    Returns a dictionary with 'disease' and 'recommendations' keys.
    """
    if not isinstance(image_data, str):
        return {
            "disease": "Error", 
            "recommendations": "Invalid image data provided. Please upload a valid image."
        }

    try:
        # Handle different base64 formats
        if image_data.startswith('data:image/'):
            image_data = image_data.split(',')[1]
        
        # Decode base64 image
        try:
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            return {
                "disease": "Error",
                "recommendations": f"Invalid base64 image data: {str(e)}"
            }
        
        # Open and process image
        try:
            pil_image = Image.open(io.BytesIO(image_bytes))
            if pil_image.mode != 'RGB':
                pil_image = pil_image.convert('RGB')
            
            # Convert to OpenCV format
            cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
            
        except Exception as e:
            return {
                "disease": "Error",
                "recommendations": f"Unable to process the uploaded image: {str(e)}"
            }

        # Dynamic analysis starts here
        analysis_results = perform_dynamic_analysis(pil_image, cv_image)
        
        # Generate diagnosis based on analysis
        diagnosis = generate_diagnosis(analysis_results)
        
        return diagnosis

    except Exception as e:
        return {
            "disease": "Analysis Error",
            "recommendations": f"Error during image analysis: {str(e)}"
        }

def perform_dynamic_analysis(pil_image, cv_image):
    """Perform comprehensive dynamic analysis of the plant image"""
    results = {}
    
    # 1. Color distribution analysis
    results['colors'] = analyze_color_distribution(pil_image)
    
    # 2. Texture analysis
    results['texture'] = analyze_texture_patterns(cv_image)
    
    # 3. Shape and contour analysis
    results['shapes'] = analyze_shapes_and_contours(cv_image)
    
    # 4. Statistical analysis
    results['stats'] = analyze_image_statistics(pil_image)
    
    # 5. Spot and lesion detection
    results['anomalies'] = detect_anomalies(cv_image)
    
    return results

def analyze_color_distribution(image):
    """Analyze color distribution to detect discoloration patterns"""
    hsv_image = image.convert('HSV')
    pixels = np.array(hsv_image)
    
    hue_values = pixels[:, :, 0].flatten()
    sat_values = pixels[:, :, 1].flatten()
    val_values = pixels[:, :, 2].flatten()
    
    rgb_pixels = np.array(image).reshape(-1, 3)
    
    # Fix: Better way to count unique colors
    unique_pixels = np.unique(rgb_pixels.view(np.dtype((np.void, rgb_pixels.dtype.itemsize*3))))
    n_colors = min(5, len(unique_pixels))
    
    if n_colors > 1:
        kmeans = KMeans(n_clusters=n_colors, random_state=42, n_init=10)
        kmeans.fit(rgb_pixels)
        dominant_colors = kmeans.cluster_centers_
    else:
        dominant_colors = [np.mean(rgb_pixels, axis=0)]
    
    green_dominance = np.mean([color[1] for color in dominant_colors]) / 255
    brown_yellow_presence = sum(1 for color in dominant_colors 
                               if color[0] > color[2] and color[1] > color[2]) / len(dominant_colors)
    
    return {
        'dominant_colors': dominant_colors.tolist(),
        'green_dominance': float(green_dominance),
        'discoloration_index': float(brown_yellow_presence),
        'hue_variance': float(np.var(hue_values)),
        'saturation_mean': float(np.mean(sat_values)),
        'brightness_mean': float(np.mean(val_values))
    }

def analyze_texture_patterns(cv_image):
    """Analyze texture to detect disease patterns"""
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Calculate texture measures
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    
    # Edge density
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.sum(edges > 0) / edges.size
    
    # Local binary pattern approximation
    kernel = np.ones((3,3), np.uint8)
    closing = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
    texture_contrast = np.std(closing)
    
    return {
        'variance': float(variance),
        'edge_density': float(edge_density),
        'texture_contrast': float(texture_contrast),
        'roughness_index': float(variance * edge_density)
    }

def analyze_shapes_and_contours(cv_image):
    """Analyze shapes to detect lesions, spots, and abnormal structures"""
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    _, thresholded = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 10]
    perimeters = [cv2.arcLength(c, True) for c in contours if cv2.contourArea(c) > 10]
    
    circularities = []
    for i, contour in enumerate(contours):
        if len(areas) > i and areas[i] > 10:
            circularity = 4 * np.pi * areas[i] / (perimeters[i] ** 2) if perimeters[i] > 0 else 0
            circularities.append(circularity)
    
    return {
        'spot_count': len(areas),
        'avg_spot_size': float(np.mean(areas)) if areas else 0,
        'shape_irregularity': float(1 - np.mean(circularities)) if circularities else 0,
        'size_variance': float(np.var(areas)) if len(areas) > 1 else 0
    }

def analyze_image_statistics(image):
    """Perform statistical analysis of image properties"""
    stat = ImageStat.Stat(image)
    
    return {
        'mean_rgb': stat.mean,
        'std_rgb': stat.stddev,
        'extrema': stat.extrema,
        'brightness_uniformity': float(np.std(stat.mean)),
        'color_balance': float(max(stat.mean) - min(stat.mean))
    }

def detect_anomalies(cv_image):
    """Detect anomalous regions that might indicate disease"""
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    
    # Fix: Check if image has sufficient contrast
    if np.percentile(gray, 20) == np.percentile(gray, 80):
        return {
            'dark_lesion_ratio': 0.0,
            'bright_discoloration_ratio': 0.0,
            'edge_damage_intensity': 0.0,
            'anomaly_score': 0.0
        }
    
    _, dark_spots = cv2.threshold(gray, np.percentile(gray, 20), 255, cv2.THRESH_BINARY_INV)
    dark_spot_ratio = np.sum(dark_spots > 0) / dark_spots.size
    
    _, bright_spots = cv2.threshold(gray, np.percentile(gray, 80), 255, cv2.THRESH_BINARY)
    bright_spot_ratio = np.sum(bright_spots > 0) / bright_spots.size
    
    edges = cv2.Canny(gray, 30, 100)
    edge_intensity = np.sum(edges > 0) / edges.size
    
    return {
        'dark_lesion_ratio': float(dark_spot_ratio),
        'bright_discoloration_ratio': float(bright_spot_ratio),
        'edge_damage_intensity': float(edge_intensity),
        'anomaly_score': float(dark_spot_ratio + bright_spot_ratio + edge_intensity)
    }

def generate_diagnosis(analysis_results):
    """Generate dynamic diagnosis based on analysis results"""
    # Fix: Use .get() with default values to handle missing keys
    colors = analysis_results.get('colors', {})
    texture = analysis_results.get('texture', {})
    shapes = analysis_results.get('shapes', {})
    anomalies = analysis_results.get('anomalies', {})
    
    green_dominance = colors.get('green_dominance', 0.5)
    discoloration = colors.get('discoloration_index', 0)
    texture_roughness = texture.get('roughness_index', 0)
    spot_count = shapes.get('spot_count', 0)
    anomaly_score = anomalies.get('anomaly_score', 0)
    brightness_mean = colors.get('brightness_mean', 128)
    
    health_score = green_dominance * 100
    disease_indicators = []
    recommendations = []
    
    if discoloration > 0.3:
        disease_indicators.append(f"Significant discoloration detected ({discoloration:.1%})")
        recommendations.append("Monitor for nutrient deficiencies or fungal infections")
        health_score -= 20
    
    if texture_roughness > 500:
        disease_indicators.append("Abnormal leaf texture detected")
        recommendations.append("Check for pest damage or disease lesions")
        health_score -= 15
    
    if spot_count > 10:
        disease_indicators.append(f"Multiple spots/lesions found ({spot_count} detected)")
        recommendations.append("Apply appropriate fungicides and remove affected leaves")
        health_score -= 25
    
    if anomaly_score > 0.1:
        disease_indicators.append("Tissue damage indicators present")
        recommendations.append("Improve growing conditions and air circulation")
        health_score -= 10
    
    if brightness_mean < 100:
        disease_indicators.append("Low leaf brightness indicating possible stress")
        recommendations.append("Check watering schedule and light conditions")
        health_score -= 10
    
    # Generate final diagnosis
    if health_score >= 80:
        disease = "Plant Appears Healthy"
        if not recommendations:
            recommendations = ["Continue current care routine", "Monitor regularly for changes"]
    elif health_score >= 60:
        disease = "Minor Health Issues Detected"
        recommendations.insert(0, "Early intervention recommended")
    elif health_score >= 40:
        disease = "Moderate Disease Symptoms"
        recommendations.insert(0, "Immediate treatment advised")
    else:
        disease = "Severe Disease Indicators"
        recommendations.insert(0, "Urgent intervention required")
    
    if disease_indicators:
        disease += f" - {', '.join(disease_indicators[:2])}"
    
    return {
        'disease': disease,
        'recommendations': '. '.join(recommendations[:3]) if recommendations else "Consult with agricultural expert for detailed analysis."
    }