# responder/responder_available_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTimer
from datetime import datetime
import styles


class ResponderAvailablePage(QWidget):
    """Pending incidents that match this responder's category."""

    def __init__(self, user, db):
        super().__init__()
        self.user = user
        self.db = db
        self.init_ui()
        self.load_data()

        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(5000)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)

        title = QLabel("Available Incidents")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        layout.addWidget(title)

        info = QLabel(
            "Showing pending incidents that match your specialization category."
        )
        info.setStyleSheet("color: #6B7280;")
        layout.addWidget(info)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Type", "Category", "Location", "Priority", "Reporter", "Actions"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def _category_matches(self, incident_cat: str) -> bool:
        if not self.user.responder_category:
            return True  # no specialization -> see all
        user_cat = self.user.responder_category.lower().replace(" ", "_")
        inc_cat = (incident_cat or "").lower().replace(" ", "_")
        return user_cat == inc_cat

    def load_data(self):
        all_incidents = self.db.get_all_incidents()
        pending = [
            inc
            for inc in all_incidents
            if inc.status == "pending" and self._category_matches(inc.incident_category)
        ]

        self.table.setRowCount(len(pending))
        for row, inc in enumerate(pending):
            self.table.setItem(row, 0, QTableWidgetItem(inc.id))
            self.table.setItem(row, 1, QTableWidgetItem(inc.type))
            self.table.setItem(row, 2, QTableWidgetItem(inc.incident_category or "General"))
            self.table.setItem(row, 3, QTableWidgetItem(inc.location))

            p_item = QTableWidgetItem(inc.priority if getattr(inc, 'priority', None) else "N/A")
            pcode = (getattr(inc, 'priority', '') or "").upper()
            if pcode == 'P1':
                p_item.setBackground(QColor(220, 38, 38))
            elif pcode == 'P2':
                p_item.setBackground(QColor(239, 68, 68))
            elif pcode == 'P3':
                p_item.setBackground(QColor(245, 158, 11))
            elif pcode == 'P4':
                p_item.setBackground(QColor(16, 185, 129))
            else:
                p_item.setBackground(QColor(108, 117, 125))
            p_item.setForeground(QColor(255, 255, 255))
            self.table.setItem(row, 4, p_item)

            self.table.setItem(row, 5, QTableWidgetItem(inc.reporter_name or ""))

            btn = QPushButton("Accept")
            btn.setStyleSheet(styles.STYLES["button_style"])
            btn.clicked.connect(lambda checked, incident=inc: self.accept_incident(incident))
            self.table.setCellWidget(row, 6, btn)

    def accept_incident(self, incident):
        incident.responder_id = self.user.id
        incident.responder_name = self.user.name
        incident.status = "ongoing"
        incident.updated_at = datetime.now()

        self.user.active_incidents += 1
        if self.user.active_incidents > 0:
            self.user.status = "busy"

        self.db.update_incident(incident)
        self.db.update_user(self.user)

        self.load_data()
        QMessageBox.information(self, "Success", f"Incident {incident.id} accepted.")
