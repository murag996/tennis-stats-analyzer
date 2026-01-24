# ARCHITETTURA & BEST PRACTICES

## Architettura del Progetto

### Pattern: Data Pipeline Modulare

```
DOWNLOAD → CLEAN → ANALYZE → VISUALIZE → EXPORT
  ↓          ↓        ↓         ↓         ↓
GitHub    Pandas   Pandas    Matplotlib CSV
```

### Moduli & Responsabilità

| Modulo | Responsabilità | Output |
|--------|----------------|--------|
| `downloader.py` | Fetch dati da GitHub, fallback locale | DataFrame raw |
| `cleaner.py` | Validazione, pulizia, feature eng. | DataFrame pulito |
| `analyzer.py` | EDA, statistiche, insights | Dict risultati |
| `visualizer.py` | Grafici professionali | PNG files |
| `config.py` | Configurazioni centralizzate | Constants |
| `logger.py` | Logging strutturato | Console output |

### Flusso Dati

```
atp_matches_XXXX.csv (raw)
         ↓
    downloader.py
         ↓
    df_raw (300K+ records)
         ↓
    cleaner.py
    ├─ validate_columns()
    ├─ clean_data()
    ├─ add_derived_columns()
    └─ generate_summary()
         ↓
    df_clean (280K+ records, 25+ colonne)
         ↓
    analyzer.py
    ├─ analyze_top_atp_days()
    ├─ analyze_total_wins()
    ├─ analyze_surface_performance()
    ├─ analyze_tournament_levels()
    └─ get_era_dominators()
         ↓
    analysis_results (Dict)
         ↓
    visualizer.py → 5 grafici PNG
         ↓
    output/clean_data.csv + visuals/*.png
```

---

## Best Practices Implementate

### 1. **Logging Strutturato**
```python
from .logger import setup_logger
logger = setup_logger(__name__)

logger.info("Step completato")      # Info
logger.warning("Attenzione")        # Warning
logger.error("Errore critico")      # Error
```

✅ Output consistente su console
✅ Format standardizzato con timestamp
✅ Scalabile a file logging se necessario

### 2. **Error Handling Robusto**
```python
try:
    response = requests.get(url, timeout=self.timeout)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logger.error(f"Download fallito: {e}")
    return None  # Fallback gracefully
```

✅ Try-except per ogni operazione critica
✅ Logging degli errori dettagliato
✅ Fallback a dati locali se possibile

### 3. **Type Hints (Python 3.13)**
```python
def download_matches_year(self, year: int) -> Optional[pd.DataFrame]:
    """Scarica match per anno."""
    # ...

def analyze_total_wins(self, top_n: int = 20) -> pd.DataFrame:
    """Analizza vittorie."""
    # ...
```

✅ Codice auto-documentato
✅ Validazione IDE
✅ Future type checking con mypy

### 4. **Configurazione Centralizzata**
```python
# config.py
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"

ANALYSIS_YEARS = range(2015, 2026)
MIN_MATCHES_PLAYER = 20
```

✅ Single source of truth
✅ Facile modifica parametri
✅ Path management portabile

### 5. **Pulizia Dati Completa**
```python
# Rimozione duplicate
df = df.drop_duplicates(subset=['tourney_date', 'winner_name', 'loser_name'])

# Conversione date
df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d', errors='coerce')

# Normalizzazione nomi
df['winner_name'] = df['winner_name'].str.strip().str.title()

# Validazione superficie
valid_surfaces = ['Hard', 'Clay', 'Grass', 'Carpet']
df.loc[~df['surface'].isin(valid_surfaces), 'surface'] = 'Unknown'

# Null handling
df = df.dropna(subset=['tourney_date', 'winner_name', 'loser_name'])
```

✅ Quality gates ad ogni step
✅ Data validation logging
✅ Tracciamento pulizia

### 6. **Feature Engineering Intelligente**
```python
# Colonne derivate meaningful
df['year'] = df['tourney_date'].dt.year
df['upset_indicator'] = (df['loser_rank'] < df['winner_rank']).astype(int)
df['favorite_rank'] = df[['winner_rank', 'loser_rank']].min(axis=1)
df['month'] = df['tourney_date'].dt.month
```

✅ Aggiunge contesto semantico
✅ Facilita analisi
✅ Prepara per ML

### 7. **Visualizzazioni Professionali**
```python
# Stile consistente
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

# Alto DPI
plt.savefig(filepath, dpi=300, bbox_inches='tight')

# Annotazioni chiare
ax.set_xlabel('Giorni come N.1 ATP', fontsize=12, fontweight='bold')
ax.set_title('Top Giocatori: Giorni come N.1', fontsize=14, fontweight='bold')
```

✅ Output pubblicabile
✅ Leggibile e professionale
✅ Riusabile in presentazioni

