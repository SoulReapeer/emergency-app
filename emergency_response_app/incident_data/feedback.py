#incident_data/feedback.py

emergency_feedback = {
    "medical": { # 8
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
    },

    "fire" : { # 9
        "structure_fire": "Evacuate immediately. Do not attempt to gather belongings. Stay low to avoid smoke.",
        "vehicle_fire": "Stay away from the vehicle. Do not try to extinguish it yourself if it's large.",
        "wildfire": "Leave the area immediately if instructed. Do not attempt to defend property.",
        "electrical_fire": "Do not use water. Evacuate and report if safe. Shut off electricity if possible.",
        "gas_leak": "Do not use any electronics or light switches. Leave the area and call emergency services.",
        "smoke_investigation": "Evacuate if unsure of the source. Report details to emergency services.",
        "explosion": "Move to a safe location. Watch for secondary explosions. Help others if safe."
    },

    "police": { # 10
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
    },

    "traffic": { # 11
        "motor_vehicle_accident": "Turn on hazard lights. Don't move injured people unless there's danger.",
        "hit_and_run": "Get the vehicle's plate number and description if safe. Do not chase the driver.",
        "pedestrian_struck": "Do not move the victim unless necessary. Keep them calm and still.",
        "road_blocked": "Warn others if safe. Avoid causing traffic. Report exact location.",
        "vehicle_stalled": "Turn on hazard lights. Stay in the car with seatbelt fastened if in a traffic lane.",
        "highway_pileup": "Stay in your vehicle if safe. Turn on hazards and call emergency services."
    },

    "natural_disaster": { # 12
        "flooding": "Avoid walking or driving through floodwaters. Move to higher ground immediately.",
        "earthquake": "Drop, cover, and hold on. Stay indoors until the shaking stops.",
        "tornado": "Seek shelter in a basement or interior room. Avoid windows.",
        "hurricane": "Follow evacuation orders. Have emergency supplies ready. Stay indoors away from windows.",
        "landslide": "Evacuate the area immediately. Stay uphill and away from moving debris.",
        "lightning_strike": "Stay indoors. Avoid electrical appliances and water during the storm.",
        "building_collapse": "Stay still and call for help. Tap on pipes if you're trapped.",
        "power_outage": "Use flashlights instead of candles. Unplug appliances. Stay warm or cool appropriately."
    },

    "hazardous_material": { # 13
        "chemical_spill": "Avoid inhaling or touching the substance. Evacuate the area.",
        "gas_leak_or_smell": "Do not use electronics or ignite flames. Evacuate and report immediately.",
        "biohazard_exposure": "Limit contact. Wash with soap and water. Report exposure immediately.",
        "radiation_leak": "Evacuate immediately if directed. Avoid exposure. Follow public health instructions.",
        "unknown_substance": "Do not touch or move the substance. Report its appearance and location.",
        "environmental_hazard": "Avoid the area. Warn others. Provide detailed information to emergency services."
    },

    "special_situation": { # 14
        "suicidal_person": "Stay calm and keep the person talking. Remove any dangerous objects nearby.",
        "hostage_situation": "Stay quiet if you're involved. Do not attempt to negotiate or act. Follow dispatcher instructions.",
        "active_shooter": "Run, hide, fight—only if necessary. Stay quiet. Silence your phone.",
        "bomb_threat": "Evacuate if instructed. Do not use cell phones or radios near the scene.",
        "kidnapping": "Provide as much detail as possible. Do not attempt a rescue.",
        "animal_attack": "Move to safety. Do not provoke the animal further. Apply first aid if bitten.",
        "emergency_assistance": "Stay calm. Follow instructions from responders. Give clear information.",
        "alarm_activation": "Evacuate if it's a fire alarm. Wait for emergency responders to assess the situation."
    },

    "cyber_incident": { # 15
        "data_breach": "Disconnect affected systems. Notify cybersecurity team immediately.",
        "system_hack": "Do not use the system. Notify IT/security and preserve any evidence.",
        "phishing_attack": "Do not click further. Report to your IT/security team.",
        "ransomware": "Do not pay ransom. Disconnect affected systems and contact IT security."
    },

    "utility_emergency": { # 16
        "gas_line_rupture": "Avoid using electronics or lights. Evacuate the area and alert others.",
        "water_main_break": "Avoid the flooded area. Do not use electrical appliances if water is near.",
        "power_grid_failure": "Stay indoors if safe. Report downed lines and avoid contact with them."
    },

    "weather_alert": { # 17
        "heavy_snowfall": "Avoid travel unless necessary. Clear snow from driveways and walkways.",
        "blizzard": "Stay indoors. Keep warm and have emergency supplies ready.",
        "heatwave": "Stay hydrated. Avoid outdoor activities during peak heat. Use fans or AC if available.",
        "storm_surge": "Evacuate if instructed. Move to higher ground and avoid coastal areas."
    },

    "marine_incident": { # 18
        "boat_capsize": "Call for marine rescue. Do not enter rough waters unless trained.",
        "drowning": "Call 911 and keep the person in sight. Use a flotation device if available.",
        "oil_spill": "Avoid contact. Report the source and extent to environmental authorities.",
        "water_rescue": "Do not attempt rescue without training. Wait for marine responders."
    },

    "aviation_incident": { # 19
        "airplane_crash": "Move to a safe distance. Do not enter the crash site unless trained.",
        "emergency_landing": "Clear the area if safe. Assist passengers if needed.",
        "mid_air_distress": "Contact air traffic control. Provide as much detail as possible."
    },

    "public_health_incident": { # 20
        "disease_outbreak": "Isolate affected individuals. Report to public health authorities.",
        "food_contamination": "Do not consume the food. Report to health department.",
        "mass_poisoning": "Keep affected individuals calm. Do not induce vomiting unless instructed."
    },

    "crowd_control": { # 21
        "riot": "Stay away from the area. Do not engage. Report details to police.",
        "stampede": "Find a safe place to shelter. Do not try to stop the crowd.",
        "mass_protest": "Avoid confrontation. Stay safe and report any violence.",
        "overcrowded_event": "Alert event security. Help direct people to safety if possible."
    },

    "infrastructure_failure": { # 22
        "bridge_collapse": "Stay away from the area. Do not attempt to cross or enter.",
        "tunnel_cave_in": "Avoid the area. Report to authorities and assist with evacuation if safe.",
        "building_integrity_risk": "Evacuate the building if safe. Do not re-enter until cleared by professionals."
    }
}


def get_feedback_for_incident(incident_type):
    for category, incidents in emergency_feedback.items():
        if incident_type in incidents:
            return incidents[incident_type]
    return "Follow general emergency procedures. Stay safe and await professional help."
