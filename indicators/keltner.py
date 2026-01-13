# KC 52 (3.5)
from indicators.ema import ema


def atr(bars, period):
    """Calcula ATR usando EMA del True Range (igual que TradingView)"""
    if len(bars) < period + 1:
        return None

    trs = []

    for i in range(len(bars) - 1, 0, -1):
        high = bars[i]["high"]
        low = bars[i]["low"]
        prev_close = bars[i - 1]["close"]

        tr = max(
            high - low,
            abs(high - prev_close),
            abs(low - prev_close)
        )
        trs.append(tr)

    if len(trs) < period:
        return None

    # ATR es una EMA del True Range
    k = 2 / (period + 1)
    
    # Inicializar con SMA de los primeros 'period' valores
    atr_value = sum(trs[:period]) / period
    
    # Aplicar EMA al resto
    for tr in trs[period:]:
        atr_value = tr * k + atr_value * (1 - k)

    return atr_value


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
