# reporter/reporter_dashboard.py
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QPushButton, QFrame, QTableWidget, QTableWidgetItem,
                            QHeaderView, QMessageBox, QFormLayout, QLineEdit,
                            QComboBox, QTextEdit, QDialog, QGroupBox, QScrollArea,
                            QSizePolicy) 

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor
from models import Incident
from datetime import datetime
import styles
from incident_data import (incident_categories, incident_display_names, 
                          get_questions_for_incident, get_feedback_for_incident,
                          get_responders_for_incident, get_incident_display_name)

class ReporterDashboard(QWidget):
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
        header = QLabel('Reporter Dashboard')
        header.setFont(QFont('Arial', 18, QFont.Bold))
        header.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        self.total_incidents_card = self.create_stat_card("Total Incidents", "0")
        self.pending_incidents_card = self.create_stat_card("Pending", "0", styles.STYLES['status_pending'])
        self.ongoing_incidents_card = self.create_stat_card("Ongoing", "0", styles.STYLES['status_ongoing'])
        self.solved_incidents_card = self.create_stat_card("Solved", "0", styles.STYLES['status_solved'])
        
        stats_layout.addWidget(self.total_incidents_card)
        stats_layout.addWidget(self.pending_incidents_card)
        stats_layout.addWidget(self.ongoing_incidents_card)
        stats_layout.addWidget(self.solved_incidents_card)
        layout.addLayout(stats_layout)
        
        # Actions
        actions_layout = QHBoxLayout()

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(styles.STYLES["button_style"])
        refresh_btn.setFixedWidth(120)
        refresh_btn.setFixedHeight(36)
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.clicked.connect(self.load_data)

        actions_layout.addWidget(refresh_btn)
        actions_layout.addStretch()
        layout.addLayout(actions_layout)
        
        # Recent incidents table
        incidents_label = QLabel('Recent Incidents')
        incidents_label.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(incidents_label)
        
        self.incidents_table = QTableWidget()
        self.incidents_table.setColumnCount(7)
        self.incidents_table.setHorizontalHeaderLabels(['ID', 'Type', 'Category', 'Location', 'Priority', 'Status', 'Created'])
        self.incidents_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.incidents_table)
        
        self.setLayout(layout)
    
    def create_stat_card(self, title, value, style=""):
        card = QFrame()
        card.setStyleSheet(styles.STYLES['card_style'])
        card.setFixedHeight(80)
        
        layout = QVBoxLayout()
        
        value_label = QLabel(value)
        value_label.setFont(QFont('Arial', 20, QFont.Bold))
        value_label.setStyleSheet(style)
        value_label.setAlignment(Qt.AlignCenter)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #7f8c8d;")
        
        layout.addWidget(value_label)
        layout.addWidget(title_label)
        card.setLayout(layout)
        
        return card
    
    def load_data(self):
        incidents = self.db.get_incidents_by_reporter(self.user.id)
        
        # Update stats
        total = len(incidents)
        pending = len([i for i in incidents if i.status == 'pending'])
        ongoing = len([i for i in incidents if i.status == 'ongoing'])
        solved = len([i for i in incidents if i.status == 'solved'])
        
        self.total_incidents_card.layout().itemAt(0).widget().setText(str(total))
        self.pending_incidents_card.layout().itemAt(0).widget().setText(str(pending))
        self.ongoing_incidents_card.layout().itemAt(0).widget().setText(str(ongoing))
        self.solved_incidents_card.layout().itemAt(0).widget().setText(str(solved))
        
        # Update table
        self.incidents_table.setRowCount(len(incidents))
        for row, incident in enumerate(incidents):
            self.incidents_table.setItem(row, 0, QTableWidgetItem(incident.id))
            self.incidents_table.setItem(row, 1, QTableWidgetItem(get_incident_display_name(incident.type)))
            self.incidents_table.setItem(row, 2, QTableWidgetItem(incident.incident_category or "General"))
            self.incidents_table.setItem(row, 3, QTableWidgetItem(incident.location))
            
            priority_item = QTableWidgetItem(incident.priority if getattr(incident, 'priority', None) else "N/A")
            pcode = (getattr(incident, 'priority', '') or "").upper()
            if pcode == 'P1':
                priority_item.setBackground(QColor(220, 38, 38))
            elif pcode == 'P2':
                priority_item.setBackground(QColor(239, 68, 68))
            elif pcode == 'P3':
                priority_item.setBackground(QColor(245, 158, 11))
            elif pcode == 'P4':
                priority_item.setBackground(QColor(16, 185, 129))
            else:
                priority_item.setBackground(QColor(108, 117, 125))
            priority_item.setForeground(QColor(255, 255, 255))
            self.incidents_table.setItem(row, 4, priority_item) 
            
            status_item = QTableWidgetItem(incident.status.title())
            if incident.status == 'pending':
                status_item.setBackground(QColor(243, 156, 18))
            elif incident.status == 'ongoing':
                status_item.setBackground(QColor(52, 152, 219))
            else:
                status_item.setBackground(QColor(39, 174, 96))
            status_item.setForeground(QColor(255, 255, 255))
            self.incidents_table.setItem(row, 5, status_item)
            
            self.incidents_table.setItem(row, 6, QTableWidgetItem(incident.created_at.strftime('%Y-%m-%d %H:%M')))
    
    def show_new_incident_form(self):
        dialog = NewIncidentDialog(self.user, self.db, self)
        if dialog.exec_() == QDialog.Accepted:
            self.load_data()
            self.show_toast("Incident reported successfully!", "success")

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

