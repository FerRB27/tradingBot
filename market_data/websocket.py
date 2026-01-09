# Trades en tiempo real (Binance)
from binance import ThreadedWebsocketManager
from config.secrets import API_KEY, API_SECRET
from market_data.range_builder import RangeBarBuilder

from indicators.ema import ema
from indicators.regression import linear_regression
from indicators.keltner import keltner_channel


RANGE_SIZE = 100


def start_trade_stream():
    range_builder = RangeBarBuilder(RANGE_SIZE)
    bars = []

    def handle_trade(msg):
        if msg["e"] != "trade":
            return

        price = float(msg["p"])
        completed_bar = range_builder.process_trade(price)

        if completed_bar:
            bars.append(completed_bar)

            closes = [b["close"] for b in bars]

            ema20 = ema(closes, 20)
            ema80 = ema(closes, 80)
            lr = linear_regression(closes, 89)
            kc = keltner_channel(bars)

            print("\n🟦 NUEVO RANGE BAR")
            print(
                f"O:{completed_bar['open']} "
                f"H:{completed_bar['high']} "
                f"L:{completed_bar['low']} "
                f"C:{completed_bar['close']}"
            )

            if ema20 and ema80:
                print(f"EMA20: {ema20:.2f} | EMA80: {ema80:.2f}")

            if lr:
                print(f"LR89: {lr[0]:.2f} | Pendiente: {lr[1]:.4f}")

            if kc:
                print(
                    f"Keltner → "
                    f"Upper: {kc['upper']:.2f} "
                    f"Basis: {kc['basis']:.2f} "
                    f"Lower: {kc['lower']:.2f}"
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

    print("🟢 MDC Bot | Range Bars + Indicadores activos")

    twm.join()
