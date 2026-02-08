"""
EXAMPLE: Advanced Usage - Tennis Stats Analyzer
Esempi di utilizzo avanzato dei moduli
"""

from pathlib import Path
import sys
import pandas as pd


# Setup path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


from tennis_analyzer import (
    setup_logger,
    download_atp_data,
    clean_atp_data,
    ATPAnalyzer,
    ATPVisualizer,
    ATPDataCleaner,
    config
)

logger = setup_logger(__name__)


# ================================================================
# EXAMPLE 1: Download dato specifico anno
# ================================================================
def example_1_download_specific_year():
    """Scarica dataset per anno specifico"""
    logger.info("EXAMPLE 1: Download anno specifico")
    
    from tennis_analyzer.downloader import ATPDataDownloader
    
    downloader = ATPDataDownloader()
    df_2023 = downloader.download_matches_year(2023)
    
    if df_2023 is not None:
        logger.info(f"  Scaricati {len(df_2023)} match 2023")
        logger.info(f"  Giocatori: {df_2023['winner_name'].nunique()} unici")
    
    return df_2023


# ================================================================
# EXAMPLE 2: Custom cleaning pipeline
# ================================================================
def example_2_custom_cleaning():
    """Custom cleaning con parametri modificati"""
    logger.info("EXAMPLE 2: Custom cleaning")
    
    df = download_atp_data(years=range(2020, 2026))
    
    cleaner = ATPDataCleaner()
    
    # Validare
    if not cleaner.validate_columns(df):
        logger.error("Validazione fallita")
        return None
    
    # Pulire
    df_clean = cleaner.clean_data(df)
    
    # Summary
    summary = cleaner.generate_summary(df_clean)
    logger.info(f"  Summary: {summary}")
    
    return df_clean


# ================================================================
# EXAMPLE 3: Analisi di un giocatore specifico
# ================================================================
def example_3_player_analysis(df: 'pd.DataFrame', player_name: str):
    """Analizza statistiche di un giocatore"""
    logger.info(f"EXAMPLE 3: Analisi giocatore {player_name}")
    
    # Vittorie come winner
    wins = df[df['winner_name'] == player_name].copy()
    
    # Sconfitte come loser
    losses = df[df['loser_name'] == player_name].copy()
    
    logger.info(f"  Vittorie: {len(wins)}")
    logger.info(f"  Sconfitte: {len(losses)}")
    logger.info(f"  Win rate: {len(wins)/(len(wins)+len(losses))*100:.1f}%")
    
    # Performance per superficie
    for surface in ['Hard', 'Clay', 'Grass']:
        surface_wins = wins[wins['surface'] == surface]
        surface_losses = losses[losses['surface'] == surface]
        total = len(surface_wins) + len(surface_losses)
        if total > 0:
            rate = len(surface_wins) / total * 100
            logger.info(f"  {surface}: {len(surface_wins)}-{len(surface_losses)} ({rate:.0f}%)")
    
    # Grand Slams
    gs_wins = wins[wins['tourney_level_name'] == 'Grand Slam']
    logger.info(f"  Grand Slam Wins: {len(gs_wins)}")
    
    return {
        'wins': len(wins),
        'losses': len(losses),
        'win_rate': len(wins) / (len(wins) + len(losses)) if len(wins) + len(losses) > 0 else 0,
        'grand_slam_wins': len(gs_wins)
    }


# ================================================================
# EXAMPLE 4: Confronto head-to-head
# ================================================================
def example_4_head_to_head(df: 'pd.DataFrame', player1: str, player2: str):
    """Confronta head-to-head tra due giocatori"""
    logger.info(f"EXAMPLE 4: Head-to-head {player1} vs {player2}")
    
    # Match dove player1 ha vinto
    p1_wins = df[(df['winner_name'] == player1) & (df['loser_name'] == player2)]
    
    # Match dove player2 ha vinto
    p2_wins = df[(df['winner_name'] == player2) & (df['loser_name'] == player1)]
    
    logger.info(f"  {player1}: {len(p1_wins)} vittorie")
    logger.info(f"  {player2}: {len(p2_wins)} vittorie")
    
    if not p1_wins.empty or not p2_wins.empty:
        logger.info(f"  Record: {len(p1_wins)}-{len(p2_wins)}")
        logger.info(f"  Ultimi match: {p1_wins['tourney_date'].max() if not p1_wins.empty else p2_wins['tourney_date'].max()}")
    
    return {
        'player1_wins': len(p1_wins),
        'player2_wins': len(p2_wins),
        'recent_matches': len(p1_wins) + len(p2_wins)
    }


