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
from admin.user_dossier import UserDossier
from admin.case_file import CaseFile
import styles
from styles import theme


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
        self.user_dossier_view = None
        self.case_file_view = None
        self.init_ui()

    # ---------------------------------------------------------------
    def init_ui(self):
        self.setWindowTitle(f"Emergency Response System - {self.user.name}")
        self.setGeometry(100, 100, 1400, 900)
        self.showMaximized()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        self.central_widget.setLayout(main_layout)

        # Sidebar on the left
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)

        # Main stacked content area on the right
        self.content_area = QStackedWidget()
        main_layout.addWidget(self.content_area, 1)

        # Setup role-specific dashboard and pages
        self.setup_dashboard()

        # Register for theme changes and apply initial theme
        theme.register(self.apply_theme)
        self.apply_theme()

    def apply_theme(self):
        """Repaint the main window shell when theme changes."""
        s = theme.STYLES
        bg = s['bg_main']
        self.central_widget.setStyleSheet(f"background-color: {bg};")
        self.content_area.setStyleSheet(
            f"QStackedWidget {{ background-color: {bg}; border: none; }}"
        )

        sidebar_bg   = s['sidebar_bg']
        sidebar_hdr  = s['sidebar_header']
        sidebar_hvr  = s['sidebar_hover']
        sidebar_bdr  = s['sidebar_border']
        text_color   = '#ffffff' if s['is_dark'] else '#ffffff'

        self.sidebar.setStyleSheet(
            f"QFrame {{ background-color: {sidebar_bg}; color: {text_color}; border: none; }}"
        )
        self._sidebar_user_section.setStyleSheet(
            f"QFrame {{ background-color: {sidebar_hdr}; border-bottom: 2px solid {sidebar_bdr}; }}"
        )

        # Update theme toggle button label
        self._theme_btn.setText("☀️  Light Mode" if s['is_dark'] else "🌙  Dark Mode")
        self._theme_btn.setStyleSheet(self._theme_btn_style(s['is_dark']))

        # Refresh nav button styles
        for btn in self.sidebar.findChildren(QPushButton):
            if btn.property("nav_btn") and not btn.property("is_logout") and not btn.property("is_theme"):
                btn.setStyleSheet(self._nav_btn_style(sidebar_hvr))

    def _nav_btn_style(self, hover_color):
        return f"""
            QPushButton {{
                background-color: transparent;
                color: white;
                border: none;
                padding: 16px 22px;
                text-align: left;
                border-radius: 0px;
                font-size: 15px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {hover_color};
                border-left: 4px solid #3498db;
            }}
        """

    def _theme_btn_style(self, is_dark):
        return """
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
                background-color: #3498db;
                border-left: 4px solid #2980b9;
            }
        """

    # ---------------------------------------------------------------
    def create_sidebar(self) -> QFrame:
        sidebar = QFrame()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ---------- User header area ----------
        self._sidebar_user_section = QFrame()
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
        self._sidebar_user_section.setLayout(user_layout)
        layout.addWidget(self._sidebar_user_section)

        # ---------- Navigation buttons ----------
        nav_buttons = self.create_nav_buttons()
        for btn in nav_buttons:
            btn.setProperty("nav_btn", True)
            layout.addWidget(btn)

        layout.addStretch()

        # ---------- Dark / Light toggle ----------
        self._theme_btn = QPushButton("🌙  Dark Mode")
        self._theme_btn.setProperty("is_theme", True)
        self._theme_btn.setCursor(Qt.PointingHandCursor)
        self._theme_btn.clicked.connect(self._on_theme_toggle)
        layout.addWidget(self._theme_btn)

        # ---------- Profile button ----------
        profile_btn = QPushButton("🙍 My Profile")
        profile_btn.setProperty("view", "profile")
        profile_btn.setProperty("nav_btn", True)
        profile_btn.setCursor(Qt.PointingHandCursor)
        profile_btn.clicked.connect(self.handle_navigation)
        layout.addWidget(profile_btn)

        # ---------- Logout button ----------
        logout_btn = QPushButton("🚪 Logout")
        logout_btn.setProperty("is_logout", True)
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
            QPushButton:hover { background-color: #c0392b; }
            """
        )
        logout_btn.clicked.connect(self.handle_logout)
        layout.addWidget(logout_btn)

        sidebar.setLayout(layout)
        return sidebar

    def _on_theme_toggle(self):
        theme.toggle()

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

            # FIX: AdminUsers ekhon ekta argument (db) niye call hocche
            self.admin_users_view = AdminUsers(self.db)
            self.content_area.addWidget(self.admin_users_view)

            # Analytics
            self.admin_analytics_view = AdminAnalytics(self.db)
            self.content_area.addWidget(self.admin_analytics_view)

            # User Dossier & Case File — added on demand, placeholders for now
            # (actual widgets created in open_user_dossier / open_case_file)

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

        # Reset all nav buttons to default style
        hover = theme.STYLES['sidebar_hover']
        for btn in self.sidebar.findChildren(QPushButton):
            if btn.property("nav_btn"):
                btn.setStyleSheet(self._nav_btn_style(hover))

        # Highlight the active button
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

    def open_user_dossier(self, user):
        """Create (or replace) the UserDossier page and show it."""
        if self.user_dossier_view is not None:
            self.content_area.removeWidget(self.user_dossier_view)
            self.user_dossier_view.deleteLater()

        self.user_dossier_view = UserDossier(user, self.db)
        self.user_dossier_view.open_case.connect(self.open_case_file)
        self.content_area.addWidget(self.user_dossier_view)
        self.content_area.setCurrentWidget(self.user_dossier_view)

    def open_case_file(self, incident_id):
        """Create (or replace) the CaseFile page and show it."""
        incident = self.db.get_incident_by_id(incident_id)
        if not incident:
            return

        if self.case_file_view is not None:
            self.content_area.removeWidget(self.case_file_view)
            self.case_file_view.deleteLater()

        self.case_file_view = CaseFile(incident, self.db)
        self.case_file_view.closed.connect(self._on_case_file_closed)
        self.content_area.addWidget(self.case_file_view)
        self.content_area.setCurrentWidget(self.case_file_view)

    def _on_case_file_closed(self):
        """Return to the user dossier if it exists, otherwise to the users list."""
        if self.user_dossier_view is not None:
            self.content_area.setCurrentWidget(self.user_dossier_view)
        elif self.admin_users_view is not None:
            self.content_area.setCurrentWidget(self.admin_users_view)

    def handle_navigation_by_view(self, view_name):
        """Used by sub-pages (e.g. UserDossier back button) to navigate."""
        if view_name == "users" and self.admin_users_view is not None:
            self.content_area.setCurrentWidget(self.admin_users_view)

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
