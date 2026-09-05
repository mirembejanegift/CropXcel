import os
import requests

BASE_URL = "https://api.isda-africa.com"


def get_isda_token():
    """
    Logs into iSDAsoil using credentials from environment variables
    and returns an access token string.
    """
    username = os.getenv("ISDA_USERNAME")
    password = os.getenv("ISDA_PASSWORD")

    if not username or not password:
        raise ValueError("ISDA_USERNAME or ISDA_PASSWORD not set in environment")

    payload = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/login", data=payload, timeout=10)
    response.raise_for_status()

    token = response.json().get("access_token")

    if not token:
        raise ValueError("Login succeeded but no access_token found in response")

    return token


def get_soil_profile(latitude, longitude):
    """
    Fetches pH, Nitrogen, Phosphorus, and Potassium for a coordinate
    from iSDAsoil, and returns a clean, farmer-friendly dictionary.
    """
    token = get_isda_token()
    headers = {"Authorization": f"Bearer {token}"}

    properties_needed = [
        "ph",
        "nitrogen_total",
        "phosphorous_extractable",
        "potassium_extractable"
    ]

    profile = {}

    for prop_name in properties_needed:
        params = {
            "lat": latitude,
            "lon": longitude,
            "property": prop_name,
            "depth": "0-20"
        }

        response = requests.get(
            f"{BASE_URL}/isdasoil/v2/soilproperty",
            headers=headers,
            params=params,
            timeout=15
        )
        response.raise_for_status()

        entry = response.json()["property"][prop_name][0]["value"]
        profile[prop_name] = {
            "value": entry["value"],
            "unit": entry["unit"]
        }

    return profile
    """
    Fetches pH, Nitrogen, Phosphorus, and Potassium for a coordinate
    from iSDAsoil, and returns a clean, farmer-friendly dictionary.
    """
    token = get_isda_token()
    headers = {"Authorization": f"Bearer {token}"}

    params = {
        "lat": latitude,
        "lon": longitude,
        "property": "ph,nitrogen_total,phosphorous_extractable,potassium_extractable",
        "depth": "0-20"
    }

    response = requests.get(
        f"{BASE_URL}/isdasoil/v2/soilproperty",
        headers=headers,
        params=params,
        timeout=15
    )
    response.raise_for_status()

    data = response.json()["property"]

    def extract(prop_name):
        entry = data[prop_name][0]["value"]
        return {
            "value": entry["value"],
            "unit": entry["unit"]
        }

    return {
        "ph": extract("ph"),
        "nitrogen_total": extract("nitrogen_total"),
        "phosphorous_extractable": extract("phosphorous_extractable"),
        "potassium_extractable": extract("potassium_extractable")
    }