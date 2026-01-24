"""
Modulo per il download dei dataset ATP da GitHub (Jeff Sackmann)
"""
import requests
import pandas as pd
from pathlib import Path
from typing import List, Optional
import io

from .logger import setup_logger
from . import config

logger = setup_logger(__name__)


class ATPDataDownloader:
    """Download e gestione dataset ATP tennis da GitHub"""
    
    def __init__(self):
        self.base_url = "https://raw.githubusercontent.com/JeffSackmann/tennis_atp/master"
        self.timeout = 30
        self.raw_data_dir = config.RAW_DATA_DIR
    
    def download_matches_year(self, year: int) -> Optional[pd.DataFrame]:
        """
        Scarica i match ATP per un anno specifico.
        
        Args:
            year: Anno da scaricare (es. 2024)
        
        Returns:
            DataFrame con i match, None se errore
        """
        url = f"{self.base_url}/atp_matches_{year}.csv"
        csv_file = self.raw_data_dir / f"atp_matches_{year}.csv"
        
        try:
            logger.info(f"Scaricando match ATP per {year} da {url}")
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Salvare localmente
            csv_file.write_bytes(response.content)
            logger.info(f"✓ Download completato: {csv_file}")
            
            # Caricare in DataFrame
            df = pd.read_csv(io.StringIO(response.text))
            logger.info(f"  - Record scaricati: {len(df)}")
            
            return df
        
        except requests.exceptions.RequestException as e:
            logger.error(f"✗ Errore download {year}: {e}")
            return None
    
    def download_multiple_years(self, years: range) -> pd.DataFrame:
        """
        Scarica e consolida match per più anni.
        
        Args:
            years: Range anni (es. range(2015, 2026))
        
        Returns:
            DataFrame consolidato con tutti i match
        """
        all_matches = []
        
        for year in years:
            df = self.download_matches_year(year)
            if df is not None:
                all_matches.append(df)
        
        if not all_matches:
            logger.error("Nessun dato scaricato!")
            return pd.DataFrame()
        
        consolidated_df = pd.concat(all_matches, ignore_index=True)
        logger.info(f"\n📊 Consolidamento: {len(consolidated_df)} match totali da {len(all_matches)} anni")
        
        return consolidated_df
    
    def load_local_csv(self, filepath: Path) -> Optional[pd.DataFrame]:
        """
        Carica CSV locale se già scaricato.
        
        Args:
            filepath: Percorso file CSV
        
        Returns:
            DataFrame o None se errore
        """
        try:
            if filepath.exists():
                logger.info(f"Caricando da file locale: {filepath}")
                df = pd.read_csv(filepath)
                logger.info(f"✓ Caricati {len(df)} record")
                return df
            else:
                logger.warning(f"File non trovato: {filepath}")
                return None
        except Exception as e:
            logger.error(f"Errore caricamento CSV: {e}")
            return None
    
    def get_consolidated_data(self, years: range = None, use_local: bool = True) -> pd.DataFrame:
        """
        Scarica e consolida dataset ATP, con fallback locale.
        
        Args:
            years: Range anni, default da config
            use_local: Se True, tenta caricamento locale prima di download
        
        Returns:
            DataFrame consolidato
        """
        if years is None:
            years = config.ANALYSIS_YEARS
        
        consolidated_file = config.PROCESSED_DATA_DIR / "atp_matches_consolidated.csv"
        
        # Provare caricamento da file consolidato locale
        if use_local and consolidated_file.exists():
            logger.info("Tentando caricamento da file consolidato locale...")
            df = self.load_local_csv(consolidated_file)
            if df is not None:
                return df
        
        # Altrimenti scaricare
        logger.info(f"Scaricando dati ATP per anni {years.start}-{years.stop-1}...")
        df = self.download_multiple_years(years)
        
        # Salvare consolidato localmente
        if not df.empty:
            df.to_csv(consolidated_file, index=False)
            logger.info(f"✓ Consolidato salvato: {consolidated_file}")
        
        return df


# Funzione di utilità
def download_atp_data(years: range = None) -> pd.DataFrame:
    """
    Funzione wrapper per download rapido dataset ATP.
    
    Args:
        years: Range anni (default da config)
    
    Returns:
        DataFrame con tutti i match
    """
    downloader = ATPDataDownloader()
    return downloader.get_consolidated_data(years=years)
