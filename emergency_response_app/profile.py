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
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Scroll area — fills all available space and shrinks with the window
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setSizePolicy(
            scroll_area.sizePolicy().horizontalPolicy(),
            scroll_area.sizePolicy().verticalPolicy()
        )

        container = QWidget()
        container.setMinimumWidth(400)   # never clip below 400 px wide
        layout = QVBoxLayout(container)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 24, 30, 30)

        # ── Page title ──────────────────────────────────────────
        title = QLabel("My Profile")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        layout.addWidget(title)

        # ── Profile card ────────────────────────────────────────
        profile_card = QFrame()
        profile_card.setStyleSheet(
            "QFrame { background-color: white; border-radius: 12px;"
            " border: 1px solid #E5E7EB; }"
        )
        profile_layout = QVBoxLayout(profile_card)
        profile_layout.setContentsMargins(24, 24, 24, 24)
        profile_layout.setSpacing(20)

        self._build_header_section(profile_layout)

        # Thin divider
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setStyleSheet("color: #E5E7EB;")
        profile_layout.addWidget(divider)

        self._build_personal_section(profile_layout)
        self._build_account_section(profile_layout)
        self._build_responder_section_if_needed(profile_layout)
        self._build_member_since(profile_layout)
        self._build_actions(profile_layout)

        layout.addWidget(profile_card)
        layout.addStretch()

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    # ── reusable helpers ────────────────────────────────────────────────────

    def _section_title(self, text: str) -> QLabel:
        """Bold section heading — visible and prominent."""
        lbl = QLabel(text)
        lbl.setFont(QFont("Arial", 16, QFont.Bold))
        lbl.setStyleSheet(
            "color: #111827;"
            " padding-top: 8px;"
            " padding-bottom: 4px;"
            " border-bottom: 2px solid #E5E7EB;"
        )
        return lbl

    def _field_label(self, text: str) -> QLabel:
        """Bold label shown ABOVE the input box."""
        lbl = QLabel(text)
        lbl.setFont(QFont("Arial", 11, QFont.Bold))
        lbl.setStyleSheet("color: #374151;")
        return lbl

    def _input_style(self, readonly: bool = False) -> str:
        bg = "#F9FAFB" if readonly else "white"
        return (
            f"QLineEdit {{ padding: 8px 10px; font-size: 13px; color: #111827;"
            f" background: {bg}; border: 1px solid #D1D5DB;"
            f" border-radius: 6px; }}"
            f"QLineEdit:focus {{ border: 1px solid #3498db; }}"
        )

    def _make_field(self, label_text: str, value: str,
                    readonly: bool = False) -> tuple:
        """Return (container QVBoxLayout, QLineEdit) for one labelled field."""
        col = QVBoxLayout()
        col.setSpacing(4)
        col.addWidget(self._field_label(label_text))
        inp = QLineEdit(value or "")
        inp.setMinimumHeight(36)
        inp.setReadOnly(readonly)
        inp.setStyleSheet(self._input_style(readonly))
        col.addWidget(inp)
        return col, inp

    def _row(self, *cols) -> QHBoxLayout:
        """Place several QVBoxLayout columns side by side with equal stretch."""
        h = QHBoxLayout()
        h.setSpacing(16)
        for c in cols:
            h.addLayout(c, 1)
        return h

    # ── section builders ────────────────────────────────────────────────────

    def _build_header_section(self, parent_layout: QVBoxLayout):
        top = QHBoxLayout()
        top.setSpacing(20)

        # Avatar
        self.avatar_label = QLabel("👤")
        self.avatar_label.setFixedSize(90, 90)
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setStyleSheet(
            "font-size: 48px; background-color: #F3F4F6;"
            " border-radius: 45px;"
        )

        av_col = QVBoxLayout()
        av_col.setSpacing(6)
        av_col.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        av_col.addWidget(self.avatar_label)

        change_btn = QPushButton("Change Photo")
        change_btn.setFixedHeight(28)
        change_btn.setStyleSheet(
            "QPushButton { background: #6B7280; color: white; border: none;"
            " border-radius: 5px; font-size: 11px; padding: 0 10px; }"
            "QPushButton:hover { background: #4B5563; }"
        )
        change_btn.clicked.connect(self.change_avatar)
        av_col.addWidget(change_btn)

        top.addLayout(av_col)

        # Name + role badge
        info_col = QVBoxLayout()
        info_col.setSpacing(6)
        info_col.setAlignment(Qt.AlignVCenter)

        display_name = self.profile_data.get("full_name") or self.current_user.name
        name_lbl = QLabel(display_name)
        name_lbl.setFont(QFont("Arial", 18, QFont.Bold))
        name_lbl.setStyleSheet("color: #111827;")
        info_col.addWidget(name_lbl)

        role_color = {
            "admin": "#EF4444",
            "responder": "#3B82F6",
            "reporter": "#10B981",
        }.get(self.current_user.role, "#6B7280")
        badge = QLabel(self.current_user.role.upper())
        badge.setFixedHeight(26)
        badge.setStyleSheet(
            f"background-color: {role_color}; color: white;"
            " padding: 2px 14px; border-radius: 13px;"
            " font-size: 11px; font-weight: bold;"
        )
        info_col.addWidget(badge)

        spec = (
            self.profile_data.get("responder_category")
            or getattr(self.current_user, "responder_category", "")
        )
        if self.current_user.role in ("responder", "admin") and spec:
            spec_lbl = QLabel(f"Specialization: {spec}")
            spec_lbl.setStyleSheet("color: #6B7280; font-size: 12px;")
            info_col.addWidget(spec_lbl)

        top.addLayout(info_col)
        top.addStretch()
        parent_layout.addLayout(top)

    def _build_personal_section(self, form_layout: QVBoxLayout):
        form_layout.addWidget(self._section_title("Personal Information"))

        # Row 1 — Full Name | Email
        c1, self.name_input = self._make_field(
            "Full Name *",
            self.profile_data.get("full_name") or self.current_user.name
        )
        c2, self.email_input = self._make_field(
            "Email Address *",
            self.profile_data.get("email") or self.current_user.email
        )
        form_layout.addLayout(self._row(c1, c2))

        # Row 2 — Phone | Country
        c3, self.phone_input = self._make_field(
            "Phone Number *",
            self.profile_data.get("phone") or (self.current_user.phone or "")
        )
        c4, self.country_input = self._make_field(
            "Country",
            self.profile_data.get("country") or ""
        )
        form_layout.addLayout(self._row(c3, c4))

        # Row 3 — City | Work Position
        c5, self.city_input = self._make_field(
            "City",
            self.profile_data.get("city") or ""
        )
        c6, self.position_input = self._make_field(
            "Work Position / Title",
            self.profile_data.get("work_position") or ""
        )
        form_layout.addLayout(self._row(c5, c6))

        # Address — full width
        addr_col = QVBoxLayout()
        addr_col.setSpacing(4)
        addr_col.addWidget(self._field_label("Address"))
        self.address_input = QTextEdit(self.profile_data.get("address") or "")
        self.address_input.setFixedHeight(64)
        self.address_input.setStyleSheet(
            "QTextEdit { padding: 8px 10px; font-size: 13px; color: #111827;"
            " background: white; border: 1px solid #D1D5DB; border-radius: 6px; }"
            "QTextEdit:focus { border: 1px solid #3498db; }"
        )
        addr_col.addWidget(self.address_input)
        form_layout.addLayout(addr_col)

        # Backup phone numbers
        form_layout.addWidget(self._field_label("Backup Phone Numbers"))
        self.backup_phone_layout = QVBoxLayout()
        self.backup_phone_layout.setSpacing(6)
        form_layout.addLayout(self.backup_phone_layout)
        for num in (self.profile_data.get("backup_numbers") or [""]):
            self._add_backup_phone_field(num)
        add_bp = QPushButton("+ Add backup number")
        add_bp.setFixedHeight(30)
        add_bp.setStyleSheet(
            "QPushButton { background: #E5E7EB; color: #374151; border: none;"
            " padding: 0 12px; border-radius: 6px; font-size: 12px; }"
            "QPushButton:hover { background: #D1D5DB; }"
        )
        add_bp.clicked.connect(lambda: self._add_backup_phone_field(""))
        form_layout.addWidget(add_bp)

        # Backup addresses
        form_layout.addWidget(self._field_label("Backup Addresses"))
        self.backup_address_layout = QVBoxLayout()
        self.backup_address_layout.setSpacing(6)
        form_layout.addLayout(self.backup_address_layout)
        for addr in (self.profile_data.get("backup_addresses") or [""]):
            self._add_backup_address_field(addr)
        add_ba = QPushButton("+ Add backup address")
        add_ba.setFixedHeight(30)
        add_ba.setStyleSheet(
            "QPushButton { background: #E5E7EB; color: #374151; border: none;"
            " padding: 0 12px; border-radius: 6px; font-size: 12px; }"
            "QPushButton:hover { background: #D1D5DB; }"
        )
        add_ba.clicked.connect(lambda: self._add_backup_address_field(""))
        form_layout.addWidget(add_ba)

    def _build_account_section(self, form_layout: QVBoxLayout):
        form_layout.addWidget(self._section_title("Account Information"))

        c1, self.username_input = self._make_field(
            "Username *", self.current_user.username
        )
        c2, _ = self._make_field(
            "Role", self.current_user.role.title(), readonly=True
        )
        form_layout.addLayout(self._row(c1, c2))

    def _build_responder_section_if_needed(self, form_layout: QVBoxLayout):
        if self.current_user.role not in ("responder", "admin"):
            return

        form_layout.addWidget(self._section_title("Responder / Role Information"))

        # Read values set at account creation — display only, not editable
        existing_cat = (
            self.profile_data.get("responder_category")
            or getattr(self.current_user, "responder_category", "")
            or ""
        )
        existing_role = self.profile_data.get("responder_role") or ""

        # Human-readable category label
        category_display = existing_cat.replace("_", " ").title() if existing_cat else "Not set"

        # Get roles list for this category so we can show the saved role
        roles_for_cat = get_roles_for_category(
            existing_cat.replace("_", " ").title()
        ) if existing_cat else []
        role_display = existing_role if existing_role else (
            roles_for_cat[0] if roles_for_cat else "Not set"
        )

        # Show as read-only fields — same grey style as Role and Member Since
        c1, _ = self._make_field("Responder Category", category_display, readonly=True)
        c2, _ = self._make_field("Role in Category", role_display, readonly=True)
        form_layout.addLayout(self._row(c1, c2))

        # Explanatory note
        note = QLabel(
            "ℹ  Category and role were set when the account was created "
            "and cannot be changed here."
        )
        note.setWordWrap(True)
        note.setStyleSheet("color: #9CA3AF; font-size: 11px; padding-top: 2px;")
        form_layout.addWidget(note)

        # Set to None so save_profile and _on_category_changed ignore them safely
        self.category_combo = None
        self.role_combo = None

    def _build_member_since(self, form_layout: QVBoxLayout):
        c, _ = self._make_field(
            "Member Since",
            (
                self.current_user.created_at.strftime("%B %d, %Y")
                if getattr(self.current_user, "created_at", None)
                else "N/A"
            ),
            readonly=True,
        )
        h = QHBoxLayout()
        h.addLayout(c)
        h.addStretch()
        form_layout.addLayout(h)

    def _build_actions(self, profile_layout: QVBoxLayout):
        # Thin divider above buttons
        div = QFrame()
        div.setFrameShape(QFrame.HLine)
        div.setStyleSheet("color: #E5E7EB;")
        profile_layout.addWidget(div)

        actions = QHBoxLayout()
        actions.setSpacing(10)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(38)
        cancel_btn.setStyleSheet(
            "QPushButton { background: #6B7280; color: white; border: none;"
            " padding: 0 20px; border-radius: 7px; font-size: 13px; }"
            "QPushButton:hover { background: #4B5563; }"
        )
        cancel_btn.clicked.connect(self._reset_form_from_profile_data)

        save_btn = QPushButton("💾  Save Changes")
        save_btn.setFixedHeight(38)
        save_btn.setStyleSheet(
            "QPushButton { background: #10B981; color: white; border: none;"
            " padding: 0 20px; border-radius: 7px; font-size: 13px; font-weight: bold; }"
            "QPushButton:hover { background: #059669; }"
        )
        save_btn.clicked.connect(self.save_profile)

        pwd_btn = QPushButton("🔒  Change Password")
        pwd_btn.setFixedHeight(38)
        pwd_btn.setStyleSheet(
            "QPushButton { background: #3B82F6; color: white; border: none;"
            " padding: 0 20px; border-radius: 7px; font-size: 13px; }"
            "QPushButton:hover { background: #2563EB; }"
        )
        pwd_btn.clicked.connect(self.change_password)

        actions.addWidget(cancel_btn)
        actions.addStretch()
        actions.addWidget(pwd_btn)
        actions.addWidget(save_btn)
        profile_layout.addLayout(actions)

    # --------------------
    # Helper widget logic
    # --------------------
    def _add_backup_phone_field(self, value: str = ""):
        # Create a horizontal layout for the field and remove button
        field_layout = QHBoxLayout()
        
        field = QLineEdit(value)
        field.setPlaceholderText("Backup phone number")
        field.setStyleSheet(
            "padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        
        remove_btn = QPushButton("Remove")
        remove_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            """
        )
        remove_btn.clicked.connect(lambda: self._remove_backup_phone_field(field_layout))
        
        field_layout.addWidget(field)
        field_layout.addWidget(remove_btn)
        field_layout.addStretch()  # Push remove button to the right
        
        self.backup_phone_inputs.append(field)
        self.backup_phone_layout.addLayout(field_layout)

    def _remove_backup_phone_field(self, field_layout):
        # Find the QLineEdit in the layout
        for i in range(field_layout.count()):
            widget = field_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.backup_phone_inputs.remove(widget)
                break
        # Remove the layout from the parent layout
        for i in range(self.backup_phone_layout.count()):
            item = self.backup_phone_layout.itemAt(i)
            if item.layout() == field_layout:
                # Remove all widgets from the layout
                while field_layout.count():
                    child = field_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                self.backup_phone_layout.removeItem(item)
                break

    def _add_backup_address_field(self, value: str = ""):
        # Create a horizontal layout for the field and remove button
        field_layout = QHBoxLayout()
        
        field = QLineEdit(value)
        field.setPlaceholderText("Backup address")
        field.setStyleSheet(
            "padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px;"
        )
        
        remove_btn = QPushButton("Remove")
        remove_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #EF4444;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
                margin-left: 10px;
            }
            QPushButton:hover {
                background-color: #DC2626;
            }
            """
        )
        remove_btn.clicked.connect(lambda: self._remove_backup_address_field(field_layout))
        
        field_layout.addWidget(field)
        field_layout.addWidget(remove_btn)
        field_layout.addStretch()  # Push remove button to the right
        
        self.backup_address_inputs.append(field)
        self.backup_address_layout.addLayout(field_layout)

    def _remove_backup_address_field(self, field_layout):
        # Find the QLineEdit in the layout
        for i in range(field_layout.count()):
            widget = field_layout.itemAt(i).widget()
            if isinstance(widget, QLineEdit):
                self.backup_address_inputs.remove(widget)
                break
        # Remove the layout from the parent layout
        for i in range(self.backup_address_layout.count()):
            item = self.backup_address_layout.itemAt(i)
            if item.layout() == field_layout:
                # Remove all widgets from the layout
                while field_layout.count():
                    child = field_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
                self.backup_address_layout.removeItem(item)
                break

    def _on_category_changed(self):
        # Only relevant if editable combos exist (not the read-only profile view)
        if not self.category_combo or not self.role_combo:
            return
        roles = get_roles_for_category(self.category_combo.currentText())
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
        # Clear all layouts in backup_phone_layout
        while self.backup_phone_layout.count():
            item = self.backup_phone_layout.takeAt(0)
            if item.layout():
                # Remove all widgets from the sub-layout
                sub_layout = item.layout()
                while sub_layout.count():
                    child = sub_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            elif item.widget():
                item.widget().deleteLater()
        self.backup_phone_inputs.clear()
        
        # Clear all layouts in backup_address_layout
        while self.backup_address_layout.count():
            item = self.backup_address_layout.takeAt(0)
            if item.layout():
                # Remove all widgets from the sub-layout
                sub_layout = item.layout()
                while sub_layout.count():
                    child = sub_layout.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()
            elif item.widget():
                item.widget().deleteLater()
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
