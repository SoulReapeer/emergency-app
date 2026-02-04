# profile.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QFrame, QLineEdit, QComboBox,
                             QMessageBox, QTextEdit, QFileDialog, QScrollArea)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from datetime import datetime
import json


# -------------------------------
# Categorized Responder Directory
# -------------------------------
# Keys are internal category codes, values are the possible roles in that category.
RESPONDER_CATEGORIES = {
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


def get_category_list():
    """
    Return human-readable category names for the combo box,
    e.g. 'Medical', 'Natural Disaster'.
    """
    return [key.replace("_", " ").title() for key in RESPONDER_CATEGORIES.keys()]


def get_roles_for_category(category_label: str):
    """
    Convert the label from the combo box (e.g. 'Natural Disaster')
    back to the dictionary key (e.g. 'natural_disaster') and
    return the list of roles.
    """
    key = category_label.lower().replace(" ", "_")
    return RESPONDER_CATEGORIES.get(key, [])


#------------------------------
class Profile(QWidget):
    def __init__(self, current_user, db):
        super().__init__()
        self.current_user = current_user
        self.db = db

        # Extended profile data (address, backups, etc.)
        self.profile_data = {}
        self.backup_phone_inputs = []
        self.backup_address_inputs = []

        # Responder/admin widgets (created conditionally)
        self.category_combo = None
        self.role_combo = None
        self.position_input = None

        # Avatar label (for changing photo)
        self.avatar_label = None

        # Ensure extra profile table exists, then load data
        self._ensure_profile_table()
        self.profile_data = self._load_profile_data()

        self.init_ui()

    # -----------------------------
    # DB helpers for extra profile
    # -----------------------------
    def _ensure_profile_table(self):
        """Create a user_profiles table if it doesn't exist yet."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                full_name TEXT,
                address TEXT,
                phone TEXT,
                backup_numbers TEXT,
                email TEXT,
                backup_addresses TEXT,
                country TEXT,
                city TEXT,
                responder_category TEXT,
                responder_role TEXT,
                work_position TEXT,
                extra_json TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            """
        )
        conn.commit()
        conn.close()

    def _load_profile_data(self):
        """Load extended profile info (address, backups, etc.) from user_profiles."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (self.current_user.id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return {
                "full_name": self.current_user.name or "",
                "address": "",
                "phone": self.current_user.phone or "",
                "backup_numbers": [],
                "email": self.current_user.email or "",
                "backup_addresses": [],
                "country": "",
                "city": "",
                "responder_category": getattr(self.current_user, "responder_category", "") or "",
                "responder_role": "",
                "work_position": "",
                "extra_json": {},
            }

        # row indices must match CREATE TABLE order above
        backup_numbers = json.loads(row[4]) if row[4] else []
        backup_addresses = json.loads(row[6]) if row[6] else []
        extra_json = json.loads(row[12]) if row[12] else {}

        return {
            "full_name": row[1] or "",
            "address": row[2] or "",
            "phone": row[3] or "",
            "backup_numbers": backup_numbers,
            "email": row[5] or "",
            "backup_addresses": backup_addresses,
            "country": row[7] or "",
            "city": row[8] or "",
            "responder_category": row[9] or "",
            "responder_role": row[10] or "",
            "work_position": row[11] or "",
            "extra_json": extra_json,
        }

    def _save_profile_data(self, data: dict):
        """Insert or update the user_profiles row for this user."""
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Check if row exists
        cursor.execute("SELECT 1 FROM user_profiles WHERE user_id = ?", (self.current_user.id,))
        exists = cursor.fetchone() is not None

        backup_numbers_json = json.dumps(data.get("backup_numbers", []))
        backup_addresses_json = json.dumps(data.get("backup_addresses", []))
        extra_json = json.dumps(data.get("extra_json", {}))

        if exists:
            cursor.execute(
                """
                UPDATE user_profiles
                SET full_name=?, address=?, phone=?, backup_numbers=?, email=?,
                    backup_addresses=?, country=?, city=?, responder_category=?,
                    responder_role=?, work_position=?, extra_json=?
                WHERE user_id=?
                """,
                (
                    data.get("full_name", ""),
                    data.get("address", ""),
                    data.get("phone", ""),
                    backup_numbers_json,
                    data.get("email", ""),
                    backup_addresses_json,
                    data.get("country", ""),
                    data.get("city", ""),
                    data.get("responder_category", ""),
                    data.get("responder_role", ""),
                    data.get("work_position", ""),
                    extra_json,
                    self.current_user.id,
                ),
            )
        else:
            cursor.execute(
                """
                INSERT INTO user_profiles (
                    user_id, full_name, address, phone, backup_numbers, email,
                    backup_addresses, country, city, responder_category,
                    responder_role, work_position, extra_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.current_user.id,
                    data.get("full_name", ""),
                    data.get("address", ""),
                    data.get("phone", ""),
                    backup_numbers_json,
                    data.get("email", ""),
                    backup_addresses_json,
                    data.get("country", ""),
                    data.get("city", ""),
                    data.get("responder_category", ""),
                    data.get("responder_role", ""),
                    data.get("work_position", ""),
                    extra_json,
                ),
            )

        conn.commit()
        conn.close()

    # -------------
    # UI Building
    # -------------
    def init_ui(self):
        # Top-level layout for this widget
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Scroll area so the whole profile page can scroll vertically
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(QFrame.NoFrame)

        # Container widget that will actually hold your existing profile layout
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(25)
        layout.setContentsMargins(30, 30, 30, 30)


        # Header
        header_layout = QHBoxLayout()
        title = QLabel("My Profile")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        header_layout.addWidget(title)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Profile card
        profile_card = QFrame()
        profile_card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                border: 1px solid #E5E7EB;
            }
            """
        )
        profile_layout = QVBoxLayout(profile_card)

        # Top (avatar + name + role)
        self._build_header_section(profile_layout)

        # Main form
        form_layout = QVBoxLayout()
        form_layout.setSpacing(20)

        self._build_personal_section(form_layout)
        self._build_account_section(form_layout)
        self._build_responder_section_if_needed(form_layout)
        self._build_member_since(form_layout)

        profile_layout.addLayout(form_layout)

        # Action buttons
        self._build_actions(profile_layout)

        # Add the profile card into the container layout
        layout.addWidget(profile_card)

        # Put the container (all content) inside the scroll area
        scroll_area.setWidget(container)

        # Add scroll area to the main layout
        main_layout.addWidget(scroll_area)

        # Apply main_layout to this widget
        self.setLayout(main_layout)

    def _build_header_section(self, parent_layout: QVBoxLayout):
        top_layout = QHBoxLayout()

        # Avatar section
        avatar_section = QFrame()
        avatar_section.setStyleSheet("background: transparent;")
        avatar_layout = QVBoxLayout(avatar_section)

        self.avatar_label = QLabel("👤")
        self.avatar_label.setStyleSheet(
            """
            font-size: 64px;
            background-color: #F3F4F6;
            border-radius: 50%;
            padding: 30px;
            min-width: 120px;
            max-width: 120px;
            min-height: 120px;
            max-height: 120px;
            """
        )
        self.avatar_label.setAlignment(Qt.AlignCenter)

        change_avatar_btn = QPushButton("Change Photo")
        change_avatar_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
            """
        )
        change_avatar_btn.clicked.connect(self.change_avatar)

        avatar_layout.addWidget(self.avatar_label)
        avatar_layout.addWidget(change_avatar_btn)
        avatar_layout.setAlignment(Qt.AlignCenter)

        # Basic info section
        info_section = QFrame()
        info_section.setStyleSheet("background: transparent;")
        info_layout = QVBoxLayout(info_section)

        name_label = QLabel(self.profile_data.get("full_name") or self.current_user.name)
        name_label.setFont(QFont("Arial", 24, QFont.Bold))
        name_label.setStyleSheet("color: #1F2937; margin-bottom: 5px;")

        role_badge = QLabel(self.current_user.role.upper())
        role_color = {
            "admin": "#EF4444",
            "responder": "#3B82F6",
            "reporter": "#10B981",
        }.get(self.current_user.role, "#6B7280")
        role_badge.setStyleSheet(
            f"""
            background-color: {role_color};
            color: white;
            padding: 6px 16px;
            border-radius: 16px;
            font-size: 12px;
            font-weight: bold;
            max-width: 120px;
            """
        )

        # Optional specialization line for responders/admins
        specialization = (
            self.profile_data.get("responder_category")
            or getattr(self.current_user, "responder_category", "")
        )
        if self.current_user.role in ("responder", "admin") and specialization:
            category_label = QLabel(f"Specialization: {specialization}")
            category_label.setStyleSheet(
                "color: #6B7280; font-size: 14px; margin-top: 5px;"
            )
            info_layout.addWidget(category_label)

        info_layout.addWidget(name_label)
        info_layout.addWidget(role_badge)
        info_layout.addStretch()

        top_layout.addWidget(avatar_section)
        top_layout.addWidget(info_section)
        top_layout.addStretch()

        parent_layout.addLayout(top_layout)

    def _build_personal_section(self, form_layout: QVBoxLayout):
        # Section title
        personal_section = QLabel("Personal Information")
        personal_section.setFont(QFont("Arial", 16, QFont.Bold))
        personal_section.setStyleSheet("color: #1F2937; margin: 20px 0 10px 0;")
        form_layout.addWidget(personal_section)

        # Name + Email
        name_email_layout = QHBoxLayout()

        name_layout = QVBoxLayout()
        name_label = QLabel("Full Name *")
        name_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.name_input = QLineEdit(self.profile_data.get("full_name") or self.current_user.name)
        self.name_input.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        name_layout.addWidget(name_label)
        name_layout.addWidget(self.name_input)

        email_layout = QVBoxLayout()
        email_label = QLabel("Email Address *")
        email_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.email_input = QLineEdit(self.profile_data.get("email") or self.current_user.email)
        self.email_input.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        email_layout.addWidget(email_label)
        email_layout.addWidget(self.email_input)

        name_email_layout.addLayout(name_layout)
        name_email_layout.addLayout(email_layout)
        form_layout.addLayout(name_email_layout)

        # Phone + Country
        phone_country_layout = QHBoxLayout()

        phone_layout = QVBoxLayout()
        phone_label = QLabel("Phone Number *")
        phone_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.phone_input = QLineEdit(self.profile_data.get("phone") or self.current_user.phone)
        self.phone_input.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        phone_layout.addWidget(phone_label)
        phone_layout.addWidget(self.phone_input)

        country_layout = QVBoxLayout()
        country_label = QLabel("Country")
        country_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.country_input = QLineEdit(self.profile_data.get("country") or "")
        self.country_input.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        country_layout.addWidget(country_label)
        country_layout.addWidget(self.country_input)

        phone_country_layout.addLayout(phone_layout)
        phone_country_layout.addLayout(country_layout)
        form_layout.addLayout(phone_country_layout)

        # City + Work Position
        city_position_layout = QHBoxLayout()

        city_layout = QVBoxLayout()
        city_label = QLabel("City")
        city_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.city_input = QLineEdit(self.profile_data.get("city") or "")
        self.city_input.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        city_layout.addWidget(city_label)
        city_layout.addWidget(self.city_input)

        position_layout = QVBoxLayout()
        position_label = QLabel("Work Position / Title")
        position_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.position_input = QLineEdit(self.profile_data.get("work_position") or "")
        self.position_input.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        position_layout.addWidget(position_label)
        position_layout.addWidget(self.position_input)

        city_position_layout.addLayout(city_layout)
        city_position_layout.addLayout(position_layout)
        form_layout.addLayout(city_position_layout)

        # Address (multi-line)
        address_layout = QVBoxLayout()
        address_label = QLabel("Address")
        address_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.address_input = QTextEdit(self.profile_data.get("address") or "")
        self.address_input.setMaximumHeight(60)
        self.address_input.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        address_layout.addWidget(address_label)
        address_layout.addWidget(self.address_input)
        form_layout.addLayout(address_layout)

        # Backup phone numbers
        backup_phone_section = QVBoxLayout()
        backup_phone_label = QLabel("Backup Phone Numbers")
        backup_phone_label.setFont(QFont("Arial", 11, QFont.Bold))
        backup_phone_section.addWidget(backup_phone_label)

        self.backup_phone_layout = QVBoxLayout()
        backup_phone_section.addLayout(self.backup_phone_layout)

        backup_numbers = self.profile_data.get("backup_numbers") or []
        if not backup_numbers:
            self._add_backup_phone_field("")
        else:
            for number in backup_numbers:
                self._add_backup_phone_field(number)

        add_backup_phone_btn = QPushButton("+ Add backup number")
        add_backup_phone_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #E5E7EB;
                color: #374151;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #D1D5DB;
            }
            """
        )
        add_backup_phone_btn.clicked.connect(lambda: self._add_backup_phone_field(""))
        backup_phone_section.addWidget(add_backup_phone_btn)

        form_layout.addLayout(backup_phone_section)

        # Backup addresses
        backup_address_section = QVBoxLayout()
        backup_address_label = QLabel("Backup Addresses")
        backup_address_label.setFont(QFont("Arial", 11, QFont.Bold))
        backup_address_section.addWidget(backup_address_label)

        self.backup_address_layout = QVBoxLayout()
        backup_address_section.addLayout(self.backup_address_layout)

        backup_addresses = self.profile_data.get("backup_addresses") or []
        if not backup_addresses:
            self._add_backup_address_field("")
        else:
            for addr in backup_addresses:
                self._add_backup_address_field(addr)

        add_backup_address_btn = QPushButton("+ Add backup address")
        add_backup_address_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #E5E7EB;
                color: #374151;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #D1D5DB;
            }
            """
        )
        add_backup_address_btn.clicked.connect(lambda: self._add_backup_address_field(""))
        backup_address_section.addWidget(add_backup_address_btn)

        form_layout.addLayout(backup_address_section)

    def _build_account_section(self, form_layout: QVBoxLayout):
        account_section = QLabel("Account Information")
        account_section.setFont(QFont("Arial", 16, QFont.Bold))
        account_section.setStyleSheet("color: #1F2937; margin: 20px 0 10px 0;")
        form_layout.addWidget(account_section)

        username_role_layout = QHBoxLayout()

        # Username
        username_layout = QVBoxLayout()
        username_label = QLabel("Username *")
        username_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.username_input = QLineEdit(self.current_user.username)
        self.username_input.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)

        # Role (read-only)
        role_layout = QVBoxLayout()
        role_label = QLabel("Role")
        role_label.setFont(QFont("Arial", 11, QFont.Bold))
        role_display = QLineEdit(self.current_user.role.title())
        role_display.setReadOnly(True)
        role_display.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px; background-color: #F3F4F6;"
        )
        role_layout.addWidget(role_label)
        role_layout.addWidget(role_display)

        username_role_layout.addLayout(username_layout)
        username_role_layout.addLayout(role_layout)
        form_layout.addLayout(username_role_layout)

    def _build_responder_section_if_needed(self, form_layout: QVBoxLayout):
        if self.current_user.role not in ("responder", "admin"):
            return

        responder_section = QLabel("Responder / Role Information")
        responder_section.setFont(QFont("Arial", 16, QFont.Bold))
        responder_section.setStyleSheet("color: #1F2937; margin: 20px 0 10px 0;")
        form_layout.addWidget(responder_section)

        # Category + Role row
        cat_role_layout = QHBoxLayout()

        # Category
        category_layout = QVBoxLayout()
        category_label = QLabel("Responder Category")
        category_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.category_combo = QComboBox()
        self.category_combo.addItems(get_category_list())

        # Try to select existing category if present
        existing_cat = (
            self.profile_data.get("responder_category")
            or getattr(self.current_user, "responder_category", "")
        )

        if existing_cat:
            pretty = existing_cat.replace("_", " ").title()
            for idx in range(self.category_combo.count()):
                if self.category_combo.itemText(idx).lower() == pretty.lower():
                    self.category_combo.setCurrentIndex(idx)
                    break

        self.category_combo.currentIndexChanged.connect(self._on_category_changed)
        category_layout.addWidget(category_label)
        category_layout.addWidget(self.category_combo)

        # Role within category
        role_layout = QVBoxLayout()
        role_label = QLabel("Role in Category")
        role_label.setFont(QFont("Arial", 11, QFont.Bold))
        self.role_combo = QComboBox()
        role_layout.addWidget(role_label)
        role_layout.addWidget(self.role_combo)

        cat_role_layout.addLayout(category_layout)
        cat_role_layout.addLayout(role_layout)
        form_layout.addLayout(cat_role_layout)

        # Initialize roles for the initial category
        self._on_category_changed()

        # Select existing role if present
        existing_role = self.profile_data.get("responder_role") or ""
        if existing_cat:
            pretty = existing_cat.replace("_", " ").title()
            for idx in range(self.category_combo.count()):
                if self.category_combo.itemText(idx).lower() == pretty.lower():
                    self.category_combo.setCurrentIndex(idx)
                    break


    def _build_member_since(self, form_layout: QVBoxLayout):
        member_since_layout = QVBoxLayout()
        member_since_label = QLabel("Member Since")
        member_since_label.setFont(QFont("Arial", 11, QFont.Bold))
        member_since = (
            self.current_user.created_at.strftime("%B %d, %Y")
            if getattr(self.current_user, "created_at", None)
            else "N/A"
        )
        member_since_display = QLineEdit(member_since)
        member_since_display.setReadOnly(True)
        member_since_display.setStyleSheet(
            "padding: 10px; border: 1px solid #D1D5DB; border-radius: 6px; background-color: #F3F4F6;"
        )
        member_since_layout.addWidget(member_since_label)
        member_since_layout.addWidget(member_since_display)
        form_layout.addLayout(member_since_layout)

    def _build_actions(self, profile_layout: QVBoxLayout):
        actions_layout = QHBoxLayout()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #6B7280;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #4B5563;
            }
            """
        )
        cancel_btn.clicked.connect(self._reset_form_from_profile_data)

        save_btn = QPushButton("💾 Save Changes")
        save_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #10B981;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #059669;
            }
            """
        )
        save_btn.clicked.connect(self.save_profile)

        change_password_btn = QPushButton("🔒 Change Password")
        change_password_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #3B82F6;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2563EB;
            }
            """
        )
        change_password_btn.clicked.connect(self.change_password)

        actions_layout.addWidget(cancel_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(change_password_btn)
        actions_layout.addWidget(save_btn)

        profile_layout.addLayout(actions_layout)

    # --------------------
    # Helper widget logic
    # --------------------
    def _add_backup_phone_field(self, value: str = ""):
        field = QLineEdit(value)
        field.setPlaceholderText("Backup phone number")
        field.setStyleSheet(
            "padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        self.backup_phone_inputs.append(field)
        self.backup_phone_layout.addWidget(field)

    def _add_backup_address_field(self, value: str = ""):
        field = QLineEdit(value)
        field.setPlaceholderText("Backup address")
        field.setStyleSheet(
            "padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        self.backup_address_inputs.append(field)
        self.backup_address_layout.addWidget(field)

    def _on_category_changed(self):
        if not self.category_combo or not self.role_combo:
            return
        category = self.category_combo.currentText()
        roles = get_roles_for_category(category)
        self.role_combo.clear()
        self.role_combo.addItems(roles)

    def _reset_form_from_profile_data(self):
        """Reset inputs back to the last loaded/saved profile_data."""
        self.name_input.setText(self.profile_data.get("full_name") or self.current_user.name)
        self.email_input.setText(self.profile_data.get("email") or self.current_user.email)
        self.phone_input.setText(self.profile_data.get("phone") or self.current_user.phone)
        self.country_input.setText(self.profile_data.get("country") or "")
        self.city_input.setText(self.profile_data.get("city") or "")
        self.position_input.setText(self.profile_data.get("work_position") or "")
        self.address_input.setPlainText(self.profile_data.get("address") or "")
        self.username_input.setText(self.current_user.username)

        # Reset backup lists
        for w in self.backup_phone_inputs:
            w.deleteLater()
        for w in self.backup_address_inputs:
            w.deleteLater()
        self.backup_phone_inputs.clear()
        self.backup_address_inputs.clear()

        for num in self.profile_data.get("backup_numbers") or [""]:
            self._add_backup_phone_field(num)
        for addr in self.profile_data.get("backup_addresses") or [""]:
            self._add_backup_address_field(addr)

        # Responder fields
        if self.category_combo:
            existing_cat = (
                self.profile_data.get("responder_category")
                or getattr(self.current_user, "responder_category", "")
            )
            if existing_cat:
                for idx in range(self.category_combo.count()):
                    if self.category_combo.itemText(idx).lower() == existing_cat.lower():
                        self.category_combo.setCurrentIndex(idx)
                        break
            self._on_category_changed()

        if self.role_combo and self.profile_data.get("responder_role"):
            for idx in range(self.role_combo.count()):
                if self.role_combo.itemText(idx).lower() == self.profile_data[
                    "responder_role"
                ].lower():
                    self.role_combo.setCurrentIndex(idx)
                    break

    # -----------------
    # Public actions
    # -----------------
    def save_profile(self):
        # Validate required fields
        if not all(
            [
                self.name_input.text().strip(),
                self.email_input.text().strip(),
                self.phone_input.text().strip(),
                self.username_input.text().strip(),
            ]
        ):
            QMessageBox.warning(self, "Validation Error", "Please fill in all required fields.")
            return

        username = self.username_input.text().strip()
        email = self.email_input.text().strip()

        # Check for username / email uniqueness (excluding current user)
        existing_user = self.db.get_user_by_username(username)
        if existing_user and existing_user.id != self.current_user.id:
            QMessageBox.warning(self, "Error", "This username is already taken.")
            return

        existing_email_user = self.db.get_user_by_email(email)
        if existing_email_user and existing_email_user.id != self.current_user.id:
            QMessageBox.warning(self, "Error", "This email is already registered.")
            return

        # Collect backup numbers and addresses
        backup_numbers = [
            w.text().strip() for w in self.backup_phone_inputs if w.text().strip()
        ]
        backup_addresses = [
            w.text().strip() for w in self.backup_address_inputs if w.text().strip()
        ]

        # Responder fields
        responder_category = ""
        responder_role = ""
        if self.current_user.role in ("responder", "admin") and self.category_combo:
            pretty = self.category_combo.currentText().strip()
            responder_category = pretty.lower().replace(" ", "_")
            responder_role = self.role_combo.currentText().strip() if self.role_combo else ""

        # Update in-memory current_user (core fields only)
        self.current_user.name = self.name_input.text().strip()
        self.current_user.email = email
        self.current_user.phone = self.phone_input.text().strip()
        self.current_user.username = username
        if responder_category:
            self.current_user.responder_category = responder_category

        # Persist to users table
        self.db.update_user(self.current_user)

        # Prepare extended profile data and save to user_profiles table
        extended_data = {
            "full_name": self.name_input.text().strip(),
            "address": self.address_input.toPlainText().strip(),
            "phone": self.phone_input.text().strip(),
            "backup_numbers": backup_numbers,
            "email": email,
            "backup_addresses": backup_addresses,
            "country": self.country_input.text().strip(),
            "city": self.city_input.text().strip(),
            "responder_category": responder_category,
            "responder_role": responder_role,
            "work_position": self.position_input.text().strip(),
            "extra_json": self.profile_data.get("extra_json", {}),
        }

        self._save_profile_data(extended_data)
        # keep local copy in sync so Cancel works correctly
        self.profile_data = extended_data

        QMessageBox.information(self, "Success", "Profile updated successfully!")

    def change_password(self):
        # You can replace this placeholder with a real "Change Password" dialog later
        QMessageBox.information(
            self,
            "Change Password",
            "Password change functionality would be implemented here.",
        )

    def change_avatar(self):
        """Let the user pick an image file and display it in the avatar label."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Profile Photo", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if not file_path:
            return
        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            QMessageBox.warning(self, "Error", "Could not load selected image.")
            return
        # Scale to fit the avatar circle area
        scaled = pixmap.scaled(120, 120, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.avatar_label.setPixmap(scaled)
        self.avatar_label.setText("")  # remove emoji text
