from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QComboBox, QDialog,
    QFormLayout, QLineEdit, QTextEdit, QGroupBox,
    QSizePolicy,
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from datetime import datetime

import styles
from incident_data import get_incident_display_name, get_responders_for_incident


class AdminDashboard(QWidget):
    def __init__(self, user, db):
        super().__init__()
        self.user = user
        self.db = db
        self.init_ui()
        self.load_data()

        # Auto-refresh every 5 seconds
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(5000)

    # ------------------------------------------------------------------ UI
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # Header
        header = QLabel("Admin Dashboard")
        header.setFont(QFont("Arial", 18, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(header)

        # Stats cards
        stats_layout = QHBoxLayout()
        self.total_users_card = self.create_stat_card("Total Users", "0")
        self.total_incidents_card = self.create_stat_card("Total Incidents", "0")
        self.pending_incidents_card = self.create_stat_card(
            "Pending", "0", styles.STYLES["status_pending"]
        )
        self.ongoing_incidents_card = self.create_stat_card(
            "Ongoing", "0", styles.STYLES["status_ongoing"]
        )
        self.solved_incidents_card = self.create_stat_card(
            "Solved", "0", styles.STYLES["status_solved"]
        )

        # optional: equal stretch
        stats_layout.addWidget(self.total_users_card, 1)
        stats_layout.addWidget(self.total_incidents_card, 1)
        stats_layout.addWidget(self.pending_incidents_card, 1)
        stats_layout.addWidget(self.ongoing_incidents_card, 1)
        stats_layout.addWidget(self.solved_incidents_card, 1)
        layout.addLayout(stats_layout)

        # Actions
        actions_layout = QHBoxLayout()

        manage_users_btn = QPushButton("Manage Users")
        manage_users_btn.setStyleSheet(styles.STYLES["button_style"])
        manage_users_btn.clicked.connect(self.show_user_management)

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(styles.STYLES["button_style"])
        refresh_btn.clicked.connect(self.load_data)

        actions_layout.addWidget(manage_users_btn)
        actions_layout.addWidget(refresh_btn)
        actions_layout.addStretch()
        layout.addLayout(actions_layout)

        # Incidents table
        incidents_label = QLabel("All Incidents")
        incidents_label.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(incidents_label)

        self.incidents_table = QTableWidget()
        self.incidents_table.setColumnCount(9)
        self.incidents_table.setHorizontalHeaderLabels(
            [
                "ID",
                "Type",
                "Category",
                "Location",
                "Severity",
                "Status",
                "Reporter",
                "Responder",
                "Actions",
            ]
        )
        self.incidents_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.incidents_table)

        self.setLayout(layout)

    def create_stat_card(self, title, value, style=""):
        card = QFrame()
        card.setStyleSheet(styles.STYLES["card_style"])

        card.setMinimumHeight(110)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)

        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 22, QFont.Bold))
        value_label.setStyleSheet(style)
        value_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")

        layout.addWidget(value_label)
        layout.addWidget(title_label)
        card.setLayout(layout)

        return card

    # ------------------------------------------------------------------ DATA LOAD
    def load_data(self):
        users = self.db.get_all_users()
        incidents = self.db.get_all_incidents()

        # Update stats
        self.total_users_card.layout().itemAt(0).widget().setText(str(len(users)))
        self.total_incidents_card.layout().itemAt(0).widget().setText(str(len(incidents)))
        self.pending_incidents_card.layout().itemAt(0).widget().setText(
            str(len([i for i in incidents if i.status == "pending"]))
        )
        self.ongoing_incidents_card.layout().itemAt(0).widget().setText(
            str(len([i for i in incidents if i.status == "ongoing"]))
        )
        self.solved_incidents_card.layout().itemAt(0).widget().setText(
            str(len([i for i in incidents if i.status == "solved"]))
        )

        # Update incidents table
        self.incidents_table.setRowCount(len(incidents))
        for row, incident in enumerate(incidents):
            self.incidents_table.setItem(row, 0, QTableWidgetItem(incident.id))
            self.incidents_table.setItem(
                row, 1, QTableWidgetItem(get_incident_display_name(incident.type))
            )
            self.incidents_table.setItem(
                row, 2, QTableWidgetItem(incident.incident_category or "General")
            )
            self.incidents_table.setItem(row, 3, QTableWidgetItem(incident.location))

            # Severity with color
            severity_item = QTableWidgetItem(incident.severity.title())
            if incident.severity == "low":
                severity_item.setBackground(QColor(39, 174, 96))
            elif incident.severity == "medium":
                severity_item.setBackground(QColor(243, 156, 18))
            else:
                severity_item.setBackground(QColor(231, 76, 60))
            severity_item.setForeground(QColor(255, 255, 255))
            self.incidents_table.setItem(row, 4, severity_item)

            # Status with color
            status_item = QTableWidgetItem(incident.status.title())
            if incident.status == "pending":
                status_item.setBackground(QColor(243, 156, 18))
            elif incident.status == "ongoing":
                status_item.setBackground(QColor(52, 152, 219))
            else:
                status_item.setBackground(QColor(39, 174, 96))
            status_item.setForeground(QColor(255, 255, 255))
            self.incidents_table.setItem(row, 5, status_item)

            self.incidents_table.setItem(
                row, 6, QTableWidgetItem(incident.reporter_name or "")
            )
            self.incidents_table.setItem(
                row, 7, QTableWidgetItem(incident.responder_name or "Unassigned")
            )

            # Action buttons
            actions_widget = QWidget()
            actions_layout = QHBoxLayout()
            actions_layout.setContentsMargins(0, 0, 0, 0)

            # View details button
            details_btn = QPushButton("Details")
            details_btn.setStyleSheet(styles.STYLES["button_style"])
            details_btn.clicked.connect(
                lambda checked, inc=incident: self.show_incident_details(inc)
            )

            # Assign button for pending incidents
            if incident.status == "pending":
                assign_btn = QPushButton("Assign")
                assign_btn.setStyleSheet(styles.STYLES["button_style"])
                assign_btn.clicked.connect(
                    lambda checked, inc=incident: self.show_assign_dialog(inc)
                )
                actions_layout.addWidget(assign_btn)

            actions_layout.addWidget(details_btn)
            actions_widget.setLayout(actions_layout)
            self.incidents_table.setCellWidget(row, 8, actions_widget)

    # ------------------------------------------------------------------ ACTIONS
    def show_incident_details(self, incident):
        """ONLY show details dialog (no weird overrides)."""
        dialog = IncidentDetailsDialog(incident, self.db, self)
        dialog.exec_()

    def show_assign_dialog(self, incident):
        dialog = AssignResponderDialog(incident, self.db, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
            self.show_toast(f"Responder assigned to {incident.id}", "success")

    def show_user_management(self):
        dialog = UserManagementDialog(self.db, self)
        dialog.exec_()

    def show_toast(self, message, msg_type="info"):
        msg_box = QMessageBox()
        if msg_type == "success":
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Success")
        else:
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Info")

        msg_box.setText(message)
        msg_box.exec_()


# ---------------------------------------------------------------------- Dialogs
class IncidentDetailsDialog(QDialog):
    def __init__(self, incident, db, parent=None):
        super().__init__(parent)
        self.incident = incident
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Incident Details - {self.incident.id}")
        self.setFixedSize(600, 500)

        layout = QVBoxLayout()

        # Basic Information
        basic_group = QGroupBox("Basic Information")
        basic_layout = QFormLayout()

        basic_layout.addRow("ID:", QLabel(self.incident.id))
        basic_layout.addRow(
            "Type:", QLabel(get_incident_display_name(self.incident.type))
        )
        basic_layout.addRow(
            "Category:", QLabel(self.incident.incident_category or "General")
        )
        basic_layout.addRow("Location:", QLabel(self.incident.location))
        basic_layout.addRow("Severity:", QLabel(self.incident.severity.title()))
        basic_layout.addRow("Status:", QLabel(self.incident.status.title()))
        basic_layout.addRow("Reporter:", QLabel(self.incident.reporter_name))
        basic_layout.addRow(
            "Responder:", QLabel(self.incident.responder_name or "Unassigned")
        )
        basic_layout.addRow(
            "Created:",
            QLabel(self.incident.created_at.strftime("%Y-%m-%d %H:%M")),
        )
        basic_layout.addRow(
            "Updated:",
            QLabel(self.incident.updated_at.strftime("%Y-%m-%d %H:%M")),
        )

        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)

        # Description
        desc_group = QGroupBox("Description")
        desc_layout = QVBoxLayout()
        desc_label = QLabel(self.incident.description)
        desc_label.setWordWrap(True)
        desc_layout.addWidget(desc_label)
        desc_group.setLayout(desc_layout)
        layout.addWidget(desc_group)

        # Specific Questions
        if self.incident.specific_questions:
            questions_group = QGroupBox("Additional Information")
            questions_layout = QFormLayout()

            for key, value in self.incident.specific_questions.items():
                if value:  # Only show answered questions
                    questions_layout.addRow(
                        f"{key.replace('_', ' ').title()}:",
                        QLabel(str(value)),
                    )

            questions_group.setLayout(questions_layout)
            layout.addWidget(questions_group)

        # Emergency Feedback
        if self.incident.emergency_feedback:
            feedback_group = QGroupBox("Emergency Instructions")
            feedback_layout = QVBoxLayout()
            feedback_label = QLabel(self.incident.emergency_feedback)
            feedback_label.setWordWrap(True)
            feedback_label.setStyleSheet(
                "padding: 10px; background-color: #fff3cd; border-radius: 4px;"
            )
            feedback_layout.addWidget(feedback_label)
            feedback_group.setLayout(feedback_layout)
            layout.addWidget(feedback_group)

        # Recommended Responders
        if self.incident.assigned_responders:
            responders_group = QGroupBox("Recommended Responders")
            responders_layout = QVBoxLayout()
            responders_label = QLabel(", ".join(self.incident.assigned_responders))
            responders_label.setWordWrap(True)
            responders_layout.addWidget(responders_label)
            responders_group.setLayout(responders_layout)
            layout.addWidget(responders_group)

        # Close button
        close_btn = QPushButton("Close")
        close_btn.setStyleSheet(styles.STYLES["button_style"])
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

        self.setLayout(layout)


