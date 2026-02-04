# reporter/reporter_history_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import QTimer
import styles


class ReporterHistoryPage(QWidget):
    """List of all incidents reported by this user."""

    def __init__(self, user, db):
        super().__init__()
        self.user = user
        self.db = db
        self.init_ui()
        self.load_data()

        # auto refresh every 5s like dashboard
        self.timer = QTimer()
        self.timer.timeout.connect(self.load_data)
        self.timer.start(5000)

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(16)

        title = QLabel("My Incident History")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Type",
                "Category",
                "Location",
                "Priority",
                "Status",
                "Responder",
                "Created",
                "Updated",
            ]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def load_data(self):
        incidents = self.db.get_incidents_by_reporter(self.user.id)

        self.table.setRowCount(len(incidents))
        for row, inc in enumerate(incidents):
            self.table.setItem(row, 0, QTableWidgetItem(inc.id))
            self.table.setItem(row, 1, QTableWidgetItem(inc.type))
            self.table.setItem(row, 2, QTableWidgetItem(inc.incident_category or "General"))
            self.table.setItem(row, 3, QTableWidgetItem(inc.location))

            # priority with color
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

            # status with color
            status_item = QTableWidgetItem(inc.status.title())
            if inc.status == "pending":
                status_item.setBackground(QColor(243, 156, 18))
            elif inc.status == "ongoing":
                status_item.setBackground(QColor(52, 152, 219))
            else:
                status_item.setBackground(QColor(39, 174, 96))
            status_item.setForeground(QColor(255, 255, 255))
            self.table.setItem(row, 5, status_item)

            self.table.setItem(row, 6, QTableWidgetItem(inc.responder_name or "Unassigned"))
            self.table.setItem(row, 7, QTableWidgetItem(inc.created_at.strftime("%Y-%m-%d %H:%M")))
            self.table.setItem(row, 8, QTableWidgetItem(inc.updated_at.strftime("%Y-%m-%d %H:%M")))
