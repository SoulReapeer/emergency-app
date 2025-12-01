import sqlite3
import json
from datetime import datetime
from models import User, Incident

class Database:
    def __init__(self, db_name="emergency_response.db"):
        self.db_name = db_name
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    
    def init_database(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Enhanced Users table with new fields
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                phone TEXT,
                gender TEXT,
                date_of_birth TEXT,
                responder_category TEXT,
                status TEXT DEFAULT 'available',
                active_incidents INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Enhanced Incidents table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                type TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                reporter_id TEXT NOT NULL,
                reporter_name TEXT NOT NULL,
                responder_id TEXT,
                responder_name TEXT,
                incident_category TEXT,
                specific_questions TEXT,
                emergency_feedback TEXT,
                assigned_responders TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (reporter_id) REFERENCES users (id),
                FOREIGN KEY (responder_id) REFERENCES users (id)
            )
        ''')
        
        # Create default admin user
        cursor.execute('''
            INSERT OR IGNORE INTO users (id, name, username, email, password, role, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('admin001', 'System Admin', 'Admin', 'admin@ers.com', 'Admin@123', 'admin', 'available'))

        
        # Create sample responders
        cursor.execute('''
            INSERT OR IGNORE INTO users (id, name, username, email, password, role, status, responder_category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('resp001', 'John Responder', 'john_responder', 'responder@ers.com', 'Resp@123', 'responder', 'available', 'Medical'))
        
        cursor.execute('''
            INSERT OR IGNORE INTO users (id, name, username, email, password, role, status, responder_category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('resp002', 'Sarah Medic', 'sarah_medic', 'medic@ers.com', 'Medic@123', 'responder', 'available', 'Fire'))
        
        conn.commit()
        conn.close()
    
    def create_user(self, user):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (id, name, username, email, password, role, phone, gender, date_of_birth, responder_category, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user.id, user.name, getattr(user, 'username', ''), user.email, user.password, user.role,
              getattr(user, 'phone', ''), getattr(user, 'gender', ''), getattr(user, 'date_of_birth', ''),
              getattr(user, 'responder_category', ''), user.status))
        conn.commit()
        conn.close()
    
    def get_user_by_username(self, username):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_user(row)
        return None
    
    def get_user_by_email(self, email):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_user(row)
        return None
    
    def get_user_by_id(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_user(row)
        return None
    
    def get_user_by_email_and_phone(self, email, phone):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND phone = ?', (email, phone))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_user(row)
        return None
    
    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_user(row) for row in rows]
    
    def get_responders(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE role = "responder"')
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_user(row) for row in rows]
    
    def create_incident(self, incident):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO incidents 
            (id, type, location, description, severity, status, reporter_id, reporter_name, 
             incident_category, specific_questions, emergency_feedback, assigned_responders,
             created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (incident.id, incident.type, incident.location, incident.description, 
              incident.severity, incident.status, incident.reporter_id, 
              incident.reporter_name, incident.incident_category,
              json.dumps(incident.specific_questions), incident.emergency_feedback,
              json.dumps(incident.assigned_responders), incident.created_at, incident.updated_at))
        conn.commit()
        conn.close()
    
    def get_incident_by_id(self, incident_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM incidents WHERE id = ?', (incident_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return self._row_to_incident(row)
        return None
    
    def get_all_incidents(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM incidents ORDER BY created_at DESC')
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_incident(row) for row in rows]
    
    def get_incidents_by_reporter(self, reporter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM incidents WHERE reporter_id = ? ORDER BY created_at DESC', (reporter_id,))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_incident(row) for row in rows]
    
    def get_incidents_by_responder(self, responder_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM incidents WHERE responder_id = ? ORDER BY created_at DESC', (responder_id,))
        rows = cursor.fetchall()
        conn.close()
        return [self._row_to_incident(row) for row in rows]
    
    def update_incident(self, incident):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE incidents SET 
            type=?, location=?, description=?, severity=?, status=?, 
            reporter_id=?, reporter_name=?, responder_id=?, responder_name=?, 
            incident_category=?, specific_questions=?, emergency_feedback=?,
            assigned_responders=?, updated_at=?
            WHERE id=?
        ''', (incident.type, incident.location, incident.description, incident.severity,
              incident.status, incident.reporter_id, incident.reporter_name,
              incident.responder_id, incident.responder_name, incident.incident_category,
              json.dumps(incident.specific_questions), incident.emergency_feedback,
              json.dumps(incident.assigned_responders), incident.updated_at, incident.id))
        conn.commit()
        conn.close()
    
    def update_user(self, user):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET 
            name=?, username=?, email=?, password=?, role=?, phone=?, gender=?,
            date_of_birth=?, responder_category=?, status=?, active_incidents=?
            WHERE id=?
        ''', (user.name, user.username, user.email, user.password, user.role, 
              user.phone, user.gender, user.date_of_birth, user.responder_category,
              user.status, user.active_incidents, user.id))
        conn.commit()
        conn.close()
    
    def get_incident_count_by_status(self, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM incidents WHERE status = ?', (status,))
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_next_incident_id(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM incidents')
        count = cursor.fetchone()[0]
        conn.close()
        return f"INC-{count + 1:03d}"
    
    def get_next_user_id(self, role):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = ?', (role,))
        count = cursor.fetchone()[0]
        conn.close()
        prefix = "admin" if role == "admin" else "resp" if role == "responder" else "rept"
        return f"{prefix}{count + 1:03d}"
    
    def _row_to_user(self, row):
        return User(
            id=row[0],
            name=row[1],
            username=row[2],
            email=row[3],
            password=row[4],
            role=row[5],
            phone=row[6],
            gender=row[7],
            date_of_birth=row[8],
            responder_category=row[9],
            status=row[10],
            active_incidents=row[11],
            created_at=datetime.fromisoformat(row[12]) if isinstance(row[12], str) else row[12]
        )
    
    def _row_to_incident(self, row):
        return Incident(
            id=row[0],
            type=row[1],
            location=row[2],
            description=row[3],
            severity=row[4],
            status=row[5],
            reporter_id=row[6],
            reporter_name=row[7],
            responder_id=row[8],
            responder_name=row[9],
            incident_category=row[10],
            specific_questions=json.loads(row[11]) if row[11] else {},
            emergency_feedback=row[12],
            assigned_responders=json.loads(row[13]) if row[13] else [],
            created_at=datetime.fromisoformat(row[14]) if isinstance(row[14], str) else row[14],
            updated_at=datetime.fromisoformat(row[15]) if isinstance(row[15], str) else row[15]
        )

    def assign_responder(self, incident_id, responder_id, responder_name):
        """Set responder and mark incident as assigned."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE incidents
            SET responder_id = ?, responder_name = ?, status = ?, updated_at = ?
            WHERE id = ?
        """, (responder_id, responder_name, "assigned", datetime.now().isoformat(), incident_id))
        conn.commit()
        conn.close()

    def update_user_status(self, user_id, new_status):
        """Activate/deactivate a user."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users
            SET status = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, datetime.now().isoformat(), user_id))
        conn.commit()
        conn.close()
