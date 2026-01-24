"""
Logging centralizzato per il progetto Tennis Stats Analyzer
"""
import logging
import sys
from pathlib import Path

def setup_logger(name: str, log_level: int = logging.INFO) -> logging.Logger:
    """
    Configura un logger con output su console e file.
    
    Args:
        name: Nome del logger (tipicamente __name__)
        log_level: Livello logging (default: INFO)
    
    Returns:
        Logger configurato
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Evita duplicate handlers
    if logger.handlers:
        return logger
    
    # Formato log
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Handler console (output colorato è opzionale)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


# Logger globale per il modulo
logger = setup_logger(__name__)
