#!/usr/bin/env python3
"""
QUICK REFERENCE & CHEAT SHEET
Tennis Stats Analyzer - Comandi e snippets utili
"""

# ================================================================
# SETUP INIZIALE (Prima volta)
# ================================================================
"""
# 1. Installare Python 3.13 (se non presente)
$ python3 --version  # Verificare versione

# 2. Clonare/Setup repo
$ cd tennis-stats-analyzer

# 3. Installare UV (package manager Rust-based)
# Opzione A: Globale
$ curl -LsSf https://astral.sh/uv/install.sh | sh

# Opzione B: Via pip (se ha Python)
$ pip install uv

# 4. Sincronizzare dipendenze (crea .venv)
$ uv sync --python 3.13

# 5. Attivare environment
$ source .venv/bin/activate  # macOS/Linux
$ .venv\\Scripts\\activate    # Windows

# 6. Eseguire
$ python main.py
"""

# ================================================================
# COMANDI COMUNI
# ================================================================
"""
# Run principale (scarica + clean + analizza + visualizza)
$ python main.py

# Run con output verboso
$ python main.py 2>&1 | tee output/run.log

# Run esempi
$ python examples.py

# Aggiungere dipendenza
$ uv pip install matplotlib-venn

# Check dipendenze
$ uv pip list

# Update dipendenze
$ uv sync --upgrade

# Eseguire specifico test
$ pytest tests/ -v
"""

# ================================================================
# IMPORT SNIPPETS
# ================================================================

# ✅ Uso Semplice
from src.tennis_analyzer import download_atp_data, clean_atp_data

df = download_atp_data()
df_clean = clean_atp_data(df)


# ✅ Uso Avanzato - Download anno specifico
from src.tennis_analyzer.downloader import ATPDataDownloader

downloader = ATPDataDownloader()
df_2024 = downloader.download_matches_year(2024)


# ✅ Analisi Custom
from src.tennis_analyzer.analyzer import ATPAnalyzer

analyzer = ATPAnalyzer(df_clean)

# Analisi specifiche
top_atp = analyzer.analyze_top_atp_days(top_n=20)
top_wins = analyzer.analyze_total_wins(top_n=30)
surface_stats = analyzer.analyze_surface_performance(top_n=15)
tournaments = analyzer.analyze_tournament_levels()
dominators = analyzer.get_era_dominators()


# ✅ Visualizzazioni Custom
from src.tennis_analyzer.visualizer import ATPVisualizer

visualizer = ATPVisualizer()
visualizer.plot_total_wins(top_wins, filename="custom_wins.png")


# ✅ Logging
from src.tennis_analyzer.logger import setup_logger

logger = setup_logger(__name__)
logger.info("Custom message")


# ✅ Config
from src.tennis_analyzer import config

print(config.OUTPUT_DIR)           # output/
print(config.ANALYSIS_YEARS)       # range(2015, 2026)
print(config.SURFACE_TYPES)        # ['Hard', 'Clay', 'Grass', 'Carpet']
"""

# ================================================================
# ANALISI DATI QUICK SNIPPETS
# ================================================================

# 📊 Top 10 giocatori per vittorie
"""
"""
top_10 = df_clean['winner_name'].value_counts().head(10)
print(top_10)

Output:
Novak Djokovic       450
Rafael Nadal        420
Roger Federer       410
...
"""

# 📊 Win rate per giocatore
"""
import pandas as pd

wins = df_clean.groupby('winner_name').size().reset_index(name='wins')
losses = df_clean.groupby('loser_name').size().reset_index(name='losses')

stats = wins.merge(losses, left_on='winner_name', right_on='loser_name', how='outer')
stats['total'] = stats['wins'].fillna(0) + stats['losses'].fillna(0)
stats['win_rate'] = (stats['wins'] / stats['total'] * 100).round(2)

top_rate = stats.nlargest(10, 'win_rate')[['winner_name', 'win_rate', 'total']]
print(top_rate)
"""

