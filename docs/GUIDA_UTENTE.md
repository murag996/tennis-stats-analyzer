# GUIDA D'USO - Tennis Stats Analyzer

## Quick Start (2 minuti)

```bash
# 1. Clonare il repository
cd tennis-stats-analyzer

# 2. Installare dipendenze con UV (velocissimo!)
uv sync --python 3.13

# 3. Eseguire il progetto
python main.py
```

**Fatto!** I dati saranno in `output/`

---

## Requisiti Soddisfatti ✅

### 1. **Python 3.13 + UV**
- ✅ `pyproject.toml` configurato per Python 3.13
- ✅ Tutte le dipendenze gestite via `uv` (Rust-based, ultra-veloce)
- ✅ Lock file automatico

### 2. **Dataset ATP Reali**
- ✅ Jeff Sackmann GitHub (ATP matches 2015-2025)
- ✅ Download automatico da `https://github.com/JeffSackmann/tennis_atp`
- ✅ Fallback locale se dati già scaricati
- ✅ ~40 anni di history disponibile

### 3. **Data Cleaning Completo**
- ✅ Rimozione duplicate
- ✅ Conversione date (tourney_date)
- ✅ Normalizzazione nomi giocatori
- ✅ Standardizzazione surface (Hard, Clay, Grass, Carpet)
- ✅ Conversione ranking points a numerico
- ✅ Rimozione valori NULL critici
- ✅ Feature engineering (year, upset_indicator, ecc.)

### 4. **Analisi Esplorative (EDA)**

#### Grafico 1: Top N.1 ATP per Giorni
```
Giocatori che hanno mantenuto la posizione #1 per più giorni
→ Mostra dominanza prolungata (Federer, Djokovic, Nadal)
```

#### Grafico 2: Total Wins
```
Left: Bar chart con vittorie totali per giocatore
Right: Scatter plot win rate vs total matches
→ Identifica chi vince di più e con quale consistenza
```

#### Grafico 3: Performance per Superficie
```
Heatmap mostrando specializzazione per superficie
Hard (veloce), Clay (Nadal), Grass (Federer)
```

#### Grafico 4: Distribuzione Match nel Tempo
```
Left: Serie temporale match per anno
Right: Pie chart distribuzione per superficie
→ Trend storici e preferenze delle superfici
```

#### Grafico 5: Win Rate Analysis
```
Left: Top 20 giocatori per win rate (%)
Right: Istogramma distribuzione con media/mediana
→ Qualità vs Quantità: chi vince più consistentemente
```

### 5. **Export Dati & Grafici**

```
output/
├── clean_data.csv                    # 40K+ record puliti
└── visuals/
    ├── 01_top_atp_days.png          # Dominanza N.1
    ├── 02_total_wins.png            # Vittorie totali
    ├── 03_wins_by_surface.png       # Performance per superficie
    ├── 04_matches_distribution.png  # Trend temporali
    └── 05_win_rate_analysis.png     # Qualità vittorie
```

---

## Struttura Progetto

```
tennis-stats-analyzer/
├── src/tennis_analyzer/
│   ├── __init__.py                 # Exports principali
│   ├── config.py                   # Configurazioni centralizzate
│   ├── logger.py                   # Logging
│   ├── downloader.py               # Download da GitHub (ATPDataDownloader)
│   ├── cleaner.py                  # Cleaning/normalizazione (ATPDataCleaner)
│   ├── analyzer.py                 # EDA (ATPAnalyzer)
│   └── visualizer.py               # Grafici (ATPVisualizer)
├── data/
│   ├── raw/                        # CSV scaricati da GitHub
│   └── processed/                  # Dati consolidati
├── output/
│   ├── clean_data.csv              # Dataset pulito
│   └── visuals/                    # PNG grafici
├── pyproject.toml                  # Configurazione UV
├── main.py                         # Entry point
├── README.md                       # Documentazione
└── .gitignore
```

---

## Comandi Utili

### Installazione
```bash
# Con UV (consigliato - 10x più veloce di pip)
uv sync --python 3.13

# Attivare environment
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
```

### Esecuzione
```bash
# Run principale
python main.py

# Con output verboso
python main.py 2>&1 | tee output/execution.log
```

### Sviluppo
```bash
# Aggiungere nuova dipendenza
uv pip install <package>

# Installare dev tools
uv sync --extra dev

# Linting
black src/
ruff check src/

# Type checking
mypy src/tennis_analyzer/
```

---

## Descrizione Moduli

### **downloader.py**
Scarica dataset ATP da GitHub con:
- Error handling automatico
- Fallback locale per evitare riscaricamenti
- Consolidamento multi-anno
- Logging dettagliato

**Classe principale:** `ATPDataDownloader`

### **cleaner.py**
Data quality pipeline:
- Validazione colonne essenziali
- Pulizia duplicate
- Conversione tipi
- Feature engineering
- Summary statistiche

