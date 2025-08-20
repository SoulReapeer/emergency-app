import os
from datetime import datetime
import time
import re
from threading import Lock

# Thread-safe file operations
file_lock = Lock()

# Configuration
CONFIG = {
    "MAX_INCIDENTS_PER_REPORT": 10,
    "REFRESH_INTERVAL": 5,
    "VALID_PHONE_FORMATS": [r"^\d{5}-\d{6}$", r"^\d{11}$"],
    "ALLOWED_SPECIAL_CHARS": " -.,#/",
    "LOG_DIR": "incident_logs",
    "RESOLVED_DIR": "resolved_incidents"
}

# Create log directories if not exists
os.makedirs(CONFIG["LOG_DIR"], exist_ok=True)
os.makedirs(CONFIG["RESOLVED_DIR"], exist_ok=True)

# Incident types and questions
incident_display_names = {
    "cardiac_arrest": "Cardiac Arrest / Heart Attack",
    "stroke": "Stroke",
    "breathing_difficulty": "Difficulty Breathing",
    "seizure": "Seizure",
    "unconscious_person": "Unconscious Person",
    "serious_bleeding": "Serious Bleeding",
    "burns": "Burns",
    "allergic_reaction": "Allergic Reaction",
    "drug_overdose": "Drug Overdose",
    "childbirth": "Childbirth",
    "mental_health_crisis": "Mental Health Crisis",
    "structure_fire": "Structure Fire",
    "vehicle_fire": "Vehicle Fire",
    "wildfire": "Wildfire",
    "electrical_fire": "Electrical Fire",
    "gas_leak": "Gas Leak",
    "smoke_investigation": "Smoke Investigation",
    "explosion": "Explosion",
    "robbery": "Robbery",
    "assault": "Assault",
    "suspicious_activity": "Suspicious Activity",
    "burglary": "Burglary",
    "gunshots_heard": "Gunshots Heard",
    "weapons_complaint": "Weapons Complaint",
    "missing_person": "Missing Person",
    "vandalism": "Vandalism",
    "fight": "Fight",
    "drug_activity": "Drug Activity",
    "public_disturbance": "Public Disturbance",
    "motor_vehicle_accident": "Motor Vehicle Accident",
    "hit_and_run": "Hit and Run",
    "pedestrian_struck": "Pedestrian Struck",
    "road_blocked": "Road Blocked",
    "vehicle_stalled": "Vehicle Stalled",
    "highway_pileup": "Highway Pileup",
    "flooding": "Flooding",
    "earthquake": "Earthquake",
    "tornado": "Tornado",
    "hurricane": "Hurricane",
    "landslide": "Landslide",
    "lightning_strike": "Lightning Strike",
    "building_collapse": "Building Collapse",
    "power_outage": "Power Outage",
    "chemical_spill": "Chemical Spill",
    "gas_leak_or_smell": "Gas Leak or Smell",
    "biohazard_exposure": "Biohazard Exposure",
    "radiation_leak": "Radiation Leak",
    "unknown_substance": "Unknown Substance",
    "environmental_hazard": "Environmental Hazard",
    "suicidal_person": "Suicidal Person",
    "hostage_situation": "Hostage Situation",
    "active_shooter": "Active Shooter",
    "bomb_threat": "Bomb Threat",
    "kidnapping": "Kidnapping",
    "animal_attack": "Animal Attack",
    "emergency_assistance": "Emergency Assistance",
    "alarm_activation": "Alarm Activation",   "data_breach": "Data Breach", 
    "system_hack": "System Heck",
    "phishing_attack": "Phishing Attack", 
    "ransomware": "Ransomware",
    "gas_line_rupture": "Gas Line Rupture", 
    "water_main_break": "Water Main Break", 
    "power_grid_failure": "Power Grid Failure",
    "heavy_snowfall": "Heavy Snowfall",
    "blizzard": "Blizzard",
    "heatwave": "Heatwave",
    "storm_surge": "Storm Surge",
    "boat_capsize": "Boat Capsize",
    "drowning": "Drowning",
    "oil_spill": "Oil Spill",
    "water_rescue": "Water Rescue",
    "airplane_crash": "Airplane Crash",
    "emergency_landing": "Emergency Landing",
    "mid_air_distress": "Mid-Air Distress",
    "disease_outbreak": "Disease Outbreak",
    "food_contamination": "Food Contamination",
    "mass_poisoning": "Mass Poisoning",
    "riot": "Riot",
    "stampede": "Stampede",
    "mass_protest": "Mass Protest",
    "overcrowded_event": "Overcrowded Event",
    "bridge_collapse": "Bridge Collapse",
    "tunnel_cave_in": "Tunnel Cave-In",
    "building_integrity_risk": "Building Integrity Risk"
}

