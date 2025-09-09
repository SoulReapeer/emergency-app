# 1-IMPORTS
import os
from datetime import datetime
import time
import re
from threading import Lock
import json

# 2-Configuration
CONFIG = {
    "MAX_INCIDENTS_PER_REPORT": 10,
    "REFRESH_INTERVAL": 5,
    "VALID_PHONE_FORMATS": [r"^\d{5}-\d{6}$", r"^\d{11}$"],
    "ALLOWED_SPECIAL_CHARS": " -.,#/",
    "LOG_DIR": "incident_logs",
    "RESOLVED_DIR": "resolved_incidents",
    "RESPONDER_LOG_DIR": "responder_logs",
    "REPORTS_DIR": "reports",
    "BACKUP_DIR": "backups",
    "PRIORITY_LEVELS": ["Critical", "High", "Medium", "Low"],
    "RESOURCE_INVENTORY": {
        "ambulances": 5,
        "fire_trucks": 3,
        "police_cars": 8,
        "tow_trucks": 2
    }
}

# 3-Create log directories if they do not exists
for directory in [CONFIG["LOG_DIR"], CONFIG["RESOLVED_DIR"], CONFIG["RESPONDER_LOG_DIR"], 
                CONFIG["REPORTS_DIR"], CONFIG["BACKUP_DIR"]]:
    os.makedirs(directory, exist_ok=True)

# 4-Incident display names and types
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
    "alarm_activation": "Alarm Activation",   
    "data_breach": "Data Breach", 
    "system_hack": "System Hack",
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

# 5-Incident categories and their types
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

# 6-General questions for all incidents
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