# ================================================================
# EXAMPLE 5: Analisi trend temporale
# ================================================================
def example_5_temporal_analysis(df: 'pd.DataFrame'):
    """Analizza trend nel tempo"""
    logger.info("EXAMPLE 5: Analisi temporale")
    
    # Top player per ogni anno
    for year in sorted(df['year'].unique())[-5:]:  # Ultimi 5 anni
        year_df = df[df['year'] == year]
        top_player = year_df['winner_name'].value_counts().index[0]
        wins = year_df['winner_name'].value_counts().iloc[0]
        
        logger.info(f"  {year}: {top_player} ({int(wins)} wins)")
    
    # Trend superficie preferita
    logger.info("\n  Trend superficie:")
    for year in sorted(df['year'].unique())[-3:]:
        year_df = df[df['year'] == year]
        surface_dist = year_df['surface'].value_counts()
        logger.info(f"    {year}: {dict(surface_dist.head(2))}")


# ================================================================
# EXAMPLE 6: Custom visualization
# ================================================================
def example_6_custom_visualization(df: 'pd.DataFrame'):
    """Crea visualizzazione custom"""
    logger.info("EXAMPLE 6: Custom visualization")
    
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    # Top 10 giocatori
    top_players = df['winner_name'].value_counts().head(10)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(range(len(top_players)), top_players.values, color='steelblue')
    ax.set_yticks(range(len(top_players)))
    ax.set_yticklabels(top_players.index)
    ax.set_xlabel('Vittorie Totali')
    ax.set_title('Top 10 Giocatori - Custom Visualization')
    ax.invert_yaxis()
    
    output_path = config.VISUALS_DIR / "custom_top10.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    logger.info(f"  Salvato: {output_path}")
    plt.close()


# ================================================================
# EXAMPLE 7: Export statistics to CSV
# ================================================================
def example_7_export_statistics(df: 'pd.DataFrame'):
    """Esporta statistiche custom in CSV"""
    logger.info("EXAMPLE 7: Export statistiche")
    
    # Player stats
    player_stats = []
    
    for player in df['winner_name'].unique()[:100]:  # Top 100
        wins = len(df[df['winner_name'] == player])
        losses = len(df[df['loser_name'] == player])
        
        if wins + losses >= 20:  # Minimo match
            player_stats.append({
                'player': player,
                'wins': wins,
                'losses': losses,
                'total_matches': wins + losses,
                'win_rate': wins / (wins + losses),
                'tournaments': df[df['winner_name'] == player]['tourney_name'].nunique()
            })
    
    stats_df = pd.DataFrame(player_stats).sort_values('win_rate', ascending=False)
    
    output_path = config.OUTPUT_DIR / "player_statistics.csv"
    stats_df.to_csv(output_path, index=False)
    logger.info(f"  Salvato: {output_path}")
    logger.info(f"  Record esportati: {len(stats_df)}")
    
    return stats_df


# ================================================================
# MAIN: Run examples
# ================================================================
if __name__ == "__main__":
    logger.info("\n" + "="*60)
    logger.info("TENNIS STATS ANALYZER - ADVANCED EXAMPLES")
    logger.info("="*60 + "\n")
    
    # Download data
    logger.info("Downloading data...")
    df = download_atp_data(years=range(2015, 2026))
    
    if df.empty:
        logger.error("Failed to download data")
        sys.exit(1)
    
    # Clean data
    logger.info("Cleaning data...")
    df_clean = clean_atp_data(df)
    
    # Run examples
    # example_1_download_specific_year()
    # example_2_custom_cleaning()
    
    if not df_clean.empty:
        logger.info("\nRunning player analysis examples...\n")
        example_3_player_analysis(df_clean, "Novak Djokovic")
        example_3_player_analysis(df_clean, "Rafael Nadal")
        
        logger.info("\n" + "="*60)
        logger.info("Head-to-head examples:\n")
        example_4_head_to_head(df_clean, "Novak Djokovic", "Rafael Nadal")
        example_4_head_to_head(df_clean, "Roger Federer", "Novak Djokovic")
        example_4_head_to_head(df_clean, "Jannik Sinner", "Carlos Alcaraz")
        
        logger.info("\n" + "="*60)
        example_5_temporal_analysis(df_clean)
        
        logger.info("\n" + "="*60)
        example_6_custom_visualization(df_clean)
        
        logger.info("\n" + "="*60)
        example_7_export_statistics(df_clean)
    
    logger.info("\n✅ Tutti gli esempi completati!")
