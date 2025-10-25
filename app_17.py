# 1-IMPORTS
import os 
from datetime import datetime
import time
import re
from threading import Lock
import json
import sqlite3
from typing import Dict, List, Any, Optional, Tuple

# 2-Configuration
CONFIG = {
    "MAX_INCIDENTS_PER_REPORT": 10,
    "REFRESH_INTERVAL": 5,
    "VALID_PHONE_FORMATS": [r"^\d{5}-\d{6}$", r"^\d{11}$"],
    "ALLOWED_SPECIAL_CHARS": " -.,#/",
    "PRIORITY_LEVELS": ["Critical", "High", "Medium", "Low"],
    "RESOURCE_INVENTORY": {
        "ambulances": 5,
        "fire_trucks": 3,
        "police_cars": 8,
        "tow_trucks": 2
    },
    "DATABASE_NAME": "emergency_response.db"
}


# 3-Database Setup and Management
class DatabaseManager:
    # Initialize database manager
    def __init__(self, db_name=CONFIG["DATABASE_NAME"]):
        self.db_name = db_name
        self.connection = None
        self.connect()
        self.init_database()
    
    # Establish database connection
    def connect(self):
        """Establish connection to SQLite database"""
        try:
            self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
            self.connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            raise
    
    # Initialize database tables
    def init_database(self):
        """Initialize database tables if they don't exist"""
        try:
            cursor = self.connection.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Incidents table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incidents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_number INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    priority TEXT NOT NULL,
                    emergency_type TEXT NOT NULL,
                    specific_incident TEXT NOT NULL,
                    location TEXT NOT NULL,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Incident details table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incident_details (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_id INTEGER NOT NULL,
                    question_key TEXT NOT NULL,
                    response TEXT NOT NULL,
                    question_type TEXT NOT NULL,
                    FOREIGN KEY (incident_id) REFERENCES incidents (id) ON DELETE CASCADE
                )
            ''')
            
            # Resources table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    resource_type TEXT UNIQUE NOT NULL,
                    available_count INTEGER NOT NULL,
                    total_count INTEGER NOT NULL
                )
            ''')
            
            # Deployed resources table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS deployed_resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_id INTEGER NOT NULL,
                    resource_type TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    deployed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    returned_at TIMESTAMP,
                    FOREIGN KEY (incident_id) REFERENCES incidents (id) ON DELETE CASCADE
                )
            ''')
            
            # Responder actions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS responder_actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    incident_id INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    responder_source TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    purpose TEXT NOT NULL,
                    status TEXT NOT NULL,
                    location TEXT NOT NULL,
                    additional_info TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (incident_id) REFERENCES incidents (id) ON DELETE CASCADE
                )
            ''')
            
            # Activity log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    activity TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Initialize resources
            cursor.execute('SELECT COUNT(*) FROM resources')
            if cursor.fetchone()[0] == 0:
                for resource_type, count in CONFIG["RESOURCE_INVENTORY"].items():
                    cursor.execute(
                        'INSERT INTO resources (resource_type, available_count, total_count) VALUES (?, ?, ?)',
                        (resource_type, count, count)
                    )
            
            # Initialize default users if none exist
            cursor.execute('SELECT COUNT(*) FROM users')
            if cursor.fetchone()[0] == 0:
                default_users = [
                    ('admin', 'admin123', 'administrator'),
                    ('responder1', 'resp123', 'responder'),
                    ('reporter1', 'report123', 'reporter')
                ]
                cursor.executemany(
                    'INSERT INTO users (username, password, role) VALUES (?, ?, ?)',
                    default_users
                )
            
            self.connection.commit()
            
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            raise
    
    # Execute a SQL query
    def execute_query(self, query, params=()):
        """Execute a SQL query and return results"""
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.connection.commit()
                return cursor.lastrowid
                
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

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

#26-Responder Management Database Structure
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

