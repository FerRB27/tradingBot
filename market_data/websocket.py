# Trades en tiempo real (Binance)
from binance import ThreadedWebsocketManager
from config.secrets import API_KEY, API_SECRET
from market_data.range_builder import RangeBarBuilder


RANGE_SIZE = 100  # dólares


def start_trade_stream():
    range_builder = RangeBarBuilder(RANGE_SIZE)

    def handle_trade(msg):
        if msg["e"] != "trade":
            return

        price = float(msg["p"])

        completed_bar = range_builder.process_trade(price)

        if completed_bar:
            print(
                f"RANGE BAR | "
                f"O:{completed_bar['open']} "
                f"H:{completed_bar['high']} "
                f"L:{completed_bar['low']} "
                f"C:{completed_bar['close']}"
            )

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

    print("🟢 Construyendo Range Bars de BTCUSDT (100R)")

    twm.join()
