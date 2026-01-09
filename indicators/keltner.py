# KC 52 (3.5)
from indicators.ema import ema


def atr(bars, period):
    if len(bars) < period + 1:
        return None

    trs = []

    for i in range(1, period + 1):
        high = bars[-i]["high"]
        low = bars[-i]["low"]
        prev_close = bars[-i - 1]["close"]

        tr = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )
        trs.append(tr)

    return sum(trs) / period


def keltner_channel(bars, period=52, mult=3.5):
    closes = [bar["close"] for bar in bars]

    basis = ema(closes, period)
    atr_value = atr(bars, period)

    if basis is None or atr_value is None:
        return None

    upper = basis + mult * atr_value
    lower = basis - mult * atr_value

    return {
        "basis": basis,
        "upper": upper,
        "lower": lower
    }