#27-Enhanced Systems
class UserSession:
    # Initialize user session
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.logged_in_user = None
        self.user_role = None
        self.login_time = None

    # User login
    def login(self, username, role):
        self.logged_in_user = username
        self.user_role = role
        self.login_time = datetime.now()
        self.log_activity(f"Login at {self.login_time}")
        print(f"Welcome, {username} ({role})!")

    # Log user activity
    def log_activity(self, activity):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db_manager.execute_query(
            "INSERT INTO activity_log (username, activity, timestamp) VALUES (?, ?, ?)",
            (self.logged_in_user, activity, timestamp)
        )

    # Show session summary
    def show_session_summary(self):
        if self.logged_in_user:
            activities = self.db_manager.execute_query(
                "SELECT activity, timestamp FROM activity_log WHERE username = ? ORDER BY timestamp DESC LIMIT 5",
                (self.logged_in_user,)
            )
            print(f"\n=== Session Summary for {self.logged_in_user} ===")
            print(f"Login time: {self.login_time}")
            print(f"Role: {self.user_role}")
            print("Recent activities:")
            for activity in activities:
                print(f"  - {activity['timestamp']}: {activity['activity']}")

    # User logout
    def logout(self):
        if self.logged_in_user:
            self.log_activity("Logout")
            print(f"Goodbye, {self.logged_in_user}!")
            self.logged_in_user = None

#28-Resource Management System
class ResourceManager:
    # Initialize resource manager
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # Deploy resources to an incident
    def deploy_resource(self, resource_type, incident_id, quantity=1):
    # Check if enough resources are available
        result = self.db_manager.execute_query(
            "SELECT available_count FROM resources WHERE resource_type = ?",
            (resource_type,)
        )
    
        if result and result[0]['available_count'] >= quantity:
        # Update available count
            self.db_manager.execute_query(
                "UPDATE resources SET available_count = available_count - ? WHERE resource_type = ?",
                (quantity, resource_type)
            )
        
            # Log deployment
            self.db_manager.execute_query(
                "INSERT INTO deployed_resources (incident_id, resource_type, quantity) VALUES (?, ?, ?)",
                (incident_id, resource_type, quantity)
            )
        
            return True
        return False

    # Return resources from an incident
    def return_resource(self, incident_id, resource_type, quantity=1):
        # Check if resources are deployed to this incident
        result = self.db_manager.execute_query(
            "SELECT quantity FROM deployed_resources WHERE incident_id = ? AND resource_type = ? AND returned_at IS NULL",
            (incident_id, resource_type)
        )
    
        if result and result[0]['quantity'] >= quantity:
            # Update available count
            self.db_manager.execute_query(
                "UPDATE resources SET available_count = available_count + ? WHERE resource_type = ?",
                (quantity, resource_type)
            )
        
            # Mark as returned
            self.db_manager.execute_query(
                "UPDATE deployed_resources SET returned_at = CURRENT_TIMESTAMP WHERE incident_id = ? AND resource_type = ? AND returned_at IS NULL",
                (incident_id, resource_type)
            )
        
            return True
        return False

    # Get current resource status
    def get_available_resources(self):
        result = self.db_manager.execute_query("SELECT resource_type, available_count FROM resources")
        return {row['resource_type']: row['available_count'] for row in result} if result else {}

    # Get deployed resources
    def get_deployed_resources(self):
        result = self.db_manager.execute_query(
            "SELECT incident_id, resource_type, quantity FROM deployed_resources WHERE returned_at IS NULL"
        )
    
        deployed = {}
        if result:
            for row in result:
                if row['incident_id'] not in deployed:
                    deployed[row['incident_id']] = {}
                deployed[row['incident_id']][row['resource_type']] = row['quantity']
    
        return deployed
    
