# responder/responder_dashboard.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTableWidget, QTableWidgetItem,
    QHeaderView, QMessageBox, QDialog, QFormLayout,
    QSizePolicy,       
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from datetime import datetime
import styles

class ResponderDashboard(QWidget):
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
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Header
        header = QLabel('Responder Dashboard')
        header.setFont(QFont('Arial', 18, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        self.total_assignments_card = self.create_stat_card("My Assignments", "0")
        self.active_incidents_card = self.create_stat_card("Active Incidents", "0", styles.STYLES['status_ongoing'])
        self.pending_incidents_card = self.create_stat_card("Available", "0", styles.STYLES['status_pending'])
        
        stats_layout.addWidget(self.total_assignments_card)
        stats_layout.addWidget(self.active_incidents_card)
        stats_layout.addWidget(self.pending_incidents_card)
        layout.addLayout(stats_layout)
        
        # Refresh button
        refresh_btn = QPushButton('Refresh')
        refresh_btn.setStyleSheet(styles.STYLES['button_style'])
        refresh_btn.setFixedWidth(120)       # 🔹 Button width fixed
        refresh_btn.setFixedHeight(36)       # 🔹 Height fixed
        refresh_btn.setCursor(Qt.PointingHandCursor)

        # 🔹 Left-align the button
        refresh_btn_layout = QHBoxLayout()
        refresh_btn_layout.addWidget(refresh_btn)
        refresh_btn_layout.addStretch()       # Pushes nothing to the right, keeping button left

        layout.addLayout(refresh_btn_layout)

        # Available incidents table
        available_label = QLabel('Available Incidents (Pending)')
        available_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(available_label)
        
        self.available_table = QTableWidget()
        self.available_table.setColumnCount(6)
        self.available_table.setHorizontalHeaderLabels(['ID', 'Type', 'Location', 'Priority', 'Reporter', 'Actions'])
        self.available_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.available_table)
        
        # My assignments table
        assignments_label = QLabel('My Assignments')
        assignments_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(assignments_label)
        
        self.assignments_table = QTableWidget()
        self.assignments_table.setColumnCount(6)
        self.assignments_table.setHorizontalHeaderLabels(['ID', 'Type', 'Location', 'Priority', 'Status', 'Actions'])
        self.assignments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.assignments_table)
        
        self.setLayout(layout)
    
    def create_stat_card(self, title, value, style=""):
        card = QFrame()
        card.setStyleSheet(styles.STYLES['card_style'])

        card.setMinimumHeight(110)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.setContentsMargins(16, 12, 16, 12)

        value_label = QLabel(value)
        value_label.setFont(QFont('Arial', 22, QFont.Bold))
        value_label.setStyleSheet(style)
        value_label.setAlignment(Qt.AlignCenter)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")

        layout.addWidget(value_label)
        layout.addWidget(title_label)
        card.setLayout(layout)

        return card
    
    def load_data(self):
        # Get all pending incidents
        all_incidents = self.db.get_all_incidents()
        pending_incidents = [i for i in all_incidents if i.status == 'pending']
        my_assignments = self.db.get_incidents_by_responder(self.user.id)
        
        # Update stats
        self.total_assignments_card.layout().itemAt(0).widget().setText(str(len(my_assignments)))
        self.active_incidents_card.layout().itemAt(0).widget().setText(str(len([i for i in my_assignments if i.status == 'ongoing'])))
        self.pending_incidents_card.layout().itemAt(0).widget().setText(str(len(pending_incidents)))
        
        # Update available incidents table
        self.available_table.setRowCount(len(pending_incidents))
        for row, incident in enumerate(pending_incidents):
            self.available_table.setItem(row, 0, QTableWidgetItem(incident.id))
            self.available_table.setItem(row, 1, QTableWidgetItem(incident.type))
            self.available_table.setItem(row, 2, QTableWidgetItem(incident.location))
            
            p_item = QTableWidgetItem(incident.priority if getattr(incident, 'priority', None) else "N/A")
            pcode = (getattr(incident, 'priority', '') or "").upper()
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
            self.available_table.setItem(row, 3, p_item) 
            
            self.available_table.setItem(row, 4, QTableWidgetItem(incident.reporter_name))
            
            # Accept button
            accept_btn = QPushButton('Accept')
            accept_btn.setStyleSheet(styles.STYLES['button_style'])
            accept_btn.clicked.connect(lambda checked, inc=incident: self.accept_incident(inc))
            self.available_table.setCellWidget(row, 5, accept_btn)
        
        # Update assignments table
        self.assignments_table.setRowCount(len(my_assignments))
        for row, incident in enumerate(my_assignments):
            self.assignments_table.setItem(row, 0, QTableWidgetItem(incident.id))
            self.assignments_table.setItem(row, 1, QTableWidgetItem(incident.type))
            self.assignments_table.setItem(row, 2, QTableWidgetItem(incident.location))
            
            p_item = QTableWidgetItem(incident.priority if getattr(incident, 'priority', None) else "N/A")
            pcode = (getattr(incident, 'priority', '') or "").upper()
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
            self.assignments_table.setItem(row, 3, p_item)
            
            status_item = QTableWidgetItem(incident.status.title())
            if incident.status == 'ongoing':
                status_item.setBackground(QColor(52, 152, 219))
                status_item.setForeground(QColor(255, 255, 255))
            self.assignments_table.setItem(row, 4, status_item)
            
            # Solve button for ongoing incidents
            if incident.status == 'ongoing':
                solve_btn = QPushButton('Mark Solved')
                solve_btn.setStyleSheet(styles.STYLES['success_button_style'])
                solve_btn.clicked.connect(lambda checked, inc=incident: self.solve_incident(inc))
                self.assignments_table.setCellWidget(row, 5, solve_btn)
    
    def accept_incident(self, incident):
        incident.responder_id = self.user.id
        incident.responder_name = self.user.name
        incident.status = 'ongoing'
        incident.updated_at = datetime.now()
        
        self.user.active_incidents += 1
        if self.user.active_incidents > 0:
            self.user.status = 'busy'
        
        self.db.update_incident(incident)
        self.db.update_user(self.user)
        
        self.load_data()
        self.show_toast(f"Incident {incident.id} accepted successfully!", "success")
    
    def solve_incident(self, incident):
        incident.status = 'solved'
        incident.updated_at = datetime.now()
        
        self.user.active_incidents -= 1
        if self.user.active_incidents == 0:
            self.user.status = 'available'
        
        self.db.update_incident(incident)
        self.db.update_user(self.user)
        
        self.load_data()
        self.show_toast(f"Incident {incident.id} marked as solved!", "success")
    
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
