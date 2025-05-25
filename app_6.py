import os
from datetime import datetime

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
    "alarm_activation": "Alarm Activation"
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
    ]
}

# General questions for all incidents
general_questions = {
    "location": "What is the address of the emergency?",
    "phone_number": "What is the phone number you're calling from?",
    "name": "What is your name?",
    "incident_description": "Tell me exactly what happened."
}

# Incident-specific questions
incident_questions = {
    "cardiac_arrest": {
        "patient_age": "How old is the patient?",
        "conscious": "Is the patient conscious? (yes/no)",
        "breathing": "Is the patient breathing? (yes/no)"
    },
    "structure_fire": {
        "fire_description": "What is on fire and how big is it?",
        "people_inside": "Is anyone inside the building? (yes/no)"
    },
    "robbery": {
        "suspect_description": "Can you describe the suspect?",
        "weapons_involved": "Were any weapons involved? (yes/no)"
    },
    # Add other incident-specific questions similarly
}

# Emergency feedback instructions
medical_feedback = {
    "cardiac_arrest": "Start CPR immediately if you're trained. Push hard and fast in the center of the chest.",
    "stroke": "Keep the person calm and still. Don't give them food, water, or medicine.",
    # Add other medical feedback similarly
}

fire_feedback = {
    "structure_fire": "Evacuate immediately. Do not attempt to gather belongings. Stay low to avoid smoke.",
    # Add other fire feedback similarly
}

police_feedback = {
    "robbery": "Stay on the line and in a safe location. Do not confront the suspect.",
    # Add other police feedback similarly
}

traffic_feedback = {
    "motor_vehicle_accident": "Turn on hazard lights. Don't move injured people unless there's danger.",
    # Add other traffic feedback similarly
}

disaster_feedback = {
    "flooding": "Avoid walking or driving through floodwaters. Move to higher ground immediately.",
    # Add other disaster feedback similarly
}

hazard_feedback = {
    "chemical_spill": "Avoid inhaling or touching the substance. Evacuate the area.",
    # Add other hazard feedback similarly
}

special_situation_feedback = {
    "suicidal_person": "Stay calm and keep the person talking. Remove any dangerous objects nearby.",
    # Add other special situation feedback similarly
}

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
    else:
        return "Help is on the way. Please remain calm."

def ask_questions(questions):
    """Ask questions and collect responses"""
    responses = {}
    for key, question in questions.items():
        response = input(question + " ")
        responses[key] = response
    return responses

def get_next_incident_number():
    """Get the next incident number by checking existing files"""
    incident_files = [f for f in os.listdir() if f.startswith("incident_") and f.endswith(".txt")]
    if not incident_files:
        return 1
    numbers = [int(f.split('_')[1].split('.')[0]) for f in incident_files]
    return max(numbers) + 1

def log_incident(responses, incident_type, specific_incident, feedback):
    """Save incident to a uniquely numbered file with timestamp"""
    try:
        incident_number = get_next_incident_number()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"incident_{incident_number:03d}_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(f"=== Incident #{incident_number} ===\n")
            file.write(f"Reported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            file.write(f"Emergency Type: {incident_type}\n")
            file.write(f"Specific Incident: {incident_display_names.get(specific_incident, specific_incident)}\n\n")
            
            file.write("=== General Information ===\n")
            for key, value in responses['general_info'].items():
                file.write(f"{key}: {value}\n")
            
            file.write("\n=== Incident Details ===\n")
            for key, value in responses['incident_info'].items():
                file.write(f"{key}: {value}\n")
            
            file.write(f"\n=== Emergency Instructions ===\n{feedback}\n")
        
        return filename
    except Exception as e:
        print(f"Error saving incident: {e}")
        return None

def main():
    print("\n=== Emergency Response System ===\n")
    
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
            choice = int(input("Enter category number: ")) - 1
            if 0 <= choice < len(categories):
                incident_type = categories[choice]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    # Select specific incident
    print(f"\nSelect the specific type of {incident_type} emergency:")
    incidents = incident_types[incident_type]
    for i, incident in enumerate(incidents):
        print(f"{i+1}. {incident_display_names.get(incident, incident)}")
    
    while True:
        try:
            choice = int(input("Enter incident number: ")) - 1
            if 0 <= choice < len(incidents):
                specific_incident = incidents[choice]
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a number.")
    
    # Ask incident-specific questions
    print(f"\nPlease provide details about the {incident_display_names.get(specific_incident)}:")
    incident_info = ask_questions(incident_questions.get(specific_incident, {}))
    
    # Get emergency feedback
    feedback = get_feedback(incident_type, specific_incident)
    print(f"\n=== Emergency Instructions ===\n{feedback}\n")
    
    # Log the incident
    responses = {
        'general_info': general_info,
        'incident_info': incident_info
    }
    saved_file = log_incident(responses, incident_type, specific_incident, feedback)
    
    if saved_file:
        print(f"Incident logged successfully in {saved_file}.")
        print("Help is on the way! Please follow the instructions provided.")
    else:
        print("Failed to save incident report. Help is still on the way!")

if __name__ == "__main__":
    main()