class NewIncidentDialog(QDialog):
    def __init__(self, user, db, parent=None):
        super().__init__(parent)
        self.user = user
        self.db = db
        self.dynamic_widgets = {}
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle('Report New Incident')
        self.setFixedSize(600, 700)
        
        layout = QVBoxLayout()
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Incident Category
        category_group = QGroupBox("Incident Category")
        category_layout = QFormLayout()
        
        self.category_combo = QComboBox()
        self.category_combo.addItems([cat.title() for cat in incident_categories.keys()])
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        category_layout.addRow('Category:', self.category_combo)
        
        # Incident Type
        self.type_combo = QComboBox()
        category_layout.addRow('Incident Type:', self.type_combo)
        
        # Priority
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(['P1', 'P2', 'P3', 'P4', 'P5'])
        category_layout.addRow('Priority:', self.priority_combo)
        
        category_group.setLayout(category_layout)
        scroll_layout.addWidget(category_group)
        
        # Location
        location_group = QGroupBox("Location Information")
        location_layout = QFormLayout()
        
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter exact address or location")
        location_layout.addRow('Location:', self.location_input)
        
        location_group.setLayout(location_layout)
        scroll_layout.addWidget(location_group)
        
        # Description
        desc_group = QGroupBox("Incident Description")
        desc_layout = QVBoxLayout()
        
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Describe the incident in detail...")
        self.description_input.setFixedHeight(100)
        desc_layout.addWidget(self.description_input)
        
        desc_group.setLayout(desc_layout)
        scroll_layout.addWidget(desc_group)
        
        # Dynamic Questions Area
        self.questions_group = QGroupBox("Additional Information")
        self.questions_layout = QFormLayout()
        self.questions_group.setLayout(self.questions_layout)
        scroll_layout.addWidget(self.questions_group)
        
        # Emergency Feedback Area
        self.feedback_group = QGroupBox("Emergency Instructions")
        feedback_layout = QVBoxLayout()
        self.feedback_label = QLabel("Select an incident type to see emergency instructions.")
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setStyleSheet("padding: 10px; background-color: #fff3cd; border-radius: 4px;")
        feedback_layout.addWidget(self.feedback_label)
        self.feedback_group.setLayout(feedback_layout)
        scroll_layout.addWidget(self.feedback_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        submit_btn = QPushButton('Submit Report')
        submit_btn.setStyleSheet(styles.STYLES['button_style'])
        submit_btn.clicked.connect(self.submit_incident)
        
        cancel_btn = QPushButton('Cancel')
        cancel_btn.setStyleSheet(styles.STYLES['danger_button_style'])
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(submit_btn)
        buttons_layout.addWidget(cancel_btn)
        scroll_layout.addLayout(buttons_layout)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        self.setLayout(layout)
        
        # Initialize with first category
        self.on_category_changed(self.category_combo.currentText())
    
    def on_category_changed(self, category):
        category_lower = category.lower()
        self.type_combo.clear()
        
        if category_lower in incident_categories:
            incident_types = incident_categories[category_lower]
            for incident_type in incident_types:
                display_name = get_incident_display_name(incident_type)
                self.type_combo.addItem(display_name, incident_type)
        
        self.type_combo.currentIndexChanged.connect(self.on_incident_type_changed)
        self.on_incident_type_changed()
    
    def on_incident_type_changed(self):
        # Clear previous dynamic widgets
        for widget in self.dynamic_widgets.values():
            widget.deleteLater()
        self.dynamic_widgets.clear()
        
        # Clear questions layout
        for i in reversed(range(self.questions_layout.count())):
            item = self.questions_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
        
        incident_type = self.type_combo.currentData()
        if not incident_type:
            return
        
        # Get questions for this incident type
        questions = get_questions_for_incident(incident_type)
        
        # Create dynamic form fields
        for key, question in questions.items():
            if key in ['location', 'incident_description']:  # Already handled
                continue
                
            if 'yes/no' in question.lower() or question.endswith('(yes/no)'):
                widget = QComboBox()
                widget.addItems(['', 'Yes', 'No'])
            else:
                widget = QLineEdit()
                widget.setPlaceholderText(f"Enter {key.replace('_', ' ').title()}")
            
            self.questions_layout.addRow(question, widget)
            self.dynamic_widgets[key] = widget
        
        # Update emergency feedback
        feedback = get_feedback_for_incident(incident_type)
        self.feedback_label.setText(feedback)
    
    def get_incident_data(self):
        incident_type = self.type_combo.currentData()
        questions_data = {}
        
        for key, widget in self.dynamic_widgets.items():
            if isinstance(widget, QComboBox):
                questions_data[key] = widget.currentText()
            else:
                questions_data[key] = widget.text()
        
        return incident_type, questions_data
    
    def submit_incident(self):
        location = self.location_input.text().strip()
        description = self.description_input.toPlainText().strip()
        priority = self.priority_combo.currentText()
        incident_type, specific_questions = self.get_incident_data()
        
        if not location or not description:
            self.show_error("Please fill in location and description")
            return
        
        if not incident_type:
            self.show_error("Please select an incident type")
            return
        
        incident_id = self.db.get_next_incident_id()
        category = None
        for cat, types in incident_categories.items():
            if incident_type in types:
                category = cat
                break
        
        new_incident = Incident(
            id=incident_id,
            type=incident_type,
            location=location,
            description=description,
            priority=priority,
            reporter_id=self.user.id,
            reporter_name=self.user.name,
            incident_category=category,
            specific_questions=specific_questions,
            emergency_feedback=get_feedback_for_incident(incident_type),
            assigned_responders=get_responders_for_incident(incident_type),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        
        self.db.create_incident(new_incident)
        self.show_toast(f"Incident {incident_id} reported successfully!\nRecommended responders: {', '.join(new_incident.assigned_responders)}", "success")
        self.accept()
    
    def show_error(self, message):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()
    
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
