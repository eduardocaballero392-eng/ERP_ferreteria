"""
Core module - Configuración central de la aplicación
"""
from .config import settings
from .csv_handler import CSVHandler, get_csv_handler

__all__ = ["settings", "CSVHandler", "get_csv_handler"]
