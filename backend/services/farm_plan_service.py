from datetime import date, timedelta

CROP_MATURITY_DAYS = {
    "rice": 120, "maize": 100, "chickpea": 100, "kidneybeans": 90,
    "pigeonpeas": 150, "mothbeans": 75, "mungbean": 65, "blackgram": 90,
    "lentil": 110, "pomegranate": 180, "banana": 300, "mango": 150,
    "grapes": 150, "watermelon": 85, "muskmelon": 80, "apple": 150,
    "orange": 240, "papaya": 270, "coconut": 365, "cotton": 180,
    "jute": 120, "coffee": 270
}
DEFAULT_MATURITY_DAYS = 100


def estimate_harvest_window(crop, planting_status):
    maturity_days = CROP_MATURITY_DAYS.get(crop.lower(), DEFAULT_MATURITY_DAYS)

    if planting_status == "Favourable to plant now":
        planting_date = date.today()
        harvest_start = planting_date + timedelta(days=maturity_days)
        harvest_end = planting_date + timedelta(days=maturity_days + 14)
        return f"{harvest_start.strftime('%b %d, %Y')} – {harvest_end.strftime('%b %d, %Y')}"
    else:
        return f"Approximately {maturity_days} days after planting (timing depends on when conditions improve)"


def generate_farm_plan(crop, farm_profile):
    rainfall = farm_profile["weather"]["rainfall_last_30_days"]

    if rainfall >= 50:
        planting_status = "Favourable to plant now"
        guidance = f"Recent rainfall ({rainfall}mm over the last 30 days) suggests reasonable soil moisture. This is a good window to plant {crop}."
    elif rainfall >= 20:
        planting_status = "Prepare land; monitor rainfall"
        guidance = f"Recent rainfall ({rainfall}mm over the last 30 days) is moderate. Prepare your land for {crop} and monitor rainfall before planting."
    else:
        planting_status = "Outside favourable planting window"
        guidance = f"Recent rainfall ({rainfall}mm over the last 30 days) is low. Consider waiting for the next rainy season before planting {crop}, or ensure irrigation is available."

    harvest_range = estimate_harvest_window(crop, planting_status)

    return {
        "crop": crop,
        "planting_status": planting_status,
        "guidance": guidance,
        "expected_harvest_range": harvest_range,
        "location": farm_profile["location"]
    }