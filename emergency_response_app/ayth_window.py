#ayth_window.py


from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,        # UI elements and layouts
    QLineEdit, QPushButton, QMessageBox, QFormLayout, # input fields, buttons, popups, forms
    QDialog, QFrame, QComboBox                        # dialog window, frame, dropdowns
)
from PyQt5.QtCore import Qt, pyqtSignal               # core features (alignment, custom signals)
from PyQt5.QtGui import QFont, QIcon                  # font styles and icons
import uuid                                           # for generating unique user IDs
import re                                             # for regex validation
import os                                             # for file/system operations

from database import Database                         # database interaction class
from models import User                               # User model structure
import styles                                         # custom stylesheet for UI

import hashlib

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Base directory for loading icons
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(BASE_DIR, "icons")

# ------------------------------------------------------------------ Password Validation
def validate_password(password: str) -> bool:
    """Validate that password is at least 8 chars, has upper+lower and a special char.""" 
    if len(password) < 8: 
        return False
    if not re.search(r"[A-Z]", password): 
        return False
    if not re.search(r"[a-z]", password): 
        return False
    if not re.search(r"[^A-Za-z0-9]", password): 
        return False
    return True 

# ---------------------------------------------------------------------- Auth Window
class AuthWindow(QWidget):
    """Main login window."""

    login_success = pyqtSignal(object)  # Emits a User object

    def __init__(self):
        super().__init__()
        self.db = Database()
        self.init_ui()

    # ------------------------------------------------------------------ UI
    def init_ui(self):
        self.setWindowTitle("Emergency Response System - Login")
        self.setStyleSheet("background-color: #ecf0f1;")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Title
        title = QLabel("Emergency Response System")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 24, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin-bottom: 25px;")
        main_layout.addWidget(title)

        # Login card
        login_box = QFrame()
        login_box.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 12px;
                padding: 30px;
                border: 1px solid #dcdcdc;
            }
            """
        )
        login_box.setFixedWidth(550)

        box_layout = QVBoxLayout(login_box)
        box_layout.setSpacing(20)

        # ------------- Username row -------------
        username_row = QHBoxLayout()
        username_row.setSpacing(10)

        username_label = QLabel("Username:")
        username_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #2c3e50;
                background: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                padding: 8px 12px;
                min-width: 120px;
            }
            """
        )
        
        username_label.setFixedHeight(36)

        self.login_username = QLineEdit()
        self.login_username.setPlaceholderText("Enter your username")
        self.login_username.setStyleSheet(
            """
            QLineEdit {
                font-size: 16px;
                background: #f4f6f7;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                padding: 8px 12px;
                min-height: 40px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                background: #ffffff;
            }
            """
        )
        self.login_username.setFixedHeight(36)

        username_row.addWidget(username_label)
        username_row.addWidget(self.login_username)
        box_layout.addLayout(username_row)

        # ------------- Password row -------------
        password_row = QHBoxLayout()
        password_row.setSpacing(10)

        password_label = QLabel("Password:")
        password_label.setStyleSheet(
            """
            QLabel {
                font-size: 16px;
                color: #2c3e50;
                background: #ffffff;
                border: 1px solid #dcdcdc;
                border-radius: 6px;
                padding: 8px 12px;
                min-width: 120px;
            }
            """
        )
        password_label.setFixedHeight(36)

        # wrapper for password + eye button
        password_field_wrapper = QWidget()
        password_field_layout = QHBoxLayout(password_field_wrapper)
        password_field_layout.setContentsMargins(0, 0, 0, 0)
        password_field_layout.setSpacing(0)

        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Enter your password")
        self.login_password.setEchoMode(QLineEdit.Password)
        self.login_password.setStyleSheet(
            """
            QLineEdit {
                font-size: 16px;
                background: #f4f6f7;
                border: 1px solid #dcdcdc;
                border-top-left-radius: 6px;
                border-bottom-left-radius: 6px;
                border-right: none;
                padding: 8px 12px;
                min-height: 36px;
            }
            QLineEdit:focus {
                border: 1px solid #3498db;
                border-right: none;
                background: #ffffff;
            }
            """
        )
        self.login_password.setFixedHeight(36)

        self.show_pass_btn = QPushButton()
        self.show_pass_btn.setCheckable(True)
        self.show_pass_btn.setFixedSize(40, 36)
        # default icon: password hidden -> eye icon
        self.show_pass_btn.setIcon(QIcon(os.path.join(ICON_DIR, "eye.png")))
        self.show_pass_btn.clicked.connect(self.toggle_password_visibility)
        self.show_pass_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #dcdcdc;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }
            QPushButton:checked {
                background-color: #e8f3ff;
                border-color: #3498db;
            }
            """
        )

        password_field_layout.addWidget(self.login_password)
        password_field_layout.addWidget(self.show_pass_btn)

        password_row.addWidget(password_label)
        password_row.addWidget(password_field_wrapper)
        box_layout.addLayout(password_row)

        # ------------- Buttons row -------------
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        login_btn = QPushButton("Login")
        login_btn.setStyleSheet(styles.STYLES["button_style"])
        login_btn.clicked.connect(self.handle_login)
        btn_layout.addWidget(login_btn)

        create_btn = QPushButton("Create Account")
        create_btn.setStyleSheet(styles.STYLES["button_style"])
        create_btn.clicked.connect(self.open_create_account_window)
        btn_layout.addWidget(create_btn)

        forgot_btn = QPushButton("Forgot Password?")
        forgot_btn.setFlat(True)
        forgot_btn.setStyleSheet("color: #2c3e50; margin-left: 10px;")
        forgot_btn.clicked.connect(self.open_password_recovery_dialog)
        btn_layout.addWidget(forgot_btn)

        btn_layout.addStretch()
        box_layout.addLayout(btn_layout)

        main_layout.addWidget(login_box)

    # ------------------------------------------------------------------ Logic
    def toggle_password_visibility(self):
        """Show/hide password and swap eye icon."""
        if self.show_pass_btn.isChecked():
            # SHOW password
            self.login_password.setEchoMode(QLineEdit.Normal)
            self.show_pass_btn.setIcon(QIcon(os.path.join(ICON_DIR, "eye-off.png")))
        else:
            # HIDE password
            self.login_password.setEchoMode(QLineEdit.Password)
            self.show_pass_btn.setIcon(QIcon(os.path.join(ICON_DIR, "eye.png")))

    def handle_login(self):
        username = self.login_username.text().strip()
        password = self.login_password.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        user = self.db.get_user_by_username(username)
        if not user or user.password != hash_password(password):
            QMessageBox.warning(self, "Error", "Invalid username or password.")
            return


        # success
        self.login_success.emit(user)
        self.close()

    def open_create_account_window(self):
        self.create_window = CreateAccountWindow(self.db)
        self.create_window.show()


    def open_password_recovery_dialog(self):
        dialog = PasswordRecoveryDialog(self.db, self)
        dialog.exec_()


# ---------------------------------------------------------------------- Create Account
class CreateAccountWindow(QWidget):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Create Account")
        self.resize(700, 650)
        self.setMinimumSize(650, 600)
        

        layout = QFormLayout()
        layout.setSpacing(15)

        # Full name
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter your full name")
        layout.addRow("Full Name:", self.name_input)

        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        layout.addRow("Username:", self.username_input)

        # Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a strong password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Password:", self.password_input)

        # Confirm Password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Re-enter password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addRow("Confirm Password:", self.confirm_password_input)

        # Date of birth
        self.dob_input = QLineEdit()
        self.dob_input.setPlaceholderText("YYYY-MM-DD (optional)")
        layout.addRow("Date of Birth:", self.dob_input)

        # Gender
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["", "Male", "Female", "Other"])
        layout.addRow("Gender:", self.gender_combo)

        # Email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        layout.addRow("Email:", self.email_input)

        # Phone
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your phone number")
        layout.addRow("Phone:", self.phone_input)

        # Role
        self.role_combo = QComboBox()
        self.role_combo.addItems(["Reporter", "Responder"])
        self.role_combo.currentTextChanged.connect(self.on_role_changed)
        layout.addRow("Role:", self.role_combo)

        # Responder category (only for responder)
        self.responder_category_input = QLineEdit()
        self.responder_category_input.setPlaceholderText("e.g. Medical, Fire, Police")
        layout.addRow("Responder Category:", self.responder_category_input)

        # Buttons
        btn_layout = QHBoxLayout()
        create_btn = QPushButton("Create")
        create_btn.setStyleSheet(styles.STYLES["button_style"])
        create_btn.clicked.connect(self.handle_create)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(styles.STYLES["danger_button_style"])
        cancel_btn.clicked.connect(self.close)

        btn_layout.addWidget(create_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)
        self.setLayout(layout)

        # initialize state
        self.on_role_changed(self.role_combo.currentText())

    def on_role_changed(self, role_text: str):
        """Only enable responder category if role is Responder."""
        is_responder = role_text.lower() == "responder"
        self.responder_category_input.setVisible(is_responder)

    def handle_create(self):
        

        name = self.name_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_password_input.text().strip()
        dob = self.dob_input.text().strip()
        gender = self.gender_combo.currentText()
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_pattern, email):
            QMessageBox.warning(self, "Error", "Invalid email format.")
            return
        if not phone.isdigit():
            QMessageBox.warning(self, "Error", "Phone number must contain only digits.")
            return
        ROLE_MAP = {
            "Reporter": "reporter",
            "Responder": "responder"
        }

        role = ROLE_MAP[self.role_combo.currentText()] # "reporter" or "responder"
        
        responder_category = (
            self.responder_category_input.text().strip() if role == "responder" else ""
        )

        if not (name and username and password and email and phone and role):
            QMessageBox.warning(self, "Error", "Please fill in all required fields.")
            return

        # Password validation
        if not validate_password(password):
            QMessageBox.warning(
                self,
                "Weak Password",
                "Password must be at least 8 characters, include upper, lower, and a special character.",
            )
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return

        # Uniqueness checks
        if self.db.get_user_by_username(username):
            QMessageBox.warning(self, "Error", "Username already exists.")
            return

        if self.db.get_user_by_email(email):
            QMessageBox.warning(self, "Error", "Email already in use.")
            return

        # Create user
        user = User(
            id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=hash_password(password),
            role=role,
            username=username,
            phone=phone,
            gender=gender,
            date_of_birth=dob,
            responder_category=responder_category,
        )

        self.db.create_user(user)
        QMessageBox.information(self, "Success", "Account created successfully.")
        self.close()


# ---------------------------------------------------------------------- Password Recovery
class PasswordRecoveryDialog(QDialog):
    def __init__(self, db: Database, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Password Recovery")
        self.setFixedSize(400, 220)

        layout = QFormLayout()
        layout.setSpacing(15)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your registered email")
        layout.addRow("Email:", self.email_input)

        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter your registered phone number")
        layout.addRow("Phone:", self.phone_input)

        btn_layout = QHBoxLayout()
        recover_btn = QPushButton("Recover")
        recover_btn.setStyleSheet(styles.STYLES["button_style"])
        recover_btn.clicked.connect(self.handle_recover)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(styles.STYLES["danger_button_style"])
        cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(recover_btn)
        btn_layout.addWidget(cancel_btn)

        layout.addRow(btn_layout)
        self.setLayout(layout)

    
    def handle_recover(self):
        email = self.email_input.text().strip()
        phone = self.phone_input.text().strip()

        if not email or not phone:
            QMessageBox.warning(self, "Error", "Please provide both email and phone.")
            return

        user = self.db.get_user_by_email_and_phone(email, phone)
        if user:
            QMessageBox.information(
                self,
                "Recovery Successful",
                "Your identity was verified.\nPlease contact admin to reset your password."
            )
            self.accept()

        else:
            QMessageBox.warning(self, "Not Found", "No user found with that email and phone.")
