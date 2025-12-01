# reporter_incident_page.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGroupBox,
    QLabel, QLineEdit, QTextEdit, QComboBox, QPushButton,
    QScrollArea, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

from models import Incident
from incident_data import (
    incident_categories,
    get_questions_for_incident,
    get_feedback_for_incident,
    get_responders_for_incident,
    get_incident_display_name,
)
import styles


class ReporterNewIncidentPage(QWidget):
    """Full-page incident report form for reporters."""

    def __init__(self, user, db):
        super().__init__()
        self.user = user
        self.db = db
        self.dynamic_widgets = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(16)

        title = QLabel("Report New Incident")
        title.setFont(QFont("Arial", 20, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        main_layout.addWidget(title)

        # scrollable area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # ---- Incident category group ----
        category_group = QGroupBox("Incident Category")
        category_layout = QFormLayout()

        self.category_combo = QComboBox()
        self.category_combo.addItems([cat.title() for cat in incident_categories.keys()])
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        category_layout.addRow("Category:", self.category_combo)

        self.type_combo = QComboBox()
        category_layout.addRow("Incident Type:", self.type_combo)

        self.severity_combo = QComboBox()
        self.severity_combo.addItems(["low", "medium", "high"])
        category_layout.addRow("Severity:", self.severity_combo)

        category_group.setLayout(category_layout)
        scroll_layout.addWidget(category_group)

        # ---- Location group ----
        location_group = QGroupBox("Location Information")
        location_layout = QFormLayout()
        self.location_input = QLineEdit()
        self.location_input.setPlaceholderText("Enter exact address or location")
        location_layout.addRow("Location:", self.location_input)
        location_group.setLayout(location_layout)
        scroll_layout.addWidget(location_group)

        # ---- Description group ----
        desc_group = QGroupBox("Incident Description")
        desc_layout = QVBoxLayout()
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Describe the incident in detail...")
        self.description_input.setFixedHeight(120)
        desc_layout.addWidget(self.description_input)
        desc_group.setLayout(desc_layout)
        scroll_layout.addWidget(desc_group)

        # ---- Dynamic questions ----
        self.questions_group = QGroupBox("Additional Information")
        self.questions_layout = QFormLayout()
        self.questions_group.setLayout(self.questions_layout)
        scroll_layout.addWidget(self.questions_group)

        # ---- Emergency instructions ----
        self.feedback_group = QGroupBox("Emergency Instructions")
        feedback_layout = QVBoxLayout()
        self.feedback_label = QLabel(
            "Select an incident type to see emergency instructions."
        )
        self.feedback_label.setWordWrap(True)
        self.feedback_label.setStyleSheet(
            "padding: 10px; background-color: #fff3cd; border-radius: 4px;"
        )
        feedback_layout.addWidget(self.feedback_label)
        self.feedback_group.setLayout(feedback_layout)
        scroll_layout.addWidget(self.feedback_group)

        # ---- Action buttons ----
        btn_layout = QHBoxLayout()
        submit_btn = QPushButton("Submit Report")
        submit_btn.setStyleSheet(styles.STYLES["button_style"])
        submit_btn.clicked.connect(self.submit_incident)

        clear_btn = QPushButton("Clear")
        clear_btn.setStyleSheet(styles.STYLES["danger_button_style"])
        clear_btn.clicked.connect(self.reset_form)

        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addStretch()
        scroll_layout.addLayout(btn_layout)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

        # init first category
        self.on_category_changed(self.category_combo.currentText())

    # ----------------- dynamic questions -----------------
    def on_category_changed(self, category_text: str):
        cat_key = category_text.lower()
        self.type_combo.clear()

        if cat_key in incident_categories:
            for incident_type in incident_categories[cat_key]:
                display_name = get_incident_display_name(incident_type)
                self.type_combo.addItem(display_name, incident_type)

        self.type_combo.currentIndexChanged.connect(self.on_incident_type_changed)
        self.on_incident_type_changed()

    def on_incident_type_changed(self):
        # clear old widgets
        for w in self.dynamic_widgets.values():
            w.deleteLater()
        self.dynamic_widgets.clear()

        while self.questions_layout.count():
            item = self.questions_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        incident_type = self.type_combo.currentData()
        if not incident_type:
            return

        questions = get_questions_for_incident(incident_type)

        for key, question in questions.items():
            if key in ["location", "incident_description"]:
                continue
            if "yes/no" in question.lower() or question.lower().endswith("(yes/no)"):
                widget = QComboBox()
                widget.addItems(["", "Yes", "No"])
            else:
                widget = QLineEdit()
                widget.setPlaceholderText(key.replace("_", " ").title())

            self.questions_layout.addRow(question, widget)
            self.dynamic_widgets[key] = widget

        feedback = get_feedback_for_incident(incident_type)
        self.feedback_label.setText(feedback)

    # ----------------- helpers -----------------
    def _collect_specific_questions(self):
        data = {}
        for key, widget in self.dynamic_widgets.items():
            if isinstance(widget, QComboBox):
                data[key] = widget.currentText()
            else:
                data[key] = widget.text()
        return data

    def reset_form(self):
        self.location_input.clear()
        self.description_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.severity_combo.setCurrentIndex(0)
        self.on_category_changed(self.category_combo.currentText())

    def submit_incident(self):
        location = self.location_input.text().strip()
        description = self.description_input.toPlainText().strip()
        severity = self.severity_combo.currentText()
        incident_type = self.type_combo.currentData()

        if not location or not description:
            QMessageBox.warning(self, "Error", "Please fill in location and description.")
            return
        if not incident_type:
            QMessageBox.warning(self, "Error", "Please select an incident type.")
            return

        incident_id = self.db.get_next_incident_id()

        # derive category from type
        category = None
        for cat, types in incident_categories.items():
            if incident_type in types:
                category = cat
                break

        specific_questions = self._collect_specific_questions()

        incident = Incident(
            id=incident_id,
            type=incident_type,
            location=location,
            description=description,
            severity=severity,
            reporter_id=self.user.id,
            reporter_name=self.user.name,
            incident_category=category,
            specific_questions=specific_questions,
            emergency_feedback=get_feedback_for_incident(incident_type),
            assigned_responders=get_responders_for_incident(incident_type),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        self.db.create_incident(incident)

        QMessageBox.information(
            self,
            "Success",
            f"Incident {incident_id} reported successfully!\n"
            f"Recommended responders: {', '.join(incident.assigned_responders)}",
        )
        self.reset_form()
