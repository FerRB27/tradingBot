# Trades en tiempo real (Binance)
from binance import ThreadedWebsocketManager
from config.secrets import API_KEY, API_SECRET


def handle_trade(msg):
    if msg['e'] != 'trade':
        return

    price = float(msg['p'])
    qty = float(msg['q'])

    print(f"TRADE | Precio: {price} | Cantidad: {qty}")


def start_trade_stream():
    twm = ThreadedWebsocketManager(
        api_key=API_KEY,
        api_secret=API_SECRET,
        testnet=True
    )

    twm.start()

    twm.start_trade_socket(
        symbol="BTCUSDT",
        callback=handle_trade
    )

    print("🟢 Escuchando trades de BTCUSDT (Futures Testnet)...")

    twm.join()
