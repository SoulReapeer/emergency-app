# admin/admin_users.py
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QLineEdit,
    QMessageBox, QGridLayout, QComboBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import styles


class AdminUsers(QWidget):
    """
    Admin Users management screen.

    - Loads all users from the Database
    - Shows them as cards in a scrollable grid
    - Allows filtering by role and simple text search
    - Allows toggling user availability (status available/busy)
    """

    def __init__(self, db):
        super().__init__()
        self.db = db

        # Data
        self.all_users = []   # full list from DB
        self.filtered_users = []  # list after filters/search

        # UI references
        self.search_input = None
        self.role_filter = None
        self.users_container_layout = None

        self.init_ui()
        self.load_users()

    # -----------------------
    # UI SETUP
    # -----------------------
    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(16)

        # Header
        header_layout = QHBoxLayout()
        title = QLabel("User Management")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setStyleSheet("color: #1F2937;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        refresh_btn = QPushButton("Refresh")
        refresh_btn.setStyleSheet(styles.STYLES["button_style"])
        refresh_btn.clicked.connect(self.load_users)
        header_layout.addWidget(refresh_btn)

        main_layout.addLayout(header_layout)

        # Filters row
        filters_layout = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by name, email or username...")
        self.search_input.setStyleSheet(
            "padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; min-width: 220px;"
        )
        self.search_input.textChanged.connect(self.apply_filters)
        filters_layout.addWidget(self.search_input)

        self.role_filter = QComboBox()
        self.role_filter.addItems(["All Roles", "Reporter", "Responder", "Admin"])
        self.role_filter.currentIndexChanged.connect(self.apply_filters)
        self.role_filter.setStyleSheet(
            "padding: 8px; border: 1px solid #D1D5DB; border-radius: 6px; min-width: 140px;"
        )
        filters_layout.addWidget(self.role_filter)

        filters_layout.addStretch()
        main_layout.addLayout(filters_layout)

        # Card container inside scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("border: none;")

        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Grid layout for user cards
        self.users_container_layout = QGridLayout()
        self.users_container_layout.setSpacing(16)
        container_layout.addLayout(self.users_container_layout)
        container_layout.addStretch()

        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    # -----------------------
    # DATA LOADING & FILTERS
    # -----------------------
    def load_users(self):
        """Load all users from DB and apply filters."""
        self.all_users = self.db.get_all_users()
        self.apply_filters()

    def apply_filters(self):
        """Filter users based on search text and role, then rebuild UI."""
        text = (self.search_input.text() or "").strip().lower()
        role_selected = self.role_filter.currentText()

        def role_matches(user_role: str) -> bool:
            if role_selected == "All Roles":
                return True
            return user_role.lower() == role_selected.lower()

        filtered = []
        for u in self.all_users:
            if not role_matches(u.role):
                continue

            if text:
                haystack = f"{u.name} {u.email} {u.username}".lower()
                if text not in haystack:
                    continue

            filtered.append(u)

        self.filtered_users = filtered
        self._rebuild_user_cards()

    # -----------------------
    # UI BUILDING
    # -----------------------
    def _clear_layout(self, layout: QGridLayout):
        """Remove all widgets from the grid layout."""
        while layout.count():
            item = layout.takeAt(0)
            w = item.widget()
            if w is not None:
                w.deleteLater()

    def _rebuild_user_cards(self):
        """Rebuild the grid of user cards from filtered_users."""
        self._clear_layout(self.users_container_layout)

        if not self.filtered_users:
            # Show a simple "no users" label
            empty_label = QLabel("No users found.")
            empty_label.setAlignment(Qt.AlignCenter)
            empty_label.setStyleSheet("color: #6B7280; margin-top: 16px;")
            self.users_container_layout.addWidget(empty_label, 0, 0)
            return

        # Simple 2-column grid (adjust if you want more/less)
        columns = 2
        for idx, user in enumerate(self.filtered_users):
            row = idx // columns
            col = idx % columns
            card = self._create_user_card(user)
            self.users_container_layout.addWidget(card, row, col)

    def _create_user_card(self, user):
        """Create a single user card frame."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E5E7EB;
            }
            """
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(8)

        # Top row: name + role
        top_layout = QHBoxLayout()
        name_label = QLabel(user.name or "(No name)")
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        name_label.setStyleSheet("color: #111827;")
        top_layout.addWidget(name_label)

        role_label = QLabel(user.role.title())
        role_label.setStyleSheet(
            """
            QLabel {
                background-color: #E5E7EB;
                color: #374151;
                padding: 4px 8px;
                border-radius: 999px;
                font-size: 11px;
            }
            """
        )
        top_layout.addStretch()
        top_layout.addWidget(role_label)
        card_layout.addLayout(top_layout)

        # Email / username row
        email_label = QLabel(f"Email: {user.email}")
        email_label.setStyleSheet("color: #4B5563; font-size: 11px;")
        card_layout.addWidget(email_label)

        username_label = QLabel(f"Username: {user.username}")
        username_label.setStyleSheet("color: #4B5563; font-size: 11px;")
        card_layout.addWidget(username_label)

        # Phone row
        if getattr(user, "phone", ""):
            phone_label = QLabel(f"Phone: {user.phone}")
            phone_label.setStyleSheet("color: #4B5563; font-size: 11px;")
            card_layout.addWidget(phone_label)

        # Status row
        status_layout = QHBoxLayout()
        status_text = user.status or "unknown"

        status_label = QLabel(status_text.title())
        if status_text.lower() == "available":
            bg = styles.STYLES["success_color"]
        elif status_text.lower() == "busy":
            bg = styles.STYLES["warning_color"]
        else:
            bg = "#9CA3AF"

        status_label.setStyleSheet(
            f"""
            QLabel {{
                background-color: {bg};
                color: white;
                padding: 4px 10px;
                border-radius: 999px;
                font-size: 11px;
            }}
            """
        )
        status_layout.addWidget(QLabel("Status:"))
        status_layout.addWidget(status_label)
        status_layout.addStretch()
        card_layout.addLayout(status_layout)

        # Actions row
        actions_layout = QHBoxLayout()

        toggle_btn = QPushButton("Toggle Availability")
        toggle_btn.setStyleSheet(styles.STYLES["button_style"])
        toggle_btn.clicked.connect(lambda _, u=user: self.toggle_user_status(u))
        actions_layout.addWidget(toggle_btn)

        # Placeholder for future actions
        # reset_btn = QPushButton("Reset Password")
        # reset_btn.setStyleSheet(styles.STYLES["danger_button_style"])
        # reset_btn.clicked.connect(lambda _, u=user: self.reset_password(u))
        # actions_layout.addWidget(reset_btn)

        actions_layout.addStretch()
        card_layout.addLayout(actions_layout)

        return card

    # -----------------------
    # ACTIONS
    # -----------------------
    def toggle_user_status(self, user):
        """
        Toggle between 'available' and 'busy' for this user
        and persist to DB via update_user.
        """
        current = (user.status or "").lower()
        if current == "available":
            new_status = "busy"
        else:
            new_status = "available"

        user.status = new_status
        self.db.update_user(user)
        QMessageBox.information(
            self,
            "Status Updated",
            f"{user.name}'s status changed to {new_status.title()}."
        )
        # Reload data to refresh cards
        self.load_users()

    # You can add more admin actions here later, e.g.:
    #
    # def reset_password(self, user):
    #     ...
    #     self.db.update_user(user)
    #     QMessageBox.information(self, "Success", "Password reset.")