### 8. **Documentazione Inline**
```python
def analyze_total_wins(self, top_n: int = 20) -> pd.DataFrame:
    """
    Analizza numero totale di match vinti per giocatore.
    
    Args:
        top_n: Top N giocatori da ritornare (default: 20)
    
    Returns:
        DataFrame con player_name, total_wins, win_rate, ecc.
    
    Raises:
        Nessuna eccezione, returns empty se dati insufficienti
    
    Example:
        >>> analyzer = ATPAnalyzer(df_clean)
        >>> top_wins = analyzer.analyze_total_wins(top_n=15)
    """
```

✅ Docstring dettagliati
✅ Type hints complete
✅ Esempi di utilizzo

### 9. **Memory Efficiency**
```python
# Usare generator per grandi dataset
for year in ANALYSIS_YEARS:
    df_year = downloader.download_matches_year(year)
    all_matches.append(df_year)  # Concat solo al fine

# Concatenare in one go
consolidated_df = pd.concat(all_matches, ignore_index=True)

# Dropna esplicito
df = df.dropna(subset=critical_cols)
```

✅ Evita creazione copie innecesarie
✅ Gestione memoria ottimale
✅ Scalabile a dataset grandi

### 10. **Testing Friendly**
```python
# Moduli testabili
class ATPDataDownloader:
    def __init__(self):
        self.base_url = "..."  # Mockabile

# Funzioni pure
def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
    # Input: DataFrame
    # Output: DataFrame pulito
    # Effetti collaterali: logging only
```

✅ Facile unit testing
✅ Mockable dependencies
✅ Deterministic output

---

## Differenze da Approccio Junior vs Senior

### ❌ Junior Approach
```python
# main.py - tutto in un file
df = pd.read_csv("data.csv")
df['date'] = pd.to_datetime(df['date'])
# 500 righe di codice...
plt.plot(...)
plt.savefig("output.png")
```

### ✅ Senior Approach (Questo Progetto)
```python
# main.py - orchestrazione
downloader = ATPDataDownloader()
df_raw = downloader.get_consolidated_data()

cleaner = ATPDataCleaner()
df_clean = cleaner.process_pipeline(df_raw)

analyzer = ATPAnalyzer(df_clean)
results = analyzer.run_full_analysis()

visualizer = ATPVisualizer()
visualizer.generate_all_plots(df_clean, results)
```

**Vantaggi:**
- ✅ Modularità e riusabilità
- ✅ Testing indipendente
- ✅ Maintenance facilità
- ✅ Scaling capability
- ✅ Code clarity

---

## Performance Considerations

### Optimizzazioni Implementate

1. **Lazy Loading**
   - Download solo anni richiesti
   - Cache locale fallback

2. **Efficient Filtering**
   ```python
   # Veloce
   rank_1_matches = df[df['winner_rank'] == 1.0]
   
   # Lento
   rank_1_matches = df[df['winner_rank'].apply(lambda x: x == 1.0)]
   ```

3. **Vectorized Operations**
   ```python
   # Veloce (vectorized)
   df['upset_indicator'] = (df['loser_rank'] < df['winner_rank']).astype(int)
   
   # Lento (loop)
   for idx, row in df.iterrows():
       df.loc[idx, 'upset_indicator'] = 1 if row['loser_rank'] < row['winner_rank'] else 0
   ```

### Benchmark Tipici
- Download: 30-60 sec (primo run)
- Cleaning: 2-5 sec
- Analisi: 3-10 sec
- Visualizzazioni: 5-15 sec
- **Totale**: ~1-2 minuti (primo run), ~30 sec con cache

---

## Extensibility

### Come Aggiungere Nuove Analisi

1. **Aggiungere metodo in `analyzer.py`**
   ```python
   def analyze_custom_metric(self) -> pd.DataFrame:
       """Nuova analisi custom"""
       # ... implementazione
       return results
   ```

2. **Aggiungere risultato in `run_full_analysis()`**
   ```python
   results['custom_metric'] = self.analyze_custom_metric()
   ```

3. **Aggiungere visualizzazione in `visualizer.py`**
   ```python
   def plot_custom_metric(self, data: pd.DataFrame):
       """Nuova visualizzazione"""
       # ... implementazione
       plt.savefig(...)
   ```

---

## Future Roadmap

- [ ] Database PostgreSQL per persistenza
- [ ] REST API con FastAPI
- [ ] Dashboard interattivo Plotly
- [ ] ML predictions (win probability)
- [ ] Elo rating calculation
- [ ] Automated reporting (PDF/Excel)
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)

---

## Conclusione

Questo progetto dimostra best practices di data engineering:
- ✅ **Modulare**: Separazione dei concerns
- ✅ **Robusto**: Error handling e validation
- ✅ **Documentato**: Docstring e type hints
- ✅ **Scalabile**: Facile estensione
- ✅ **Professionale**: Output publication-ready
- ✅ **Efficiente**: Memory e performance optimized

**Perfect for**: Portfolio, job interviews, production deployments.
