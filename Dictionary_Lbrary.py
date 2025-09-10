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
