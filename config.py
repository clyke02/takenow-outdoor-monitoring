"""
Configuration file untuk Dashboard Kelayakan Alat
"""
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "dataset"

# Data files
KATALOG_FILE = DATA_DIR / "katalog_barang.xlsx"
RIWAYAT_PENYEWAAN_FILE = DATA_DIR / "riwayat_penyewaan.csv"
RIWAYAT_MAINTENANCE_FILE = DATA_DIR / "riwayat_maintenance.csv"
INSIGHT_FILE = DATA_DIR / "insight_kelayakan_alat.csv"

# Streamlit config
PAGE_TITLE = "Dashboard Kelayakan Alat Camping"
PAGE_ICON = "⛺"
LAYOUT = "wide"

# Chart colors
COLORS = {
    'primary': '#1f77b4',
    'success': '#2ecc71',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#3498db',
    'secondary': '#95a5a6'
}

# Status colors
STATUS_COLORS = {
    'KONDISI SANGAT BAIK': COLORS['success'],
    'LAYAK OPERASIONAL': COLORS['info'],
    'TINGKATKAN PEMELIHARAAN': COLORS['warning'],
    'PERLU PERHATIAN KHUSUS': COLORS['danger']
}

# Severity colors
SEVERITY_COLORS = {
    'Ringan': COLORS['info'],
    'Sedang': COLORS['warning'],
    'Berat': COLORS['danger']
}

# Condition colors
CONDITION_COLORS = {
    'Baik': COLORS['success'],
    'Perlu Perhatian': COLORS['warning'],
    'Kurang Baik': COLORS['danger']
}

# Dashboard settings
CACHE_TTL = 3600  # Cache duration in seconds (1 hour)
MAX_ROWS_DISPLAY = 15  # Maximum rows to display in tables (reduced for performance)
CHART_HEIGHT_DEFAULT = 400  # Default chart height
ENABLE_PROFILER = False  # Set to True to debug performance

# Authentication settings
# Multi-user with role-based access control
USERS = {
    "owner": {
        "password": "owner123",
        "display_name": "Admin Owner",
        "role": "owner",
        "description": "Full access to Executive and Planning"
    },
    "operational": {
        "password": "ops123",
        "display_name": "Admin Operational",
        "role": "operational",
        "description": "Access to Operational only"
    }
}

# Role-based menu access
ROLE_PERMISSIONS = {
    "owner": {
        "executive": True,
        "operational": False,
        "planning": True
    },
    "operational": {
        "executive": False,
        "operational": True,
        "planning": False
    }
}