#29-User Management System
class UserManager:
# Initialize user manager
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    #Authenticate user credentials
    def authenticate(self, username, password):
        result = self.db_manager.execute_query(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password)
        )

        if result and result[0]['password'] == password:
            return dict(result[0])
        return None
    
    # Create a new user
    def create_user(self, username, password, role):
        try:
            self.db_manager.execute_query(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            return True
        except sqlite3.IntegrityError:
            return False

    # Get all users
    def get_all_users(self):
        result = self.db_manager.execute_query("SELECT username, role FROM users ORDER BY username")
        return [dict(row) for row in result] if result else []

#30-Responder Management System
class ResponderManager:
    # Initialize responder manager
    def __init__(self, db_manager):
        self.db_manager = db_manager

    # Log responder action for an incident
    def log_responder_action(self, incident_id, category, action_data):
        """Log responder management action"""
        additional_info = json.dumps(action_data.get('additional_info', {}))
        
        self.db_manager.execute_query(
            """INSERT INTO responder_actions 
            (incident_id, category, responder_source, destination, purpose, status, location, additional_info) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (incident_id, category, action_data['responder_source'], action_data['destination'], 
            action_data['purpose'], action_data['status'], action_data['location'], additional_info)
        )
        
        return True

    # Get responder log for a specific incident
    def get_incident_responder_log(self, incident_id):
        """Get responder management log for specific incident"""
        result = self.db_manager.execute_query(
            "SELECT * FROM responder_actions WHERE incident_id = ? ORDER BY timestamp DESC",
            (incident_id,)
        )
        
        actions = []
        if result:
            for row in result:
                action = dict(row)
                action['additional_info'] = json.loads(action['additional_info']) if action['additional_info'] else {}
                actions.append(action)
        
        return actions

    # Get overall responder statistics
    def get_responder_stats(self):
        """Get statistics about responder actions"""
        stats = {
            "total_incidents": 0,
            "by_category": {},
            "by_status": {},
            "recent_actions": []
        }
        
        # Get total incidents with responder actions
        result = self.db_manager.execute_query(
            "SELECT COUNT(DISTINCT incident_id) as total FROM responder_actions"
        )
        if result:
            stats["total_incidents"] = result[0]['total']
        
        # Get stats by category
        result = self.db_manager.execute_query(
            "SELECT category, COUNT(*) as count FROM responder_actions GROUP BY category"
        )
        if result:
            for row in result:
                stats["by_category"][row['category']] = row['count']
        
        # Get stats by status
        result = self.db_manager.execute_query(
            "SELECT status, COUNT(*) as count FROM responder_actions GROUP BY status"
        )
        if result:
            for row in result:
                stats["by_status"][row['status']] = row['count']
        
        # Get recent actions
        result = self.db_manager.execute_query(
            "SELECT * FROM responder_actions ORDER BY timestamp DESC LIMIT 10"
        )
        if result:
            for row in result:
                action = dict(row)
                action['additional_info'] = json.loads(action['additional_info']) if action['additional_info'] else {}
                stats["recent_actions"].append(action)
        
        return stats

#31-GLOBAL INSTANCES AND UTILITIES
db_manager = DatabaseManager()
user_session = UserSession(db_manager)
resource_manager = ResourceManager(db_manager)
user_manager = UserManager(db_manager)
responder_manager = ResponderManager(db_manager)

#32-Utility Functions
def validate_input(prompt, validation_func, error_msg="Invalid input. Please try again."):
    while True:
        user_input = input(prompt).strip()
        if validation_func(user_input):
            return user_input
        print(error_msg)

#33-Validation functions
def validate_yes_no(input_str):
    return input_str.lower() in ('yes', 'no', 'y', 'n')

#34-Simple phone number validation
def validate_phone(phone_str):
    return any(re.match(pattern, phone_str) for pattern in CONFIG["VALID_PHONE_FORMATS"])

#35-Simple text validation
def validate_text(input_str):
    return all(c.isalnum() or c in CONFIG["ALLOWED_SPECIAL_CHARS"] for c in input_str)

#36-Get feedback based on incident type and specific incident
def get_feedback(incident_type, specific_incident):
    feedback_mapping = {
    "medical": medical_feedback, 
    "fire": fire_feedback, 
    "police": police_feedback,
    "traffic": traffic_feedback, 
    "natural_disaster": disaster_feedback,
    "hazardous_material": hazard_feedback, 
    "special_situations": special_situation_feedback,
    "cyber_incident": cyber_feedback, 
    "utility_emergency": utility_feedback,
    "weather_alert": weather_alert_feedback, 
    "marine_incident": marine_feedback,
    "aviation_incident": aviation_feedback, 
    "public_health_incident": public_health_feedback,
    "crowd_control": crowd_control_feedback, 
    "infrastructure_failure": infrastructure_feedback
    }
    return feedback_mapping.get(incident_type, {}).get(specific_incident, "Help is on the way. Please remain calm.")

#37-Get next incident number
def get_next_incident_number():
    result = db_manager.execute_query("SELECT MAX(incident_number) as max_num FROM incidents")
    return (result[0]['max_num'] + 1) if result and result[0]['max_num'] else 1

#38-Question Asking System
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

#39-Priority System
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

#40-Auto-deploy resources based on incident type
def auto_deploy_resources(incident_type, incident_id):
    deployment_rules = {
    "medical": {"ambulances": 1}, "fire": {"fire_trucks": 1, "ambulances": 1},
    "police": {"police_cars": 1}, "traffic": {"police_cars": 1, "tow_trucks": 1}
    }

    resources_to_deploy = deployment_rules.get(incident_type, {})
    for resource, quantity in resources_to_deploy.items():
        if resource_manager.deploy_resource(resource, incident_id, quantity):
            print(f"Auto-deployed {quantity} {resource} to incident #{incident_id}")

#41-Log Single Incident to Database
def log_incident_to_db(responses, incident_type, specific_incident, feedback=None):
    try:
        # Generate a new incident number
        incident_number = get_next_incident_number()

        # Assign priority based on incident type & responses
        priority = assign_incident_priority(
            incident_type,
            specific_incident,
            responses['general_info']
        )

        # Insert into incidents table
        incident_id = db_manager.execute_query(
            """INSERT INTO incidents 
                (incident_number, priority, emergency_type, specific_incident, location) 
                VALUES (?, ?, ?, ?, ?)""",
            (
                incident_number,
                priority,
                incident_type,
                specific_incident,
                responses['general_info'].get('location', 'Unknown')
            )
        )

        # Insert general information
        for key, value in responses['general_info'].items():
            db_manager.execute_query(
                """INSERT INTO incident_details 
                    (incident_id, question_key, response, question_type) 
                    VALUES (?, ?, ?, ?)""",
                (incident_id, key, value, 'general')
            )

        # Insert incident-specific information
        for key, value in responses['incident_info'].items():
            db_manager.execute_query(
                """INSERT INTO incident_details 
                    (incident_id, question_key, response, question_type) 
                    VALUES (?, ?, ?, ?)""",
                (incident_id, key, value, 'specific')
            )

        # Store feedback if provided
        if feedback:
            db_manager.execute_query(
                """INSERT INTO incident_feedback 
                    (incident_id, feedback) VALUES (?, ?)""",
                (incident_id, feedback)
            )

        # Auto-deploy resources
        auto_deploy_resources(incident_type, incident_id)

        return incident_id

    except Exception as e:
        # Use logging in real projects instead of print
        print(f"[ERROR] Critical error logging incident: {e}")
        return None


#42-Responder Management System
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
    print("\n--- Summary of Responder Management ---")
    print(f"Responder Source: {responder_source}")
    print(f"Destination: {destination}")
    print(f"Purpose: {purpose}")
    print(f"Status: {status}")
    print(f"Location: {location}")
    if additional_info:
        print("Additional Info:")
        for k, v in additional_info.items():
            print(f"  - {k.replace('_', ' ').capitalize()}: {v}")
            
    print(f"\n Responder management logged for incident #{incident_id}")

    return management_data

#43-User Authentication
def authenticate_user():
    print("\n=== User Authentication ===")
    username = input("Username: ")
    password = input("Password: ")
    user = user_manager.authenticate(username, password)
    if user: 
        return user, username
    print("Authentication failed. Please try again.")
    return None, None

#44-Categorized Responder Selection
def show_categorized_responder_menu():
    print("\n=== Select Your Response Category ===")

    available_categories = [cat for cat in responder_categories.keys() if responder_categories[cat]]
    for i, category in enumerate(available_categories, 1): 
        print(f"{i}. {category.capitalize()}")
        
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

#45-Incident Retrieval
def get_active_incidents():
    result = db_manager.execute_query(
    "SELECT id, incident_number, emergency_type, specific_incident, location, timestamp FROM incidents WHERE status = 'active' ORDER BY timestamp DESC LIMIT ?",
    (CONFIG["MAX_INCIDENTS_PER_REPORT"],)
    )
    return [dict(row) for row in result] if result else []

#46-Incident List Display
def display_incident_list(incidents):
    print("\n=== Active Incidents ===")
    print(f"{'#':<3} {'ID':<5} {'Type':<20} {'Location':<30} {'Time':<20}")
    print("-" * 80)
    for i, incident in enumerate(incidents, 1):
        incident_time = incident['timestamp'].split(' ')[1] if ' ' in incident['timestamp'] else incident['timestamp']
    print(f"{i:<3} {incident['id']:<5} {incident['emergency_type'][:18]:<20} {incident['location'][:28]:<30} {incident_time[:8]:<20}")

#47-Incident Detail View and Recommendations
def display_incident_details(incident_id, responder_role, responder_category):
    # Get incident details
    incident_result = db_manager.execute_query(
    "SELECT * FROM incidents WHERE id = ?", (incident_id,)
    )
    if not incident_result:
        print("Incident not found.")
        return None, None

    incident = dict(incident_result[0])

    # Get incident details (questions and responses)
    details_result = db_manager.execute_query(
        "SELECT question_key, response, question_type FROM incident_details WHERE incident_id = ? ORDER BY question_type, question_key",
        (incident_id,)
    )

    print(f"\n{'='*40}\nINCIDENT: #{incident['incident_number']}\n{'-'*40}")
    print(f"Reported at: {incident['timestamp']}")
    print(f"Priority: {incident['priority']}")
    print(f"Emergency Type: {incident['emergency_type']}")
    print(f"Specific Incident: {incident_display_names.get(incident['specific_incident'], incident['specific_incident'])}")
    print(f"Location: {incident['location']}")
    print("\n=== Details ===")

    current_section = None
    for detail in details_result:
        detail = dict(detail)
        if detail['question_type'] != current_section:
            current_section = detail['question_type']
            section_title = "General Information" if detail['question_type'] == 'general' else "Incident Details"
            print(f"\n{section_title}:")
        
        question_key = detail['question_key'].replace('_', ' ').title()
        print(f"  {question_key}: {detail['response']}")

    # Get feedback
    feedback = get_feedback(incident['emergency_type'], incident['specific_incident'])
    print(f"\n=== Emergency Instructions ===\n{feedback}")

    # Show suggested responders
    incident_type = incident['emergency_type']
    if incident_type in responders:
        print("\n[SUGGESTED RESPONSE TEAM]")
        print(', '.join(responders[incident_type]))
        if incident_type == responder_category:
            print(f"\n\033[1;31mALERT: This {incident_type} incident matches your {responder_category} specialization!\033[0m")
        elif responder_role in responders[incident_type]:
            print(f"\n\033[1;33mNOTICE: Your specific role ({responder_role}) is recommended for this incident!\033[0m")

    return incident['emergency_type'], incident['location']

#48-Responder Interaction Loop
def handle_responder_input(incidents, responder_role, responder_category):
    print("\n[ACTIONS] Enter incident number to view details")
    print("Press 'r' to refresh list")
    print("Press 'q' to quit")

    while True:
        selection = input("\nSelection: ").lower()
        if selection == 'q': return False
        elif selection == 'r': return True
        
        try:
            incident_num = int(selection) - 1
            if 0 <= incident_num < len(incidents):
                incident = incidents[incident_num]
                incident_type, location = display_incident_details(incident['id'], responder_role, responder_category)
                
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
                        user_session.log_activity(f"Acknowledged incident #{incident['id']}")
                        print("Incident acknowledged.")
                    elif action == '2':
                        backup_type = input("Enter backup type needed: ")
                        user_session.log_activity(f"Requested {backup_type} backup for incident #{incident['id']}")
                        print(f"{backup_type} backup requested.")
                    elif action == '3':
                        note = input("Enter your notes: ")
                        user_session.log_activity(f"Added notes to incident #{incident['id']}")
                        # Store notes in the database (could add a notes table)
                        print("Notes added.")
                    elif action == '4':
                        if incident_type and location:
                            user_session.log_activity(f"Accessed responder management for incident #{incident['id']}")
                            responder_info = responder_management(incident['id'], incident_type, location)
                        else:
                            print("Cannot access responder management without incident type and location.")
                    elif action == '5':
                        user_session.log_activity(f"Resolved incident #{incident['id']}")
                        # Return deployed resources
                        deployed_resources = resource_manager.get_deployed_resources().get(incident['id'], {})
                        for resource, count in deployed_resources.items():
                            resource_manager.return_resource(incident['id'], resource, count)
                        # Mark incident as resolved
                        db_manager.execute_query(
                            "UPDATE incidents SET status = 'resolved' WHERE id = ?",
                            (incident['id'],)
                        )
                        print("Incident marked as resolved.")
                        return True
                    elif action == '6': break
                    else: print("Invalid choice. Please enter 1-6")
                return True
            print(f"Please enter 1-{len(incidents)}, 'r', or 'q'")
        except ValueError:
            print("Invalid input. Please enter a number, 'r', or 'q'")

#49-Responder Report Generation
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

    print(report_content)
    return report_content    

#50-View Responder Management Details
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

#51-Daily Reporting
def generate_daily_report():
    today = datetime.now().strftime("%Y-%m-%d")

    # Get today's incidents
    incidents_result = db_manager.execute_query(
        "SELECT emergency_type, COUNT(*) as count FROM incidents WHERE DATE(timestamp) = ? GROUP BY emergency_type",
        (today,)
    )

    # Get resolved incidents
    resolved_result = db_manager.execute_query(
        "SELECT COUNT(*) as count FROM incidents WHERE status = 'resolved' AND DATE(timestamp) = ?",
        (today,)
    )

    # Get active incidents
    active_result = db_manager.execute_query(
        "SELECT COUNT(*) as count FROM incidents WHERE status = 'active' AND DATE(timestamp) = ?",
        (today,)
    )

    report_content = f"Daily Incident Report - {today}\n{'='*50}\n\n"

    if resolved_result and active_result:
        total_incidents = resolved_result[0]['count'] + active_result[0]['count']
        report_content += f"Total Incidents: {total_incidents}\n"
        report_content += f"Active Incidents: {active_result[0]['count']}\n"
        report_content += f"Resolved Incidents: {resolved_result[0]['count']}\n\n"

    if incidents_result:
        report_content += "Incidents by Category:\n"
        for row in incidents_result:
            report_content += f"  {row['emergency_type']}: {row['count']}\n"

    print(report_content)
    return report_content

#52-System Statistics
def show_system_statistics():
    print("\n=== System Statistics ===")

    # Get incident counts
    active_result = db_manager.execute_query("SELECT COUNT(*) as count FROM incidents WHERE status = 'active'")
    resolved_result = db_manager.execute_query("SELECT COUNT(*) as count FROM incidents WHERE status = 'resolved'")

    if active_result and resolved_result:
        active_incidents = active_result[0]['count']
        resolved_incidents = resolved_result[0]['count']
        print(f"Active Incidents: {active_incidents}")
        print(f"Resolved Incidents: {resolved_incidents}")
        print(f"Total Incidents: {active_incidents + resolved_incidents}")

    # Get resource status
    print("\nResource Status:")
    available = resource_manager.get_available_resources()
    deployed = resource_manager.get_deployed_resources()

    for resource, count in available.items():
        deployed_count = sum(incident_resources.get(resource, 0) for incident_resources in deployed.values())
        print(f"  {resource}: {count} available, {deployed_count} deployed")

    # Get incidents by category
    category_result = db_manager.execute_query(
        "SELECT emergency_type, COUNT(*) as count FROM incidents GROUP BY emergency_type"
    )

    if category_result:
        print("\nIncidents by Category:")
        for row in category_result:
            print(f"  {row['emergency_type']}: {row['count']}")

#53-User Management
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
            users = user_manager.get_all_users()
            for user in users:
                print(f"  {user['username']}: {user['role']}")
        elif choice == '2':
            username = input("Enter new username: ")
            password = input("Enter password: ")
            role = input("Enter role (administrator/responder/reporter): ")
            if user_manager.create_user(username, password, role):
                print(f"User {username} created successfully!")
            else: print("User creation failed. Username may already exist.")
        elif choice == '3': break
        else: print("Invalid choice. Please try again.")

#54-Resource Status Display
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

#55-Multi-Incident Reporting System
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

#56-Consolidated Incident Logging
def log_multi_incident_report(incident_reports):
    """Log multiple incidents with consolidated emergency instructions"""
    try:
        incident_number = get_next_incident_number()

        # If only one incident, use its type and specific_incident
        if len(incident_reports) == 1:
            main_type = incident_reports[0]['incident_type']
            main_specific = incident_reports[0]['specific_incident']
        else:
            main_type = "multi"
            main_specific = "multiple_incidents"

        # Create a consolidated incident record
        incident_id = db_manager.execute_query(
            """INSERT INTO incidents 
            (incident_number, priority, emergency_type, specific_incident, location) 
            VALUES (?, ?, ?, ?, ?)""",
            (incident_number, "High", main_type, main_specific, incident_reports[0]['general_info']['location'])
        )

        # Create a consolidated incident record
        incident_id = db_manager.execute_query(
            """INSERT INTO incidents 
            (incident_number, priority, emergency_type, specific_incident, location) 
            VALUES (?, ?, ?, ?, ?)""",
            (incident_number, "High", "multi", "multiple_incidents", incident_reports[0]['general_info']['location'])
        )
        
        # Add general information
        for key, value in incident_reports[0]['general_info'].items():
            db_manager.execute_query(
                "INSERT INTO incident_details (incident_id, question_key, response, question_type) VALUES (?, ?, ?, ?)",
                (incident_id, key, value, 'general')
            )
        
        # Add incident-specific information for each incident
        for report in incident_reports:
            # Store the incident type and specific incident
            db_manager.execute_query(
                "INSERT INTO incident_details (incident_id, question_key, response, question_type) VALUES (?, ?, ?, ?)",
                (incident_id, f"{report['incident_type']}_type", report['specific_incident'], 'multi')
            )
            
            # Store the incident details
            for key, value in report['incident_info'].items():
                db_manager.execute_query(
                    "INSERT INTO incident_details (incident_id, question_key, response, question_type) VALUES (?, ?, ?, ?)",
                    (incident_id, f"{report['incident_type']}_{key}", value, 'multi')
                )
        
        # Auto-deploy resources for the highest priority incident
        highest_priority = "Medium"
        for report in incident_reports:
            priority = assign_incident_priority(report['incident_type'], report['specific_incident'], report['general_info'])
            if priority == "Critical":
                highest_priority = "Critical"
                break
            elif priority == "High" and highest_priority != "Critical":
                highest_priority = "High"
        
        # Deploy resources based on the highest priority incident type
        for report in incident_reports:
            priority = assign_incident_priority(report['incident_type'], report['specific_incident'], report['general_info'])
            if priority == highest_priority:
                auto_deploy_resources(report['incident_type'], incident_id)
                break
        
        return incident_id
        
    except Exception as e:
        print(f"Error logging incident report: {e}")
        return None

#57-Reporter Mode
def handle_reporter_mode():
    """Main function for reporter operations - Now only multi-incident reporting"""
    print("\n=== Emergency Reporting ===")

    incident_reports = handle_multi_incident_report()
    if incident_reports:
        incident_id = log_multi_incident_report(incident_reports)
        
        if incident_id:
            print(f"\n{'=' * 50}")
            print(f"Incident(s) logged with ID #{incident_id}")
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

#58-Responder Mode
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
                incidents = get_active_incidents()
                if not incidents:
                    print("\nNo active incidents found")
                    time.sleep(2)
                    continue
                display_incident_list(incidents)
            
            if not handle_responder_input(incidents, responder_role, responder_category): break
                
    except KeyboardInterrupt: print("\nExiting responder mode...")
    except Exception as e: print(f"Error in responder mode: {e}")
    finally: user_session.logout()

#59-Enhanced Menu System
def show_advanced_menu():
    while True:
        print("\n=== Advanced Menu ===")
        print("1. View System Statistics")
        print("2. Generate Daily Report")
        print("3. View Session History")
        print("4. Manage Users")
        print("5. View Resource Status")
        print("6. Responder Management Report")
        print("7. View Responder Actions")
        print("8. Return to Main Menu")

        choice = input("Enter your choice (1-8): ")
        if choice == '1': show_system_statistics()
        elif choice == '2': generate_daily_report()
        elif choice == '3': user_session.show_session_summary()
        elif choice == '4': manage_users_menu()
        elif choice == '5': show_resource_status()
        elif choice == '6': generate_responder_report()
        elif choice == '7':
            incident_id = input("Enter incident ID to view actions: ")
            if incident_id.isdigit():
                view_responder_management(int(incident_id))
        elif choice == '8': break
        else: print("Invalid choice. Please enter a number between 1-8.")

#60-Main Function
def main():
    try:
        print("=== Emergency Response System ===")
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
    finally: 
        db_manager.close()
        print("\nSystem shutdown")

#61-Entry Point
if __name__ == "__main__":
    main()
