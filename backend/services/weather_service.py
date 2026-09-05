import requests
from datetime import date, timedelta

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"


def get_current_conditions(latitude, longitude):
    """
    Fetches current temperature and humidity for a coordinate.
    """
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m"
    }

    response = requests.get(FORECAST_URL, params=params, timeout=10)
    response.raise_for_status()

    current = response.json()["current"]

    return {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"]
    }


def get_recent_rainfall(latitude, longitude, days=30):
    """
    Fetches total accumulated precipitation over the past `days` days
    (default 30) using Open-Meteo's historical archive API.
    """
    end_date = date.today() - timedelta(days=1)  # archive data usually lags by ~1 day
    start_date = end_date - timedelta(days=days - 1)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "daily": "precipitation_sum",
        "timezone": "auto"
    }

    response = requests.get(ARCHIVE_URL, params=params, timeout=15)
    response.raise_for_status()

    daily_values = response.json()["daily"]["precipitation_sum"]

    # Sum, ignoring any None values that might appear for missing days
    total_rainfall = sum(v for v in daily_values if v is not None)

    return round(total_rainfall, 1)


def get_weather_profile(latitude, longitude):
    """
    Combines current temperature/humidity with recent accumulated rainfall
    into a single weather profile dictionary.
    """
    current = get_current_conditions(latitude, longitude)
    rainfall = get_recent_rainfall(latitude, longitude)

    return {
        "temperature": current["temperature"],
        "humidity": current["humidity"],
        "rainfall_last_30_days": rainfall
    }