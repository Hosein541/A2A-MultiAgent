from datetime import date
import requests

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Server")

GEOCODING_API = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_API = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_API = "https://archive-api.open-meteo.com/v1/archive"


def get_coordinates(location: str):
    response = requests.get(
        GEOCODING_API,
        params={
            "name": location,
            "count": 1
        },
        timeout=10,
    )

    response.raise_for_status()

    results = response.json().get("results")

    if not results:
        raise ValueError(f"Location '{location}' not found.")

    result = results[0]

    return (
        result["latitude"],
        result["longitude"],
        result["name"],
        result.get("country", "")
    )


@mcp.tool()
def get_current_weather(location: str) -> dict:
    """
    Retrieve the current weather conditions for a location.
    
    Use this tool for questions about the current temperature, humidity,
    wind speed, precipitation, or general weather conditions.
    
    Examples:
    - Weather in Tehran
    - Current weather in New York
    - Is it raining in Tokyo?
    """

    lat, lon, city, country = get_coordinates(location)

    response = requests.get(
        FORECAST_API,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "apparent_temperature",
                "precipitation",
                "wind_speed_10m",
                "weather_code",
            ],
        },
        timeout=10,
    )

    response.raise_for_status()

    return {
        "location": f"{city}, {country}",
        **response.json()["current"],
    }


@mcp.tool()
def get_weather_forecast(location: str, days: int = 7) -> dict:
    """
    Retrieve the weather forecast for a location.

    Use this tool when the user asks about future weather conditions.

    Examples:
    - Weather tomorrow in Paris
    - Forecast for the next 7 days
    - Will it rain this weekend?
    """

    lat, lon, city, country = get_coordinates(location)

    response = requests.get(
        FORECAST_API,
        params={
            "latitude": lat,
            "longitude": lon,
            "forecast_days": days,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "wind_speed_10m_max",
                "weather_code",
            ],
        },
        timeout=10,
    )

    response.raise_for_status()

    return {
        "location": f"{city}, {country}",
        "forecast": response.json()["daily"],
    }


@mcp.tool()
def get_historical_weather(
    location: str,
    start_date: str,
    end_date: str,
) -> dict:
    """
    Retrieve historical weather observations for a location.
    
    Use this tool when the user asks about weather conditions in the past.
    
    Examples:
    - Weather in London on January 1st
    - Temperature last week in Dubai
    """

    lat, lon, city, country = get_coordinates(location)

    response = requests.get(
        ARCHIVE_API,
        params={
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": [
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "wind_speed_10m_max",
            ],
        },
        timeout=10,
    )

    response.raise_for_status()

    return {
        "location": f"{city}, {country}",
        "history": response.json()["daily"],
    }


if __name__ == "__main__":
    mcp.run()