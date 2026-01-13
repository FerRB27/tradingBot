# Simulación MDC / Ejecuta estrategia y mide resultados
from backtesting.data_loader import load_klines
from backtesting.range_replay import build_range_bars

from indicators.regression import linear_regression
from indicators.keltner import keltner_channel

from strategy.impulses import detect_impulse
from strategy.entries import A1Strategy, A2Strategy, A3Strategy
from risk.stop_take import calculate_sl_tp


RANGE_SIZE = 100


def run_backtest(interval="1m", limit=1000):
    """
    Ejecuta backtest de estrategias A1, A2 y A3
    
    Args:
        interval: Intervalo de velas (1m, 5m, 15m, 1h, etc.)
        limit: Cantidad de velas a cargar (max 1500)
    """
    print("📥 Cargando datos históricos de Binance...")
    trades = load_klines(interval=interval, limit=limit)
    print(f"✅ {len(trades)} puntos de precio cargados ({limit} velas de {interval})")
    
    print(f"🔨 Construyendo Range Bars ({RANGE_SIZE} puntos)...")
    bars = build_range_bars(trades, RANGE_SIZE)
    print(f"✅ {len(bars)} Range Bars generadas\n")
    
    if len(bars) < 100:
        print(f"⚠️ Advertencia: Solo {len(bars)} barras disponibles. Se necesitan al menos 89 para LR.")
        print(f"   Intenta aumentar 'limit' o usar un intervalo más pequeño (ej: 1m)\n")

    slopes = []
    closes = []
    
    # Inicializar estrategias A1, A2 y A3
    a1_strategy = A1Strategy()
    a2_strategy = A2Strategy()
    a3_strategy = A3Strategy()

    position = None
    entry_price = None
    stop_loss = None
    take_profit = None

    results = []

    for i, bar in enumerate(bars):
        closes.append(bar["close"])

        # Calcular Linear Regression 89
        lr = linear_regression(closes, 89)
        lr_value = lr[0] if lr else None
        lr_slope = lr[1] if lr else None
        slopes.append(lr_slope)

        # Calcular Keltner Channel 52 (3.5)
        kc = keltner_channel(bars[:i+1])

        # Detectar impulsos
        impulse = None
        if len(slopes) >= 2:
            impulse = detect_impulse(slopes[-2], slopes[-1])
            if impulse:
                a1_strategy.set_impulse(impulse)
                a2_strategy.set_impulse(impulse)
                a3_strategy.set_impulse(impulse)

        # Evaluar señales A1, A2 y A3 (prioridad A1 > A2 > A3)
        signal_a1 = a1_strategy.evaluate(
            bar=bar,
            lr_value=lr_value,
            lr_slope=lr_slope,
            keltner=kc
        )
        
        signal_a2 = a2_strategy.evaluate(
            bar=bar,
            lr_value=lr_value,
            lr_slope=lr_slope,
            keltner=kc
        )
        
        signal_a3 = a3_strategy.evaluate(
            bar=bar,
            lr_value=lr_value,
            lr_slope=lr_slope,
            keltner=kc
        )
        
        signal = signal_a1 or signal_a2 or signal_a3

        # --- ENTRADA ---
        if not position and signal:
            position = signal
            entry_price = bar["close"]

            # Calcular SL y TP con ratio 2:1
            sl_tp = calculate_sl_tp(
                entry_price=entry_price,
                signal_type=signal,
                keltner=kc,
                risk_percentage=0.01
            )
            
            if sl_tp:
                stop_loss = sl_tp["stop_loss"]
                take_profit = sl_tp["take_profit"]
                
                print(f"\n🚨 {signal} @ {entry_price:.2f}")
                print(f"   SL: {stop_loss:.2f} | TP: {take_profit:.2f}")

        # --- GESTIÓN ---
        if position and position.startswith("LONG"):
            if bar["low"] <= stop_loss:
                results.append(-1)  # Pérdida de 1R
                print(f"   ❌ Stop Loss alcanzado @ {bar['low']:.2f}")
                position = None
            elif bar["high"] >= take_profit:
                results.append(2)  # Ganancia de 2R
                print(f"   ✅ Take Profit alcanzado @ {bar['high']:.2f}")
                position = None

        if position and position.startswith("SHORT"):
            if bar["high"] >= stop_loss:
                results.append(-1)  # Pérdida de 1R
                print(f"   ❌ Stop Loss alcanzado @ {bar['high']:.2f}")
                position = None
            elif bar["low"] <= take_profit:
                results.append(2)  # Ganancia de 2R
                print(f"   ✅ Take Profit alcanzado @ {bar['low']:.2f}")
                position = None

    print_results(results)


def print_results(results):
    total = len(results)
    wins = len([r for r in results if r > 0])
    losses = len([r for r in results if r < 0])

    net = sum(results)
    
    win_rate = (wins / total * 100) if total > 0 else 0
    expectancy = (net / total) if total > 0 else 0

    print("\n" + "="*50)
    print("📊 BACKTEST RESULTADOS - ESTRATEGIA A1 MDC")
    print("="*50)
    print(f"Total Trades:     {total}")
    print(f"Ganadores:        {wins} ({win_rate:.1f}%)")
    print(f"Perdedores:       {losses} ({100-win_rate:.1f}%)")
    print(f"Resultado Neto:   {net:+.2f}R")
    print(f"Expectativa:      {expectancy:+.2f}R por trade")
    print("="*50)


if __name__ == "__main__":
    # Ejecutar backtest con velas de 1 minuto (últimas 1500)
    # Puedes cambiar a "5m", "15m", "1h" para diferentes períodos
    run_backtest(interval="1m", limit=1500)
