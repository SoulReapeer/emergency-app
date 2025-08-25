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
    if emergency_type.lower() == "police":
        return "Dispatching police..."
    elif emergency_type.lower() == "fire":
        return "Dispatching fire department..."
    elif emergency_type.lower() == "medical":
        return "Dispatching medical services..."
    else:
        return "Invalid emergency type."

# Function to log the incident to a text file
def log_incident(responses):
    with open("incidents.txt", "a") as file:
        file.write("=== New Incident ===\n")
        for key, value in responses.items():
            file.write(f"{questions[key]} {value}\n")
        file.write("\n")  # Blank line between incidents

# Main function
def main():
    print("Welcome to the Emergency Response System!")
    responses = ask_questions()
    print(dispatch_service(responses["emergency_type"]))
    log_incident(responses)
    print("Incident logged successfully. Help is on the way!")

if __name__ == "__main__":
    main()
