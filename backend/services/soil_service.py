import os
import time
import requests

BASE_URL = "https://api.isda-africa.com"

# Simple in-memory token cache so we don't log in on every single property request
_token_cache = {
    "token": None,
    "expires_at": 0
}


def get_isda_token():
    """
    Logs into iSDAsoil using credentials from environment variables
    and returns an access token string. Reuses a cached token if it's
    still valid (tokens last ~60 minutes; we refresh a bit early to be safe).
    """
    now = time.time()

    if _token_cache["token"] and now < _token_cache["expires_at"]:
        return _token_cache["token"]

    username = os.getenv("ISDA_USERNAME")
    password = os.getenv("ISDA_PASSWORD")

    if not username or not password:
        raise ValueError("ISDA_USERNAME or ISDA_PASSWORD not set in environment")

    payload = {
        "username": username,
        "password": password
    }

    response = requests.post(f"{BASE_URL}/login", data=payload, timeout=20)
    response.raise_for_status()

    token = response.json().get("access_token")

    if not token:
        raise ValueError("Login succeeded but no access_token found in response")

    # Cache it for 50 minutes (tokens last 60; refreshing early avoids edge-case expiry)
    _token_cache["token"] = token
    _token_cache["expires_at"] = now + (50 * 60)

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
            timeout=20
        )
        response.raise_for_status()

        entry = response.json()["property"][prop_name][0]["value"]
        profile[prop_name] = {
            "value": entry["value"],
            "unit": entry["unit"]
        }
