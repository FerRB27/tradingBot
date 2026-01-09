# Trades en tiempo real (Binance)
from binance import ThreadedWebsocketManager
from config.secrets import API_KEY, API_SECRET
from market_data.range_builder import RangeBarBuilder

from indicators.ema import ema
from indicators.regression import linear_regression
from indicators.keltner import keltner_channel

from strategy.impulses import detect_impulse
from strategy.entries import entry_A1


RANGE_SIZE = 100


def start_trade_stream():
    range_builder = RangeBarBuilder(RANGE_SIZE)
    bars = []
    slopes = []

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
            slope = lr[1] if lr else None
            slopes.append(slope)

            kc = keltner_channel(bars)

            impulse = None
            if len(slopes) >= 2:
                impulse = detect_impulse(slopes[-2], slopes[-1])

            signal = entry_A1(
                impulse=impulse,
                price=completed_bar["close"],
                ema20=ema20,
                ema80=ema80,
                keltner=kc
            )

            print("\n🟦 RANGE BAR")
            print(f"O:{completed_bar['open']} C:{completed_bar['close']}")

            if impulse:
                print(f"IMPULSO: {impulse}")

            if signal:
                print(f"🚨 SEÑAL MDC → {signal}")

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

    print("🟢 MDC Bot | Impulsos + A1 activos")

    twm.join()
