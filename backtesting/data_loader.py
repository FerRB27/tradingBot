# Carga datos históricos para backtesting
from binance.client import Client
from config.secrets import API_KEY, API_SECRET


def load_trades(symbol="BTCUSDT", limit=1000):
    """
    Carga trades recientes (solo útil para datos muy recientes)
    Nota: 1000 trades pueden cubrir solo unos minutos de mercado
    """
    client = Client(API_KEY, API_SECRET, testnet=True)

    trades = client.futures_recent_trades(
        symbol=symbol,
        limit=limit
    )

    return [
        {
            "price": float(t["price"]),
            "qty": float(t["qty"])
        }
        for t in trades
    ]


def load_klines(symbol="BTCUSDT", interval="1m", limit=1000):
    """
    Carga velas históricas (más eficiente para backtesting)
    
    Args:
        symbol: Par de trading (ej: BTCUSDT)
        interval: Intervalo de tiempo (1m, 5m, 15m, 1h, etc.)
        limit: Cantidad de velas (max 1500)
    
    Returns:
        Lista de trades extraídos de las velas para construir Range Bars
    """
    client = Client(API_KEY, API_SECRET, testnet=True)
    
    klines = client.futures_klines(
        symbol=symbol,
        interval=interval,
        limit=limit
    )
    
    # Convertir klines a formato de trades para RangeBarBuilder
    # Cada kline tiene: [open_time, open, high, low, close, volume, ...]
    trades = []
    
    for kline in klines:
        open_price = float(kline[1])
        high_price = float(kline[2])
        low_price = float(kline[3])
        close_price = float(kline[4])
        
        # Simular trades: open -> high -> low -> close
        trades.append({"price": open_price, "qty": 0.01})
        trades.append({"price": high_price, "qty": 0.01})
        trades.append({"price": low_price, "qty": 0.01})
        trades.append({"price": close_price, "qty": 0.01})
    
    return trades
