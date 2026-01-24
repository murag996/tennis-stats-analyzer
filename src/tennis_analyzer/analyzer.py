"""
Modulo per analisi esplorative (EDA) del dataset ATP
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

from .logger import setup_logger
from . import config

logger = setup_logger(__name__)


class ATPAnalyzer:
    """Analisi esplorative su dati ATP tennis"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inizializza analyzer con dataset pulito.
        
        Args:
            df: DataFrame pulito da cleaner
        """
        self.df = df
        self.logger = logger
    
    def get_all_players(self) -> pd.Series:
        """
        Ottiene lista di tutti i giocatori (winner + loser).
        
        Returns:
            Series con nomi unici
        """
        winners = self.df['winner_name'].unique()
        losers = self.df['loser_name'].unique()
        all_players = pd.Series(list(set(winners) | set(losers)))
        return all_players.sort_values().reset_index(drop=True)
    
    def analyze_top_atp_days(self, top_n: int = 15) -> pd.DataFrame:
        """
        Analizza giocatori che sono stati n.1 ATP per più giorni.
        
        Args:
            top_n: Top N giocatori da ritornare
        
        Returns:
            DataFrame con rank_1_days, prime, title_wins
        """
        logger.info("\n📊 ANALISI: Top N.1 ATP per giorni")
        
        # Giocatori che hanno avuto rank 1
        rank_1_matches = self.df[self.df['winner_rank'] == 1.0]
        
        if rank_1_matches.empty:
            logger.warning("Nessun giocatore con rank 1 trovato")
            return pd.DataFrame()
        
        # Group by vincitore quando era n.1
        rank_1_data = rank_1_matches.groupby('winner_name').agg({
            'tourney_date': ['min', 'max', 'count'],
            'tourney_level_name': lambda x: (x == 'Grand Slam').sum()
        }).reset_index()
        
        # Flatten colonne
        rank_1_data.columns = ['player_name', 'first_rank1_date', 'last_rank1_date', 
                               'matches_as_rank1', 'grand_slam_as_rank1']
        
        # Calcolare giorni approssimati (dalla prima all'ultima data)
        rank_1_data['days_at_rank1'] = (
            rank_1_data['last_rank1_date'] - rank_1_data['first_rank1_date']
        ).dt.days
        
        rank_1_data['days_at_rank1'] = rank_1_data['days_at_rank1'].fillna(0).astype(int)
        
        # Order by giorni
        rank_1_data = rank_1_data.sort_values('days_at_rank1', ascending=False).head(top_n)
        
        logger.info(f"✓ Top {len(rank_1_data)} giocatori n.1 ATP:")
        for idx, row in rank_1_data.iterrows():
            logger.info(
                f"  {row['player_name']:20} | "
                f"{row['days_at_rank1']:5} giorni | "
                f"{row['matches_as_rank1']:3} match | "
                f"{row['grand_slam_as_rank1']} GS"
            )
        
        return rank_1_data
    
    def analyze_total_wins(self, top_n: int = 20) -> pd.DataFrame:
        """
        Analizza numero totale di match vinti per giocatore.
        
        Args:
            top_n: Top N giocatori da ritornare
        
        Returns:
            DataFrame con statistiche vittorie
        """
        logger.info("\n📊 ANALISI: Giocatori per Total Wins")
        
        # Contare vittorie per ogni giocatore
        wins = self.df.groupby('winner_name').agg({
            'tourney_date': 'count',
            'tourney_level_name': lambda x: (x == 'Grand Slam').sum(),
            'surface': lambda x: (x == 'Hard').sum(),
        }).reset_index()
        
        wins.columns = ['player_name', 'total_wins', 'grand_slam_wins', 'hard_court_wins']
        
        # Win rate (wins vs partecipazioni stimate)
        # Giocatori che hanno perso
        losses = self.df.groupby('loser_name').size().reset_index(name='total_losses')
        
        wins = wins.merge(losses, left_on='player_name', right_on='loser_name', how='left')
        wins = wins.drop('loser_name', axis=1)
        wins['total_losses'] = wins['total_losses'].fillna(0).astype(int)
        wins['total_matches'] = wins['total_wins'] + wins['total_losses']
        wins['win_rate'] = (wins['total_wins'] / wins['total_matches'] * 100).round(2)
        
        # Filter: minimo di match richiesti
        wins = wins[wins['total_matches'] >= config.MIN_MATCHES_PLAYER]
        
        # Order by wins
        wins = wins.sort_values('total_wins', ascending=False).head(top_n)
        
        logger.info(f"✓ Top {len(wins)} per total wins:")
        for idx, row in wins.iterrows():
            logger.info(
                f"  {row['player_name']:20} | "
                f"{int(row['total_wins']):4} W | "
                f"{int(row['total_losses']):4} L | "
                f"{row['win_rate']:5.1f}% | "
                f"{int(row['grand_slam_wins'])} GS"
            )
        
        return wins
    
    def analyze_surface_performance(self, top_n: int = 10) -> pd.DataFrame:
        """
        Analizza performance per superficie.
        
        Args:
            top_n: Top N giocatori per superficie
        
        Returns:
            DataFrame con performance per superficie
        """
        logger.info("\n📊 ANALISI: Performance per superficie")
        
        surface_stats = []
        
        for surface in config.SURFACE_TYPES:
            surface_df = self.df[self.df['surface'] == surface]
            
            if surface_df.empty:
                continue
            
            wins = surface_df.groupby('winner_name').size().reset_index(name='wins')
            losses = surface_df.groupby('loser_name').size().reset_index(name='losses')
            
            stats = wins.merge(losses, left_on='winner_name', right_on='loser_name', how='outer')
            stats = stats.drop('loser_name', axis=1)
            stats.columns = ['player_name', 'wins', 'losses']
            stats = stats.fillna(0).astype({'wins': int, 'losses': int})
            stats['total'] = stats['wins'] + stats['losses']
            stats['win_rate'] = (stats['wins'] / stats['total'] * 100).round(1)
            stats['surface'] = surface
            
            # Top per questa superficie
            surface_stats.append(stats.sort_values('wins', ascending=False).head(top_n))
        
        result = pd.concat(surface_stats, ignore_index=True)
        
        logger.info(f"✓ Performance per superficie (top {top_n}):")
        for surface in config.SURFACE_TYPES:
            surf_data = result[result['surface'] == surface]
            if not surf_data.empty:
                logger.info(f"  {surface}: {len(surf_data)} giocatori analizzati")
        
        return result
    
    def analyze_tournament_levels(self) -> pd.DataFrame:
        """
        Analizza distribuzione match per livello torneo.
        
        Returns:
            DataFrame con statistiche per livello
        """
        logger.info("\n📊 ANALISI: Distribuzione per livello torneo")
        
        level_stats = self.df['tourney_level_name'].value_counts().reset_index()
        level_stats.columns = ['tourney_level', 'match_count']
        level_stats['percentage'] = (level_stats['match_count'] / level_stats['match_count'].sum() * 100).round(1)
        
        logger.info("✓ Distribuzione tornei:")
        for idx, row in level_stats.iterrows():
            logger.info(
                f"  {row['tourney_level']:20} | "
                f"{int(row['match_count']):5} match | "
                f"{row['percentage']:5.1f}%"
            )
        
        return level_stats
    
    def get_era_dominators(self) -> Dict[int, Dict]:
        """
        Identifica dominatori per ogni anno.
        
        Returns:
            Dict con dominatore per anno
        """
        logger.info("\n📊 ANALISI: Dominatori per anno")
        
        dominators = {}
        
        for year in sorted(self.df['year'].unique()):
            year_df = self.df[self.df['year'] == year]
            wins = year_df['winner_name'].value_counts()
            
            if not wins.empty:
                top_player = wins.index[0]
                dominators[year] = {
                    'player': top_player,
                    'wins': int(wins.iloc[0]),
                    'tournaments': year_df[year_df['winner_name'] == top_player]['tourney_name'].nunique()
                }
                
                logger.info(
                    f"  {year}: {top_player:20} ({int(wins.iloc[0])} wins, "
                    f"{dominators[year]['tournaments']} tornei)"
                )
        
        return dominators
    
    def run_full_analysis(self) -> Dict:
        """
        Esegue tutte le analisi.
        
        Returns:
            Dict consolidato con tutti i risultati
        """
        logger.info("\n" + "="*60)
        logger.info("ANALISI ESPLORATIVE COMPLETE")
        logger.info("="*60)
        
        results = {
            'top_atp_days': self.analyze_top_atp_days(),
            'total_wins': self.analyze_total_wins(),
            'surface_performance': self.analyze_surface_performance(),
            'tournament_levels': self.analyze_tournament_levels(),
            'era_dominators': self.get_era_dominators(),
        }
        
        return results
