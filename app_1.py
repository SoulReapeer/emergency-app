import sqlite3

# Define the questions
questions = {
    "name": "What is your name?",
    "location": "What is your address?",
    "emergency_type": "What is the nature of the emergency? (police, fire, medical)",
    "injuries": "Are there any injuries? (yes/no)",
    "suspect_description": "If a crime is involved, can you describe the suspect?",
    "medical_details": "If a medical emergency, what are the patient's symptoms?",
    "phone_number": "What is your phone number?",
    "witness_information": "Are there any witnesses? (yes/no)",
    "weapons_involved": "Are there any weapons involved? (yes/no)"
}

# Function to ask questions and collect responses
def ask_questions():
    responses = {}
    for key, question in questions.items():
        response = input(question + " ")
        responses[key] = response
    return responses

# Function to dispatch services based on emergency type
def dispatch_service(emergency_type):
    if emergency_type == "police":
        return "Dispatching police..."
    elif emergency_type == "fire":
        return "Dispatching fire department..."
    elif emergency_type == "medical":
        return "Dispatching medical services..."
    else:
        return "Invalid emergency type."

# Function to log the incident in a database
def log_incident(responses):
    conn = sqlite3.connect('incidents.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS incidents
                 (name TEXT, location TEXT, emergency_type TEXT, injuries TEXT,
                  suspect_description TEXT, medical_details TEXT, phone_number TEXT,
                  witness_information TEXT, weapons_involved TEXT)''')
    
    # Insert the incident into the database
    c.execute('''INSERT INTO incidents VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (responses["name"], responses["location"], responses["emergency_type"],
               responses["injuries"], responses["suspect_description"],
               responses["medical_details"], responses["phone_number"],
               responses["witness_information"], responses["weapons_involved"]))
    
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
