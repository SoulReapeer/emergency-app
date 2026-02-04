# admin/admin_incidents.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QTabWidget,
    QLineEdit, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

from incident_data import get_incident_display_name


class AdminIncidents(QWidget):
    """
    Admin incident management view.

    Works with your existing Incident model:
    - type
    - location
    - description
    - severity
    - status: 'pending', 'ongoing', 'solved'
    - reporter_name, responder_name
    - incident_category
    - created_at, updated_at
    """

    def __init__(self, incidents, users, db):
        super().__init__()
        self.incidents = incidents
        self.users = users          # list[User]
        self.db = db                # Database instance
        self.init_ui()

    # ------------------------------------------------------------------ UI
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # ---------------- Header ----------------
        header_layout = QHBoxLayout()

        title = QLabel('Incidents Management')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet('color: #1F2937;')

        # Filters (UI only for now – you can wire them up later)
        filters_layout = QHBoxLayout()

        status_filter = QComboBox()
        status_filter.addItems(['All Status', 'Pending', 'Ongoing', 'Solved'])
        status_filter.setStyleSheet(
            'padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px;'
        )

        category_filter = QComboBox()
        # You can extend these categories later, they’re just labels here
        category_filter.addItems(
            ['All Categories', 'Medical', 'Fire', 'Police', 'Rescue']
        )
        category_filter.setStyleSheet(
            'padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px;'
        )

        search_input = QLineEdit()
        search_input.setPlaceholderText('Search incidents...')
        search_input.setStyleSheet(
            'padding: 8px; border: 1px solid #D1D5DB; '
            'border-radius: 6px; min-width: 250px;'
        )

        filters_layout.addWidget(QLabel('Status:'))
        filters_layout.addWidget(status_filter)
        filters_layout.addWidget(QLabel('Category:'))
        filters_layout.addWidget(category_filter)
        filters_layout.addWidget(search_input)

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addLayout(filters_layout)
        layout.addLayout(header_layout)

        # ---------------- Stats bar ----------------
        stats_layout = QHBoxLayout()

        stats_data = [
            ('Total', len(self.incidents), '#6B7280'),
            (
                'Pending',
                len([i for i in self.incidents if i.status == 'pending']),
                '#F59E0B',
            ),
            (
                'Ongoing',
                len([i for i in self.incidents if i.status == 'ongoing']),
                '#EAB308',
            ),
            (
                'Solved',
                len([i for i in self.incidents if i.status == 'solved']),
                '#10B981',
            ),
        ]

        for text, value, color in stats_data:
            stat_label = QLabel(f'{text}: {value}')
            stat_label.setStyleSheet(
                f'''
                background-color: {color};
                color: white;
                padding: 6px 12px;
                border-radius: 16px;
                font-size: 12px;
                font-weight: bold;
            '''
            )
            stats_layout.addWidget(stat_label)

        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # ---------------- Tabs by status ----------------
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(
            '''
            QTabWidget::pane {
                border: 1px solid #E5E7EB;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #F3F4F6;
                color: #6B7280;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }
            QTabBar::tab:selected {
                background-color: white;
                color: #3B82F6;
                border-bottom: 2px solid #3B82F6;
            }
            QTabBar::tab:hover {
                background-color: #E5E7EB;
            }
        '''
        )

        # Create tabs for each status
        self.create_incident_tab('All Incidents', self.incidents)
        self.create_incident_tab(
            'Pending',
            [i for i in self.incidents if i.status == 'pending'],
        )
        self.create_incident_tab(
            'Ongoing',
            [i for i in self.incidents if i.status == 'ongoing'],
        )
        self.create_incident_tab(
            'Solved',
            [i for i in self.incidents if i.status == 'solved'],
        )

        layout.addWidget(self.tabs)
        self.setLayout(layout)

    def create_incident_tab(self, status_name, incidents):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet('border: none; background: transparent;')

        incidents_widget = QWidget()
        incidents_layout = QVBoxLayout(incidents_widget)
        incidents_layout.setSpacing(12)

        if incidents:
            for incident in incidents:
                incident_card = self.create_incident_card(incident)
                incidents_layout.addWidget(incident_card)
        else:
            no_incidents = QLabel(f'No {status_name.lower()} incidents')
            no_incidents.setStyleSheet(
                'color: #6B7280; font-style: italic; padding: 40px;'
            )
            no_incidents.setAlignment(Qt.AlignCenter)
            incidents_layout.addWidget(no_incidents)

        incidents_layout.addStretch()
        scroll.setWidget(incidents_widget)
        layout.addWidget(scroll)

        self.tabs.addTab(tab, f'{status_name} ({len(incidents)})')

    # ---------------------------------------------------------------- cards
    def create_incident_card(self, incident):
        """
        Build one incident card using your Incident model fields.
        """
        card = QFrame()
        card.setStyleSheet(
            '''
            QFrame {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                border: 1px solid #E5E7EB;
            }
            QFrame:hover {
                border-color: #3B82F6;
                box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
            }
        '''
        )
        card_layout = QVBoxLayout(card)

        # ----- Header: title + status -----
        header_layout = QHBoxLayout()

        # Use incident type display name as the title
        title_text = get_incident_display_name(incident.type) or incident.type
        title = QLabel(title_text)
        title.setFont(QFont('Arial', 16, QFont.Bold))
        title.setStyleSheet('color: #1F2937;')

        status_color = {
            'pending': '#F59E0B',
            'ongoing': '#EAB308',
            'solved': '#22C55E',
        }.get(incident.status, '#6B7280')

        status = QLabel(incident.status.upper())
        status.setStyleSheet(
            f'''
            background-color: {status_color};
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 10px;
            font-weight: bold;
        '''
        )

        header_layout.addWidget(title)
        header_layout.addStretch()
        header_layout.addWidget(status)
        card_layout.addLayout(header_layout)

        # ----- Category + priority -----
        meta_layout = QHBoxLayout()

        category_text = incident.incident_category or "General"
        category = QLabel(f'📋 {category_text}')
        category.setStyleSheet('color: #6B7280; font-weight: bold;')

        priority_code = (getattr(incident, 'priority', '') or "").upper()
        priority_color = {
            'P1': '#DC2626',  # critical
            'P2': '#EF4444',
            'P3': '#F59E0B',
            'P4': '#10B981',
            'P5': '#6B7280',
        }.get(priority_code, '#6B7280')

        priority_label = priority_code if priority_code else "UNKNOWN"
        priority = QLabel(f'⚡ {priority_label}')
        priority.setStyleSheet(
            f'color: {priority_color}; font-weight: bold;'
        )

        meta_layout.addWidget(category)
        meta_layout.addWidget(priority)
        meta_layout.addStretch()
        card_layout.addLayout(meta_layout)

        # ----- Description -----
        description = QLabel(incident.description or "")
        description.setStyleSheet('color: #6B7280; margin: 8px 0;')
        description.setWordWrap(True)
        card_layout.addWidget(description)

        # ----- Details grid -----
        details_layout = QHBoxLayout()

        left_details = QVBoxLayout()
        left_details.addWidget(
            QLabel(f'📍 Location: {incident.location or "N/A"}')
        )

        right_details = QVBoxLayout()
        right_details.addWidget(
            QLabel(f'👤 Reporter: {incident.reporter_name or "N/A"}')
        )
        if incident.responder_name:
            right_details.addWidget(
                QLabel(f'🚑 Responder: {incident.responder_name}')
            )
        else:
            right_details.addWidget(
                QLabel('🚑 Responder: Not assigned')
            )

        details_layout.addLayout(left_details)
        details_layout.addLayout(right_details)
        card_layout.addLayout(details_layout)

        # ----- Timestamps -----
        time_layout = QHBoxLayout()
        created = (
            incident.created_at.strftime('%b %d, %Y %H:%M')
            if getattr(incident, "created_at", None)
            else 'N/A'
        )
        updated = (
            incident.updated_at.strftime('%b %d, %Y %H:%M')
            if getattr(incident, "updated_at", None)
            else 'N/A'
        )

        time_layout.addWidget(QLabel(f'🕒 Reported: {created}'))
        time_layout.addStretch()
        time_layout.addWidget(QLabel(f'📝 Updated: {updated}'))
        card_layout.addLayout(time_layout)

        # ----- Action buttons -----
        if incident.status != 'solved':
            actions_layout = QHBoxLayout()

            # For pending incidents, allow assigning a responder
            if incident.status == 'pending':
                assign_btn = QPushButton('Assign Responder')
                assign_btn.setStyleSheet(
                    '''
                    QPushButton {
                        background-color: #3B82F6;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 6px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2563EB;
                    }
                '''
                )
                # capture the incident in the lambda
                assign_btn.clicked.connect(
                    lambda _, inc=incident: self.assign_responder(inc)
                )
                actions_layout.addWidget(assign_btn)

            # View details button (simplified to show a dialog for now)
            view_btn = QPushButton('View Details')
            view_btn.setStyleSheet(
                '''
                QPushButton {
                    background-color: #6B7280;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 6px;
                }
                QPushButton:hover {
                    background-color: #4B5563;
                }
            '''
            )
            view_btn.clicked.connect(
                lambda _, inc=incident: self.view_incident_details(inc)
            )
            actions_layout.addWidget(view_btn)

            # For ongoing incidents, allow marking as solved
            if incident.status == 'ongoing':
                update_btn = QPushButton('Mark as Solved')
                update_btn.setStyleSheet(
                    '''
                    QPushButton {
                        background-color: #10B981;
                        color: white;
                        border: none;
                        padding: 8px 16px;
                        border-radius: 6px;
                    }
                    QPushButton:hover {
                        background-color: #059669;
                    }
                '''
                )
                update_btn.clicked.connect(
                    lambda _, inc=incident: self.mark_incident_solved(inc)
                )
                actions_layout.addWidget(update_btn)

            actions_layout.addStretch()
            card_layout.addLayout(actions_layout)

        return card

    # ---------------------------------------------------------------- logic
    def _find_available_responder(self, incident):
        """
        Simple logic to pick an available responder.
        You can later improve this (e.g., match category/location).
        """
        candidates = [
            u for u in self.users
            if u.role == 'responder' and u.status == 'available'
        ]
        if not candidates:
            return None
        # For now, just return the first candidate.
        return candidates[0]

    def assign_responder(self, incident):
        responder = self._find_available_responder(incident)
        if not responder:
            QMessageBox.warning(
                self, 'No Responders', 'No available responders found'
            )
            return

        # Update incident
        incident.responder_id = responder.id
        incident.responder_name = responder.name
        incident.status = 'ongoing'
        incident.updated_at = datetime.now()

        # Update responder
        responder.active_incidents += 1
        if responder.active_incidents > 0:
            responder.status = 'busy'

        # Persist changes
        self.db.update_incident(incident)
        self.db.update_user(responder)

        QMessageBox.information(
            self,
            'Success',
            f'Assigned {responder.name} to incident and marked as ongoing.',
        )

    def mark_incident_solved(self, incident):
        """
        Mark an incident as solved and free the responder if applicable.
        """
        incident.status = 'solved'
        incident.updated_at = datetime.now()

        # If there is a responder, decrement their active_incidents
        responder = None
        if getattr(incident, "responder_id", None):
            for u in self.users:
                if u.id == incident.responder_id:
                    responder = u
                    break

        if responder is not None:
            if responder.active_incidents > 0:
                responder.active_incidents -= 1
            if responder.active_incidents <= 0:
                responder.status = 'available'

            self.db.update_user(responder)

        self.db.update_incident(incident)
        QMessageBox.information(self, 'Success', 'Incident marked as solved.')

    def view_incident_details(self, incident):
        """
        Simple details dialog. You can replace this with a richer dialog later.
        """
        details = (
            f"Type: {get_incident_display_name(incident.type) or incident.type}\n"
            f"Category: {incident.incident_category or 'N/A'}\n"
            f"Priority: {incident.priority or 'N/A'}\n"
            f"Location: {incident.location or 'N/A'}\n"
            f"Reporter: {incident.reporter_name or 'N/A'}\n"
            f"Responder: {incident.responder_name or 'Not assigned'}\n\n"
            f"Description:\n{incident.description or ''}"
        )
        QMessageBox.information(self, "Incident Details", details)
