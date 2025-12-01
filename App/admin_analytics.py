# admin_analytics.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class AdminAnalytics(QWidget):
    """Simple placeholder page: 'coming - future work'."""

    def __init__(self, db):
        super().__init__()
        self.db = db
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("Analytics")
        title.setFont(QFont("Arial", 22, QFont.Bold))
        title.setStyleSheet("color: #1F2937; margin-bottom: 10px;")

        subtitle = QLabel("Coming – future work")
        subtitle.setFont(QFont("Arial", 14))
        subtitle.setStyleSheet("color: #6B7280;")

        layout.addWidget(title)
        layout.addWidget(subtitle)
        self.setLayout(layout)
