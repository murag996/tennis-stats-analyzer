"""
Modulo per generazione visualizzazioni grafiche (Matplotlib + Seaborn)
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

from .logger import setup_logger
from . import config

logger = setup_logger(__name__)

# Configurare stile globale
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'sans-serif'


class ATPVisualizer:
    """Generazione visualizzazioni per analisi ATP"""
    
    def __init__(self, output_dir: Path = None):
        """
        Inizializza visualizer.
        
        Args:
            output_dir: Directory per salvare grafici
        """
        self.output_dir = output_dir or config.VISUALS_DIR
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logger
    
    def plot_top_atp_days(self, data: pd.DataFrame, filename: str = "01_top_atp_days.png"):
        """
        Grafico: Giocatori n.1 ATP per più giorni.
        
        Args:
            data: DataFrame da analyze_top_atp_days
            filename: Nome file output
        """
        if data.empty:
            logger.warning("Dati vuoti per plot_top_atp_days")
            return
        
        logger.info(f"Generando grafico: {filename}")
        
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Ordinare e selezionare top 15
        data_plot = data.sort_values('days_at_rank1', ascending=True).tail(15)
        
        # Colori gradient
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(data_plot)))
        
        bars = ax.barh(data_plot['player_name'], data_plot['days_at_rank1'], color=colors)
        
        # Aggiungere valore su barre
        for i, (player, days) in enumerate(zip(data_plot['player_name'], data_plot['days_at_rank1'])):
            ax.text(days + 10, i, f"{int(days)} days", va='center', fontsize=9, fontweight='bold')
        
        ax.set_xlabel('Giorni come N.1 ATP', fontsize=12, fontweight='bold')
        ax.set_ylabel('Giocatore', fontsize=12, fontweight='bold')
        ax.set_title('Top Giocatori: Giorni come N.1 ATP Rankings', fontsize=14, fontweight='bold', pad=20)
        ax.invert_yaxis()
        
        plt.tight_layout()
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        logger.info(f"✓ Salvato: {filepath}")
        plt.close()
    
    def plot_total_wins(self, data: pd.DataFrame, filename: str = "02_total_wins.png"):
        """
        Grafico: Total wins per giocatore.
        
        Args:
            data: DataFrame da analyze_total_wins
            filename: Nome file output
        """
        if data.empty:
            logger.warning("Dati vuoti per plot_total_wins")
            return
        
        logger.info(f"Generando grafico: {filename}")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # LEFT: Bar chart wins
        data_plot = data.sort_values('total_wins', ascending=True)
        colors = plt.cm.viridis(np.linspace(0.3, 0.9, len(data_plot)))
        
        bars = ax1.barh(data_plot['player_name'], data_plot['total_wins'], color=colors)
        ax1.set_xlabel('Total Wins', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Giocatore', fontsize=11, fontweight='bold')
        ax1.set_title('Top Giocatori: Vittorie Totali', fontsize=12, fontweight='bold')
        ax1.invert_yaxis()
        
        # Aggiungere valore
        for i, wins in enumerate(data_plot['total_wins']):
            ax1.text(wins + 5, i, f"{int(wins)}", va='center', fontsize=9)
        
        # RIGHT: Scatter win rate vs total matches
        ax2.scatter(data['total_matches'], data['win_rate'], 
                   s=data['total_wins']*2, alpha=0.6, c=data['win_rate'], 
                   cmap='coolwarm', edgecolors='black', linewidth=0.5)
        
        # Annotare top 5
        for idx, row in data.nlargest(5, 'total_wins').iterrows():
            ax2.annotate(row['player_name'], 
                        (row['total_matches'], row['win_rate']),
                        fontsize=8, alpha=0.7)
        
        ax2.set_xlabel('Total Matches', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Win Rate (%)', fontsize=11, fontweight='bold')
        ax2.set_title('Win Rate vs Total Matches', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        logger.info(f"✓ Salvato: {filepath}")
        plt.close()
    
    def plot_surface_performance(self, data: pd.DataFrame, filename: str = "03_wins_by_surface.png"):
        """
        Grafico: Performance per superficie.
        
        Args:
            data: DataFrame da analyze_surface_performance
            filename: Nome file output
        """
        if data.empty:
            logger.warning("Dati vuoti per plot_surface_performance")
            return
        
        logger.info(f"Generando grafico: {filename}")
        
        fig, ax = plt.subplots(figsize=(14, 9))
        
        # Pivot per visualizzazione
        surfaces = sorted(data['surface'].unique())
        
        # Prendere top 12 giocatori overall
        top_players = data.groupby('player_name')['wins'].sum().nlargest(12).index
        data_filtered = data[data['player_name'].isin(top_players)]
        
        # Creare matrice per heatmap
        pivot_table = data_filtered.pivot_table(
            index='player_name', 
            columns='surface', 
            values='wins', 
            fill_value=0
        )
        
        # Heatmap
        sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', 
                   cbar_kws={'label': 'Vittorie'}, ax=ax, linewidths=0.5)
        
        ax.set_title('Performance per Superficie (Top 12 Giocatori)', 
                    fontsize=14, fontweight='bold', pad=20)
        ax.set_xlabel('Superficie', fontsize=11, fontweight='bold')
        ax.set_ylabel('Giocatore', fontsize=11, fontweight='bold')
        
        plt.tight_layout()
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        logger.info(f"✓ Salvato: {filepath}")
        plt.close()
    
    def plot_matches_distribution(self, df: pd.DataFrame, filename: str = "04_matches_distribution.png"):
        """
        Grafico: Distribuzione match nel tempo.
        
        Args:
            df: Dataset pulito (raw)
            filename: Nome file output
        """
        logger.info(f"Generando grafico: {filename}")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # LEFT: Matches per anno
        matches_per_year = df.groupby('year').size()
        ax1.bar(matches_per_year.index, matches_per_year.values, color='steelblue', alpha=0.7, edgecolor='black')
        ax1.set_xlabel('Anno', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Numero Match', fontsize=11, fontweight='bold')
        ax1.set_title('Distribuzione Match per Anno', fontsize=12, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')
        
        # RIGHT: Distribuzione per superficie
        surface_counts = df['surface'].value_counts()
        colors = plt.cm.Set3(range(len(surface_counts)))
        ax2.pie(surface_counts.values, labels=surface_counts.index, autopct='%1.1f%%', 
               colors=colors, startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
        ax2.set_title('Distribuzione Match per Superficie', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        logger.info(f"✓ Salvato: {filepath}")
        plt.close()
    
    def plot_win_rate_analysis(self, data: pd.DataFrame, filename: str = "05_win_rate_analysis.png"):
        """
        Grafico: Analisi win rate.
        
        Args:
            data: DataFrame da analyze_total_wins
            filename: Nome file output
        """
        if data.empty:
            logger.warning("Dati vuoti per plot_win_rate_analysis")
            return
        
        logger.info(f"Generando grafico: {filename}")
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
        
        # LEFT: Win rate ranking
        data_plot = data.sort_values('win_rate', ascending=True).head(20)
        colors = plt.cm.RdYlGn(data_plot['win_rate'].values / 100)
        
        ax1.barh(data_plot['player_name'], data_plot['win_rate'], color=colors, edgecolor='black', linewidth=0.5)
        ax1.set_xlabel('Win Rate (%)', fontsize=11, fontweight='bold')
        ax1.set_ylabel('Giocatore', fontsize=11, fontweight='bold')
        ax1.set_title('Top 20: Win Rate', fontsize=12, fontweight='bold')
        ax1.set_xlim([50, 100])
        ax1.invert_yaxis()
        
        # Aggiungere valore
        for i, rate in enumerate(data_plot['win_rate']):
            ax1.text(rate + 0.5, i, f"{rate:.1f}%", va='center', fontsize=9)
        
        # RIGHT: Distribuzione win rate
        ax2.hist(data['win_rate'], bins=20, color='coral', alpha=0.7, edgecolor='black')
        ax2.axvline(data['win_rate'].mean(), color='red', linestyle='--', linewidth=2, label=f"Media: {data['win_rate'].mean():.1f}%")
        ax2.axvline(data['win_rate'].median(), color='green', linestyle='--', linewidth=2, label=f"Mediana: {data['win_rate'].median():.1f}%")
        ax2.set_xlabel('Win Rate (%)', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Numero Giocatori', fontsize=11, fontweight='bold')
        ax2.set_title('Distribuzione Win Rate', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        filepath = self.output_dir / filename
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        logger.info(f"✓ Salvato: {filepath}")
        plt.close()
    
    def generate_all_plots(self, df: pd.DataFrame, analysis_results: dict):
        """
        Genera tutti i grafici.
        
        Args:
            df: Dataset pulito
            analysis_results: Dict con risultati analisi
        """
        logger.info("\n" + "="*60)
        logger.info("GENERAZIONE VISUALIZZAZIONI")
        logger.info("="*60 + "\n")
        
        import numpy as np
        
        self.plot_top_atp_days(analysis_results['top_atp_days'])
        self.plot_total_wins(analysis_results['total_wins'])
        self.plot_surface_performance(analysis_results['surface_performance'])
        self.plot_matches_distribution(df)
        self.plot_win_rate_analysis(analysis_results['total_wins'])
        
        logger.info("\n✓ Tutti i grafici generati con successo!")
        logger.info(f"  Salvati in: {self.output_dir}")
