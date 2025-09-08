#!/usr/bin/env python3

from fastmcp import FastMCP
import logging
from pathlib import Path
import os
import sys
import time
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image

# --- Setup Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SmartFarmingMCP")

# --- Ensure Project Root is in Path ---
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# --- Dynamic Import System ---
# Import weather tool
try:
    from tools.weather_tool import get_weather_data
    WEATHER_AVAILABLE = True
    logger.info("✅ Weather tool imported successfully")
except ImportError as e:
    logger.warning(f"❌ Weather tool not available: {e}")
    WEATHER_AVAILABLE = False
    get_weather_data = None

# Import disease predictor
try:
    from models.disease_predictor import analyze_plant_image
    DISEASE_PREDICTOR_AVAILABLE = True
    logger.info("✅ Disease predictor imported successfully")
except ImportError as e:
    logger.warning(f"❌ Disease predictor not available: {e}")
    DISEASE_PREDICTOR_AVAILABLE = False
    analyze_plant_image = None

# Import agent creator
CREATE_AND_RUN_AVAILABLE = False
create_and_run = None

try:
    import models.agent_creator as agent_module
    logger.info("✅ Agent module imported successfully")
    
    # Check available functions in agent_creator
    available_functions = [func for func in dir(agent_module) if not func.startswith('_') and callable(getattr(agent_module, func))]
    logger.info(f"Available functions in agent_creator: {available_functions}")
    
    # Try to find a suitable function
    if hasattr(agent_module, 'create_and_run'):
        create_and_run = agent_module.create_and_run
        CREATE_AND_RUN_AVAILABLE = True
        logger.info("✅ Found create_and_run function")
    elif hasattr(agent_module, 'run_agent'):
        create_and_run = agent_module.run_agent
        CREATE_AND_RUN_AVAILABLE = True
        logger.info("✅ Found run_agent function")
    elif hasattr(agent_module, 'create_agri_agent'):
        create_and_run = agent_module.create_agri_agent
        CREATE_AND_RUN_AVAILABLE = True
        logger.info("✅ Found create_agri_agent function")
    elif hasattr(agent_module, 'execute_agent'):
        create_and_run = agent_module.execute_agent
        CREATE_AND_RUN_AVAILABLE = True
        logger.info("✅ Found execute_agent function")
    elif hasattr(agent_module, 'run'):
        create_and_run = agent_module.run
        CREATE_AND_RUN_AVAILABLE = True
        logger.info("✅ Found run function")
    else:
        logger.warning(f"❌ No suitable agent function found. Available functions: {available_functions}")
        
except ImportError as e:
    logger.warning(f"❌ Agent creator not available: {e}")

# --- Initialize MCP Server ---
mcp = FastMCP(name="Smart Farming MCP Server")

# --- TOOLS ---

@mcp.tool()
def get_weather(location: str) -> dict:
    """Fetch weather data for a given location."""
    if not WEATHER_AVAILABLE:
        return {"error": "Weather tool not available - please check tools/weather_tool.py"}
    
    try:
        logger.info(f"Fetching weather for: {location}")
        result = get_weather_data(location)
        logger.info(f"Weather data retrieved successfully for {location}")
        return result
    except Exception as e:
        logger.error(f"Weather tool failed for {location}: {e}")
        return {"error": f"Failed to fetch weather data: {str(e)}"}


@mcp.tool()
def run_agent(prompt: str) -> str:
    """Run an agent with the given prompt."""
    if not CREATE_AND_RUN_AVAILABLE:
        return "Agent functionality not available - please check models/agent_creator.py and ensure it has a proper function"
    
    try:
        logger.info(f"Running agent with prompt length: {len(prompt)}")
        result = create_and_run(prompt)
        logger.info("Agent execution completed")
        return str(result)
    except Exception as e:
        logger.error(f"Agent tool failed: {e}")
        return f"Agent execution failed: {str(e)}"

# --- Model Preloading (Keep only this block) ---
try:
    logger.info("Loading MobileNetV2 plant disease model...")
    processor = AutoImageProcessor.from_pretrained(
        "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
        cache_dir="./model_cache"  # Cache locally to avoid re-downloads
    )
    model = AutoModelForImageClassification.from_pretrained(
        "linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification",
        cache_dir="./model_cache"
    )
    model.eval()
    MODEL_STATUS = "loaded"
    logger.info("✅ Model loaded successfully")
