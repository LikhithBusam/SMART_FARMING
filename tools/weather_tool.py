# import os
# import requests
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()


# def get_weather_data(location: str) -> dict:
#     """
#     Fetch weather data for a given location.
#     Always returns a dictionary for MCP compatibility.
#     """
#     api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
#     if not api_key:
#         return {
#             "error": "OpenWeatherMap API key is not set",
#             "message": "Please set OPENWEATHERMAP_API_KEY in your .env file",
#             "location": location
#         }
    
#     try:
#         # OpenWeatherMap API endpoint
#         base_url = "http://api.openweathermap.org/data/2.5/weather"
        
#         params = {
#             'q': location,
#             'appid': api_key,
#             'units': 'metric'  # Use Celsius
#         }
        
#         response = requests.get(base_url, params=params, timeout=10)
        
#         if response.status_code == 200:
#             data = response.json()
            
#             # Extract relevant weather information
#             weather_info = {
#                 "location": f"{data['name']}, {data['sys']['country']}",
#                 "temperature": f"{data['main']['temp']}°C",
#                 "feels_like": f"{data['main']['feels_like']}°C",
#                 "humidity": f"{data['main']['humidity']}%",
#                 "pressure": f"{data['main']['pressure']} hPa",
#                 "description": data['weather'][0]['description'].title(),
#                 "wind_speed": f"{data.get('wind', {}).get('speed', 0)} m/s",
#                 "visibility": f"{data.get('visibility', 'N/A')} m" if data.get('visibility') else "N/A",
#                 "status": "success"
#             }
            
#             return weather_info
            
#         elif response.status_code == 404:
#             return {
#                 "error": "Location not found",
#                 "message": f"Could not find weather data for '{location}'",
#                 "location": location,
#                 "status": "not_found"
#             }
#         else:
#             return {
#                 "error": f"API request failed with status {response.status_code}",
#                 "message": response.text,
#                 "location": location,
#                 "status": "api_error"
#             }
            
#     except requests.exceptions.Timeout:
#         return {
#             "error": "Request timeout",
#             "message": "Weather service took too long to respond",
#             "location": location,
#             "status": "timeout"
#         }
#     except requests.exceptions.RequestException as e:
#         return {
#             "error": "Network error",
#             "message": str(e),
#             "location": location,
#             "status": "network_error"
#         }
#     except Exception as e:
#         return {
#             "error": "Unexpected error",
#             "message": str(e),
#             "location": location,
#             "status": "unknown_error"
#         }





import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def get_weather_data(location: str) -> dict:
    """
    Fetch current weather data for a given location.
    Returns a dictionary compatible with MCP tools and includes timestamp.
    """
    api_key = os.getenv('OPENWEATHERMAP_API_KEY')
    
    if not api_key:
        return {
            "error": "OpenWeatherMap API key is not set",
            "message": "Please set OPENWEATHERMAP_API_KEY in your .env file",
            "location": location,
            "status": "error"
        }
    
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': location,
            'appid': api_key,
            'units': 'metric'
        }
        
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "location": f"{data['name']}, {data['sys']['country']}",
                "temperature": f"{data['main']['temp']}°C",
                "feels_like": f"{data['main']['feels_like']}°C",
                "humidity": f"{data['main']['humidity']}%",
                "pressure": f"{data['main']['pressure']} hPa",
                "description": data['weather'][0]['description'].title(),
                "wind_speed": f"{data.get('wind', {}).get('speed', 0)} m/s",
                "visibility": f"{data.get('visibility', 'N/A')} m" if data.get('visibility') else "N/A",
                "status": "success",
                "timestamp": datetime.utcnow().isoformat() + "Z"  # UTC timestamp
            }
            return weather_info
        
        elif response.status_code == 404:
            return {
                "error": "Location not found",
                "message": f"Could not find weather data for '{location}'",
                "location": location,
                "status": "not_found",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        else:
            return {
                "error": f"API request failed with status {response.status_code}",
                "message": response.text,
                "location": location,
                "status": "api_error",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
    except requests.exceptions.Timeout:
        return {
            "error": "Request timeout",
            "message": "Weather service took too long to respond",
            "location": location,
            "status": "timeout",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except requests.exceptions.RequestException as e:
        return {
            "error": "Network error",
            "message": str(e),
            "location": location,
            "status": "network_error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "error": "Unexpected error",
            "message": str(e),
            "location": location,
            "status": "unknown_error",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
