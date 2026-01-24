"""
Modulo per data cleaning e normalizzazione dataset ATP
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Tuple

from .logger import setup_logger
from . import config

logger = setup_logger(__name__)


class ATPDataCleaner:
    """Pulizia, validazione e normalizzazione dati ATP tennis"""
    
    def __init__(self):
        self.expected_columns = [
            'tourney_id', 'tourney_name', 'surface', 'draw_size', 'tourney_level',
            'tourney_date', 'match_num', 'winner_id', 'winner_seed', 'winner_entry',
            'winner_name', 'winner_hand', 'winner_ht', 'winner_ioc', 'winner_age',
            'winner_rank', 'winner_rank_points', 'loser_id', 'loser_seed', 'loser_entry',
            'loser_name', 'loser_hand', 'loser_ht', 'loser_ioc', 'loser_age',
            'loser_rank', 'loser_rank_points', 'score', 'best_of', 'round',
            'minutes', 'w_ace', 'w_df', 'w_svpt', 'w_1stIn', 'w_1stWon', 'w_2ndWon',
            'w_SvGms', 'w_bpSaved', 'w_bpFaced', 'l_ace', 'l_df', 'l_svpt', 'l_1stIn',
            'l_1stWon', 'l_2ndWon', 'l_SvGms', 'l_bpSaved', 'l_bpFaced'
        ]
    
    def validate_columns(self, df: pd.DataFrame) -> bool:
        """
        Valida presenza colonne essenziali.
        
        Args:
            df: DataFrame da validare
        
        Returns:
            True se tutte le colonne essenziali presenti
        """
        essential_cols = [
            'tourney_date', 'winner_name', 'loser_name', 'surface',
            'winner_rank', 'loser_rank', 'score'
        ]
        
        missing = [col for col in essential_cols if col not in df.columns]
        if missing:
            logger.warning(f"Colonne mancanti: {missing}")
            return False
        
        logger.info("✓ Validazione colonne completata")
        return True
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Esegue cleaning completo del dataset.
        
        Args:
            df: DataFrame grezzo
        
        Returns:
            DataFrame pulito e normalizzato
        """
        logger.info(f"Inizio cleaning: {len(df)} record")
        
        # 1. Rimuovere duplicate
        initial_len = len(df)
        df = df.drop_duplicates(
            subset=['tourney_date', 'winner_name', 'loser_name'],
            keep='first'
        )
        logger.info(f"  - Duplicate rimosse: {initial_len - len(df)}")
        
        # 2. Convertire date
        df['tourney_date'] = pd.to_datetime(df['tourney_date'], format='%Y%m%d', errors='coerce')
        logger.info(f"  - Date convertite")
        
        # 3. Normalizzare nomi (trim, case)
        df['winner_name'] = df['winner_name'].str.strip().str.title()
        df['loser_name'] = df['loser_name'].str.strip().str.title()
        logger.info(f"  - Nomi giocatori normalizzati")
        
        # 4. Surface standardizzazione
        df['surface'] = df['surface'].str.strip()
        df['surface'] = df['surface'].fillna('Unknown')
        valid_surfaces = ['Hard', 'Clay', 'Grass', 'Carpet']
        df.loc[~df['surface'].isin(valid_surfaces), 'surface'] = 'Unknown'
        logger.info(f"  - Surface standardizzate")
        
        # 5. Ranking points - convertire a numerico
        df['winner_rank_points'] = pd.to_numeric(df['winner_rank_points'], errors='coerce')
        df['loser_rank_points'] = pd.to_numeric(df['loser_rank_points'], errors='coerce')
        
        # 6. Ranking (posizione) - convertire a numerico
        df['winner_rank'] = pd.to_numeric(df['winner_rank'], errors='coerce')
        df['loser_rank'] = pd.to_numeric(df['loser_rank'], errors='coerce')
        logger.info(f"  - Ranking points convertiti")
        
        # 7. Minutes (durata match)
        df['minutes'] = pd.to_numeric(df['minutes'], errors='coerce')
        
        # 8. Rimuovere righe con campi critici null
        critical_cols = ['tourney_date', 'winner_name', 'loser_name']
        nulls_before = df.isnull().sum().sum()
        df = df.dropna(subset=critical_cols)
        nulls_after = df.isnull().sum().sum()
        logger.info(f"  - Null rimossi: {nulls_before - nulls_after}")
        
        # 9. Aggiungere colonne derivate
        df = self._add_derived_columns(df)
        
        logger.info(f"Cleaning completato: {len(df)} record rimanenti")
        return df
    
    def _add_derived_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggiunge colonne derivate/calcolate.
        
        Args:
            df: DataFrame in cleaning
        
        Returns:
            DataFrame con nuove colonne
        """
        # Anno del match
        df['year'] = df['tourney_date'].dt.year
        
        # Ranking favorito (lower rank = better)
        df['favorite_rank'] = df[['winner_rank', 'loser_rank']].min(axis=1)
        df['upset_indicator'] = (df['loser_rank'] < df['winner_rank']).astype(int)
        
        # Mesi per trend stagionale
        df['month'] = df['tourney_date'].dt.month
        
        # Tipo torneo
        level_map = {
            'G': 'Grand Slam',
            'M': 'Masters 1000',
            'A': 'ATP Tour',
            'D': 'Davis Cup',
            'F': 'Finals',
            'C': 'Challenger',
            'I': 'ITF'
        }
        df['tourney_level_name'] = df.get('tourney_level', 'A').map(level_map).fillna('Other')
        
        logger.info(f"  - Colonne derivate aggiunte (year, upset_indicator, ecc.)")
        
        return df
    
    def generate_summary(self, df: pd.DataFrame) -> dict:
        """
        Genera statistiche di summary del dataset.
        
        Args:
            df: DataFrame pulito
        
        Returns:
            Dict con statistiche
        """
        summary = {
            'total_matches': len(df),
            'date_range': f"{df['tourney_date'].min().date()} to {df['tourney_date'].max().date()}",
            'unique_players': len(set(df['winner_name'].unique()) | set(df['loser_name'].unique())),
            'tournaments': df['tourney_name'].nunique(),
            'surfaces': df['surface'].value_counts().to_dict(),
            'avg_match_duration': df['minutes'].mean(),
            'years_covered': sorted(df['year'].unique().tolist()),
        }
        
        return summary
    
    def process_pipeline(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Pipeline completo di cleaning.
        
        Args:
            df: Raw data
        
        Returns:
            Dati puliti e pronti per analisi
        """
        logger.info("\n" + "="*60)
        logger.info("PIPELINE CLEANING ATP DATA")
        logger.info("="*60)
        
        # Validare
        if not self.validate_columns(df):
            logger.error("Validazione fallita")
            return pd.DataFrame()
        
        # Pulire
        df_clean = self.clean_data(df)
        
        # Summary
        summary = self.generate_summary(df_clean)
        logger.info("\n📊 SUMMARY DATASET PULITO:")
        for key, value in summary.items():
            logger.info(f"  - {key}: {value}")
        
        return df_clean


# Funzione di utilità
def clean_atp_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Funzione wrapper per cleaning rapido.
    
    Args:
        df: Raw DataFrame
    
    Returns:
        DataFrame pulito
    """
    cleaner = ATPDataCleaner()
    return cleaner.process_pipeline(df)
