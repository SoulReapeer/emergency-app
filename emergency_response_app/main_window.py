#main_window.py
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QMessageBox,
    QLabel, QPushButton, QFrame, QStackedWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from reporter.reporter_dashboard import ReporterDashboard
from responder.responder_dashboard import ResponderDashboard
from admin.admin_dashboard import AdminDashboard
from admin.admin_incidents import AdminIncidents
from admin.admin_users import AdminUsers
from profile import Profile
from reporter.reporter_incident_page import ReporterNewIncidentPage
from reporter.reporter_history_page import ReporterHistoryPage
from responder.responder_assignments_page import ResponderAssignmentsPage
from responder.responder_available_page import ResponderAvailablePage
from admin.admin_analytics import AdminAnalytics
import styles


class MainWindow(QMainWindow):
    logout_signal = pyqtSignal()

    def __init__(self, user, db):
        super().__init__()
        self.user = user
        self.db = db

        # Views
        self.dashboard = None
        self.profile_view = None
        self.admin_incidents_view = None
        self.admin_users_view = None
        self.reporter_new_incident_view = None
        self.reporter_history_view = None
        self.responder_assignments_view = None
        self.responder_available_view = None
        self.admin_analytics_view = None
        self.init_ui()

    # ---------------------------------------------------------------
    def init_ui(self):
        self.setWindowTitle(f"Emergency Response System - {self.user.name}")
        self.setGeometry(100, 100, 1400, 900)
        self.showMaximized()

        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #f8f9fa;")
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        central_widget.setLayout(main_layout)

        # Sidebar on the left
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Main stacked content area on the right
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet(
            """
            QStackedWidget {
                background-color: #f8f9fa;
                border: none;
            }
            """
        )
        main_layout.addWidget(self.content_area, 1)

        # Setup role-specific dashboard and pages
        self.setup_dashboard()

    # ---------------------------------------------------------------
    def create_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setStyleSheet(
            """
            QFrame {
                background-color: #2c3e50;
                color: white;
                border: none;
            }
            """
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ---------- User header area ----------
        user_section = QFrame()
        user_section.setStyleSheet(
            """
            QFrame {
                background-color: #34495e;
                border-bottom: 2px solid #3498db;
            }
            """
        )
        user_layout = QVBoxLayout()
        user_layout.setContentsMargins(20, 30, 20, 30)

        avatar_label = QLabel("👤")
        avatar_label.setAlignment(Qt.AlignCenter)
        avatar_label.setStyleSheet("font-size: 40px; margin-bottom: 10px;")

        user_name = QLabel(self.user.name)
        user_name.setAlignment(Qt.AlignCenter)
        user_name.setFont(QFont("Arial", 14, QFont.Bold))
        user_name.setStyleSheet("color: white; margin-bottom: 5px;")

        user_role = QLabel(self.user.role.title())
        user_role.setAlignment(Qt.AlignCenter)
        user_role.setFont(QFont("Arial", 11))
        user_role.setStyleSheet("color: #bdc3c7;")

        user_layout.addWidget(avatar_label)
        user_layout.addWidget(user_name)
        user_layout.addWidget(user_role)
        user_section.setLayout(user_layout)
        layout.addWidget(user_section)

        # ---------- Navigation buttons ----------
        nav_buttons = self.create_nav_buttons()
        for btn in nav_buttons:
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: transparent;
                    color: white;
                    border: none;
                    padding: 16px 22px;
                    text-align: left;
                    border-radius: 0px;
                    font-size: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #34495e;
                    border-left: 4px solid #3498db;
                }
                """
            )
            layout.addWidget(btn)

        layout.addStretch()

        # ---------- Profile button ----------
        profile_btn = QPushButton("🙍 My Profile")
        profile_btn.setProperty("view", "profile")
        profile_btn.setCursor(Qt.PointingHandCursor)
        profile_btn.clicked.connect(self.handle_navigation)
        profile_btn.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;
                border: none;
                padding: 15px 20px;
                text-align: left;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #34495e;
                border-left: 4px solid #3498db;
            }
            """
        )
        layout.addWidget(profile_btn)

        # ---------- Logout button ----------
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 15px;
                text-align: center;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            """
        )
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)

        sidebar.setLayout(layout)
        return sidebar

    # ---------------------------------------------------------------
    def create_nav_buttons(self):
        buttons = []

        if self.user.role == "reporter":
            nav_items = [
                ("📊 Dashboard", "dashboard"),
                ("🚨 Report Incident", "new_incident"),
                ("📋 My History", "history"),
            ]

        elif self.user.role == "responder":
            nav_items = [
                ("📊 Dashboard", "dashboard"),
                ("✅ My Assignments", "assignments"),
                ("🔔 Available Incidents", "available"),
            ]

        else:  # admin
            nav_items = [
                ("📊 Dashboard", "dashboard"),
                ("🚨 Incidents", "incidents"),
                ("👥 Users", "users"),
                ("📈 Analytics", "analytics"),
            ]

        for text, view in nav_items:
            btn = QPushButton(text)
            btn.setProperty("view", view)
            btn.clicked.connect(self.handle_navigation)
            btn.setCursor(Qt.PointingHandCursor)
            buttons.append(btn)

        return buttons

    # ---------------------------------------------------------------
    def setup_dashboard(self):
        if self.user.role == "reporter":
            self.dashboard = ReporterDashboard(self.user, self.db)

            # 👇 Report Incident full-page
            self.reporter_new_incident_view = ReporterNewIncidentPage(self.user, self.db)
            self.content_area.addWidget(self.reporter_new_incident_view)

            # 👇 My History page
            self.reporter_history_view = ReporterHistoryPage(self.user, self.db)
            self.content_area.addWidget(self.reporter_history_view)

        elif self.user.role == "responder":
            self.dashboard = ResponderDashboard(self.user, self.db)

            # 👇 My Assignments page
            self.responder_assignments_view = ResponderAssignmentsPage(self.user, self.db)
            self.content_area.addWidget(self.responder_assignments_view)

            # 👇 Available Incidents page
            self.responder_available_view = ResponderAvailablePage(self.user, self.db)
            self.content_area.addWidget(self.responder_available_view)

        else:  # admin
            self.dashboard = AdminDashboard(self.user, self.db)

            incidents = self.db.get_all_incidents()
            users = self.db.get_all_users()
            self.admin_incidents_view = AdminIncidents(incidents, users, self.db)
            self.content_area.addWidget(self.admin_incidents_view)

            # 🔧 FIX: AdminUsers ekhon ekta argument (db) niye call hocche
            self.admin_users_view = AdminUsers(self.db)
            self.content_area.addWidget(self.admin_users_view)

            # 👇 Analytics placeholder page
            self.admin_analytics_view = AdminAnalytics(self.db)
            self.content_area.addWidget(self.admin_analytics_view)

        # dashboard + profile same thakbe
        self.content_area.addWidget(self.dashboard)
        self.profile_view = Profile(self.user, self.db)
        self.content_area.addWidget(self.profile_view)
        self.content_area.setCurrentWidget(self.dashboard)

    # ---------------------------------------------------------------
    def refresh_data(self):
        """Refresh admin incident/user data (called from admin views)."""
        if self.user.role != "admin":
            return

        incidents = self.db.get_all_incidents()
        users = self.db.get_all_users()

        current = self.content_area.currentWidget()

        # Rebuild admin incidents view
        if self.admin_incidents_view is not None:
            is_current = current is self.admin_incidents_view
            self.content_area.removeWidget(self.admin_incidents_view)
            self.admin_incidents_view.deleteLater()
            self.admin_incidents_view = AdminIncidents(incidents, users, self.db)
            self.content_area.addWidget(self.admin_incidents_view)
            if is_current:
                self.content_area.setCurrentWidget(self.admin_incidents_view)

        # Rebuild admin users view
        if self.admin_users_view is not None:
            is_current = current is self.admin_users_view
            self.content_area.removeWidget(self.admin_users_view)
            self.admin_users_view.deleteLater()
            self.admin_users_view = AdminUsers(self.db)
            self.content_area.addWidget(self.admin_users_view)
            if is_current:
                self.content_area.setCurrentWidget(self.admin_users_view)

    def handle_navigation(self):
        sender = self.sender()
        view = sender.property("view")

        # Reset styles only for nav/profile buttons (those that have 'view')
        for btn in self.sidebar.findChildren(QPushButton):
            if btn.property("view") is not None:
                btn.setStyleSheet(
                    """
                    QPushButton {
                        background-color: transparent;
                        color: white;
                        border: none;
                        padding: 15px 20px;
                        text-align: left;
                        border-radius: 0px;
                        font-size: 14px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #34495e;
                        border-left: 4px solid #3498db;
                    }
                    """
                )

        # Highlight active button (again, only nav/profile)
        sender.setStyleSheet(
            """
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 15px 20px;
                text-align: left;
                border-radius: 0px;
                font-size: 14px;
                font-weight: bold;
                border-left: 4px solid #2980b9;
            }
            """
        )

        # Handle different views
        if view == "dashboard":
            self.content_area.setCurrentWidget(self.dashboard)

        elif view == "profile":
            self.content_area.setCurrentWidget(self.profile_view)

        # Admin-only pages
        elif view == "incidents" and self.user.role == "admin":
            if self.admin_incidents_view is not None:
                self.content_area.setCurrentWidget(self.admin_incidents_view)

        elif view == "users" and self.user.role == "admin":
            if self.admin_users_view is not None:
                self.content_area.setCurrentWidget(self.admin_users_view)

        elif view == "analytics" and self.user.role == "admin":
            if self.admin_analytics_view is not None:
                self.content_area.setCurrentWidget(self.admin_analytics_view)

        # Reporter pages
        elif view == "new_incident" and self.user.role == "reporter":
            if self.reporter_new_incident_view is not None:
                self.content_area.setCurrentWidget(self.reporter_new_incident_view)

        elif view == "history" and self.user.role == "reporter":
            if self.reporter_history_view is not None:
                self.content_area.setCurrentWidget(self.reporter_history_view)

        # Responder pages
        elif view == "assignments" and self.user.role == "responder":
            if self.responder_assignments_view is not None:
                self.content_area.setCurrentWidget(self.responder_assignments_view)

        elif view == "available" and self.user.role == "responder":
            if self.responder_available_view is not None:
                self.content_area.setCurrentWidget(self.responder_available_view)

    def handle_logout(self):
        reply = QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to logout?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            self.logout_signal.emit()
            self.close()
