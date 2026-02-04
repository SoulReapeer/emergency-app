#incident_data/questions.py

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


def get_questions_for_incident(incident_type):
    """
    Get all questions for a specific incident type
    """
    general = general_questions.copy()
    specific = incident_questions.get(incident_type, {})
    general.update(specific)
    return general
