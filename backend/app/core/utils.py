"""
Utilidades generales para la aplicación
"""
from datetime import datetime
from typing import Optional


def calcular_igv(subtotal: float, tasa_igv: float = 0.18) -> float:
    """
    Calcula el IGV (Impuesto General a las Ventas) de Perú
    
    Args:
        subtotal: Monto sin IGV
        tasa_igv: Tasa de IGV (por defecto 18% = 0.18)
    
    Returns:
        Monto del IGV
    """
    return round(subtotal * tasa_igv, 2)


def calcular_total_con_igv(subtotal: float, tasa_igv: float = 0.18) -> float:
    """
    Calcula el total incluyendo IGV
    
    Args:
        subtotal: Monto sin IGV
        tasa_igv: Tasa de IGV (por defecto 18% = 0.18)
    
    Returns:
        Total con IGV incluido
    """
    igv = calcular_igv(subtotal, tasa_igv)
    return round(subtotal + igv, 2)


def obtener_estado_stock(stock_actual: int, stock_minimo: int) -> str:
    """
    Determina el estado del stock de un producto
    
    Args:
        stock_actual: Cantidad actual en stock
        stock_minimo: Cantidad mínima requerida
    
    Returns:
        Estado: 'AGOTADO', 'REPONER', 'OK'
    """
    if stock_actual <= 0:
        return "AGOTADO"
    elif stock_actual <= stock_minimo:
        return "REPONER"
    else:
        return "OK"


def formatear_fecha_peru(fecha: datetime) -> str:
    """
    Formatea una fecha en el formato usado en Perú (dd/mm/yyyy)
    
    Args:
        fecha: Objeto datetime
    
    Returns:
        Fecha formateada como string
    """
    return fecha.strftime("%d/%m/%Y %H:%M:%S")


def validar_ruc(ruc: str) -> bool:
    """
    Valida formato básico de RUC peruano (11 dígitos)
    
    Args:
        ruc: Número de RUC
    
    Returns:
        True si el formato es válido
    """
    if not ruc:
        return False
    
    # RUC debe tener 11 dígitos
    if len(ruc) != 11:
        return False
    
    # Debe ser numérico
    if not ruc.isdigit():
        return False
    
    # Debe empezar con 10, 15, 17 o 20
    prefijos_validos = ["10", "15", "17", "20"]
    if ruc[:2] not in prefijos_validos:
        return False
    
    return True


def validar_dni(dni: str) -> bool:
    """
    Valida formato básico de DNI peruano (8 dígitos)
    
    Args:
        dni: Número de DNI
    
    Returns:
        True si el formato es válido
    """
    if not dni:
        return False
    
    # DNI debe tener 8 dígitos
    if len(dni) != 8:
        return False
    
    # Debe ser numérico
    return dni.isdigit()
