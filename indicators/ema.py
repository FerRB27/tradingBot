# EMA 20 / EMA 80
def ema(values, period):
    """Calcula EMA iniciando con SMA (igual que TradingView)"""
    if len(values) < period:
        return None

    k = 2 / (period + 1)
    
    # Inicializar con SMA de los primeros 'period' valores
    ema_value = sum(values[:period]) / period

    # Aplicar EMA al resto
    for price in values[period:]:
        ema_value = price * k + ema_value * (1 - k)

    return ema_value
