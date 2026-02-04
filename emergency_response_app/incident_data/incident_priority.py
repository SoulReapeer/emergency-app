# incident_data/incident_priority.py

# ======================
# P1 — IMMEDIATE LIFE THREAT
# ======================
P1_CRITICAL = [
    # Medical
    "cardiac_arrest", "stroke", "breathing_difficulty",
    "unconscious_person", "seizure", "serious_bleeding",
    "drug_overdose", "allergic_reaction", "childbirth",

    # Fire / Explosion
    "structure_fire", "wildfire", "explosion",

    # Violence / Police
    "active_shooter", "hostage_situation", "kidnapping",
    "gunshots_heard", "assault",

    # Traffic
    "highway_pileup", "pedestrian_struck",

    # Disaster / Infrastructure
    "earthquake", "building_collapse", "bridge_collapse",
    "tunnel_cave_in",

    # Hazard
    "radiation_leak", "biohazard_exposure",

    # Marine / Aviation
    "drowning", "boat_capsize",
    "airplane_crash", "mid_air_distress",

    # Public Health
    "mass_poisoning", "disease_outbreak",

    # Crowd
    "stampede", "riot"
]

# ======================
# P2 — HIGH RISK / ESCALATING
# ======================
P2_HIGH = [
    # Medical
    "burns", "mental_health_crisis",

    # Fire / Hazard
    "vehicle_fire", "electrical_fire",
    "gas_leak", "chemical_spill",
    "unknown_substance",

    # Police
    "robbery", "weapons_complaint", "fight",

    # Traffic
    "motor_vehicle_accident", "hit_and_run",

    # Disaster / Weather
    "flooding", "tornado", "hurricane", "landslide",

    # Utility
    "gas_line_rupture", "power_grid_failure",

    # Cyber
    "ransomware", "system_hack",

    # Aviation / Marine
    "emergency_landing", "water_rescue",

    # Crowd
    "overcrowded_event"
]

# ======================
# P3 — CONTROLLED BUT IMPORTANT
# ======================
P3_MEDIUM = [
    # Fire
    "smoke_investigation",

    # Police
    "burglary", "suspicious_activity",
    "missing_person", "drug_activity",
    "public_disturbance",

    # Traffic
    "road_blocked", "vehicle_stalled",

    # Weather
    "heavy_snowfall", "blizzard",
    "heatwave", "storm_surge",

    # Utility
    "water_main_break",

    # Cyber
    "data_breach",

    # Public Health
    "food_contamination",

    # Infrastructure
    "building_integrity_risk"
]

# ======================
# P4 — LOW URGENCY
# ======================
P4_LOW = [
    "vandalism",
    "alarm_activation",
    "lightning_strike",
    "power_outage",
    "mass_protest",
    "phishing_attack",
    "emergency_assistance"
]

# ======================
# P5 — MINIMAL / ADMIN
# ======================
P5_MINIMAL = [
    # Reserved for future non-emergency / informational events
]

# ======================
# MASTER MAP
# ======================
INCIDENT_PRIORITY_MAP = {
    "P1": P1_CRITICAL,
    "P2": P2_HIGH,
    "P3": P3_MEDIUM,
    "P4": P4_LOW,
    "P5": P5_MINIMAL
}

DEFAULT_PRIORITY = "P3"


def get_incident_priority(incident_type: str) -> str:
    """
    Returns priority code: P1, P2, P3, P4, or P5
    """
    for priority, incidents in INCIDENT_PRIORITY_MAP.items():
        if incident_type in incidents:
            return priority
    return DEFAULT_PRIORITY
