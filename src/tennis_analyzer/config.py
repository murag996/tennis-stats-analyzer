"""
Configurazione centralizzata e costanti del progetto Tennis Stats Analyzer
"""
import logging
from pathlib import Path
from datetime import datetime

# Percorsi base
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = PROJECT_ROOT / "output"
VISUALS_DIR = OUTPUT_DIR / "visuals"

# Creare directory se non esistono
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
VISUALS_DIR.mkdir(parents=True, exist_ok=True)

# URL Dataset
GITHUB_SACKMANN_URL = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master"
MATCHES_FILE_URL = f"{GITHUB_SACKMANN_URL}/atp_matches_2015.csv"

# Parametri di analisi
ANALYSIS_YEARS = range(2015, 2026)  # Ultimi 10+ anni
MIN_MATCHES_PLAYER = 20  # Minimo match per inclusione analisi

# Logging
LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Colori per visualizzazioni
COLORS_PALETTE = {
    "primary": "#0066cc",
    "secondary": "#ff6600",
    "success": "#00cc66",
    "danger": "#ff3333",
    "neutral": "#333333",
}

# Output files
CLEAN_DATA_CSV = OUTPUT_DIR / "clean_data.csv"
RANKING_EVOLUTION_PNG = VISUALS_DIR / "01_top_atp_days.png"
WINS_BY_PLAYER_PNG = VISUALS_DIR / "02_total_wins.png"
WINS_BY_SURFACE_PNG = VISUALS_DIR / "03_wins_by_surface.png"
MATCH_DISTRIBUTION_PNG = VISUALS_DIR / "04_matches_distribution.png"
WIN_RATE_ANALYSIS_PNG = VISUALS_DIR / "05_win_rate_analysis.png"

# Feature engineering
SURFACE_TYPES = ["Hard", "Clay", "Grass", "Carpet"]

# Configurazione output directory
OUTPUT_FILES = {
    "clean_data": CLEAN_DATA_CSV,
    "visuals": [
        RANKING_EVOLUTION_PNG,
        WINS_BY_PLAYER_PNG,
        WINS_BY_SURFACE_PNG,
        MATCH_DISTRIBUTION_PNG,
        WIN_RATE_ANALYSIS_PNG,
    ]
}

if __name__ == "__main__":
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
