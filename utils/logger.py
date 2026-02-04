# Sistema de logging mejorado para OrderBlocks y errores
import logging
from datetime import datetime
import os

# Crear directorio de logs si no existe
os.makedirs('logs', exist_ok=True)


# === Logger para OrderBlocks ===
ob_logger = logging.getLogger('order_blocks')
ob_logger.setLevel(logging.INFO)

# Handler para archivo
ob_file_handler = logging.FileHandler('logs/order_blocks.log', encoding='utf-8')
ob_file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
)
ob_logger.addHandler(ob_file_handler)

# Handler para consola
ob_console_handler = logging.StreamHandler()
ob_console_handler.setFormatter(
    logging.Formatter('%(asctime)s - OB - %(message)s', '%H:%M:%S')
)
ob_logger.addHandler(ob_console_handler)


# === Logger para errores ===
error_logger = logging.getLogger('errors')
error_logger.setLevel(logging.ERROR)

error_file_handler = logging.FileHandler('logs/errors.log', encoding='utf-8')
error_file_handler.setFormatter(
    logging.Formatter('%(asctime)s - ERROR - %(message)s', '%Y-%m-%d %H:%M:%S')
)
error_logger.addHandler(error_file_handler)

error_console_handler = logging.StreamHandler()
error_console_handler.setFormatter(
    logging.Formatter('%(asctime)s - ❌ ERROR - %(message)s', '%H:%M:%S')
)
error_logger.addHandler(error_console_handler)


# === Logger general ===
info_logger = logging.getLogger('info')
info_logger.setLevel(logging.INFO)

info_file_handler = logging.FileHandler('logs/bot.log', encoding='utf-8')
info_file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
)
info_logger.addHandler(info_file_handler)


def log_order_block(ob_type, candle, additional_info=None):
    """
    Registra una alerta de OrderBlock
    
    Args:
        ob_type: 'bullish' o 'bearish'
        candle: dict con datos de la vela
        additional_info: dict con información adicional (opcional)
    """
    emoji = "🟢" if ob_type == "bullish" else "🔴"
    tipo_texto = "ALCISTA" if ob_type == "bullish" else "BAJISTA"
    
    message = f"{emoji} ORDER BLOCK {tipo_texto} detectado"
    message += f" | O: ${candle['open']:.2f} H: ${candle['high']:.2f} L: ${candle['low']:.2f} C: ${candle['close']:.2f}"
    
    if additional_info:
        if 'range' in additional_info:
            message += f" | Rango: ${additional_info['range']:.2f}"
        if 'timestamp' in additional_info:
            message += f" | Tiempo: {additional_info['timestamp']}"
    
    ob_logger.info(message)
    return message


def log_error(error_message, exception=None):
    """
    Registra un error
    
    Args:
        error_message: Descripción del error
        exception: Objeto de excepción (opcional)
    """
    if exception:
        error_logger.error(f"{error_message} - Exception: {str(exception)}")
    else:
        error_logger.error(error_message)


def log_info(message):
    """
    Registra información general
    
    Args:
        message: Mensaje a registrar
    """
    info_logger.info(message)
