# styles.py

# ─────────────────────────────────────────────
#  LIGHT THEME
# ─────────────────────────────────────────────
LIGHT_STYLES = {
    'is_dark': False,

    # Colors
    'primary_color':   '#2c3e50',
    'secondary_color': '#34495e',
    'accent_color':    '#3498db',
    'success_color':   '#27ae60',
    'warning_color':   '#f39c12',
    'danger_color':    '#e74c3c',
    'light_color':     '#ecf0f1',
    'dark_color':      '#2c3e50',

    # Page / content background
    'bg_main':    '#f8f9fa',
    'bg_card':    '#ffffff',
    'bg_input':   '#f4f6f7',
    'border':     '#bdc3c7',
    'text_main':  '#1F2937',
    'text_muted': '#7f8c8d',

    # Sidebar
    'sidebar_bg':      '#2c3e50',
    'sidebar_header':  '#34495e',
    'sidebar_hover':   '#34495e',
    'sidebar_border':  '#3498db',

    # Feedback / info box
    'feedback_bg': '#fff3cd',

    'button_style': """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #2980b9; }
        QPushButton:pressed { background-color: #21618c; }
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
        QPushButton:hover { background-color: #c0392b; }
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
        QPushButton:hover { background-color: #219a52; }
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
        QPushButton:hover { background-color: #34495e; }
        QPushButton:pressed { background-color: #2980b9; }
    """,

    'status_pending': "background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;",
    'status_ongoing': "background-color: #3498db; color: white; padding: 4px 8px; border-radius: 4px;",
    'status_solved':  "background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;",

    'severity_low':    "background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;",
    'severity_medium': "background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;",
    'severity_high':   "background-color: #e74c3c; color: white; padding: 4px 8px; border-radius: 4px;",
}

# ─────────────────────────────────────────────
#  DARK THEME  (base: #1a1a1a)
# ─────────────────────────────────────────────
DARK_STYLES = {
    'is_dark': True,

    # Colors
    'primary_color':   '#1a1a1a',
    'secondary_color': '#2a2a2a',
    'accent_color':    '#3498db',
    'success_color':   '#27ae60',
    'warning_color':   '#f39c12',
    'danger_color':    '#e74c3c',
    'light_color':     '#2e2e2e',
    'dark_color':      '#1a1a1a',

    # Page / content background
    'bg_main':    '#1a1a1a',
    'bg_card':    '#252525',
    'bg_input':   '#2e2e2e',
    'border':     '#3a3a3a',
    'text_main':  '#e0e0e0',
    'text_muted': '#9ca3af',

    # Sidebar (slightly lighter than page so it stands out)
    'sidebar_bg':     '#111111',
    'sidebar_header': '#1e1e1e',
    'sidebar_hover':  '#2a2a2a',
    'sidebar_border': '#3498db',

    # Feedback / info box
    'feedback_bg': '#2e2a1a',

    'button_style': """
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 8px 16px;
            border-radius: 4px;
            font-weight: bold;
        }
        QPushButton:hover { background-color: #2980b9; }
        QPushButton:pressed { background-color: #21618c; }
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
        QPushButton:hover { background-color: #c0392b; }
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
        QPushButton:hover { background-color: #219a52; }
    """,

    'card_style': """
        QFrame {
            background-color: #252525;
            border: 1px solid #3a3a3a;
            border-radius: 8px;
            padding: 16px;
        }
    """,

    'sidebar_style': """
        QFrame {
            background-color: #111111;
            color: #e0e0e0;
        }
        QPushButton {
            background-color: transparent;
            color: #e0e0e0;
            border: none;
            padding: 12px 16px;
            text-align: left;
            border-radius: 4px;
        }
        QPushButton:hover { background-color: #2a2a2a; }
        QPushButton:pressed { background-color: #2980b9; }
    """,

    'status_pending': "background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;",
    'status_ongoing': "background-color: #3498db; color: white; padding: 4px 8px; border-radius: 4px;",
    'status_solved':  "background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;",

    'severity_low':    "background-color: #27ae60; color: white; padding: 4px 8px; border-radius: 4px;",
    'severity_medium': "background-color: #f39c12; color: white; padding: 4px 8px; border-radius: 4px;",
    'severity_high':   "background-color: #e74c3c; color: white; padding: 4px 8px; border-radius: 4px;",
}


# ─────────────────────────────────────────────
#  ThemeManager  — single global instance
#  Import this everywhere instead of STYLES
# ─────────────────────────────────────────────
class ThemeManager:
    def __init__(self):
        self._dark = False
        self._listeners = []        # callbacks registered by windows

    @property
    def STYLES(self):
        return DARK_STYLES if self._dark else LIGHT_STYLES

    @property
    def is_dark(self):
        return self._dark

    def toggle(self):
        self._dark = not self._dark
        for cb in self._listeners:
            try:
                cb()
            except Exception:
                pass

    def register(self, callback):
        """Windows call this so they get notified on toggle."""
        if callback not in self._listeners:
            self._listeners.append(callback)

    def unregister(self, callback):
        if callback in self._listeners:
            self._listeners.remove(callback)


# The one global instance every file imports
theme = ThemeManager()

# Keep STYLES as a convenience alias so old code still works
# (it always points to the current theme's dict)
STYLES = LIGHT_STYLES   # legacy alias — prefer theme.STYLES in new code
