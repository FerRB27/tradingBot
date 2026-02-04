# Carga datos históricos para backtesting con velas
from binance.client import Client
from config.secrets import API_KEY, API_SECRET
from datetime import datetime


def load_klines(symbol="BTCUSDT", interval="5m", limit=500):
    """
    Carga velas históricas para backtesting con OrderBlocks
    
    Args:
        symbol: Par de trading (ej: BTCUSDT)
        interval: Intervalo de tiempo (1m, 5m, 15m, 1h, etc.)
        limit: Cantidad de velas (max 1500)
    
    Returns:
        Lista de velas en formato dict
    """
    client = Client(API_KEY, API_SECRET, testnet=True)
    
    klines = client.futures_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )
    
    # Convertir klines a formato de velas
    # Cada kline tiene: [open_time, open, high, low, close, volume, close_time, ...]
    candles = []
    
    for kline in klines:
        candle = {
            'timestamp': datetime.fromtimestamp(int(kline[0]) / 1000),
            'open': float(kline[1]),
            'high': float(kline[2]),
            'low': float(kline[3]),
            'close': float(kline[4]),
            'volume': float(kline[5])
        }
        candles.append(candle)
    
    return candles
