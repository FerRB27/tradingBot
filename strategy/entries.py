# A1, A2, A3
def entry_A1(
    impulse,
    price,
    ema20,
    ema80,
    keltner
):
    if not impulse or not ema20 or not ema80 or not keltner:
        return None

    # A1 LONG
    if (
        impulse == "BULLISH"
        and price > ema20
        and ema20 > ema80
        and price >= keltner["basis"]
    ):
        return "LONG_A1"

    # A1 SHORT
    if (
        impulse == "BEARISH"
        and price < ema20
        and ema20 < ema80
        and price <= keltner["basis"]
    ):
        return "SHORT_A1"

    return None
