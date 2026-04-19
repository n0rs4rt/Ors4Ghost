
import logging
from core.RUTAS import *

def configurar_logging():
    logger = logging.getLogger("LOGS")
    
    if logger.handlers:
        return logger

    logging.basicConfig(
        filename=(ruta_log / "logs.txt"),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logger


