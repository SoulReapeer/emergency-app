# responder/responder_assignments_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QPushButton, QMessageBox
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTimer
from datetime import datetime
import styles


class ResponderAssignmentsPage(QWidget):
    """All incidents assigned to this responder."""

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

        title = QLabel("My Assignments")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Type", "Location", "Priority", "Status", "Reporter", "Actions"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_data(self):
        assignments = self.db.get_incidents_by_responder(self.user.id)
        self.table.setRowCount(len(assignments))

        for row, inc in enumerate(assignments):
            self.table.setItem(row, 0, QTableWidgetItem(inc.id))
            self.table.setItem(row, 1, QTableWidgetItem(inc.type))
            self.table.setItem(row, 2, QTableWidgetItem(inc.location))

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
            self.table.setItem(row, 3, p_item)

            status_item = QTableWidgetItem(inc.status.title())
            if inc.status == "ongoing":
                status_item.setBackground(QColor(52, 152, 219))
            elif inc.status == "solved":
                status_item.setBackground(QColor(39, 174, 96))
            status_item.setForeground(QColor(255, 255, 255))
            self.table.setItem(row, 4, status_item)

            self.table.setItem(row, 5, QTableWidgetItem(inc.reporter_name or ""))

            # only ongoing incidents get "Mark Solved" button
            if inc.status == "ongoing":
                btn = QPushButton("Mark Solved")
                btn.setStyleSheet(styles.STYLES["success_button_style"])
                btn.clicked.connect(lambda checked, incident=inc: self.solve_incident(incident))
                self.table.setCellWidget(row, 6, btn)

    def solve_incident(self, incident):
        incident.status = "solved"
        incident.updated_at = datetime.now()

        self.user.active_incidents = max(0, self.user.active_incidents - 1)
        if self.user.active_incidents == 0:
            self.user.status = "available"

        self.db.update_incident(incident)
        self.db.update_user(self.user)

        self.load_data()
        QMessageBox.information(self, "Success", f"Incident {incident.id} marked as solved.")
