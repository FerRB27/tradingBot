# Carga trades históricos
from binance.client import Client
from config.secrets import API_KEY, API_SECRET


def load_trades(symbol="BTCUSDT", limit=1000):
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