incident_types = {
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


# General questions for all incidents
general_questions = {
    "location": "What is the address of the emergency?",
    "phone_number": "What is the phone number you're calling from?",
    "name": "What is your name?",
    "incident_description": "Tell us exactly what happened.",
    "time_of_incident": "When did the incident occur? (Provide date and time)",
    "number_of_people_involved": "How many people are involved or affected?",
    "is_anyone_injured": "Is anyone injured? If yes, what are the injuries?",
    "is_it_still_happening": "Is the situation still ongoing?",
    "any_danger_to_others": "Is there any immediate danger to others nearby?",
    "any_weapons_involved": "Are there any weapons or hazardous materials involved?",
    "your_current_safety": "Are you currently in a safe location?",
    "first_responder_needed": "Do you think you need police, fire, or medical assistance first?",
    "access_to_location": "Is there any difficulty accessing the location (e.g., locked gate, narrow alley)?"
}


# Incident-specific questions (same as original)
incident_questions = {
    # Medical emergencies
    "cardiac_arrest": {
        "patient_age": "How old is the patient?",
        "conscious": "Is the patient conscious? (yes/no)",
        "breathing": "Is the patient breathing? (yes/no)"
    },
    "stroke": {
        "symptoms_start": "When did the symptoms start?",
        "face_drooping": "Is there facial drooping? (yes/no)",
        "arm_weakness": "Is there arm weakness? (yes/no)",
        "speech_difficulty": "Is there difficulty speaking? (yes/no)"
    },
    "breathing_difficulty": {
        "patient_age": "How old is the patient?",
        "history_asthma": "Does the patient have a history of asthma or breathing problems? (yes/no)",
        "currently_breathing": "Is the patient breathing now? (yes/no)"
    },
    "seizure": {
        "still_seizing": "Is the patient still seizing? (yes/no)",
        "duration": "How long has the seizure lasted?",
        "previous_history": "Does the patient have a history of seizures? (yes/no)"
    },
    "unconscious_person": {
        "patient_age": "How old is the person?",
        "breathing": "Is the person breathing? (yes/no)",
        "responding": "Is the person responding to touch or voice? (yes/no)"
    },
    "serious_bleeding": {
        "bleeding_location": "Where is the bleeding?",
        "bleeding_stopped": "Has the bleeding stopped or been controlled? (yes/no)"
    },
    "burns": {
        "burn_location": "Where is the burn located?",
        "burn_severity": "How severe does the burn appear? (mild/moderate/severe)",
        "trapped": "Is the person trapped or in danger? (yes/no)"
    },
    "allergic_reaction": {
        "known_allergy": "Is this a known allergy? (yes/no)",
        "breathing_difficulty": "Is there any difficulty breathing or swelling? (yes/no)"
    },
    "drug_overdose": {
        "substance_taken": "What substance was taken?",
        "conscious": "Is the person conscious? (yes/no)",
        "breathing": "Is the person breathing? (yes/no)"
    },
    "childbirth": {
        "contractions_frequency": "How frequent are the contractions (in minutes)?",
        "water_broken": "Has the water broken? (yes/no)",
        "crowning": "Is the baby visible (crowning)? (yes/no)"
    },
    "mental_health_crisis": {
        "danger_to_self": "Is the person threatening harm to themselves or others? (yes/no)",
        "weapons_present": "Are any weapons present? (yes/no)"
    },

    # Fire emergencies
    "structure_fire": {
        "fire_description": "What is on fire and how big is it?",
        "people_inside": "Is anyone inside the building? (yes/no)"
    },
    "vehicle_fire": {
        "vehicle_occupied": "Is anyone inside the vehicle? (yes/no)",
        "fire_spreading": "Is the fire spreading to other vehicles or structures? (yes/no)"
    },
    "wildfire": {
        "fire_size": "How large is the wildfire?",
        "threat_to_buildings": "Are any structures threatened? (yes/no)"
    },
    "electrical_fire": {
        "source_known": "Do you know the source of the fire (appliance, wiring, etc.)? (yes/no)",
        "evacuated": "Has everyone evacuated the area? (yes/no)"
    },
    "gas_leak": {
        "smell_detected": "Is the smell strong? (yes/no)",
        "evacuated": "Has the area been evacuated? (yes/no)"
    },
    "smoke_investigation": {
        "smoke_visible": "Is smoke visible? (yes/no)",
        "odor": "Is there any odor associated with the smoke? (yes/no)"
    },
    "explosion": {
        "building_damage": "Was there damage to a building? (yes/no)",
        "injuries_reported": "Are there any injuries reported? (yes/no)"
    },

    # Police emergencies
    "robbery": {
        "suspect_description": "Can you describe the suspect?",
        "weapons_involved": "Were any weapons involved? (yes/no)"
    },
    "assault": {
        "injuries": "Are there any injuries? (yes/no)",
        "suspect_location": "Is the suspect still nearby? (yes/no)"
    },
    "suspicious_activity": {
        "activity_description": "Describe the suspicious activity.",
        "person_description": "Can you describe the person involved?"
    },
    "burglary": {
        "location_type": "Is it a home or business?",
        "suspect_present": "Is the suspect still on scene? (yes/no)"
    },
    "gunshots_heard": {
        "shots_number": "How many shots did you hear?",
        "direction": "Which direction did the shots come from?"
    },
    "weapons_complaint": {
        "weapon_type": "What type of weapon was seen?",
        "threat_made": "Was a threat made? (yes/no)"
    },
    "missing_person": {
        "person_description": "Describe the missing person (age, clothing, etc.).",
        "last_seen": "When and where was the person last seen?"
    },
    "vandalism": {
        "property_description": "What property was vandalized?",
        "suspect_seen": "Was the suspect seen? (yes/no)"
    },
    "fight": {
        "weapons_involved": "Were any weapons involved in the fight? (yes/no)",
        "people_involved": "How many people were involved?"
    },
    "drug_activity": {
        "activity_description": "Describe the drug activity you observed.",
        "location": "Where is this occurring?"
    },
    "public_disturbance": {
        "disturbance_description": "Describe the disturbance.",
        "people_involved": "How many people are involved?"
    },

    # Traffic emergencies
    "motor_vehicle_accident": {
        "injuries": "Are there any injuries? (yes/no)",
        "vehicles_involved": "How many vehicles are involved?"
    },
    "hit_and_run": {
        "vehicle_description": "Describe the suspect vehicle.",
        "injuries": "Are there any injuries? (yes/no)"
    },
    "pedestrian_struck": {
        "pedestrian_conscious": "Is the pedestrian conscious? (yes/no)",
        "vehicle_stopped": "Did the vehicle stop? (yes/no)"
    },
    "road_blocked": {
        "blockage_description": "What is blocking the road?",
        "alternative_route": "Is there an alternative route available? (yes/no)"
    },
    "vehicle_stalled": {
        "vehicle_location": "Where is the stalled vehicle located?",
        "hazards_on": "Are the hazard lights on? (yes/no)"
    },
    "highway_pileup": {
        "vehicles_involved": "Approximately how many vehicles are involved?",
        "injuries": "Are there injuries? (yes/no)"
    },

    # Natural disasters
    "flooding": {
        "water_depth": "How deep is the water?",
        "trapped_people": "Are any people trapped? (yes/no)"
    },
    "earthquake": {
        "building_damage": "Is there any visible building damage? (yes/no)",
        "injuries_reported": "Are injuries reported? (yes/no)"
    },
    "tornado": {
        "tornado_spotted": "Was a tornado seen or confirmed? (yes/no)",
        "damage_extent": "Describe the damage extent."
    },
    "hurricane": {
        "evacuation_order": "Has there been an evacuation order? (yes/no)",
        "storm_severity": "Describe the current storm conditions."
    },
    "landslide": {
        "debris_flow": "Is debris blocking roads or homes? (yes/no)",
        "trapped_people": "Are people trapped? (yes/no)"
    },
    "lightning_strike": {
        "structure_struck": "Was a structure struck? (yes/no)",
        "injuries": "Are there injuries? (yes/no)"
    },
    "building_collapse": {
        "people_trapped": "Are people trapped inside? (yes/no)",
        "extent_of_damage": "Describe the extent of damage."
    },
    "power_outage": {
        "area_affected": "How large is the affected area?",
        "downed_lines": "Are there downed power lines? (yes/no)"
    },

    # Hazardous materials
    "chemical_spill": {
        "chemical_known": "Do you know what chemical was spilled? (yes/no)",
        "people_exposed": "Were any people exposed? (yes/no)"
    },
    "gas_leak_or_smell": {
        "location_of_leak": "Where is the leak located?",
        "strong_odor": "Is the odor strong? (yes/no)"
    },
    "biohazard_exposure": {
        "type_of_biohazard": "What type of biohazard is involved?",
        "people_exposed": "How many people are exposed?"
    },
    "radiation_leak": {
        "source_known": "Is the source of the leak known? (yes/no)",
        "evacuation_in_progress": "Is evacuation in progress? (yes/no)"
    },
    "unknown_substance": {
        "substance_description": "Describe the unknown substance.",
        "exposure": "Has anyone been exposed? (yes/no)"
    },
    "environmental_hazard": {
        "hazard_description": "Describe the environmental hazard.",
        "immediate_threat": "Is there an immediate threat to life or property? (yes/no)"
    },

    # Special situations
    "suicidal_person": {
        "weapons_present": "Are weapons present? (yes/no)",
        "person_location": "Where is the person located?"
    },
    "hostage_situation": {
        "location": "Where is the hostage situation occurring?",
        "suspect_description": "Can you describe the suspect(s)?",
        "number_of_hostages": "How many hostages are there?"
    },
    "active_shooter": {
        "location": "Where is the active shooter located?",
        "description": "Describe the shooter if possible.",
        "weapons_seen": "What weapons have been seen?"
    },
    "bomb_threat": {
        "threat_details": "What did the threat say?",
        "location_threatened": "What location was threatened?"
    },
    "kidnapping": {
        "victim_description": "Describe the kidnapped person.",
        "suspect_vehicle": "Describe the suspect's vehicle."
    },
    "animal_attack": {
        "animal_type": "What type of animal attacked?",
        "injuries_reported": "Are there injuries? (yes/no)"
    },
    "emergency_assistance": {
        "nature_of_emergency": "What is the nature of the emergency?",
        "people_involved": "How many people are involved?"
    },
    "alarm_activation": {
        "alarm_type": "What type of alarm is activated? (fire/security/etc.)",
        "visible_issue": "Is there a visible emergency or damage? (yes/no)"
    },

    #cyber_incident_questions
    "data_breach": {
        "systems_affected": "What systems or data appear to be affected?",
        "disconnect_now": "Has the affected system been disconnected from the internet? (yes/no)",
        "sensitive_data": "Is sensitive or personal data involved? (yes/no)"
    },
    "system_hack": {
        "unauthorized_access": "Is there evidence of unauthorized access? (yes/no)",
        "system_type": "What type of system is affected (e.g. email, server, website)?",
        "reported_to_it": "Has this been reported to IT or cybersecurity? (yes/no)"
    },
    "phishing_attack": {
        "link_clicked": "Did anyone click the suspicious link or provide info? (yes/no)",
        "email_content": "Can you describe the phishing email or message?"
    },
    "ransomware": {
        "locked_out": "Are you locked out of your system or files? (yes/no)",
        "ransom_demanded": "Was a ransom demand shown? If so, what did it say?"
    },

    #utility_emergency_questions
    "gas_line_rupture": {
        "location": "Where is the rupture located?",
        "evacuated_area": "Has the area been evacuated? (yes/no)",
        "strong_smell": "Is there a strong smell of gas? (yes/no)"
    },
    "water_main_break": {
        "location": "Where is the water main break?",
        "flooding": "Is there flooding in the area? (yes/no)",
        "water_pressure": "Is there a loss of water pressure? (yes/no)"
    },
    "power_grid_failure": {
        "area_affected": "What area is affected by the power outage?",
        "duration": "How long has the power been out?",
        "downed_lines": "Are there downed power lines? (yes/no)"
    },

    #weather_alert_questions
    "heavy_snowfall": {
        "snow_depth": "How deep is the snow?",
        "travel_impacted": "Is travel impacted? (yes/no)",
        "power_outage": "Are there any power outages? (yes/no)"
    },
    "blizzard": {
        "visibility": "What is the visibility like? (poor/fair/good)",
        "travel_impacted": "Is travel severely impacted? (yes/no)",
        "shelter_needed": "Is shelter needed for anyone? (yes/no)"
    },
    "heatwave": {
        "temperature": "What is the current temperature?",
        "heat_advisories": "Are there any heat advisories in effect? (yes/no)",
        "vulnerable_people": "Are there vulnerable people needing assistance? (yes/no)"
    },
    "storm_surge": {
        "flooding": "Is there flooding due to the storm surge? (yes/no)",
        "evacuated": "Has the area been evacuated? (yes/no)",
        "property_damage": "Is there property damage? (yes/no)"
    },

    #marine_incident_questions
    "boat_capsize": {
        "people_overboard": "Are there people in the water? (yes/no)",
        "rescue_in_progress": "Is a rescue in progress? (yes/no)",
        "location": "Where did the capsizing occur?"
    },
    "drowning": {
        "person_in_water": "Is the person still in the water? (yes/no)",
        "rescue_attempted": "Has a rescue attempt been made? (yes/no)",
        "location": "Where did this occur?"
    },
    "oil_spill": {
        "spill_size": "How large is the oil spill?",
        "environmental_impact": "Is there an environmental impact? (yes/no)",
        "cleanup_initiated": "Has cleanup been initiated? (yes/no)"
    },
    "water_rescue": {
        "people_in_water": "How many people are in the water?",
        "rescue_in_progress": "Is a rescue operation currently in progress? (yes/no)",
        "location": "Where is the rescue taking place?"
    },

    #aviation_incident_questions
    "airplane_crash": {
        "location": "Where did the crash occur?",
        "injuries_reported": "Are there injuries reported? (yes/no)",
        "rescue_in_progress": "Is a rescue operation in progress? (yes/no)"
    },
    "emergency_landing": {
        "location": "Where did the emergency landing occur?",
        "aircraft_type": "What type of aircraft is involved?",
        "passengers_injured": "Are there any injured passengers? (yes/no)"
    },
    "mid_air_distress": {
        "aircraft_type": "What type of aircraft is involved?",
        "nature_of_distress": "What is the nature of the distress?",
        "location": "Where is the aircraft currently located?"
    },
    #public_health_incident_questions
    "disease_outbreak": {
        "disease_name": "What disease is suspected?",
        "number_infected": "How many people are infected?",
        "symptoms_observed": "What symptoms are being observed?"
    },
    "food_contamination": {
        "contaminated_food": "What food is suspected of contamination?",
        "symptoms_reported": "What symptoms are being reported?",
        "number_affected": "How many people are affected?"
    },
    "mass_poisoning": {
        "poison_source": "What is the suspected source of the poisoning?",
        "number_affected": "How many people are affected?",
        "symptoms_observed": "What symptoms are being observed?"
    },
    #crowd_control_questions
    "riot": {
        "location": "Where is the riot occurring?",
        "number_of_people": "How many people are involved?",
        "weapons_present": "Are there any weapons present? (yes/no)"
    },
    "stampede": {
        "location": "Where is the stampede occurring?",
        "number_of_people": "How many people are involved?",
        "injuries_reported": "Are there any injuries reported? (yes/no)"
    },
    "mass_protest": {
        "location": "Where is the protest occurring?",
        "number_of_people": "How many people are involved?",
        "any_violence": "Is there any violence or property damage? (yes/no)"
    },
    "overcrowded_event": {
        "event_type": "What type of event is it (concert, sports, etc.)?",
        "number_of_people": "How many people are present?",
        "safety_concerns": "Are there any safety concerns? (yes/no)"
    },
    #infrastructure_failure_questions
    "bridge_collapse": {
        "location": "Where did the collapse occur?",
        "people_trapped": "Are there people trapped? (yes/no)",
        "extent_of_damage": "Describe the extent of the damage."
    },
    "tunnel_cave_in": {
        "location": "Where did the cave-in occur?",
        "people_trapped": "Are there people trapped? (yes/no)",
        "extent_of_damage": "Describe the extent of the damage."
    },
    "building_integrity_risk": {
        "location": "Where is the building located?",
        "visible_damage": "Is there visible damage to the building? (yes/no)",
        "people_inside": "Are there people still inside? (yes/no)"
    }

}

# Emergency feedback instructions
medical_feedback = {
    "cardiac_arrest": "Start CPR immediately if you're trained. Push hard and fast in the center of the chest.",
    "stroke": "Keep the person calm and still. Don't give them food, water, or medicine.",
    "breathing_difficulty": "Help the person sit upright. Use an inhaler if prescribed. Avoid crowding them.",
    "seizure": "Do not restrain the person. Clear the area and cushion their head. Time the seizure.",
    "unconscious_person": "Check for breathing. If not breathing, start CPR. Keep airway open.",
    "serious_bleeding": "Apply firm pressure with a clean cloth. Elevate the wound if possible.",
    "burns": "Cool the burn with running water for at least 10 minutes. Do not apply creams or ice.",
    "allergic_reaction": "Use an epinephrine auto-injector if available. Keep the person calm.",
    "drug_overdose": "If available, administer naloxone. Keep the person on their side and monitor breathing.",
    "childbirth": "Stay calm. Prepare clean towels. Don't try to delay the birth if crowning is visible.",
    "mental_health_crisis": "Speak calmly. Do not argue or escalate. Keep yourself and others safe."
}

fire_feedback = {
    "structure_fire": "Evacuate immediately. Do not attempt to gather belongings. Stay low to avoid smoke.",
    "vehicle_fire": "Stay away from the vehicle. Do not try to extinguish it yourself if it's large.",
    "wildfire": "Leave the area immediately if instructed. Do not attempt to defend property.",
    "electrical_fire": "Do not use water. Evacuate and report if safe. Shut off electricity if possible.",
    "gas_leak": "Do not use any electronics or light switches. Leave the area and call emergency services.",
    "smoke_investigation": "Evacuate if unsure of the source. Report details to emergency services.",
    "explosion": "Move to a safe location. Watch for secondary explosions. Help others if safe."
}

police_feedback = {
    "robbery": "Stay on the line and in a safe location. Do not confront the suspect.",
    "assault": "Avoid engaging. Provide first aid to victims if safe. Stay on the scene until help arrives.",
    "suspicious_activity": "Do not approach. Observe from a distance and report details to the dispatcher.",
    "burglary": "Do not enter the property. Wait for police to arrive. Stay out of sight if the suspect is present.",
    "gunshots_heard": "Take cover immediately. Stay low and indoors if possible.",
    "weapons_complaint": "Avoid the area. Keep others away. Give as much detail as possible to dispatch.",
    "missing_person": "Search immediate area safely. Provide full description. Stay accessible for updates.",
    "vandalism": "Do not touch anything. Take photos if safe and provide detailed descriptions.",
    "fight": "Keep a safe distance. Only intervene if you're trained and it's safe.",
    "drug_activity": "Do not confront anyone. Report location and behaviors to authorities.",
    "public_disturbance": "Stay calm and avoid escalation. Report numbers and any aggressive behavior."
}

traffic_feedback = {
    "motor_vehicle_accident": "Turn on hazard lights. Don't move injured people unless there's danger.",
    "hit_and_run": "Get the vehicle's plate number and description if safe. Do not chase the driver.",
    "pedestrian_struck": "Do not move the victim unless necessary. Keep them calm and still.",
    "road_blocked": "Warn others if safe. Avoid causing traffic. Report exact location.",
    "vehicle_stalled": "Turn on hazard lights. Stay in the car with seatbelt fastened if in a traffic lane.",
    "highway_pileup": "Stay in your vehicle if safe. Turn on hazards and call emergency services."
}

disaster_feedback = {
    "flooding": "Avoid walking or driving through floodwaters. Move to higher ground immediately.",
    "earthquake": "Drop, cover, and hold on. Stay indoors until the shaking stops.",
    "tornado": "Seek shelter in a basement or interior room. Avoid windows.",
    "hurricane": "Follow evacuation orders. Have emergency supplies ready. Stay indoors away from windows.",
    "landslide": "Evacuate the area immediately. Stay uphill and away from moving debris.",
    "lightning_strike": "Stay indoors. Avoid electrical appliances and water during the storm.",
    "building_collapse": "Stay still and call for help. Tap on pipes if you're trapped.",
    "power_outage": "Use flashlights instead of candles. Unplug appliances. Stay warm or cool appropriately."
}

hazard_feedback = {
    "chemical_spill": "Avoid inhaling or touching the substance. Evacuate the area.",
    "gas_leak_or_smell": "Do not use electronics or ignite flames. Evacuate and report immediately.",
    "biohazard_exposure": "Limit contact. Wash with soap and water. Report exposure immediately.",
    "radiation_leak": "Evacuate immediately if directed. Avoid exposure. Follow public health instructions.",
    "unknown_substance": "Do not touch or move the substance. Report its appearance and location.",
    "environmental_hazard": "Avoid the area. Warn others. Provide detailed information to emergency services."
}

special_situation_feedback = {
    "suicidal_person": "Stay calm and keep the person talking. Remove any dangerous objects nearby.",
    "hostage_situation": "Stay quiet if you're involved. Do not attempt to negotiate or act. Follow dispatcher instructions.",
    "active_shooter": "Run, hide, fight—only if necessary. Stay quiet. Silence your phone.",
    "bomb_threat": "Evacuate if instructed. Do not use cell phones or radios near the scene.",
    "kidnapping": "Provide as much detail as possible. Do not attempt a rescue.",
    "animal_attack": "Move to safety. Do not provoke the animal further. Apply first aid if bitten.",
    "emergency_assistance": "Stay calm. Follow instructions from responders. Give clear information.",
    "alarm_activation": "Evacuate if it's a fire alarm. Wait for emergency responders to assess the situation."
}

cyber_feedback = {
    "data_breach": "Disconnect affected systems. Notify cybersecurity team immediately.",
    "system_hack": "Do not use the system. Notify IT/security and preserve any evidence.",
    "phishing_attack": "Do not click further. Report to your IT/security team.",
    "ransomware": "Do not pay ransom. Disconnect affected systems and contact IT security."
}

utility_feedback = {
    "gas_line_rupture": "Avoid using electronics or lights. Evacuate the area and alert others.",
    "water_main_break": "Avoid the flooded area. Do not use electrical appliances if water is near.",
    "power_grid_failure": "Stay indoors if safe. Report downed lines and avoid contact with them."
}

weather_alert_feedback = {
    "heavy_snowfall": "Avoid travel unless necessary. Clear snow from driveways and walkways.",
    "blizzard": "Stay indoors. Keep warm and have emergency supplies ready.",
    "heatwave": "Stay hydrated. Avoid outdoor activities during peak heat. Use fans or AC if available.",
    "storm_surge": "Evacuate if instructed. Move to higher ground and avoid coastal areas."
}
marine_feedback = {
    "boat_capsize": "Call for marine rescue. Do not enter rough waters unless trained.",
    "drowning": "Call 911 and keep the person in sight. Use a flotation device if available.",
    "oil_spill": "Avoid contact. Report the source and extent to environmental authorities.",
    "water_rescue": "Do not attempt rescue without training. Wait for marine responders."
}
aviation_feedback = {
    "airplane_crash": "Move to a safe distance. Do not enter the crash site unless trained.",
    "emergency_landing": "Clear the area if safe. Assist passengers if needed.",
    "mid_air_distress": "Contact air traffic control. Provide as much detail as possible."
}
public_health_feedback = {
    "disease_outbreak": "Isolate affected individuals. Report to public health authorities.",
    "food_contamination": "Do not consume the food. Report to health department.",
    "mass_poisoning": "Keep affected individuals calm. Do not induce vomiting unless instructed."
}
crowd_control_feedback = {
    "riot": "Stay away from the area. Do not engage. Report details to police.",
    "stampede": "Find a safe place to shelter. Do not try to stop the crowd.",
    "mass_protest": "Avoid confrontation. Stay safe and report any violence.",
    "overcrowded_event": "Alert event security. Help direct people to safety if possible."
}
infrastructure_feedback = {
    "bridge_collapse": "Stay away from the area. Do not attempt to cross or enter.",
    "tunnel_cave_in": "Avoid the area. Report to authorities and assist with evacuation if safe.",
    "building_integrity_risk": "Evacuate the building if safe. Do not re-enter until cleared by professionals."
}

# Emergency responders for each incident type
responders = {
    "medical": [
        "Paramedics", "Doctors", "Emergency Medical Technicians (EMTs)"
    ],
    "fire": [
        "Firefighters", "Hazmat Team", "Rescue Squad"
    ],
    "police": [
        "Police Officers", "SWAT Team", "Bomb Squad", "K9 Unit"
    ],
    "traffic": [
        "Traffic Police", "Highway Patrol", "Paramedics",
        "Tow Services", "Road Maintenance Crew"
    ],
    "natural_disaster": [
        "Firefighters", "Civil Defense / Disaster Management",
        "National Guard / Military", "Medical Emergency Teams",
        "Rescue Operation Teams", "Utility Workers"
    ],
    "hazardous_material": [
        "Hazmat Response Team", "Firefighters", "Police",
        "Medical Emergency Teams", "Environmental Safety Agencies"
    ],
    "special_situations": [
        "Police Officers", "SWAT Team", "Crisis Negotiators",
        "Bomb Squad", "Paramedics", "Animal Control",
        "Mental Health Crisis Team"
    ],
    "cyber_incident": [
        "Cybersecurity Team", "Digital Forensics Experts",
        "Police Cybercrime Unit", "IT Department"
    ],
    "utility_emergency": [
        "Utility Company", "Firefighters", "Police", "Environmental Safety Team"
    ],
    "weather_alert": [
        "Meteorological Department", "Civil Defense / Disaster Relief",
        "Medical Teams", "Utility Crews"
    ],
    "marine_incident": [
        "Coast Guard", "Marine Rescue Teams", "Environmental Protection Agencies",
        "Lifeguards", "Police (Marine Units)"
    ],
    "aviation_incident": [
        "Airport Fire & Rescue", "Air Traffic Control", "Emergency Medical Teams",
        "Aviation Safety Board", "Airport Police / Security"
    ],
    "public_health_incident": [
        "Public Health Department", "Medical Teams", "Epidemiologists",
        "Environmental Inspectors", "WHO/CDC"
    ],
    "crowd_control": [
        "Riot Police", "Event Security", "Medical Teams",
        "Firefighters", "Crowd Management Specialists"
    ],
    "infrastructure_failure": [
        "Structural Engineers", "Firefighters", "Rescue Teams",
        "Police", "Construction Crews", "Utility Workers"
    ]
}

def validate_input(prompt, validation_func, error_msg="Invalid input. Please try again."):
    """Generic input validation helper"""
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        print(error_msg)

def validate_yes_no(input_str):
    """Validate yes/no answers"""
    return input_str.lower() in ('yes', 'no', 'y', 'n')

def validate_phone(phone_str):
    """Validate phone number formats"""
    return any(re.match(pattern, phone_str) for pattern in CONFIG["VALID_PHONE_FORMATS"])

def validate_text(input_str):
    """Validate general text input"""
    return all(c.isalnum() or c in CONFIG["ALLOWED_SPECIAL_CHARS"] for c in input_str)

def safe_write_file(filename, content):
    """Thread-safe file writing with error handling"""
    try:
        with file_lock:
            with open(filename, 'w') as f:
                f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

def safe_read_file(filename):
    """Thread-safe file reading with error handling"""
    try:
        with file_lock:
            with open(filename, 'r') as f:
                return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def get_feedback(incident_type, specific_incident):
    """Get appropriate feedback based on incident type"""
    if incident_type == "medical":
        return medical_feedback.get(specific_incident, "Help is on the way. Stay with the patient.")
    elif incident_type == "fire":
        return fire_feedback.get(specific_incident, "Evacuate the area and wait for responders.")
    elif incident_type == "police":
        return police_feedback.get(specific_incident, "Stay in a safe location and wait for police.")
    elif incident_type == "traffic":
        return traffic_feedback.get(specific_incident, "Turn on hazard lights and check for injuries.")
    elif incident_type == "natural_disaster":
        return disaster_feedback.get(specific_incident, "Move to a safe location immediately.")
    elif incident_type == "hazardous_material":
        return hazard_feedback.get(specific_incident, "Evacuate the area and avoid contact with the substance.")
    elif incident_type == "special_situations":
        return special_situation_feedback.get(specific_incident, "Stay in a safe location and follow instructions.")
    elif incident_type == "cyber_incident":
        return cyber_feedback.get(specific_incident, "Disconnect affected systems and notify IT.")
    elif incident_type == "utility_emergency":
        return utility_feedback.get(specific_incident, "Report the issue to the utility company.")
    elif incident_type == "weather_alert":
        return weather_alert_feedback.get(specific_incident, "Follow local advisories and stay safe.")
    elif incident_type == "marine_incident":
        return marine_feedback.get(specific_incident, "Call for marine rescue and stay clear of the area.")
    elif incident_type == "aviation_incident":
        return aviation_feedback.get(specific_incident, "Move to a safe distance and wait for responders.")
    elif incident_type == "public_health_incident":
        return public_health_feedback.get(specific_incident, "Isolate affected individuals and report to health authorities.")
    elif incident_type == "crowd_control":
        return crowd_control_feedback.get(specific_incident, "Avoid confrontation and report to police.")
    elif incident_type == "infrastructure_failure":
        return infrastructure_feedback.get(specific_incident, "Stay away from the area and report to authorities.")
    else:
        return "Help is on the way. Please remain calm."

def get_next_incident_number():
    """Improved with thread-safety and directory awareness"""
    try:
        incident_files = [f for f in os.listdir(CONFIG["LOG_DIR"]) 
                        if f.startswith("incident_") and f.endswith(".txt")]
        if not incident_files:
            return 1
        
        numbers = []
        for f in incident_files:
            try:
                num = int(f.split('_')[1].split('.')[0])
                numbers.append(num)
            except (IndexError, ValueError):
                continue
                
        return max(numbers) + 1 if numbers else 1
    except Exception as e:
        print(f"Error getting next incident number: {e}")
        return 1  # Fallback

def ask_questions(questions):
    """Enhanced with input validation"""
    responses = {}
    for key, question in questions.items():
        if "yes/no" in question.lower():
            prompt = f"{question} (yes/no): "
            response = validate_input(prompt, validate_yes_no)
        elif "phone" in key.lower():
            prompt = f"{question} (format: XXXXX-XXXXXX or XXXXXXXXXXX): "
            response = validate_input(prompt, validate_phone)
        else:
            prompt = f"{question}: "
            response = validate_input(prompt, validate_text)
        responses[key] = response
    return responses

def log_single_incident(responses, incident_type, specific_incident, feedback):
    """Enhanced with directory management and error handling"""
    try:
        incident_number = get_next_incident_number()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(CONFIG["LOG_DIR"], f"incident_{incident_number:03d}_{timestamp}.txt")
        
        content = f"""=== Incident #{incident_number} ===
Reported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Emergency Type: {incident_type}
Specific Incident: {incident_display_names.get(specific_incident, specific_incident)}

=== General Information ===
"""
        content += "\n".join(f"{k}: {v}" for k, v in responses['general_info'].items())
        content += "\n\n=== Incident Details ===\n"
        content += "\n".join(f"{k}: {v}" for k, v in responses['incident_info'].items())
        content += f"\n\n=== Emergency Instructions ===\n{feedback}\n"
        
        if safe_write_file(filename, content):
            return filename
        return None
    except Exception as e:
        print(f"Critical error logging incident: {e}")
        return None

def log_multiple_incidents(incident_reports):
    """Save multiple incidents to a single file with proper formatting"""
    try:
        incident_number = get_next_incident_number()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(CONFIG["LOG_DIR"], f"incident_{incident_number:03d}_{timestamp}.txt")

        content = f"""=== Incident #{incident_number} ===
Reported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        for i, report in enumerate(incident_reports, 1):
            content += f"--Incident No: {i:02d}--\n\n"
            content += f"Emergency Type: {report['incident_type']}\n"
            content += f"Specific Incident: {incident_display_names.get(report['specific_incident'], report['specific_incident'])}\n\n"

            content += "=== General Information ===\n"
            for key, value in report['general_info'].items():
                content += f"{key}: {value}\n"

            content += "\n=== Incident Details ===\n"
            for key, value in report['incident_info'].items():
                content += f"{key}: {value}\n"

            content += f"\n=== Emergency Instructions ===\n{report['feedback']}\n\n"

        if safe_write_file(filename, content):
            return filename
        return None
    except Exception as e:
        print(f"Error saving incident: {e}")
        return None

def handle_single_incident():
    """Process one complete incident and return its data"""
    print("\n=== New Incident Report ===\n")

    # Ask general questions
    print("Please provide general information about the emergency:")
    general_info = ask_questions(general_questions)

    # Select emergency type
    print("\nSelect the emergency category:")
    categories = list(incident_types.keys())
    for i, category in enumerate(categories):
        print(f"{i+1}. {category.capitalize()}")

    while True:
        try:
            choice = int(validate_input("Enter category number: ", lambda x: x.isdigit() and 1 <= int(x) <= len(categories))) - 1
            incident_type = categories[choice]
            break
        except ValueError:
            print("Invalid selection. Please try again.")

    # Select specific incident
    print(f"\nSelect the specific type of {incident_type} emergency:")
    incidents = incident_types[incident_type]
    for i, incident in enumerate(incidents):
        print(f"{i+1}. {incident_display_names.get(incident, incident)}")

    while True:
        try:
            choice = int(validate_input("Enter incident number: ", lambda x: x.isdigit() and 1 <= int(x) <= len(incidents))) - 1
            specific_incident = incidents[choice]
            break
        except ValueError:
            print("Invalid selection. Please try again.")

    # Ask incident-specific questions
    print(f"\nPlease provide details about the {incident_display_names.get(specific_incident)}:")
    incident_info = ask_questions(incident_questions.get(specific_incident, {}))

    # Get emergency feedback
    feedback = get_feedback(incident_type, specific_incident)
    print(f"\n=== Emergency Instructions ===\n{feedback}\n")

    return {
        'general_info': general_info,
        'incident_type': incident_type,
        'specific_incident': specific_incident,
        'incident_info': incident_info,
        'feedback': feedback
    }

def show_role_selection():
    """Display role selection menu"""
    print("\n=== Emergency Response System ===")
    print("What is your role?")
    print("1. Receiver (First Responder/Staff)")
    print("2. Reporter (Reporting an Emergency)")
    
    while True:
        choice = input("Enter your choice (1-2): ")
        if choice in ('1', '2'):
            return choice
        print("Invalid input. Please enter 1 or 2")

def show_responder_menu():
    """Display responder role selection"""
    print("\nSelect your response role:")
    # Consolidated unique roles from all categories
    all_roles = sorted(list(set(
        role for roles in responders.values() for role in roles
    )))
    
    # Display numbered list
    for i, role in enumerate(all_roles, 1):
        print(f"{i}. {role}")
    
    while True:
        try:
            choice = int(validate_input("Enter your role number: ", 
                                      lambda x: x.isdigit() and 1 <= int(x) <= len(all_roles)))
            return all_roles[choice-1]
        except ValueError:
            print(f"Please enter a number between 1-{len(all_roles)}")

def get_active_incidents():
    """Get sorted list of active incident files"""
    try:
        incident_files = [f for f in os.listdir(CONFIG["LOG_DIR"]) 
                         if f.startswith("incident_") and f.endswith(".txt")]
        return sorted(
            [os.path.join(CONFIG["LOG_DIR"], f) for f in incident_files],
            key=lambda x: os.path.getmtime(x),
            reverse=True
        )[:CONFIG["MAX_INCIDENTS_PER_REPORT"]]
    except Exception as e:
        print(f"Error getting active incidents: {e}")
        return []

def display_incident_list(incident_files):
    """Display formatted list of active incidents"""
    print("\n=== Active Incidents ===")
    print(f"{'#':<3} {'Type':<20} {'Location':<30} {'Time':<20}")
    print("-" * 75)
    
    for i, filename in enumerate(incident_files, 1):
        try:
            content = safe_read_file(filename)
            if not content:
                continue
                
            incident_type = "Unknown"
            location = "Unknown"
            timestamp = "Unknown"
            
            for line in content.split('\n'):
                if line.startswith("Emergency Type:"):
                    incident_type = line.split(":")[1].strip()
                elif line.startswith("location:"):
                    location = line.split(":")[1].strip()
                elif line.startswith("Reported at:"):
                    timestamp = line.split(":")[1].strip()
            
            print(f"{i:<3} {incident_type[:18]:<20} {location[:28]:<30} {timestamp[:18]:<20}")
        except Exception as e:
            print(f"Error displaying incident {filename}: {e}")

def display_incident_details(filename, responder_role):
    """Show detailed incident information for responders"""
    content = safe_read_file(filename)
    if not content:
        print(f"Error reading incident file: {filename}")
        return
    
    print(f"\n{'='*40}")
    print(f"INCIDENT: {os.path.basename(filename)}")
    print('-'*40)
    print(content)
    print('-'*40)
    
    # Extract incident type from file content
    incident_type = None
    for line in content.split('\n'):
        if line.startswith("Emergency Type:"):
            incident_type = line.split(":")[1].strip()
            break
    
    if incident_type and incident_type in responders:
        print("\n[SUGGESTED RESPONSE TEAM]")
        print(', '.join(responders[incident_type]))
        
        if responder_role in responders[incident_type]:
            print("\n\033[1;31mALERT: This incident matches your specialization!\033[0m")
    
    return incident_type

def handle_responder_input(incident_files, responder_role):
    """Process responder actions for an incident"""
    print("\n[ACTIONS] Enter incident number to view details")
    print("Press 'r' to refresh list")
    print("Press 'q' to quit")
    
    while True:
        selection = input("\nSelection: ").lower()
        if selection == 'q':
            return False
        elif selection == 'r':
            return True
            
        try:
            incident_num = int(selection) - 1
            if 0 <= incident_num < len(incident_files):
                filename = incident_files[incident_num]
                incident_type = display_incident_details(filename, responder_role)
                
                print("\n[ACTIONS]")
                print("1. Mark as received")
                print("2. Request backup")
                print("3. Add notes")
                print("4. Resolve incident")
                print("5. Return to list")
                
                while True:
                    action = input("Select action (1-5): ")
                    if action == '1':
                        with open(os.path.join(CONFIG["LOG_DIR"], "response_log.txt"), "a") as log:
                            log.write(f"{datetime.now()} - {responder_role} acknowledged {os.path.basename(filename)}\n")
                        print("Incident acknowledged.")
                    elif action == '2':
                        backup_type = input("Enter backup type needed: ")
                        with open(filename, "a") as f:
                            f.write(f"\n[BACKUP REQUESTED] {datetime.now()} - {backup_type} by {responder_role}\n")
                        print(f"{backup_type} backup requested.")
                    elif action == '3':
                        note = input("Enter your notes: ")
                        with open(filename, "a") as f:
                            f.write(f"\n[NOTES] {datetime.now()} - {responder_role}:\n{note}\n")
                        print("Notes added.")
                    elif action == '4':
                        resolved_filename = os.path.join(
                            CONFIG["RESOLVED_DIR"], 
                            f"resolved_{os.path.basename(filename)}"
                        )
                        os.rename(filename, resolved_filename)
                        print("Incident marked as resolved.")
                        return True
                    elif action == '5':
                        break
                    else:
                        print("Invalid choice. Please enter 1-5")
                
                # After action, show details again if not returning to list
                if action != '5':
                    display_incident_details(filename, responder_role)
                return True
                
            print(f"Please enter 1-{len(incident_files)}, 'r', or 'q'")
        except ValueError:
            print("Invalid input. Please enter a number, 'r', or 'q'")

def handle_receiver_mode():
    """Main function for receiver operations"""
    responder_role = show_responder_menu()
    print(f"\n[System] Logged in as: {responder_role}")
    last_refresh = 0
    
    while True:
        try:
            current_time = time.time()
            if current_time - last_refresh >= CONFIG["REFRESH_INTERVAL"]:
                last_refresh = current_time
                incident_files = get_active_incidents()
                
                if not incident_files:
                    print("\nNo active incidents found")
                    time.sleep(2)
                    continue
                
                display_incident_list(incident_files)
            
            if not handle_responder_input(incident_files, responder_role):
                break
                
        except KeyboardInterrupt:
            print("\nExiting responder mode...")
            break
        except Exception as e:
            print(f"Error in responder mode: {e}")
            time.sleep(2)

def handle_reporter_mode():
    """Main function for reporter operations"""
    print("\n=== Emergency Reporting ===")
    incident_reports = []
    
    while True:
        incident_data = handle_single_incident()
        incident_reports.append(incident_data)
        
        another = validate_input("\nReport another incident? (yes/no): ", validate_yes_no)
        if another.lower() != 'yes':
            break
    
    if incident_reports:
        if len(incident_reports) == 1:
            report = incident_reports[0]
            responses = {
                'general_info': report['general_info'],
                'incident_info': report['incident_info']
            }
            saved_file = log_single_incident(responses, report['incident_type'],
                                           report['specific_incident'], report['feedback'])
        else:
            saved_file = log_multiple_incidents(incident_reports)
        
        if saved_file:
            print(f"\nIncident(s) logged in {os.path.basename(saved_file)}")
            print("Help is on the way! Please follow the provided instructions.")
        
        print("\n=== Summary of Reported Incidents ===")
        for i, report in enumerate(incident_reports, 1):
            print(f"{i}. {incident_display_names.get(report['specific_incident'])} at {report['general_info']['location']}")

def main():
    """Main entry point with error handling"""
    try:
        print("\n=== Emergency Response System ===")
        print(f"Log directory: {os.path.abspath(CONFIG['LOG_DIR'])}")
        
        # Verify write access
        test_file = os.path.join(CONFIG["LOG_DIR"], "test_write.tmp")
        try:
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
        except:
            print("ERROR: Cannot write to log directory!")
            return
        
        role_choice = show_role_selection()
        
        if role_choice == '1':
            handle_receiver_mode()
        else:
            handle_reporter_mode()
            
    except Exception as e:
        print(f"Fatal error: {e}")
    finally:
        print("\nSystem shutdown")

if __name__ == "__main__":
    main()