**Classe principale:** `ATPDataCleaner`

### **analyzer.py**
Analisi esplorative:
- Top N.1 ATP per giorni
- Total wins per giocatore
- Performance per superficie
- Trend storici
- Dominatori per era

**Classe principale:** `ATPAnalyzer`

### **visualizer.py**
Generazione grafici professionali:
- Matplotlib + Seaborn
- Tema consistente
- Export PNG ad alta risoluzione (300 DPI)
- 5 visualizzazioni principali

**Classe principale:** `ATPVisualizer`

### **config.py**
Configurazione centralizzata:
- Percorsi file
- URL dataset
- Colori palette
- Parametri analisi
- Constanti

---

## Dataset Details

### Source: Jeff Sackmann ATP Database
- **URL**: `https://github.com/JeffSackmann/tennis_atp`
- **Coverage**: 1968-2025 (match completi ATP)
- **Records**: 300K+ match con statistiche dettagliate
- **Frequenza aggiornamento**: Settimanale

### Colonne Principali
```
tourney_id, tourney_name, surface, draw_size, tourney_level
tourney_date, match_num
winner_id, winner_name, winner_rank, winner_rank_points
loser_id, loser_name, loser_rank, loser_rank_points
score, best_of, round, minutes
w_ace, w_df, ... (statistiche servizio winner)
l_ace, l_df, ... (statistiche servizio loser)
```

### Post-Cleaning Aggiunto
```
year, month              # Temporal features
upset_indicator          # loser_rank < winner_rank
favorite_rank            # Min ranking
tourney_level_name       # Descrizione livello torneo
```

---

## Insights Comuni

### Dominatori Storici
- **Roger Federer**: Massimo giorni #1 (lunghissima cariera)
- **Rafael Nadal**: Specialista clay court
- **Novak Djokovic**: Dominatore 2010s

### Pattern Interessanti
- Hard court: 60-70% dei match
- Clay court: Specialmente Roland Garros (maggio-giugno)
- Grass court: Wimbledon (luglio)
- Win rate tra 50-70% per top players

### Trend Storici
- Aumento match negli ultimi 20 anni
- Specializzazione per superficie
- Volatilità ranking maggiore negli ultimi anni

---

## Troubleshooting

### Problema: "ModuleNotFoundError: No module named 'tennis_analyzer'"
**Soluzione**: Verificare che sia installato con `uv sync` e src è nel PYTHONPATH

### Problema: "ConnectionError" durante download
**Soluzione**: 
- Verificare connessione internet
- Controllare firewall/proxy
- Usare dati locali (funzione auto-fallback in downloader.py)

### Problema: "tourney_date conversion error"
**Soluzione**: 
- Formato date non standard
- Already gestito in cleaner.py con `pd.to_datetime(..., errors='coerce')`
- Check log per righe problematiche

### Problema: Grafici non generati
**Soluzione**:
- Verificare permessi directory output/
- Controllare spazio disco
- Verificare Matplotlib backend

---

## Customizzazione

### Modificare Anni Analizzati
In `config.py`:
```python
ANALYSIS_YEARS = range(2020, 2026)  # Solo ultimi 5 anni
```

### Modificare Top N per Analisi
In `config.py`:
```python
MIN_MATCHES_PLAYER = 50  # Minimo match per inclusione
```

### Aggiungere Nuove Visualizzazioni
In `visualizer.py`, aggiungere metodo `plot_custom()`:
```python
def plot_custom(self, data, filename):
    # ... implementazione
    plt.savefig(self.output_dir / filename, dpi=300)
```

---

## Performance

### Tipici Runtime
- Download dataset: 30-60 sec (primo run)
- Cleaning: 2-5 sec
- Analisi: 3-10 sec
- Visualizzazioni: 5-15 sec
- **Totale**: ~1-2 minuti primo run, ~30 sec con cache

### Memory Usage
- Raw data: ~100-150 MB
- Clean data: ~80-120 MB
- Peak memory: ~200-250 MB

---

## Prossimi Passi (Futuri Miglioramenti)

- [ ] Dashboard interattivo Plotly
- [ ] Predizioni ML (win probability)
- [ ] Player comparison tool
- [ ] Elo rating implementation
- [ ] Statistical tests (chi-square, t-test)
- [ ] API REST per queryare dati
- [ ] Database PostgreSQL integration
- [ ] Automated reporting (PDF/Excel)

---

## License & Attribution

- **Dataset**: Jeff Sackmann (GitHub)
- **Progetto**: Custom Data Engineering Pipeline
- **License**: MIT

---

## Contatti & Supporto

Per issues, domande o miglioramenti:
- Check log files in `output/`
- Verificare config.py per paths
- Review README.md per troubleshooting

**Happy Analyzing! 🎾📊**
