import os
from datetime import datetime

# Define the questions
questions = {
    "location": "What is the address of the emergency?",
    "phone_number": "What is the phone number you're calling from?",
    "name": "What is your name?",
    "incident_description": "Tell me exactly what happened.",
    "emergency_type": "What is the nature of the emergency? (medical, fire, police)",
}

# Additional questions based on emergency type
medical_questions = {
    "patient_age": "How old is the patient? (approximate age)",
    "patient_conscious": "Is the patient conscious? (yes/no)",
    "patient_breathing": "Is the patient breathing? (yes/no)",
}

fire_questions = {
    "fire_description": "What exactly is on fire? To what extent?",
    "flames_or_smoke": "Were flames observed or just smoke?",
    "smoke_color": "What color is the smoke?",
    "people_inside": "Is anyone inside the building? (yes/no)",
    "fire_cause": "Do we know how the fire started?",
    "nearby_objects": "Are there other items near the fire that it can spread to? (e.g., other buildings, trees, dry grass, etc.)",
}

police_questions = {
    "vehicle_description": "Describe the vehicle involved (license plate, make, model, color, direction of travel).",
    "suspect_description": "Describe the suspect (name, age, race, gender, height, weight, hair, clothing, distinguishing features).",
    "weapons_involved": "Did you see any weapons? Did you hear anyone talking about weapons? (yes/no)",
}

general_questions = {
    "relationship": "What is your relationship to the patient or involved parties?",
    "building_description": "Describe the building (e.g., one or two stories, color, type of building).",
    "standing_by": "Will you be standing by when responders arrive? (yes/no)",
}


def ask_questions():
    responses = {}
    for key, question in questions.items():
        response = input(question + " ")
        responses[key] = response

    emergency_type = responses["emergency_type"].lower()
    if "medical" in emergency_type:
        for key, question in medical_questions.items():
            response = input(question + " ")
            responses[key] = response
    if "fire" in emergency_type:
        for key, question in fire_questions.items():
            response = input(question + " ")
            responses[key] = response
    if "police" in emergency_type:
        for key, question in police_questions.items():
            response = input(question + " ")
            responses[key] = response

    for key, question in general_questions.items():
        response = input(question + " ")
        responses[key] = response

    return responses


def dispatch_service(emergency_type):
    if "medical" in emergency_type.lower():
        print("Dispatching medical services...")
    if "fire" in emergency_type.lower():
        print("Dispatching fire department...")
    if "police" in emergency_type.lower():
        print("Dispatching police...")
    if not any(word in emergency_type.lower() for word in ["medical", "fire", "police"]):
        return "Invalid emergency type."
    return "Help is on the way!"


def get_next_incident_number():
    """Get the next incident number by checking existing files"""
    incident_files = [f for f in os.listdir() if f.startswith(
        "incident_") and f.endswith(".txt")]
    if not incident_files:
        return 1
    numbers = [int(f.split('_')[1].split('.')[0]) for f in incident_files]
    return max(numbers) + 1


def log_incident(responses):
    """Save incident to a uniquely numbered file with timestamp"""
    try:
        incident_number = get_next_incident_number()
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"incident_{incident_number:03d}_{timestamp}.txt"

        with open(filename, "w") as file:
            file.write(f"=== Incident #{incident_number} ===\n")
            file.write(
                f"Reported at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            for key, value in responses.items():
                file.write(f"{key}: {value}\n")
        return filename
    except Exception as e:
        print(f"Error saving incident: {e}")
        return None


def main():
    print("Welcome to the Emergency Response System!")
    responses = ask_questions()
    dispatch_result = dispatch_service(responses["emergency_type"])
    print(dispatch_result)

    saved_file = log_incident(responses)
    if saved_file:
        print(
            f"Incident logged successfully in {saved_file}. Help is on the way!")
    else:
        print("Failed to save incident report.")


if __name__ == "__main__":
    main()
