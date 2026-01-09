# EMA 20 / EMA 80
def ema(values, period):
    if len(values) < period:
        return None

    k = 2 / (period + 1)
    ema_value = values[0]

    for price in values[1:]:
        ema_value = price * k + ema_value * (1 - k)

    return ema_value
