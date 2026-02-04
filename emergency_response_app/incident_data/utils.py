# incident_data/utils.py

from datetime import datetime
import re
import uuid
from .categories import incident_categories
from .display_names import incident_display_names

# ======================
# TIME UTILITIES
# ======================

def get_timestamp():
    """
    Returns current timestamp in readable format
    Example: 2026-01-15 20:45:12
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_file_timestamp():
    """
    Returns timestamp safe for filenames
    Example: 2026-01-15_20-45-12
    """
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


# ======================
# ID GENERATION
# ======================

def generate_case_id(prefix="CASE"):
    """
    Generates unique case ID
    Example: CASE-20260115-8F3A2C
    """
    short_uuid = uuid.uuid4().hex[:6].upper()
    date_part = datetime.now().strftime("%Y%m%d")
    return f"{prefix}-{date_part}-{short_uuid}"


# ======================
# INPUT SANITIZATION
# ======================

def clean_text(text):
    """
    Strips spaces and normalizes text
    """
    if not text:
        return ""
    return str(text).strip()


def normalize_yes_no(value):
    """
    Converts yes/no variations into True/False
    """
    if not value:
        return None

    value = value.strip().lower()

    if value in ("yes", "y", "true", "1"):
        return True
    if value in ("no", "n", "false", "0"):
        return False

    return None


def safe_lower(text):
    """
    Lowercase + snake_case safety
    """
    text = clean_text(text).lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^a-z0-9_]", "", text)
    return text


# ======================
# LOGGING HELPERS
# ======================

def format_log_entry(case_id, incident_type, priority, message):
    """
    Creates consistent log entry format
    """
    timestamp = get_timestamp()
    return (
        f"[{timestamp}] "
        f"[{case_id}] "
        f"[{priority}] "
        f"[{incident_type}] "
        f"{message}"
    )


def get_incident_category(incident_type):
    """Get the category for a specific incident type"""
    for category, types in incident_categories.items():
        if incident_type in types:
            return category
    return "other"


def get_incident_display_name(incident_type):
    """Get the display name for an incident type"""
    return incident_display_names.get(incident_type, incident_type.replace('_', ' ').title())
