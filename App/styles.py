STYLES = {
    'primary_color': '#2c3e50',
    'secondary_color': '#34495e',
    'accent_color': '#3498db',
    'success_color': '#27ae60',
    'warning_color': '#f39c12',
    'danger_color': '#e74c3c',
    'light_color': '#ecf0f1',
    'dark_color': '#2c3e50',
    
    'button_style': """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #21618c;
        }
    """,
    
    'danger_button_style': """
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }
    """,
    
    'success_button_style': """
        QPushButton {
            background-color: #27ae60;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #219a52;
        }
    """,
    
    'card_style': """
        QFrame {
            background-color: white;
            border: 1px solid #bdc3c7;
            border-radius: 8px;
            padding: 16px;
        }
    """,
    
    'sidebar_style': """
        QFrame {
            background-color: #2c3e50;
            color: white;
        }
        QPushButton {
            background-color: transparent;
            color: white;
            border: none;
            padding: 12px 16px;
            text-align: left;
            border-radius: 4px;
        }
        QPushButton:hover {
            background-color: #34495e;
        }
        QPushButton:pressed {
            background-color: #2980b9;
        }
    """,
    
    'status_pending': "background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;",
    'status_ongoing': "background-color: #3498db; color: white; padding: 4px 8px; border-radius: 4px;",
    'status_solved': "background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;",
    
    'severity_low': "background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;",
    'severity_medium': "background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;",
    'severity_high': "background-color: #e74c3c; color: white; padding: 4px 8px; border-radius: 4px;"
}