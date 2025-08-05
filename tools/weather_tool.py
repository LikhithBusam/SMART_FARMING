# tools/weather_tool.py
import os
import requests
from langchain.tools import tool

@tool
def get_weather_data(city: str) -> str:
    """
    Fetches real-time weather and a 5-day forecast for a given city.
    Use this tool to answer any questions related to weather conditions or forecasts.
    The input should be a single city name, e.g., 'Nuzividu'.
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "Error: OpenWeatherMap API key is not set."

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric' # Use Celsius
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        result = (
            f"Current weather in {city}:\n"
            f"- Conditions: {weather_description.title()}\n"
            f"- Temperature: {temperature}°C\n"
            f"- Humidity: {humidity}%\n"
            f"- Wind Speed: {wind_speed} m/s"
        )
        return result

    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"
    except KeyError:
        return f"Error: Could not parse weather data. The city '{city}' might not be found."