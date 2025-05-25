import sqlite3

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
    if emergency_type == "medical":
        for key, question in medical_questions.items():
            response = input(question + " ")
            responses[key] = response
    elif emergency_type == "fire":
        for key, question in fire_questions.items():
            response = input(question + " ")
            responses[key] = response
    elif emergency_type == "police":
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
    if emergency_type == "medical":
        return "Dispatching medical services..."
    elif emergency_type == "fire":
        return "Dispatching fire department..."
    elif emergency_type == "police":
        return "Dispatching police..."
    else:
        return "Invalid emergency type."

# Function to log the incident in a database
def log_incident(responses):
    conn = sqlite3.connect('incidents.db')
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS incidents
                 (location TEXT, phone_number TEXT, name TEXT, incident_description TEXT,
                  emergency_type TEXT, patient_age TEXT, patient_conscious TEXT,
                  patient_breathing TEXT, fire_description TEXT, flames_or_smoke TEXT,
                  smoke_color TEXT, people_inside TEXT, fire_cause TEXT, nearby_objects TEXT,
                  vehicle_description TEXT, suspect_description TEXT, weapons_involved TEXT,
                  relationship TEXT, building_description TEXT, standing_by TEXT)''')

    # Insert the incident into the database
    c.execute('''INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (responses.get("location"), responses.get("phone_number"), responses.get("name"),
               responses.get("incident_description"), responses.get("emergency_type"),
               responses.get("patient_age"), responses.get("patient_conscious"),
               responses.get("patient_breathing"), responses.get("fire_description"),
               responses.get("flames_or_smoke"), responses.get("smoke_color"),
               responses.get("people_inside"), responses.get("fire_cause"),
               responses.get("nearby_objects"), responses.get("vehicle_description"),
               responses.get("suspect_description"), responses.get("weapons_involved"),
               responses.get("relationship"), responses.get("building_description"),
               responses.get("standing_by")))

    conn.commit()
    conn.close()

# Main function
def main():
    print("Welcome to the Emergency Response System!")
    responses = ask_questions()
    print(dispatch_service(responses["emergency_type"]))
    log_incident(responses)
    print("Incident logged successfully. Help is on the way!")

if __name__ == "__main__":
    main()
