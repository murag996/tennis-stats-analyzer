# Tennis Stats Analyzer

Progetto di analisi dati ATP Tennis utilizzando Python, Pandas, Matplotlib e Seaborn.

## Obiettivi

- Scaricamento e pulizia dataset ATP professionistico maschile (ultimi 10 anni)
- Analisi esplorative su giocatori, ranking, vittorie
- Visualizzazioni significative
- Export dati e grafici

## Dataset Utilizzati

- **Jeff Sackmann (GitHub)**: Database storico ATP matches (gold standard)

## Struttura Progetto

```
tennis-stats-analyzer/
├── pyproject.toml              # Configurazione UV/dipendenze
├── README.md
├── src/
│   └── tennis_analyzer/
│       ├── __init__.py
│       ├── config.py           # Configurazioni e costanti
│       ├── downloader.py       # Download dataset da GitHub
│       ├── cleaner.py          # Data cleaning e normalizzazione
│       ├── analyzer.py         # Analisi esplorative
│       ├── visualizer.py       # Generazione grafici
│       └── logger.py           # Logging centralizzato
├── data/
│   ├── raw/                    # Dataset grezzi
│   └── processed/              # Dataset puliti
├── output/
│   ├── clean_data.csv          # Dati consolidati puliti
│   └── visuals/                # Grafici (PNG)
├── notebooks/
│   └── exploration.ipynb       # Analisi interattiva (opzionale)
└── main.py                     # Entry point
```



## Installazione

### Installazione uv per Windows e Linux/Mac

**Windows:**
```bash
powershell -ExecutionPolicy Bypass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/Mac:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verifica installazione:
```bash
uv --version
```

Quindi sincronizza il progetto e attiva env:
```bash
uv sync --python 3.13
source .venv/bin/activate  # Linux/Mac
# oppure
.venv\Scripts\activate  # Windows
```

## Utilizzo

```bash
python main.py
#oppure 
uv run main.py
```


## Requisiti Specifici Soddisfatti

✅ Python 3.13 con uv
✅ Dataset ATP reali (Jeff Sackmann + Tennis-data)
✅ Data cleaning completo
✅ Analisi esplorative (Top 1 ATP, Win leaders, insights aggiuntivi)
✅ Visualizzazioni con Matplotlib/Seaborn
✅ Export CSV + PNG

## Dipendenze

- **pandas**: Manipolazione dati
- **numpy**: Operazioni numeriche
- **matplotlib**: Visualizzazioni base
- **seaborn**: Visualizzazioni avanzate
- **requests**: Download HTTP

## Prossimi Passi

- Aggiungere test unitari con pytest
- Dashboard interattivo con Plotly