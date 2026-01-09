# Cambios de impulso MDC
def detect_impulse(prev_slope, current_slope):
    if prev_slope is None or current_slope is None:
        return None

    if prev_slope < 0 and current_slope > 0:
        return "BULLISH"

    if prev_slope > 0 and current_slope < 0:
        return "BEARISH"

    return None
