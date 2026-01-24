#!/usr/bin/env python3
"""
Entry point principale - Tennis Stats Analyzer
Orchestrazione completa della pipeline: download → cleaning → analisi → visualizzazione
"""
import sys
from pathlib import Path

# Aggiungere src al path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from tennis_analyzer.logger import setup_logger
from tennis_analyzer.downloader import ATPDataDownloader
from tennis_analyzer.cleaner import ATPDataCleaner
from tennis_analyzer.analyzer import ATPAnalyzer
from tennis_analyzer.visualizer import ATPVisualizer
from tennis_analyzer import config

# Logger globale
logger = setup_logger(__name__)


def main():
    """
    Pipeline principale: scarica, pulisce, analizza, visualizza dati ATP.
    """
    logger.info("\n" + "="*70)
    logger.info("  TENNIS STATS ANALYZER - ATP Data Pipeline")
    logger.info("  Data Engineer: Professional Analysis Framework")
    logger.info("="*70)
    
    try:
        # =====================================================
        # STEP 1: DOWNLOAD DATA
        # =====================================================
        logger.info("\n" + "▶"*35)
        logger.info("STEP 1: DOWNLOAD ATP DATA")
        logger.info("▶"*35)
        
        downloader = ATPDataDownloader()
        df_raw = downloader.get_consolidated_data(use_local=True)
        
        if df_raw.empty:
            logger.error("❌ Errore: Nessun dato scaricato")
            return False
        
        logger.info(f"\n✓ Raw data caricati: {len(df_raw)} record")
        logger.info(f"  Data range: {df_raw['tourney_date'].min()} → {df_raw['tourney_date'].max()}")
        
        # =====================================================
        # STEP 2: DATA CLEANING
        # =====================================================
        logger.info("\n" + "▶"*35)
        logger.info("STEP 2: DATA CLEANING & NORMALIZATION")
        logger.info("▶"*35)
        
        cleaner = ATPDataCleaner()
        df_clean = cleaner.process_pipeline(df_raw)
        
        if df_clean.empty:
            logger.error("❌ Errore: Cleaning fallito")
            return False
        
        # Salvare dataset pulito
        clean_csv_path = config.CLEAN_DATA_CSV
        df_clean.to_csv(clean_csv_path, index=False)
        logger.info(f"\n✓ Dataset pulito salvato: {clean_csv_path}")
        logger.info(f"  Dimensione finale: {len(df_clean)} record")
        logger.info(f"  Colonne: {df_clean.shape[1]}")
        
        # =====================================================
        # STEP 3: EXPLORATORY DATA ANALYSIS
        # =====================================================
        logger.info("\n" + "▶"*35)
        logger.info("STEP 3: EXPLORATORY DATA ANALYSIS (EDA)")
        logger.info("▶"*35)
        
        analyzer = ATPAnalyzer(df_clean)
        analysis_results = analyzer.run_full_analysis()
        
        # =====================================================
        # STEP 4: VISUALIZATION
        # =====================================================
        logger.info("\n" + "▶"*35)
        logger.info("STEP 4: GENERATE VISUALIZATIONS")
        logger.info("▶"*35)
        
        visualizer = ATPVisualizer()
        visualizer.generate_all_plots(df_clean, analysis_results)
        
        # =====================================================
        # SUMMARY
        # =====================================================
        logger.info("\n" + "="*70)
        logger.info("  PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("="*70)
        
        logger.info("\n📊 OUTPUT SUMMARY:")
        logger.info(f"  Clean Data (CSV): {clean_csv_path}")
        logger.info(f"  Visualizations (PNG):")
        
        visuals = [
            config.RANKING_EVOLUTION_PNG,
            config.WINS_BY_PLAYER_PNG,
            config.WINS_BY_SURFACE_PNG,
            config.MATCH_DISTRIBUTION_PNG,
            config.WIN_RATE_ANALYSIS_PNG,
        ]
        
        for viz_file in visuals:
            if viz_file.exists():
                logger.info(f"    ✓ {viz_file.name}")
        
        logger.info("\n📁 Output Directory:")
        logger.info(f"  {config.OUTPUT_DIR}")
        
        logger.info("\n✅ Analysis Ready for Presentation/Reporting!")
        
        return True
    
    except Exception as e:
        logger.error(f"\n❌ ERRORE CRITICO: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