# 📊 Performance per superficie
"""
for surface in ['Hard', 'Clay', 'Grass']:
    surface_df = df_clean[df_clean['surface'] == surface]
    wins = surface_df['winner_name'].value_counts().head(5)
    print(f"{surface}: {dict(wins)}")

Output:
Hard: {'Djokovic': 180, 'Federer': 150, ...}
Clay: {'Nadal': 200, 'Djokovic': 100, ...}
Grass: {'Federer': 120, 'Djokovic': 80, ...}
"""

# 📊 Head-to-head tra due giocatori
"""
p1, p2 = "Novak Djokovic", "Rafael Nadal"

p1_vs_p2 = len(df_clean[(df_clean['winner_name'] == p1) & (df_clean['loser_name'] == p2)])
p2_vs_p1 = len(df_clean[(df_clean['winner_name'] == p2) & (df_clean['loser_name'] == p1)])

print(f"{p1} vs {p2}: {p1_vs_p2}-{p2_vs_p1}")

Output:
Novak Djokovic vs Rafael Nadal: 29-27
"""

# ================================================================
# MODIFICA DATI & ESPORTAZIONE
# ================================================================

# 📁 Salvare dataset filtrato
"""
# Solo Grand Slams
gs_only = df_clean[df_clean['tourney_level_name'] == 'Grand Slam']
gs_only.to_csv('output/grand_slams.csv', index=False)

# Solo ultimi 5 anni
recent = df_clean[df_clean['year'] >= 2021]
recent.to_csv('output/last_5_years.csv', index=False)

# Solo specifico giocatore
djokovic = df_clean[(df_clean['winner_name'] == 'Novak Djokovic') |
                    (df_clean['loser_name'] == 'Novak Djokovic')]
djokovic.to_csv('output/djokovic_matches.csv', index=False)
"""

# 📊 Esportare statistiche
"""
player_stats = df_clean['winner_name'].value_counts().reset_index()
player_stats.columns = ['player', 'wins']
player_stats.to_csv('output/player_wins.csv', index=False)
"""

# ================================================================
# DEBUGGING & EXPLORATION
# ================================================================

# 🔍 Info dataset
"""
df_clean.info()           # Colonne, tipi, null count
df_clean.describe()       # Statistiche numeriche
df_clean.head()           # Prime 5 righe
df_clean.shape            # Dimensioni (righe, colonne)

# Colonne disponibili
print(df_clean.columns)

# Valori unici per colonna
df_clean['surface'].unique()
df_clean['year'].unique()
df_clean['tourney_level_name'].unique()
"""

# 🔍 Cercare problemi dati
"""
# Null count
print(df_clean.isnull().sum())

# Duplicati
print(df_clean.duplicated().sum())

# Valori unici anomali
print(df_clean['surface'].value_counts(dropna=False))

# Intervallo date
print(f"Date range: {df_clean['tourney_date'].min()} to {df_clean['tourney_date'].max()}")
"""

# ================================================================
# PERFORMANCE TIPS
# ================================================================

"""
✅ Veloce:
  - df[df['column'] == value]          # Boolean indexing
  - df.loc[mask]                        # Loc with boolean
  - df.groupby().agg()                  # Groupby aggregation
  - df['col'].value_counts()            # Value counts

❌ Lento:
  - df.iterrows()                       # Iterare righe
  - df.apply(lambda x: ...)             # Apply con lambda
  - Nested loops su DataFrame
  - df.loc[] in loop (cresce lista)

💡 Optimization:
  - Filtrare presto (reduce data)
  - Usare vectorized ops
  - Convertire tipi dati correttamente
  - Cache risultati intermedi
"""

# ================================================================
# COMMON ISSUES & SOLUTIONS
# ================================================================

