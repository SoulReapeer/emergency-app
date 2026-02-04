#incident_data/categories.py

incident_categories = {
    "medical": [
        "cardiac_arrest", "stroke", "breathing_difficulty", "seizure",
        "unconscious_person", "serious_bleeding", "burns", "allergic_reaction",
        "drug_overdose", "childbirth", "mental_health_crisis"
    ],
    "fire": [
        "structure_fire", "vehicle_fire", "wildfire", "electrical_fire",
        "gas_leak", "smoke_investigation", "explosion"
    ],
    "police": [
        "robbery", "assault", "suspicious_activity", "burglary",
        "gunshots_heard", "weapons_complaint", "missing_person",
        "vandalism", "fight", "drug_activity", "public_disturbance"
    ],
    "traffic": [
        "motor_vehicle_accident", "hit_and_run", "pedestrian_struck",
        "road_blocked", "vehicle_stalled", "highway_pileup"
    ],
    "natural_disaster": [
        "flooding", "earthquake", "tornado", "hurricane",
        "landslide", "lightning_strike", "building_collapse", "power_outage"
    ],
    "hazardous_material": [
        "chemical_spill", "gas_leak_or_smell", "biohazard_exposure",
        "radiation_leak", "unknown_substance", "environmental_hazard"
    ],
    "special_situations": [
        "suicidal_person", "hostage_situation", "active_shooter",
        "bomb_threat", "kidnapping", "animal_attack",
        "emergency_assistance", "alarm_activation"
    ],
    "cyber_incident": [
        "data_breach", "system_hack", "phishing_attack", "ransomware"
    ],
    "utility_emergency": [
        "gas_line_rupture", "water_main_break", "power_grid_failure"
    ],
    "weather_alert": [
        "heavy_snowfall", "blizzard", "heatwave", "storm_surge"
    ],
    "marine_incident": [
        "boat_capsize", "drowning", "oil_spill", "water_rescue"
    ],
    "aviation_incident": [
        "airplane_crash", "emergency_landing", "mid_air_distress"
    ],
    "public_health_incident": [
        "disease_outbreak", "food_contamination", "mass_poisoning"
    ],
    "crowd_control": [
        "riot", "stampede", "mass_protest", "overcrowded_event"
    ],
    "infrastructure_failure": [
        "bridge_collapse", "tunnel_cave_in", "building_integrity_risk"
    ]
}
