# models.py
from datetime import datetime
import uuid

class User:
    def __init__(self, id, name, email, password, role, status="available", active_incidents=0, 
                 username="", phone="", gender="", date_of_birth="", responder_category="", created_at=None):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.status = status
        self.active_incidents = active_incidents
        self.phone = phone
        self.gender = gender
        self.date_of_birth = date_of_birth
        self.responder_category = responder_category
        self.created_at = created_at or datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'status': self.status,
            'active_incidents': self.active_incidents,
            'phone': self.phone,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth,
            'responder_category': self.responder_category,
            'created_at': self.created_at
        }

# Keep Incident class the same as before
class Incident:
    def __init__(self, id, type, location, description, priority, status="pending", 
                 reporter_id=None, reporter_name=None, responder_id=None, responder_name=None,
                 created_at=None, updated_at=None, incident_category=None, specific_questions=None,
                 emergency_feedback=None, assigned_responders=None):
        self.id = id
        self.type = type
        self.location = location
        self.description = description
        self.priority = priority
        self.status = status
        self.reporter_id = reporter_id
        self.reporter_name = reporter_name
        self.responder_id = responder_id
        self.responder_name = responder_name
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()
        self.incident_category = incident_category
        self.specific_questions = specific_questions or {}
        self.emergency_feedback = emergency_feedback or ""
        self.assigned_responders = assigned_responders or []
    
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'location': self.location,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'reporter_id': self.reporter_id,
            'reporter_name': self.reporter_name,
            'responder_id': self.responder_id,
            'responder_name': self.responder_name,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'incident_category': self.incident_category,
            'specific_questions': self.specific_questions,
            'emergency_feedback': self.emergency_feedback,
            'assigned_responders': self.assigned_responders
        }
