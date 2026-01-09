# Simulación MDC / Ejecuta estrategia y mide resultados
from backtesting.data_loader import load_trades
from backtesting.range_replay import build_range_bars

from indicators.ema import ema
from indicators.regression import linear_regression
from indicators.keltner import keltner_channel

from strategy.impulses import detect_impulse
from strategy.entries import entry_A1


RANGE_SIZE = 100


def run_backtest():
    trades = load_trades()
    bars = build_range_bars(trades, RANGE_SIZE)

    closes = []
    slopes = []

    position = None
    entry_price = None
    stop_loss = None
    take_profit = None

    results = []

    for i, bar in enumerate(bars):
        closes.append(bar["close"])

        ema20 = ema(closes, 20)
        ema80 = ema(closes, 80)

        lr = linear_regression(closes, 89)
        slope = lr[1] if lr else None
        slopes.append(slope)

        kc = keltner_channel(bars[:i+1])

        impulse = None
        if len(slopes) >= 2:
            impulse = detect_impulse(slopes[-2], slopes[-1])

        signal = entry_A1(
            impulse,
            bar["close"],
            ema20,
            ema80,
            kc
        )

        # --- ENTRADA ---
        if not position and signal:
            position = signal
            entry_price = bar["close"]

            if signal == "LONG_A1":
                stop_loss = bar["low"]
                take_profit = entry_price + (entry_price - stop_loss) * 1.5

            if signal == "SHORT_A1":
                stop_loss = bar["high"]
                take_profit = entry_price - (stop_loss - entry_price) * 1.5

        # --- GESTIÓN ---
        if position == "LONG_A1":
            if bar["low"] <= stop_loss:
                results.append(-1)
                position = None
            elif bar["high"] >= take_profit:
                results.append(1.5)
                position = None

        if position == "SHORT_A1":
            if bar["high"] >= stop_loss:
                results.append(-1)
                position = None
            elif bar["low"] <= take_profit:
                results.append(1.5)
                position = None

    print_results(results)


def print_results(results):
    total = len(results)
    wins = len([r for r in results if r > 0])
    losses = len([r for r in results if r < 0])

    net = sum(results)

    print("\n📊 BACKTEST RESULTADOS")
    print(f"Trades: {total}")
    print(f"Ganadores: {wins}")
    print(f"Perdedores: {losses}")
    print(f"Win Rate: {wins / total * 100:.2f}%" if total else "N/A")
    print(f"Resultado neto (R): {net:.2f}")


if __name__ == "__main__":
    run_backtest()
