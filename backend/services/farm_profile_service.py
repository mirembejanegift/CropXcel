from services.soil_service import get_soil_profile
from services.weather_service import get_weather_profile


def get_farm_profile(latitude, longitude):
    """
    Combines soil data (from iSDAsoil) and weather data (from Open-Meteo)
    into a single farm profile dictionary.
    """
    soil = get_soil_profile(latitude, longitude)
    weather = get_weather_profile(latitude, longitude)

    farm_profile = {
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "soil": {
            "ph": soil["ph"]["value"],
            "nitrogen_total": soil["nitrogen_total"],       # kept as {value, unit} for display
            "phosphorous_extractable": soil["phosphorous_extractable"],
            "potassium_extractable": soil["potassium_extractable"]
        },
        "weather": {
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "rainfall_last_30_days": weather["rainfall_last_30_days"]
        }
    }

    return farm_profile