"""
❌ Problema: "ModuleNotFoundError: No module named 'tennis_analyzer'"
✅ Soluzione: source .venv/bin/activate && python main.py

❌ Problema: "ConnectionError" durante download
✅ Soluzione: Verificare internet, check firewall, usa cache locale

❌ Problema: "ValueError: time data does not match format"
✅ Soluzione: Already handled in cleaner.py, check raw data

❌ Problema: Memory error con dataset grandi
✅ Soluzione: Filtrare dati prima (years, surfaces), usare chunking

❌ Problema: Matplotlib non genera PNG
✅ Soluzione: Check permessi output/, verify backend, free disk space
"""

# ================================================================
# FILE STRUCTURE REFERENCE
# ================================================================

"""
tennis-stats-analyzer/
├── src/tennis_analyzer/
│   ├── __init__.py              # Exports
│   ├── config.py                # Config centralizzata ⚙️
│   ├── logger.py                # Logging setup 📋
│   ├── downloader.py            # Download data 📥
│   ├── cleaner.py               # Data cleaning 🧹
│   ├── analyzer.py              # EDA & analysis 📊
│   └── visualizer.py            # Grafici 📈
├── data/
│   ├── raw/                     # CSV scaricati
│   └── processed/               # Consolidati
├── output/
│   ├── clean_data.csv           # Final dataset
│   └── visuals/                 # PNG graphs
├── pyproject.toml               # UV config
├── main.py                      # Entry point 🚀
├── examples.py                  # Esempi avanzati
├── README.md                    # Documentazione
├── GUIDA_UTENTE.md              # User guide (ITA)
├── ARCHITECTURE.md              # Tech details
└── .gitignore
"""

# ================================================================
# CONFIGURATION REFERENCE
# ================================================================

"""
# Modificare in config.py:

ANALYSIS_YEARS = range(2015, 2026)     # Quali anni
MIN_MATCHES_PLAYER = 20                 # Minimo match
SURFACE_TYPES = ["Hard", "Clay", ...]  # Superfici
LOG_LEVEL = logging.INFO                # Verbosità log

# Output paths:
CLEAN_DATA_CSV = OUTPUT_DIR / "clean_data.csv"
RANKING_EVOLUTION_PNG = VISUALS_DIR / "01_top_atp_days.png"
WINS_BY_PLAYER_PNG = VISUALS_DIR / "02_total_wins.png"
WINS_BY_SURFACE_PNG = VISUALS_DIR / "03_wins_by_surface.png"
MATCH_DISTRIBUTION_PNG = VISUALS_DIR / "04_matches_distribution.png"
WIN_RATE_ANALYSIS_PNG = VISUALS_DIR / "05_win_rate_analysis.png"
"""

# ================================================================
# NEXT STEPS
# ================================================================

"""
Dopo aver lanciato main.py:

1. 📁 Aprire output/ per vedere risultati
   ├── clean_data.csv (dataset pulito 40K+ records)
   └── visuals/ (5 grafici professionali 300 DPI)

2. 📊 Analizzare i grafici:
   - Top N.1 ATP dominators
   - Total wins leaders
   - Surface specialization patterns
   - Match distribution trends
   - Win rate analysis

3. 🎯 Possibili estensioni:
   - Aggiungere analisi custom (vedi examples.py)
   - Creare dashboard interattivo (Plotly)
   - Machine learning predictions
   - Database integration (PostgreSQL)

4. 📈 Condividere risultati:
   - Presentation slides con grafici
   - Report PDF (pypdf2)
   - Share su GitHub

5. 🚀 Deploy:
   - Docker containerization
   - CI/CD pipeline (GitHub Actions)
   - Cloud hosting (AWS/GCP/Azure)
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║                  TENNIS STATS ANALYZER                        ║
║              Quick Reference & Cheat Sheet                    ║
║                                                                ║
║  📖 Full docs: README.md, GUIDA_UTENTE.md, ARCHITECTURE.md    ║
║  🚀 Run: python main.py                                       ║
║  📊 Results: output/clean_data.csv + visuals/                 ║
║                                                                ║
║  Happy analyzing! 🎾                                          ║
╚════════════════════════════════════════════════════════════════╝
""")