class AssignResponderDialog(QDialog):
    def __init__(self, incident, db, parent=None):
        super().__init__(parent)
        self.incident = incident
        self.db = db
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(f"Assign Responder to {self.incident.id}")
        self.setFixedSize(400, 200)

        layout = QFormLayout()

        # Incident info
        layout.addRow(
            QLabel(f"Type: {get_incident_display_name(self.incident.type)}")
        )
        layout.addRow(QLabel(f"Location: {self.incident.location}"))
        layout.addRow(QLabel(f"Severity: {self.incident.severity.title()}"))

        # Responder selection
        self.responder_combo = QComboBox()
        responders = self.db.get_responders()
        available_responders = [r for r in responders if r.status == "available"]

        if available_responders:
            for responder in available_responders:
                self.responder_combo.addItem(
                    f"{responder.name} ({responder.id})", responder.id
                )
        else:
            self.responder_combo.addItem("No available responders", None)

        layout.addRow("Select Responder:", self.responder_combo)

        # Buttons
        buttons_layout = QHBoxLayout()
        assign_btn = QPushButton("Assign")
        assign_btn.setStyleSheet(styles.STYLES["button_style"])
        assign_btn.clicked.connect(self.assign_responder)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setStyleSheet(styles.STYLES["danger_button_style"])
        cancel_btn.clicked.connect(self.reject)

        buttons_layout.addWidget(assign_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addRow(buttons_layout)

        self.setLayout(layout)

    def assign_responder(self):
        if self.responder_combo.currentData() is None:
            self.show_error("No available responders")
            return

        responder_id = self.responder_combo.currentData()
        responder = self.db.get_user_by_id(responder_id)

        if not responder:
            self.show_error("Selected responder not found")
            return

        # Update incident
        self.incident.responder_id = responder.id
        self.incident.responder_name = responder.name
        self.incident.status = "ongoing"
        self.incident.updated_at = datetime.now()

        # Update responder
        responder.active_incidents += 1
        if responder.active_incidents > 0:
            responder.status = "busy"

        self.db.update_incident(self.incident)
        self.db.update_user(responder)

        self.accept()

    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()


class UserManagementDialog(QDialog):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.db = db
        self.init_ui()
        self.load_users()

    def init_ui(self):
        self.setWindowTitle("User Management")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        # Header
        header = QLabel("All Users")
        header.setFont(QFont("Arial", 16, QFont.Bold))
        layout.addWidget(header)

        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(
            ["ID", "Name", "Email", "Role", "Status", "Active Incidents"]
        )
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.users_table)

        self.setLayout(layout)

    def load_users(self):
        users = self.db.get_all_users()
        self.users_table.setRowCount(len(users))

        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user.id))
            self.users_table.setItem(row, 1, QTableWidgetItem(user.name))
            self.users_table.setItem(row, 2, QTableWidgetItem(user.email))
            self.users_table.setItem(row, 3, QTableWidgetItem(user.role.title()))

            status_item = QTableWidgetItem(user.status.title())
            if user.status == "available":
                status_item.setBackground(QColor(39, 174, 96))
            else:
                status_item.setBackground(QColor(231, 76, 60))
            status_item.setForeground(QColor(255, 255, 255))
            self.users_table.setItem(row, 4, status_item)

            self.users_table.setItem(
                row, 5, QTableWidgetItem(str(user.active_incidents))
            )
