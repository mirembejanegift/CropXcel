def generate_farm_plan(crop, farm_profile):
    """
    Generates a simple, rule-based farm plan for the selected crop,
    using current rainfall as the main planting-readiness signal.
    """
    rainfall = farm_profile["weather"]["rainfall_last_30_days"]

    if rainfall >= 50:
        planting_status = "Favourable to plant now"
        guidance = (
            f"Recent rainfall ({rainfall}mm over the last 30 days) suggests "
            f"reasonable soil moisture. This is a good window to plant {crop}."
        )
    elif rainfall >= 20:
        planting_status = "Prepare land; monitor rainfall"
        guidance = (
            f"Recent rainfall ({rainfall}mm over the last 30 days) is moderate. "
            f"Prepare your land for {crop} and monitor rainfall over the coming weeks "
            f"before planting."
        )
    else:
        planting_status = "Outside favourable planting window"
        guidance = (
            f"Recent rainfall ({rainfall}mm over the last 30 days) is low. "
            f"Consider waiting for the next rainy season before planting {crop}, "
            f"or ensure irrigation is available."
        )

    return {
        "crop": crop,
        "planting_status": planting_status,
        "guidance": guidance,
        "location": farm_profile["location"],
        "based_on": {
            "rainfall_last_30_days": rainfall,
            "temperature": farm_profile["weather"]["temperature"],
            "humidity": farm_profile["weather"]["humidity"],
            "soil_ph": farm_profile["soil"]["ph"]
        }
    }