except Exception as e:
    processor = None
    model = None
    MODEL_STATUS = f"error: {e}"
    logger.error(f"❌ Failed to load model: {e}")

@mcp.tool()
def test_analysis_setup(image_path: str) -> dict:
    """
    Test the analysis setup with a given image path.
    Returns diagnostic information about file access, ML model availability,
    and actual disease prediction using preloaded MobileNetV2.
    """
    logger.info(f"Testing analysis setup for: {image_path}")
    
    results = {
        "test_timestamp": time.time(),
        "file_access": {},
        "ml_model": {
            "name": "MobileNetV2 Plant Disease",
            "version": "1.0",
            "status": MODEL_STATUS
        },
        "prediction_results": {}
    }

    # --- 1. File Access Check ---
    cwd = os.getcwd()
    file_status = {"cwd": cwd, "searched_path": image_path}
    target_path = None

    # Check absolute path first
    if os.path.isabs(image_path) and os.path.isfile(image_path):
        file_status["status"] = "success"
        file_status["found_at"] = "absolute_path"
        target_path = image_path
    # Check relative to current working directory
    elif os.path.isfile(image_path):
        file_status["status"] = "success"
        file_status["found_at"] = "relative_path"
        target_path = os.path.abspath(image_path)
    # Check in current directory with just filename
    else:
        filename = os.path.basename(image_path)
        alt_path = os.path.join(cwd, filename)
        if os.path.isfile(alt_path):
            file_status["status"] = "success"
            file_status["found_at"] = "current_directory"
            target_path = alt_path
        else:
            file_status["status"] = "failed"
            file_status["error"] = f"File not found in any of the checked locations"
            
    file_status["final_path"] = target_path
    results["file_access"] = file_status

    # --- 2. Model Status Check ---
    if MODEL_STATUS != "loaded":
        results["prediction_results"] = {
            "error": f"Model not available: {MODEL_STATUS}"
        }
        logger.error(f"Model not loaded: {MODEL_STATUS}")
        return results

    # --- 3. Prediction using Preloaded Model ---
    if target_path:
        try:
            logger.info(f"Processing image: {target_path}")
            
            # Load and preprocess image
            img = Image.open(target_path).convert("RGB")
            logger.info(f"Image loaded successfully: {img.size}")
            
            # Process with the model
            inputs = processor(images=img, return_tensors="pt")
            logger.info("Image preprocessed successfully")

            # Run inference
            with torch.no_grad():
                outputs = model(**inputs)
                logits = outputs.logits
            
            # Get predictions
            predicted_class_idx = logits.argmax(-1).item()
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            confidence_score = probabilities.max().item()

            # Get label mapping
            if hasattr(model.config, 'id2label'):
                labels = model.config.id2label
                detected_disease = labels.get(predicted_class_idx, f"Class_{predicted_class_idx}")
            else:
                detected_disease = f"Class_{predicted_class_idx}"

            results["prediction_results"] = {
                "detected_disease": detected_disease,
                "confidence": round(confidence_score, 4),
                "predicted_class_id": predicted_class_idx,
                "status": "success"
            }
            
            logger.info(f"Prediction successful: {detected_disease} (confidence: {confidence_score:.4f})")

        except Exception as e:
            error_msg = f"Prediction failed: {str(e)}"
            results["prediction_results"] = {"error": error_msg}
            logger.error(error_msg)
            
    else:
        results["prediction_results"] = {"error": "No valid image file found"}

    return results



# --- ENTRY POINT ---
if __name__ == "__main__":
    logger.info("🔌 Starting Smart Farming MCP Server in STDIO mode for MCP Inspector...")
    
    # Show module status
    logger.info(f"Weather Tool: {'✅ Available' if WEATHER_AVAILABLE else '❌ Not Available'}")
    logger.info(f"Disease Predictor: {'✅ Available' if DISEASE_PREDICTOR_AVAILABLE else '❌ Not Available'}")
    logger.info(f"Agent Creator: {'✅ Available' if CREATE_AND_RUN_AVAILABLE else '❌ Not Available'}")
    
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"Server failed to start: {e}")
        sys.exit(1)