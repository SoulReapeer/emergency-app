# Define the questions
questions = {
    "location": "What is the address of the emergency?",
    "phone_number": "What is the phone number you’re calling from?",
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

# Function to ask questions and collect responses
def ask_questions():
    responses = {}
    for key, question in questions.items():
        response = input(question + " ")
        responses[key] = response

    # Ask additional questions based on emergency type
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

    # Ask general questions
    for key, question in general_questions.items():
        response = input(question + " ")
        responses[key] = response

    return responses

# Function to dispatch services based on emergency type
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

# Function to log the incident in a text file
def log_incident(responses):
    with open("incidents.txt", "a") as file:
        file.write("=== New Incident ===\n")
        for key, value in responses.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")  # Add a blank line between incidents

# Main function
def main():
    print("Welcome to the Emergency Response System!")
    responses = ask_questions()
    dispatch_result = dispatch_service(responses["emergency_type"])
    print(dispatch_result)
    log_incident(responses)
    print("Incident logged successfully. Help is on the way!")

if __name__ == "__main__":
    main()