# 7-Incident-specific questions 
incident_questions = {
    # 7.1-Medical emergencies
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

    # 7.2-Fire emergencies
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

    # 7.3-Police emergencies
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

    # 7.4-Traffic emergencies
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

    # 7.5-Natural disasters
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

    # 7.6-Hazardous materials
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

    # 7.7-Special situations
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

    # 7.8-cyber_incident_questions
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

    # 7.9-utility_emergency_questions
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

    # 7.10-weather_alert_questions
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

    # 7.11-marine_incident_questions
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

    # 7.12-aviation_incident_questions
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

    # 7.13-public_health_incident_questions
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

    # 7.14-crowd_control_questions
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

    # 7.15-infrastructure_failure_questions
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
medical_feedback = { # 8
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

fire_feedback = { # 9
    "structure_fire": "Evacuate immediately. Do not attempt to gather belongings. Stay low to avoid smoke.",
    "vehicle_fire": "Stay away from the vehicle. Do not try to extinguish it yourself if it's large.",
    "wildfire": "Leave the area immediately if instructed. Do not attempt to defend property.",
    "electrical_fire": "Do not use water. Evacuate and report if safe. Shut off electricity if possible.",
    "gas_leak": "Do not use any electronics or light switches. Leave the area and call emergency services.",
    "smoke_investigation": "Evacuate if unsure of the source. Report details to emergency services.",
    "explosion": "Move to a safe location. Watch for secondary explosions. Help others if safe."
}

police_feedback = { # 10
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

traffic_feedback = { # 11
    "motor_vehicle_accident": "Turn on hazard lights. Don't move injured people unless there's danger.",
    "hit_and_run": "Get the vehicle's plate number and description if safe. Do not chase the driver.",
    "pedestrian_struck": "Do not move the victim unless necessary. Keep them calm and still.",
    "road_blocked": "Warn others if safe. Avoid causing traffic. Report exact location.",
    "vehicle_stalled": "Turn on hazard lights. Stay in the car with seatbelt fastened if in a traffic lane.",
    "highway_pileup": "Stay in your vehicle if safe. Turn on hazards and call emergency services."
}

disaster_feedback = { # 12
    "flooding": "Avoid walking or driving through floodwaters. Move to higher ground immediately.",
    "earthquake": "Drop, cover, and hold on. Stay indoors until the shaking stops.",
    "tornado": "Seek shelter in a basement or interior room. Avoid windows.",
    "hurricane": "Follow evacuation orders. Have emergency supplies ready. Stay indoors away from windows.",
    "landslide": "Evacuate the area immediately. Stay uphill and away from moving debris.",
    "lightning_strike": "Stay indoors. Avoid electrical appliances and water during the storm.",
    "building_collapse": "Stay still and call for help. Tap on pipes if you're trapped.",
    "power_outage": "Use flashlights instead of candles. Unplug appliances. Stay warm or cool appropriately."
}

hazard_feedback = { # 13
    "chemical_spill": "Avoid inhaling or touching the substance. Evacuate the area.",
    "gas_leak_or_smell": "Do not use electronics or ignite flames. Evacuate and report immediately.",
    "biohazard_exposure": "Limit contact. Wash with soap and water. Report exposure immediately.",
    "radiation_leak": "Evacuate immediately if directed. Avoid exposure. Follow public health instructions.",
    "unknown_substance": "Do not touch or move the substance. Report its appearance and location.",
    "environmental_hazard": "Avoid the area. Warn others. Provide detailed information to emergency services."
}

special_situation_feedback = { # 14
    "suicidal_person": "Stay calm and keep the person talking. Remove any dangerous objects nearby.",
    "hostage_situation": "Stay quiet if you're involved. Do not attempt to negotiate or act. Follow dispatcher instructions.",
    "active_shooter": "Run, hide, fight—only if necessary. Stay quiet. Silence your phone.",
    "bomb_threat": "Evacuate if instructed. Do not use cell phones or radios near the scene.",
    "kidnapping": "Provide as much detail as possible. Do not attempt a rescue.",
    "animal_attack": "Move to safety. Do not provoke the animal further. Apply first aid if bitten.",
    "emergency_assistance": "Stay calm. Follow instructions from responders. Give clear information.",
    "alarm_activation": "Evacuate if it's a fire alarm. Wait for emergency responders to assess the situation."
}

cyber_feedback = { # 15
    "data_breach": "Disconnect affected systems. Notify cybersecurity team immediately.",
    "system_hack": "Do not use the system. Notify IT/security and preserve any evidence.",
    "phishing_attack": "Do not click further. Report to your IT/security team.",
    "ransomware": "Do not pay ransom. Disconnect affected systems and contact IT security."
}

utility_feedback = { # 16
    "gas_line_rupture": "Avoid using electronics or lights. Evacuate the area and alert others.",
    "water_main_break": "Avoid the flooded area. Do not use electrical appliances if water is near.",
    "power_grid_failure": "Stay indoors if safe. Report downed lines and avoid contact with them."
}

weather_alert_feedback = { # 17
    "heavy_snowfall": "Avoid travel unless necessary. Clear snow from driveways and walkways.",
    "blizzard": "Stay indoors. Keep warm and have emergency supplies ready.",
    "heatwave": "Stay hydrated. Avoid outdoor activities during peak heat. Use fans or AC if available.",
    "storm_surge": "Evacuate if instructed. Move to higher ground and avoid coastal areas."
}

marine_feedback = { # 18
    "boat_capsize": "Call for marine rescue. Do not enter rough waters unless trained.",
    "drowning": "Call 911 and keep the person in sight. Use a flotation device if available.",
    "oil_spill": "Avoid contact. Report the source and extent to environmental authorities.",
    "water_rescue": "Do not attempt rescue without training. Wait for marine responders."
}

aviation_feedback = { # 19
    "airplane_crash": "Move to a safe distance. Do not enter the crash site unless trained.",
    "emergency_landing": "Clear the area if safe. Assist passengers if needed.",
    "mid_air_distress": "Contact air traffic control. Provide as much detail as possible."
}

public_health_feedback = { # 20
    "disease_outbreak": "Isolate affected individuals. Report to public health authorities.",
    "food_contamination": "Do not consume the food. Report to health department.",
    "mass_poisoning": "Keep affected individuals calm. Do not induce vomiting unless instructed."
}

crowd_control_feedback = { # 21
    "riot": "Stay away from the area. Do not engage. Report details to police.",
    "stampede": "Find a safe place to shelter. Do not try to stop the crowd.",
    "mass_protest": "Avoid confrontation. Stay safe and report any violence.",
    "overcrowded_event": "Alert event security. Help direct people to safety if possible."
}

infrastructure_feedback = { # 22
    "bridge_collapse": "Stay away from the area. Do not attempt to cross or enter.",
    "tunnel_cave_in": "Avoid the area. Report to authorities and assist with evacuation if safe.",
    "building_integrity_risk": "Evacuate the building if safe. Do not re-enter until cleared by professionals."
}

# 23-Emergency responders for each incident type
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

# 24-Categorized Responder Directory
responder_categories = {
    "medical": ["Doctors", "Paramedics", "EMTs", "Medical Teams"],
    "fire": ["Firefighters", "Hazmat Team", "Rescue Squad"],
    "police": ["Police Officers", "SWAT Team", "K9 Unit"],
    "traffic": ["Traffic Police", "Tow Services"],
    "natural_disaster": ["Disaster Management", "Rescue Teams"],
    "hazardous_material": ["Hazmat Team", "Environmental Safety"],
    "special_situations": ["SWAT Team", "Crisis Negotiators"],
    "cyber_incident": ["Cyber Crime Unit", "IT Security"],
    "utility_emergency": ["Utility Company", "Repair Crews"],
    "weather_alert": ["Meteorological Department"],
    "marine_incident": ["Coast Guard", "Marine Rescue"],
    "aviation_incident": ["Air Traffic Control", "Airport Rescue"],
    "public_health_incident": ["Medical Teams", "Health Department"],
    "crowd_control": ["Police Officers", "Event Security"],
    "infrastructure_failure": ["Engineers", "Repair Crews"]
}

# 25-Responder Management System
responder_management_prompts = {
    "medical": {"unit_prompt": "Enter medical unit:", "destination_prompt": "Hospital destination:", "reason_prompt": "Transport reason:", "status_options": ["Admitted", "Under Treatment", "Discharged"]},
    "fire": {"unit_prompt": "Enter fire unit:", "destination_prompt": "Evacuation location:", "reason_prompt": "Deployment reason:", "status_options": ["Contained", "Under Control", "Extinguished"]},
    "police": {"unit_prompt": "Enter police unit:", "destination_prompt": "Detention location:", "reason_prompt": "Response reason:", "status_options": ["In Custody", "Released", "Under Investigation"]},
    "traffic": {"unit_prompt": "Enter traffic unit:", "destination_prompt": "Vehicle destination:", "reason_prompt": "Response reason:", "status_options": ["Cleared", "Under Investigation", "Towed"]},
    "natural_disaster": {"unit_prompt": "Enter response team:", "destination_prompt": "Shelter location:", "reason_prompt": "Deployment reason:", "status_options": ["Rescue Complete", "Ongoing Operations", "Area Secured"]},
    "hazardous_material": {"unit_prompt": "Enter HAZMAT team:", "destination_prompt": "Containment location:", "reason_prompt": "Cleanup reason:", "status_options": ["Contained", "Cleanup Complete", "Ongoing Decontamination"]},
    "special_situations": {"unit_prompt": "Enter special team:", "destination_prompt": "Secure location:", "reason_prompt": "Deployment reason:", "status_options": ["Resolved", "Suspect Neutralized", "Ongoing Operation"]},
    "cyber_incident": {"unit_prompt": "Enter cyber team:", "destination_prompt": "Evidence location:", "reason_prompt": "Investigation reason:", "status_options": ["Contained", "Under Investigation", "Systems Restored"]},
    "utility_emergency": {"unit_prompt": "Enter utility crew:", "destination_prompt": "Repair location:", "reason_prompt": "Repair reason:", "status_options": ["Repair Complete", "Service Restored", "Ongoing Repair"]},
    "weather_alert": {"unit_prompt": "Enter response team:", "destination_prompt": "Shelter location:", "reason_prompt": "Response reason:", "status_options": ["Alert Lifted", "Ongoing Monitoring", "Recovery Operations"]},
    "marine_incident": {"unit_prompt": "Enter marine unit:", "destination_prompt": "Rescue location:", "reason_prompt": "Rescue reason:", "status_options": ["Rescue Complete", "Vessel Secured", "Ongoing Recovery"]},
    "aviation_incident": {"unit_prompt": "Enter aviation team:", "destination_prompt": "Crash location:", "reason_prompt": "Response reason:", "status_options": ["Rescue Complete", "Investigation Ongoing", "Cleanup Complete"]},
    "public_health_incident": {"unit_prompt": "Enter health team:", "destination_prompt": "Treatment location:", "reason_prompt": "Response reason:", "status_options": ["Contained", "Under Treatment", "Outbreak Controlled"]},
    "crowd_control": {"unit_prompt": "Enter control unit:", "destination_prompt": "Processing location:", "reason_prompt": "Control reason:", "status_options": ["Situation Controlled", "Crowd Dispersed", "Arrests Processed"]},
    "infrastructure_failure": {"unit_prompt": "Enter repair crew:", "destination_prompt": "Repair location:", "reason_prompt": "Repair reason:", "status_options": ["Repair Complete", "Structure Secured", "Ongoing Repair"]}
}

# 26-Responder Management Database Structure
RESPONDER_MANAGEMENT_TEMPLATES = {
    "medical": {
        "responder_sources": ["Hospital", "Clinic", "Ambulance Base", "Medical Team", "Field Hospital"],
        "destinations": ["Hospital Emergency", "ICU", "Trauma Center", "Burn Unit", "General Ward", "Discharged"],
        "purposes": ["Trauma Care", "Cardiac Emergency", "Burn Treatment", "Surgery", "Observation", "Rehabilitation"],
        "status_options": ["Admitted", "Under Treatment", "Stable", "Critical", "Discharged", "Transferred", "Deceased"]
    },
    "fire": {
        "responder_sources": ["Fire Station", "Rescue Unit", "Hazmat Team", "Aerial Unit", "Command Post"],
        "destinations": ["Shelter", "Hospital", "Temporary Housing", "Family Home", "Morgue", "Damage Assessment"],
        "purposes": ["Fire Suppression", "Rescue Operation", "Evacuation", "Investigation", "Salvage", "Overhaul"],
        "status_options": ["Contained", "Under Control", "Extinguished", "Investigation", "Cleanup", "Completed"]
    },
    "police": {
        "responder_sources": ["Police Station", "Patrol Unit", "SWAT Team", "K9 Unit", "Traffic Division"],
        "destinations": ["Police Station", "Jail", "Court", "Hospital", "Safe House", "Rehabilitation Center"],
        "purposes": ["Arrest", "Investigation", "Protection", "Traffic Control", "Evidence Collection", "Interrogation"],
        "status_options": ["In Custody", "Under Investigation", "Charged", "Released", "Transferred", "Case Closed"]
    },
    "traffic": {
        "responder_sources": ["Traffic Police", "Highway Patrol", "Tow Service", "Rescue Unit", "Maintenance Crew"],
        "destinations": ["Hospital", "Impound Lot", "Repair Shop", "Insurance Assessment", "Traffic Court"],
        "purposes": ["Accident Investigation", "Vehicle Recovery", "Traffic Control", "Road Clearance", "Citation"],
        "status_options": ["Cleared", "Under Investigation", "Towed", "Repair Needed", "Case Resolved"]
    },
    "natural_disaster": {
        "responder_sources": ["Disaster Response", "Red Cross", "Military Units", "Search & Rescue", "NGO Teams"],
        "destinations": ["Shelter", "Field Hospital", "Distribution Center", "Temporary Housing", "Evacuation Center"],
        "purposes": ["Search & Rescue", "Evacuation", "Medical Aid", "Supply Distribution", "Damage Assessment"],
        "status_options": ["Ongoing", "Stabilized", "Recovery Phase", "Rebuilding", "Completed"]
    },
    "hazardous_material": {
        "responder_sources": ["Hazmat Team", "Environmental Agency", "Fire Department", "Specialized Cleanup"],
        "destinations": ["Decontamination", "Hospital", "Secure Storage", "Disposal Facility", "Laboratory"],
        "purposes": ["Containment", "Decontamination", "Cleanup", "Investigation", "Environmental Protection"],
        "status_options": ["Contained", "Decontaminating", "Cleanup Ongoing", "Monitoring", "Resolved"]
    },
    "special_situations": {
        "responder_sources": ["SWAT Team", "Bomb Squad", "Hostage Negotiation", "Tactical Unit", "Intelligence"],
        "destinations": ["High-Security Prison", "Hospital", "Safe Location", "Evidence Lockup", "Court"],
        "purposes": ["Hostage Rescue", "Bomb Disposal", "Terrorism Response", "High-Risk Arrest", "Crisis Management"],
        "status_options": ["Active", "Resolved", "Suspect Neutralized", "Evidence Collected", "Case Ongoing"]
    },
    "cyber_incident": {
        "responder_sources": ["Cyber Crime Unit", "IT Security", "Digital Forensics", "Network Defense", "Expert Team"],
        "destinations": ["Forensic Lab", "Secure Server", "Backup System", "Recovery Center", "Legal Department"],
        "purposes": ["Intrusion Analysis", "Data Recovery", "System Hardening", "Evidence Preservation", "Legal Action"],
        "status_options": ["Investigating", "Contained", "Systems Restored", "Vulnerability Patched", "Case Closed"]
    },
    "utility_emergency": {
        "responder_sources": ["Utility Company", "Repair Crew", "Engineering Team", "Emergency Response", "Maintenance"],
        "destinations": ["Repair Site", "Substation", "Control Center", "Backup System", "Customer Service"],
        "purposes": ["Power Restoration", "Gas Line Repair", "Water Main Fix", "Infrastructure Repair", "Service Restoration"],
        "status_options": ["Repairing", "Partially Restored", "Fully Restored", "Monitoring", "Completed"]
    },
    "weather_alert": {
        "responder_sources": ["Meteorological Dept", "Emergency Management", "Rescue Teams", "Evacuation Units"],
        "destinations": ["Shelter", "Emergency Housing", "Distribution Point", "Warning Center", "Recovery Site"],
        "purposes": ["Evacuation", "Warning Dissemination", "Search & Rescue", "Supply Distribution", "Damage Assessment"],
        "status_options": ["Alert Active", "Evacuating", "Sheltering", "Recovery", "All Clear"]
    },
    "marine_incident": {
        "responder_sources": ["Coast Guard", "Navy Units", "Port Authority", "Marine Rescue", "Salvage Team"],
        "destinations": ["Hospital", "Port", "Dry Dock", "Investigation Center", "Insurance Assessment"],
        "purposes": ["Search & Rescue", "Spill Containment", "Vessel Recovery", "Investigation", "Environmental Cleanup"],
        "status_options": ["Rescue Ongoing", "Contained", "Vessel Secured", "Cleanup", "Investigation Complete"]
    },
    "aviation_incident": {
        "responder_sources": ["Airport Rescue", "NTSB Team", "Airline Response", "Medical Teams", "Investigation"],
        "destinations": ["Hospital", "Morgue", "Investigation Hangar", "Airlines Office", "Safety Board"],
        "purposes": ["Search & Rescue", "Crash Investigation", "Victim Identification", "Safety Review", "Recovery"],
        "status_options": ["Rescue Phase", "Investigation", "Recovery", "Safety Review", "Report Complete"]
    },
    "public_health_incident": {
        "responder_sources": ["Health Department", "WHO Teams", "Medical Response", "Epidemiology", "Research Teams"],
        "destinations": ["Hospital", "Quarantine", "Testing Center", "Research Lab", "Vaccination Site"],
        "purposes": ["Disease Control", "Contact Tracing", "Treatment", "Vaccination", "Research"],
        "status_options": ["Outbreak", "Contained", "Treating", "Monitoring", "Resolved"]
    },
    "crowd_control": {
        "responder_sources": ["Riot Police", "Event Security", "Crowd Management", "Tactical Units", "Medics"],
        "destinations": ["Police Station", "Hospital", "Processing Center", "Court", "Release"],
        "purposes": ["Crowd Dispersion", "Arrest", "Medical Aid", "Investigation", "Event Management"],
        "status_options": ["Active", "Controlled", "Processing", "Medical Treatment", "Resolved"]
    },
    "infrastructure_failure": {
        "responder_sources": ["Engineering Corps", "Construction Crews", "Emergency Repair", "Safety Inspectors"],
        "destinations": ["Repair Site", "Temporary Structure", "Alternative Route", "Assessment Center", "Project Office"],
        "purposes": ["Structural Repair", "Safety Assessment", "Temporary Solution", "Rebuilding", "Prevention"],
        "status_options": ["Assessing", "Emergency Repair", "Rebuilding", "Monitoring", "Completed"]
    }
}

# 27-Enhanced Systems
class UserSession: 
    # Initialize user session
    def __init__(self):
        self.logged_in_user = None
        self.user_role = None
        self.login_time = None
        self.activities = []
    
    # User login
    def login(self, username, role):
        self.logged_in_user = username
        self.user_role = role
        self.login_time = datetime.now()
        self.activities.append(f"Login at {self.login_time}")
        print(f"Welcome, {username} ({role})!")
    
    # Log user activity
    def log_activity(self, activity):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.activities.append(f"{timestamp}: {activity}")
    
    # Show session summary
    def show_session_summary(self):
        if self.logged_in_user:
            print(f"\n=== Session Summary for {self.logged_in_user} ===")
            print(f"Login time: {self.login_time}")
            print(f"Role: {self.user_role}")
            print("Recent activities:")
            for activity in self.activities[-5:]:
                print(f"  - {activity}")
    
    # User logout
    def logout(self):
        if self.logged_in_user:
            self.log_activity("Logout")
            print(f"Goodbye, {self.logged_in_user}!")
            self.logged_in_user = None

# 28-Resource Management System
class ResourceManager:
    # Initialize resource manager
    def __init__(self):
        self.resources = CONFIG["RESOURCE_INVENTORY"].copy()
        self.deployed_resources = {}
    
    # Deploy resources to an incident
    def deploy_resource(self, resource_type, incident_id, quantity=1):
        if self.resources.get(resource_type, 0) >= quantity:
            self.resources[resource_type] -= quantity
            self.deployed_resources.setdefault(incident_id, {})[resource_type] = \
                self.deployed_resources.get(incident_id, {}).get(resource_type, 0) + quantity
            return True
        return False
    
    # Return resources from an incident
    def return_resource(self, incident_id, resource_type, quantity=1):
        if self.deployed_resources.get(incident_id, {}).get(resource_type, 0) >= quantity:
            self.resources[resource_type] += quantity
            self.deployed_resources[incident_id][resource_type] -= quantity
            return True
        return False
    
    # Get current resource status
    def get_available_resources(self):
        return self.resources
    
    # Get deployed resources
    def get_deployed_resources(self):
        return self.deployed_resources

# 29-User Management System
class UserManager:
    # Initialize user manager
    def __init__(self):
        self.users = self.load_users()
    
    # Load users from file or create default users
    def load_users(self):
        users_file = "users.txt"
        users = {}
        if os.path.exists(users_file):
            try:
                with open(users_file, 'r') as f:
                    for line in f:
                        if ':' in line:
                            username, password, role = line.strip().split(':')
                            users[username] = {"password": password, "role": role}
            except:
                users = self.create_default_users()
        else:
            users = self.create_default_users()
        return users
    
    # Create default users
    def create_default_users(self):
        users = {
            "admin": {"password": "admin123", "role": "administrator"},
            "responder1": {"password": "resp123", "role": "responder"},
            "reporter1": {"password": "report123", "role": "reporter"}
        }
        self.save_users(users)
        return users
    
    # Save users to file
    def save_users(self, users):
        with open("users.txt", 'w') as f:
            for username, data in users.items():
                f.write(f"{username}:{data['password']}:{data['role']}\n")
    
    # Authenticate user credentials
    def authenticate_user(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            return user
        return None
    
    # Create a new user
    def create_user(self, username, password, role):
        if username not in self.users:
            self.users[username] = {"password": password, "role": role}
            self.save_users(self.users)
            return True
        return False

# 30-Responder Management System
class ResponderManager:
    # Initialize responder manager
    def __init__(self):
        self.responder_logs = {}
        self.management_file = "responder_management.db"
        self.load_management_data()
    
    # Load management data from file
    def load_management_data(self):
        """Load responder management data from file"""
        if os.path.exists(self.management_file):
            try:
                with open(self.management_file, 'r') as f:
                    self.responder_logs = json.load(f)
            except:
                self.responder_logs = {}
        else:
            self.responder_logs = {}
    
    # Save management data to file
    def save_management_data(self):
        """Save responder management data to file"""
        with open(self.management_file, 'w') as f:
            json.dump(self.responder_logs, f, indent=2)
    
    # Log responder action for an incident
    def log_responder_action(self, incident_id, category, action_data):
        """Log responder management action"""
        if incident_id not in self.responder_logs:
            self.responder_logs[incident_id] = []
        
        action_data.update({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "category": category
        })
        
        self.responder_logs[incident_id].append(action_data)
        self.save_management_data()
        return True
    
    # Get responder log for a specific incident
    def get_incident_responder_log(self, incident_id):
        """Get responder management log for specific incident"""
        return self.responder_logs.get(incident_id, [])
    
    # Get overall responder statistics
    def get_responder_stats(self, responder_type=None):
        """Get statistics about responder actions"""
        stats = {
            "total_incidents": len(self.responder_logs),
            "by_category": {},
            "by_status": {},
            "recent_actions": []
        }
        
        for incident_id, actions in self.responder_logs.items():
            for action in actions:
                category = action.get('category', 'unknown')
                status = action.get('status', 'unknown')
                
                stats["by_category"][category] = stats["by_category"].get(category, 0) + 1
                stats["by_status"][status] = stats["by_status"].get(status, 0) + 1
                
                if len(stats["recent_actions"]) < 10:  # Keep last 10 actions
                    stats["recent_actions"].append(action)
        
        return stats

# 31-GLOBAL INSTANCES AND UTILITIES
file_lock = Lock()
user_session = UserSession()
resource_manager = ResourceManager()
user_manager = UserManager()
responder_manager = ResponderManager()

# 32-Utility Functions
def validate_input(prompt, validation_func, error_msg="Invalid input. Please try again."):
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        print(error_msg)

# 33-Validation functions
def validate_yes_no(input_str):
    return input_str.lower() in ('yes', 'no', 'y', 'n')

# 34-Simple phone number validation
def validate_phone(phone_str):
    return any(re.match(pattern, phone_str) for pattern in CONFIG["VALID_PHONE_FORMATS"])

# 35-Simple text validation
def validate_text(input_str):
    return all(c.isalnum() or c in CONFIG["ALLOWED_SPECIAL_CHARS"] for c in input_str)

# 36-Thread-safe file operations
def safe_write_file(filename, content):
    try:
        with file_lock:
            with open(filename, 'w') as f:
                f.write(content)
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False

# 37-Thread-safe file reading
def safe_read_file(filename):
    try:
        with file_lock:
            with open(filename, 'r') as f:
                return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# 38-Get feedback based on incident type and specific incident
def get_feedback(incident_type, specific_incident):
    feedback_mapping = {
        "medical": medical_feedback, "fire": fire_feedback, "police": police_feedback,
        "traffic": traffic_feedback, "natural_disaster": disaster_feedback,
        "hazardous_material": hazard_feedback, "special_situations": special_situation_feedback,
        "cyber_incident": cyber_feedback, "utility_emergency": utility_feedback,
        "weather_alert": weather_alert_feedback, "marine_incident": marine_feedback,
        "aviation_incident": aviation_feedback, "public_health_incident": public_health_feedback,
        "crowd_control": crowd_control_feedback, "infrastructure_failure": infrastructure_feedback
    }
    return feedback_mapping.get(incident_type, {}).get(specific_incident, "Help is on the way. Please remain calm.")

# 39-Get next incident number
def get_next_incident_number():
    try:
        incident_files = [f for f in os.listdir(CONFIG["LOG_DIR"]) if f.startswith("incident_") and f.endswith(".txt")]
        if not incident_files: return 1
        numbers = []
        for f in incident_files:
            try: numbers.append(int(f.split('_')[1].split('.')[0]))
            except: continue
        return max(numbers) + 1 if numbers else 1
    except Exception as e:
        print(f"Error getting next incident number: {e}")
        return 1

# 40-Question Asking System
def ask_questions(questions):
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

# 41-Priority System
def assign_incident_priority(incident_type, specific_incident, responses):
    priority_rules = {
        "medical": {"cardiac_arrest": "Critical", "stroke": "Critical", "unconscious_person": "Critical", 
                    "serious_bleeding": "High", "breathing_difficulty": "High", "default": "Medium"},
        "fire": {"structure_fire": "Critical", "explosion": "Critical", "gas_leak": "High", 
                "vehicle_fire": "High", "default": "Medium"},
        "police": {"active_shooter": "Critical", "hostage_situation": "Critical", "robbery": "High", 
                    "assault": "High", "default": "Medium"},
        "default": "Medium"
    }
    category_rule = priority_rules.get(incident_type, priority_rules["default"])
    priority = category_rule.get(specific_incident, category_rule.get("default", "Medium"))
    if responses.get('is_anyone_injured', '').lower() in ('yes', 'y'):
        if priority == "Medium": priority = "High"
        elif priority == "Low": priority = "Medium"
    return priority

# 42-Auto-deploy resources based on incident type
def auto_deploy_resources(incident_type, incident_id):
    deployment_rules = {
        "medical": {"ambulances": 1}, "fire": {"fire_trucks": 1, "ambulances": 1},
        "police": {"police_cars": 1}, "traffic": {"police_cars": 1, "tow_trucks": 1}
    }
    resources_to_deploy = deployment_rules.get(incident_type, {})
    for resource, quantity in resources_to_deploy.items():
        if resource_manager.deploy_resource(resource, incident_id, quantity):
            print(f"Auto-deployed {quantity} {resource} to incident #{incident_id}")

# 43-Log Single Incident
def log_single_incident(responses, incident_type, specific_incident, feedback):
    try:
        incident_number = get_next_incident_number()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(CONFIG["LOG_DIR"], f"incident_{incident_number:03d}_{timestamp}.txt")
        priority = assign_incident_priority(incident_type, specific_incident, responses['general_info'])
        
        content = f"""=== Incident #{incident_number} ===
Reported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Priority: {priority}

Emergency Type: {incident_type}
Specific Incident: {incident_display_names.get(specific_incident, specific_incident)}

=== General Information ===
"""
        content += "\n".join(f"{k}: {v}" for k, v in responses['general_info'].items())
        content += "\n\n=== Incident Details ===\n"
        content += "\n".join(f"{k}: {v}" for k, v in responses['incident_info'].items())
        content += f"\n\n=== Emergency Instructions ===\n{feedback}\n"
        
        if safe_write_file(filename, content):
            auto_deploy_resources(incident_type, incident_number)
            return filename
        return None
    except Exception as e:
        print(f"Critical error logging incident: {e}")
        return None

# 44-Responder Management System
def responder_management(incident_id, incident_type, location):
    """Comprehensive responder management system for all categories"""
    print(f"\n=== RESPONDER MANAGEMENT: {incident_type.upper()} ===")
    
    if incident_type not in RESPONDER_MANAGEMENT_TEMPLATES:
        print("No specific responder management for this incident type.")
        return None
    
    template = RESPONDER_MANAGEMENT_TEMPLATES[incident_type]
    
    print("\n--- Responder Source ---")
    print("Where did the responders come from?")
    for i, source in enumerate(template["responder_sources"], 1):
        print(f"{i}. {source}")
    print(f"{len(template['responder_sources'])+1}. Custom source")
    
    source_choice = validate_input("Select responder source: ", 
        lambda x: x.isdigit() and 1 <= int(x) <= len(template["responder_sources"])+1)
    
    if int(source_choice) <= len(template["responder_sources"]):
        responder_source = template["responder_sources"][int(source_choice)-1]
    else:
        responder_source = validate_input("Enter custom responder source: ", validate_text)
    
    print("\n--- Destination ---")
    print("Where were people/resources sent?")
    for i, destination in enumerate(template["destinations"], 1):
        print(f"{i}. {destination}")
    print(f"{len(template['destinations'])+1}. Custom destination")
    
    dest_choice = validate_input("Select destination: ", 
        lambda x: x.isdigit() and 1 <= int(x) <= len(template["destinations"])+1)
    
    if int(dest_choice) <= len(template["destinations"]):
        destination = template["destinations"][int(dest_choice)-1]
    else:
        destination = validate_input("Enter custom destination: ", validate_text)
    
    print("\n--- Purpose ---")
    print("What was the purpose of this action?")
    for i, purpose in enumerate(template["purposes"], 1):
        print(f"{i}. {purpose}")
    print(f"{len(template['purposes'])+1}. Custom purpose")
    
    purpose_choice = validate_input("Select purpose: ", 
        lambda x: x.isdigit() and 1 <= int(x) <= len(template["purposes"])+1)
    
    if int(purpose_choice) <= len(template["purposes"]):
        purpose = template["purposes"][int(purpose_choice)-1]
    else:
        purpose = validate_input("Enter custom purpose: ", validate_text)
    
    print("\n--- Status ---")
    print("Current status of this response:")
    for i, status in enumerate(template["status_options"], 1):
        print(f"{i}. {status}")
    
    status_choice = validate_input("Select status: ", 
        lambda x: x.isdigit() and 1 <= int(x) <= len(template["status_options"]))
    
    status = template["status_options"][int(status_choice)-1]
    
    # Additional details based on category
    additional_info = {}
    if incident_type == "medical":
        additional_info["patient_count"] = validate_input("Number of patients: ", lambda x: x.isdigit())
        additional_info["condition"] = validate_input("Overall condition: ", validate_text)
    
    elif incident_type == "fire":
        additional_info["units_dispatched"] = validate_input("Units dispatched: ", validate_text)
        additional_info["casualties"] = validate_input("Casualties reported: ", lambda x: x.isdigit())
    
    elif incident_type == "police":
        additional_info["suspects"] = validate_input("Number of suspects: ", lambda x: x.isdigit())
        additional_info["case_id"] = validate_input("Case ID (if any): ", validate_text)
    
    elif incident_type == "traffic":
        additional_info["vehicles_involved"] = validate_input("Vehicles involved: ", lambda x: x.isdigit())
        additional_info["road_conditions"] = validate_input("Road conditions: ", validate_text)
    
    elif incident_type == "natural_disaster":
        additional_info["people_rescued"] = validate_input("People rescued: ", lambda x: x.isdigit())
        additional_info["supplies_distributed"] = validate_input("Supplies distributed: ", lambda x: x.isdigit())
    
    elif incident_type == "hazardous_material":         
        additional_info["material_type"] = validate_input("Type of hazardous material: ", validate_text)
        additional_info["containment_status"] = validate_input("Containment status: ", validate_text)
    
    elif incident_type == "special_situations":         
        additional_info["operation_duration"] = validate_input("Operation duration (minutes): ", lambda x: x.isdigit())
        additional_info["special_equipment_used"] = validate_input("Special equipment used: ", validate_text)
    
    elif incident_type == "cyber_incident":
        additional_info["systems_affected"] = validate_input("Systems affected: ", validate_text)
        additional_info["data_breach"] = validate_input("Data breach occurred (yes/no): ", validate_yes_no)
    
    elif incident_type == "utility_emergency":
        additional_info["service_type"] = validate_input("Type of utility service: ", validate_text)
        additional_info["outage_duration"] = validate_input("Outage duration (minutes): ", lambda x: x.isdigit())
    
    elif incident_type == "weather_alert":
        additional_info["alert_level"] = validate_input("Alert level: ", validate_text)
        additional_info["areas_affected"] = validate_input("Areas affected: ", validate_text)
    
    elif incident_type == "marine_incident":
        additional_info["vessel_type"] = validate_input("Type of vessel: ", validate_text)
        additional_info["rescue_operations"] = validate_input("Rescue operations conducted: ", lambda x: x.isdigit())
    
    elif incident_type == "aviation_incident":
        additional_info["aircraft_type"] = validate_input("Type of aircraft: ", validate_text)
        additional_info["passenger_count"] = validate_input("Number of passengers: ", lambda x: x.isdigit())
    
    elif incident_type == "public_health_incident":
        additional_info["disease_type"] = validate_input("Type of disease: ", validate_text)
        additional_info["cases_reported"] = validate_input("Number of cases reported: ", lambda x: x.isdigit())
    
    elif incident_type == "crowd_control":
        additional_info["crowd_size"] = validate_input("Estimated crowd size: ", lambda x: x.isdigit())
        additional_info["incidents_reported"] = validate_input("Incidents reported: ", lambda x: x.isdigit())
    
    elif incident_type == "infrastructure_failure":
        additional_info["structure_type"] = validate_input("Type of structure: ", validate_text)
        additional_info["repair_estimate"] = validate_input("Estimated repair time (hours): ", lambda x: x.isdigit())
    
    
    # Create management record
    management_data = {
        "responder_source": responder_source,
        "destination": destination,
        "purpose": purpose,
        "status": status,
        "location": location,
        "additional_info": additional_info
    }
    
    # Log the action
    responder_manager.log_responder_action(incident_id, incident_type, management_data)
    
    # Summary of management action
    print("\n--- Summary of Responder Management ---") #section header
    print(f"Responder Source: {responder_source}") #where responders came from
    print(f"Destination: {destination}") #where resources/people were sent
    print(f"Purpose: {purpose}") #purpose of action
    print(f"Status: {status}") #current status
    print(f"Location: {location}") #location of incident
    if additional_info:
        print("Additional Info:")
        for k, v in additional_info.items():
            print(f"  - {k.replace('_', ' ').capitalize()}: {v}") #formatted key-value nicely
            
    print(f"\n✅ Responder management logged for incident #{incident_id}")
    return management_data

# 45-User Authentication
def authenticate_user():
    print("\n=== User Authentication ===")
    username = input("Username: ")
    password = input("Password: ")
    user = user_manager.authenticate_user(username, password)
    if user: return user, username
    print("Authentication failed. Please try again.")
    return None, None

# 46-Categorized Responder Selection
def show_categorized_responder_menu():
    print("\n=== Select Your Response Category ===")
    available_categories = [cat for cat in responder_categories.keys() if responder_categories[cat]]
    for i, category in enumerate(available_categories, 1): print(f"{i}. {category.capitalize()}")
    
    while True:
        try:
            choice = int(validate_input("Enter category number: ", 
                lambda x: x.isdigit() and 1 <= int(x) <= len(available_categories)))
            selected_category = available_categories[choice-1]
            break
        except ValueError:
            print(f"Please enter a number between 1-{len(available_categories)}")
    
    print(f"\n=== {selected_category.upper()} Response Roles ===")
    roles = responder_categories[selected_category]
    for i, role in enumerate(roles, 1): print(f"{i}. {role}")
    
    while True:
        try:
            role_choice = int(validate_input("Enter role number: ", 
                lambda x: x.isdigit() and 1 <= int(x) <= len(roles)))
            selected_role = roles[role_choice-1]
            return selected_role, selected_category
        except ValueError:
            print(f"Please enter a number between 1-{len(roles)}")

# 47-Incident Retrieval
def get_active_incidents():
    try:
        incident_files = [f for f in os.listdir(CONFIG["LOG_DIR"]) if f.startswith("incident_") and f.endswith(".txt")]
        return sorted([os.path.join(CONFIG["LOG_DIR"], f) for f in incident_files],
            key=lambda x: os.path.getmtime(x), reverse=True)[:CONFIG["MAX_INCIDENTS_PER_REPORT"]]
    except Exception as e:
        print(f"Error getting active incidents: {e}")
        return []

# 48-Incident List Display
def display_incident_list(incident_files):
    print("\n=== Active Incidents ===")
    print(f"{'#':<3} {'Type':<20} {'Location':<30} {'Time':<20}")
    print("-" * 75)
    for i, filename in enumerate(incident_files, 1):
        try:
            content = safe_read_file(filename)
            if not content: 
                print(f"{i:<3} Unable to read file")
                continue
            
            # Debug: show first few lines of content
            print(f"DEBUG: {filename} content starts with:")
            for j, line in enumerate(content.split('\n')[:5]):
                print(f"  {j}: {line}")
            
            incident_type, location, timestamp = "Unknown", "Unknown", "Unknown"
            for line in content.split('\n'):
                if line.startswith("Emergency Type:"): 
                    incident_type = line.split(":")[1].strip()
                elif line.startswith("Location:"): 
                    location = line.split(":")[1].strip()
                elif line.startswith("Reported at:"): 
                    timestamp = line.split(":")[1].strip()
            
            print(f"{i:<3} {incident_type[:18]:<20} {location[:28]:<30} {timestamp[:18]:<20}")
        except Exception as e:
            print(f"Error displaying incident {filename}: {e}")

# 49-Incident Detail View and Recommendations
def display_incident_details(filename, responder_role, responder_category):
    content = safe_read_file(filename)
    if not content: return None, None
    print(f"\n{'='*40}\nINCIDENT: {os.path.basename(filename)}\n{'-'*40}\n{content}\n{'-'*40}")
    
    incident_type, location = None, None
    for line in content.split('\n'):
        if line.startswith("Emergency Type:"): 
            incident_type = line.split(":")[1].strip()
        elif line.startswith("Location:"):  # Changed to capital L
            location = line.split(":")[1].strip()

    if incident_type and incident_type in responders:
        print("\n[SUGGESTED RESPONSE TEAM]")
        print(', '.join(responders[incident_type]))
        if incident_type == responder_category:
            print(f"\n\033[1;31mALERT: This {incident_type} incident matches your {responder_category} specialization!\033[0m")
        elif responder_role in responders[incident_type]:
            print(f"\n\033[1;33mNOTICE: Your specific role ({responder_role}) is recommended for this incident!\033[0m")
    
    return incident_type, location

# 50-Responder Interaction Loop
def handle_responder_input(incident_files, responder_role, responder_category):
    print("\n[ACTIONS] Enter incident number to view details")
    print("Press 'r' to refresh list")
    print("Press 'q' to quit")
    
    while True:
        selection = input("\nSelection: ").lower()
        if selection == 'q': return False
        elif selection == 'r': return True
        
        try:
            incident_num = int(selection) - 1
            if 0 <= incident_num < len(incident_files):
                filename = incident_files[incident_num]
                incident_type, location = display_incident_details(filename, responder_role, responder_category)
                incident_id = int(os.path.basename(filename).split('_')[1].split('.')[0])
                
                print("\n[ACTIONS]")
                print("1. Mark as received")
                print("2. Request backup")
                print("3. Add notes")
                print("4. Responder management")
                print("5. Resolve incident")
                print("6. Return to list")
                
                while True:
                    action = input("Select action (1-6): ")
                    if action == '1':
                        user_session.log_activity(f"Acknowledged incident #{incident_id}")
                        with open(os.path.join(CONFIG["LOG_DIR"], "response_log.txt"), "a") as log:
                            log.write(f"{datetime.now()} - {responder_role} acknowledged {os.path.basename(filename)}\n")
                        print("Incident acknowledged.")
                    elif action == '2':
                        backup_type = input("Enter backup type needed: ")
                        user_session.log_activity(f"Requested {backup_type} backup for incident #{incident_id}")
                        with open(filename, "a") as f:
                            f.write(f"\n[BACKUP REQUESTED] {datetime.now()} - {backup_type} by {responder_role}\n")
                        print(f"{backup_type} backup requested.")
                    elif action == '3':
                        note = input("Enter your notes: ")
                        user_session.log_activity(f"Added notes to incident #{incident_id}")
                        with open(filename, "a") as f:
                            f.write(f"\n[NOTES] {datetime.now()} - {responder_role}:\n{note}\n")
                        print("Notes added.")
                    elif action == '4':
                        if incident_type and location:
                            user_session.log_activity(f"Accessed responder management for incident #{incident_id}")
                            responder_info = responder_management(incident_id, incident_type, location)
                            if responder_info:
                                with open(filename, "a") as f:
                                    f.write(f"\n[RESPONDER MANAGEMENT] {datetime.now()}:\n")
                                    f.write(f"Responder Source: {responder_info['responder_source']}\n")
                                    f.write(f"Destination: {responder_info['destination']}\n")
                                    f.write(f"Purpose: {responder_info['purpose']}\n")
                                    f.write(f"Status: {responder_info['status']}\n")
                                    if responder_info['additional_info']:
                                        f.write("Additional Info:\n")
                                        for key, value in responder_info['additional_info'].items():
                                            f.write(f"  {key}: {value}\n")
                        else:
                            print("Cannot access responder management without incident type and location.")
                    elif action == '5':
                        user_session.log_activity(f"Resolved incident #{incident_id}")
                        deployed_resources = resource_manager.get_deployed_resources().get(incident_id, {})
                        for resource, count in deployed_resources.items():
                            resource_manager.return_resource(incident_id, resource, count)
                        resolved_filename = os.path.join(CONFIG["RESOLVED_DIR"], f"resolved_{os.path.basename(filename)}")
                        os.rename(filename, resolved_filename)
                        print("Incident marked as resolved.")
                        return True
                    elif action == '6': break
                    else: print("Invalid choice. Please enter 1-6")
                return True
            print(f"Please enter 1-{len(incident_files)}, 'r', or 'q'")
        except ValueError:
            print("Invalid input. Please enter a number, 'r', or 'q'")

# 51-Backup and Reporting Systems
def backup_system_data():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(CONFIG["BACKUP_DIR"], f"backup_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)
    
    for data_dir in [CONFIG["LOG_DIR"], CONFIG["RESOLVED_DIR"], CONFIG["RESPONDER_LOG_DIR"], CONFIG["REPORTS_DIR"]]:
        if os.path.exists(data_dir):
            backup_subdir = os.path.join(backup_dir, os.path.basename(data_dir))
            os.makedirs(backup_subdir, exist_ok=True)
            for file in os.listdir(data_dir):
                if file.endswith(".txt"):
                    src = os.path.join(data_dir, file)
                    dst = os.path.join(backup_subdir, file)
                    with open(src, 'r') as source, open(dst, 'w') as destination:
                        destination.write(source.read())
    
    print(f"Backup created: {backup_dir}")
    return backup_dir

# 52-Responder Report Generation
def generate_responder_report():
    """Generate comprehensive responder management report"""
    stats = responder_manager.get_responder_stats()
    
    report_content = f"""=== RESPONDER MANAGEMENT REPORT ===
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Total Incidents Managed: {stats['total_incidents']}

=== Statistics by Category ===
"""
    for category, count in stats['by_category'].items():
        report_content += f"{category}: {count}\n"
    
    report_content += "\n=== Statistics by Status ===\n"
    for status, count in stats['by_status'].items():
        report_content += f"{status}: {count}\n"
    
    report_content += "\n=== Recent Responder Actions ===\n"
    for action in stats['recent_actions']:
        report_content += f"\nTime: {action.get('timestamp', 'N/A')}\n"
        report_content += f"Category: {action.get('category', 'N/A')}\n"
        report_content += f"Responder: {action.get('responder_source', 'N/A')}\n"
        report_content += f"Destination: {action.get('destination', 'N/A')}\n"
        report_content += f"Status: {action.get('status', 'N/A')}\n"
        report_content += "-" * 40 + "\n"
    
    report_file = os.path.join(CONFIG["REPORTS_DIR"], f"responder_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    safe_write_file(report_file, report_content)
    print(f"Responder report generated: {report_file}")
    return report_file

# 53-View Responder Management Details
def view_responder_management(incident_id):
    """View responder management details for specific incident"""
    actions = responder_manager.get_incident_responder_log(incident_id)
    
    if not actions:
        print(f"No responder management records found for incident #{incident_id}")
        return
    
    print(f"\n=== Responder Management for Incident #{incident_id} ===")
    for i, action in enumerate(actions, 1):
        print(f"\n--- Action #{i} ---")
        print(f"Time: {action.get('timestamp', 'N/A')}")
        print(f"Category: {action.get('category', 'N/A')}")
        print(f"Responder Source: {action.get('responder_source', 'N/A')}")
        print(f"Destination: {action.get('destination', 'N/A')}")
        print(f"Purpose: {action.get('purpose', 'N/A')}")
        print(f"Status: {action.get('status', 'N/A')}")
        
        if action.get('additional_info'):
            print("Additional Info:")
            for key, value in action['additional_info'].items():
                print(f"  {key}: {value}")

# 54-Daily Reporting
def generate_daily_report():
    today = datetime.now().strftime("%Y-%m-%d")
    incident_files = [f for f in os.listdir(CONFIG["LOG_DIR"]) if f.startswith("incident_") and today in f]
    resolved_files = [f for f in os.listdir(CONFIG["RESOLVED_DIR"]) if f.startswith("resolved_") and today in f]
    
    report_content = f"Daily Incident Report - {today}\n{'='*50}\n\n"
    report_content += f"Total Incidents: {len(incident_files) + len(resolved_files)}\n"
    report_content += f"Active Incidents: {len(incident_files)}\n"
    report_content += f"Resolved Incidents: {len(resolved_files)}\n\n"
    
    category_count = {}
    all_files = incident_files + resolved_files
    directories = [CONFIG["LOG_DIR"]] * len(incident_files) + [CONFIG["RESOLVED_DIR"]] * len(resolved_files)
    
    for file, directory in zip(all_files, directories):
        content = safe_read_file(os.path.join(directory, file))
        if content:
            for line in content.split('\n'):
                if line.startswith("Emergency Type:"):
                    category = line.split(":")[1].strip()
                    category_count[category] = category_count.get(category, 0) + 1
                    break
    
    report_content += "Incidents by Category:\n"
    for category, count in category_count.items(): report_content += f"  {category}: {count}\n"
    
    report_file = os.path.join(CONFIG["REPORTS_DIR"], f"report_{today}.txt")
    safe_write_file(report_file, report_content)
    print(f"Daily report generated: {report_file}")
    return report_file

# 55-System Statistics
def show_system_statistics():
    print("\n=== System Statistics ===")
    active_incidents = len([f for f in os.listdir(CONFIG["LOG_DIR"]) if f.startswith("incident_")])
    resolved_incidents = len([f for f in os.listdir(CONFIG["RESOLVED_DIR"]) if f.startswith("resolved_")])
    print(f"Active Incidents: {active_incidents}")
    print(f"Resolved Incidents: {resolved_incidents}")
    print(f"Total Incidents: {active_incidents + resolved_incidents}")
    
    print("\nResource Status:")
    available = resource_manager.get_available_resources()
    deployed = resource_manager.get_deployed_resources()
    for resource, count in available.items():
        deployed_count = sum(incident_resources.get(resource, 0) for incident_resources in deployed.values())
        print(f"  {resource}: {count} available, {deployed_count} deployed")
    
    category_count = {}
    for directory in [CONFIG["LOG_DIR"], CONFIG["RESOLVED_DIR"]]:
        for file in os.listdir(directory):
            if file.startswith(("incident_", "resolved_")):
                content = safe_read_file(os.path.join(directory, file))
                if content:
                    for line in content.split('\n'):
                        if line.startswith("Emergency Type:"):
                            category = line.split(":")[1].strip()
                            category_count[category] = category_count.get(category, 0) + 1
                            break
    
    print("\nIncidents by Category:")
    for category, count in category_count.items(): print(f"  {category}: {count}")


# 56-User Management
def manage_users_menu():
    if user_session.user_role != "administrator":
        print("Access denied. Administrator privileges required.")
        return
    
    while True:
        print("\n=== User Management ===")
        print("1. List Users")
        print("2. Create User")
        print("3. Back to Advanced Menu")
        
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            print("\nCurrent Users:")
            for username, data in user_manager.users.items():
                print(f"  {username}: {data['role']}")
        elif choice == '2':
            username = input("Enter new username: ")
            password = input("Enter password: ")
            role = input("Enter role (administrator/responder/reporter): ")
            if user_manager.create_user(username, password, role):
                print(f"User {username} created successfully!")
            else: print("User creation failed. Username may already exist.")
        elif choice == '3': break
        else: print("Invalid choice. Please try again.")

# 57-Resource Status Display
def show_resource_status():
    print("\n=== Resource Status ===")
    available = resource_manager.get_available_resources()
    deployed = resource_manager.get_deployed_resources()
    
    print("Available Resources:")
    for resource, count in available.items(): print(f"  {resource}: {count}")
    
    print("\nDeployed Resources:")
    if deployed:
        for incident_id, resources in deployed.items():
            print(f"  Incident #{incident_id}:")
            for resource, count in resources.items(): print(f"    {resource}: {count}")
    else: print("  No resources currently deployed")

# 58-Multi-Incident Reporting System
def handle_multi_incident_report():
    """Handle reporting of multiple incidents across categories in one go"""
    print("\n=== Emergency Reporting ===\n")
    
    # Get general information first (only once)
    print("Please provide general information about the emergency:")
    general_info = ask_questions(general_questions)
    
    selected_incidents = []  # Store (category, specific_incident) pairs
    
    print("\n" + "-" * 50)
    print("Select the emergency categories involved (separate by commas):")
    
    # Display all categories in order
    categories = list(incident_types.keys())
    for i, category in enumerate(categories, 1):
        print(f"{i}. {category.replace('_', ' ').title()}")
    
    # Get category selections
    while True:
        try:
            category_input = input("\nEnter category numbers: ").strip()
            if not category_input:
                print("Please select at least one category.")
                continue
                
            selected_category_nums = []
            for num in category_input.split(','):
                num = num.strip()
                if num.isdigit() and 1 <= int(num) <= len(categories):
                    selected_category_nums.append(int(num))
            
            if selected_category_nums:
                selected_categories = [categories[num-1] for num in selected_category_nums]
                print(f"(You selected: {', '.join([cat.replace('_', ' ').title() for cat in selected_categories])})")
                break
            else:
                print("Invalid selection. Please choose valid category numbers.")
                
        except ValueError:
            print("Please enter numbers separated by commas.")
    
    # For each selected category, let user choose specific incidents
    for category in selected_categories:
        print(f"\n{'-' * 50}")
        print(f"Select incidents for {category.replace('_', ' ').title()} (separate by commas):")
        
        incidents = incident_types[category]
        for i, incident in enumerate(incidents, 1):
            display_name = incident_display_names.get(incident, incident.replace('_', ' ').title())
            print(f"{i}. {display_name}")
        
        while True:
            try:
                incident_input = input(f"\nEnter numbers for {category.replace('_', ' ').title()}: ").strip()
                if not incident_input:
                    print("Please make a selection or type 'skip' to move on.")
                    continue
                
                if incident_input.lower() == 'skip':
                    break
                
                selected_incident_nums = []
                for num in incident_input.split(','):
                    num = num.strip()
                    if num.isdigit() and 1 <= int(num) <= len(incidents):
                        selected_incident_nums.append(int(num))
                
                if selected_incident_nums:
                    for num in selected_incident_nums:
                        specific_incident = incidents[num-1]
                        selected_incidents.append((category, specific_incident))
                    
                    # Show what was selected
                    selected_names = [incident_display_names.get(incidents[num-1], incidents[num-1].replace('_', ' ').title()) 
                                    for num in selected_incident_nums]
                    print(f"(You selected: {', '.join(selected_names)})")
                    break
                else:
                    print("Invalid selection. Please choose valid incident numbers.")
                    
            except ValueError:
                print("Please enter numbers separated by commas.")
    
    if not selected_incidents:
        print("No incidents selected. Returning to main menu.")
        return []
    
    print(f"\n{'-' * 50}")
    print("Now please provide extra details for the selected incidents:\n")
    
    incident_reports = [] 
    
    for category, specific_incident in selected_incidents:
        display_name = incident_display_names.get(specific_incident, specific_incident.replace('_', ' ').title())
        print(f"[{category.replace('_', ' ').title()} → {display_name}]")
        
        # Get incident-specific questions
        specific_questions = incident_questions.get(specific_incident, {})
        incident_info = {}
        
        for key, question in specific_questions.items():
            response = validate_input(f"{question}: ", validate_text)
            incident_info[key] = response
        
        print()  # Add spacing between incidents
        
        # Get feedback
        feedback = get_feedback(category, specific_incident)
        
        incident_reports.append({
            'general_info': general_info,
            'incident_type': category,
            'specific_incident': specific_incident,
            'incident_info': incident_info,
            'feedback': feedback
        })
    
    return incident_reports

# 59-Consolidated Incident Logging
def log_multi_incident_report(incident_reports):
    """Log multiple incidents with consolidated emergency instructions"""
    try:
        incident_number = get_next_incident_number()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join(CONFIG["LOG_DIR"], f"incident_{incident_number:03d}_{timestamp}.txt")
        
        content = f"""=== INCIDENT REPORT #{incident_number} ===
Reported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Location: {incident_reports[0]['general_info']['location']}
Total Incident Types: {len(incident_reports)}

=== General Information ===
"""
        # Add general info
        for key, value in incident_reports[0]['general_info'].items():
            content += f"{key}: {value}\n"
        
        content += "\n" + "=" * 60 + "\n\n"
        content += "=== INCIDENT DETAILS ===\n\n"
        
        # Group incidents by category
        incidents_by_category = {}
        for report in incident_reports:
            category = report['incident_type']
            if category not in incidents_by_category:
                incidents_by_category[category] = []
            incidents_by_category[category].append(report)
        
        # Add incidents by category with details
        for category, reports in incidents_by_category.items():
            content += f"--- {category.replace('_', ' ').upper()} ---\n"
            
            for report in reports:
                display_name = incident_display_names.get(report['specific_incident'], report['specific_incident'].replace('_', ' ').title())
                content += f"\n{display_name}:\n"
                
                if report['incident_info']:
                    for key, value in report['incident_info'].items():
                        content += f"  {key}: {value}\n"
            
            content += "\n"
        
        content += "=" * 60 + "\n\n"
        content += "=== EMERGENCY INSTRUCTIONS ===\n\n"
        
        # Group instructions by category
        instructions_by_category = {}
        for report in incident_reports:
            category = report['incident_type']
            display_name = incident_display_names.get(report['specific_incident'], report['specific_incident'].replace('_', ' ').title())
            
            if category not in instructions_by_category:
                instructions_by_category[category] = []
            instructions_by_category[category].append(f"{display_name}: {report['feedback']}")
        
        # Add instructions by category
        for category, instructions in instructions_by_category.items():
            content += f"- {category.replace('_', ' ').title()}:\n"
            for instruction in instructions:
                content += f"  {instruction}\n"
            content += "\n"
        
        if safe_write_file(filename, content):
            return filename
        return None
        
    except Exception as e:
        print(f"Error logging incident report: {e}")
        return None

# 60-Reporter Mode
def handle_reporter_mode():
    """Main function for reporter operations - Now only multi-incident reporting"""
    print("\n=== Emergency Reporting ===")
    
    incident_reports = handle_multi_incident_report()
    
    if incident_reports:
        saved_file = log_multi_incident_report(incident_reports)
        
        if saved_file:
            print(f"\n{'=' * 50}")
            print(f"Incident(s) logged in {os.path.basename(saved_file)}")
            print("Help is on the way! Please follow the instructions.")
            
            # Show summary
            print("\n=== Emergency Instructions ===")
            instructions_by_category = {}
            for report in incident_reports:
                category = report['incident_type']
                display_name = incident_display_names.get(report['specific_incident'], report['specific_incident'].replace('_', ' ').title())
                
                if category not in instructions_by_category:
                    instructions_by_category[category] = []
                instructions_by_category[category].append(display_name)
            
            # Show instructions by category
            for category, incidents in instructions_by_category.items():
                print(f"- {category.replace('_', ' ').title()} ({', '.join(incidents)}):")
                # Show general category instruction
                category_feedback = {
                    "medical": "Provide medical assistance and first aid. Check ABCs (Airway, Breathing, Circulation).",
                    "fire": "Evacuate area immediately. Fight fire only if safe to do so. Avoid smoke inhalation.",
                    "police": "Secure area and maintain safety. Preserve evidence if possible.",
                    "traffic": "Control traffic flow. Ensure scene safety. Provide assistance to victims.",
                    "natural_disaster": "Evacuate to safe location. Follow emergency alerts and instructions.",
                    "hazardous_material": "Evacuate immediately. Avoid contact with hazardous materials.",
                    "special_situations": "Follow specialized emergency procedures. Maintain safety perimeter.",
                    "cyber_incident": "Disconnect affected systems. Preserve digital evidence.",
                    "utility_emergency": "Avoid affected area. Wait for utility company response.",
                    "weather_alert": "Seek shelter immediately. Monitor weather updates.",
                    "marine_incident": "Deploy life-saving equipment. Coordinate water rescue.",
                    "aviation_incident": "Secure crash site. Provide emergency medical care.",
                    "public_health_incident": "Implement isolation measures. Follow health protocols.",
                    "crowd_control": "Maintain order. Ensure public safety.",
                    "infrastructure_failure": "Evacuate unsafe structures. Await engineering assessment."
                }
                print(f"  {category_feedback.get(category, 'Follow standard emergency procedures and await responder instructions.')}")
                print()

# 61-Responder Mode
def handle_receiver_mode():
    user, username = authenticate_user()
    if not user: return
    if user["role"] not in ["administrator", "responder"]:
        print("Access denied. Responder or administrator privileges required.")
        return
    
    responder_role, responder_category = show_categorized_responder_menu()
    user_session.login(username, user["role"])
    user_session.log_activity(f"Logged in as {responder_role}")
    print(f"\n[System] Logged in as: {responder_role} ({responder_category} category)")
    last_refresh = 0
    
    try:
        while True:
            current_time = time.time()
            if current_time - last_refresh >= CONFIG["REFRESH_INTERVAL"]:
                last_refresh = current_time
                incident_files = get_active_incidents()
                if not incident_files:
                    print("\nNo active incidents found")
                    time.sleep(2)
                    continue
                display_incident_list(incident_files)
            
            if not handle_responder_input(incident_files, responder_role, responder_category): break
                
    except KeyboardInterrupt: print("\nExiting responder mode...")
    except Exception as e: print(f"Error in responder mode: {e}")
    finally: user_session.logout()

# 62-Enhanced Menu System
def show_advanced_menu():
    while True:
        print("\n=== Advanced Menu ===")
        print("1. View System Statistics")
        print("2. Generate Daily Report")
        print("3. Create System Backup")
        print("4. View Session History")
        print("5. Manage Users")
        print("6. View Resource Status")
        print("7. Responder Management Report")
        print("8. View Responder Actions")
        print("9. Return to Main Menu")
        
        choice = input("Enter your choice (1-9): ")
        if choice == '1': show_system_statistics()
        elif choice == '2': generate_daily_report()
        elif choice == '3': backup_system_data()
        elif choice == '4': user_session.show_session_summary()
        elif choice == '5': manage_users_menu()
        elif choice == '6': show_resource_status()
        elif choice == '7': 
            generate_responder_report()
        elif choice == '8':
            incident_id = input("Enter incident ID to view actions: ")
        elif choice == '9': break
        else: print("Invalid choice. Please enter a number between 1-9.")

# 63-Role Selection
def show_role_selection():
    print("\n=== Emergency Response System ===")
    print("What is your role?")
    print("1. Receiver (First Responder/Staff)")
    print("2. Reporter (Reporting an Emergency)")
    
    while True:
        choice = input("Enter your choice (1-2): ")
        if choice in ('1', '2'): return choice
        print("Invalid input. Please enter 1 or 2")

# 64-Main Function
def main():
    try:
        print("\n=== Emergency Response System ===")
        
        while True:
            print("\n=== Main Menu ===")
            print("1. Responder Mode")
            print("2. Reporter Mode")
            print("3. Advanced Options")
            print("4. Exit System")
            
            choice = input("Enter your choice (1-4): ")
            if choice == '1': handle_receiver_mode()
            elif choice == '2': handle_reporter_mode()
            elif choice == '3': show_advanced_menu()
            elif choice == '4':
                print("Thank you for using the Emergency Response System!")
                break
            else: print("Invalid choice. Please try again.")
                
    except Exception as e: print(f"Fatal error: {e}")
    finally: print("\nSystem shutdown")

# 65-Entry Point
if __name__ == "__main__":
    main()
