# Demo Backtest con datos simulados (sin conexión a Binance)
import random
from backtesting.range_replay import build_range_bars
from indicators.regression import linear_regression
from indicators.keltner import keltner_channel
from strategy.impulses import detect_impulse
from strategy.entries import A1Strategy
from risk.stop_take import calculate_sl_tp


RANGE_SIZE = 100


def generate_demo_price_data(start_price=94000, num_points=10000):
    """
    Genera datos de precio simulados con tendencias más marcadas
    Para asegurar que se generen señales A1
    """
    prices = []
    price = start_price
    trend = 1
    trend_duration = 0
    
    for i in range(num_points):
        # Cambiar tendencia cada 200-400 puntos para crear impulsos
        if trend_duration > random.randint(200, 400):
            # Cambio de tendencia (crea impulsos)
            trend = -trend
            trend_duration = 0
        
        # Movimiento del precio con tendencia
        trend_component = trend * random.uniform(2, 5)
        noise = random.uniform(-3, 3)
        price = price + trend_component + noise
        
        # Evitar precios negativos
        price = max(price, 10000)
        
        prices.append({"price": price, "qty": 0.01})
        trend_duration += 1
    
    return prices


def run_demo_backtest():
    """
    Ejecuta backtest con datos simulados
    """
    print("🎲 Generando datos de precio simulados con tendencias...")
    trades = generate_demo_price_data(start_price=94000, num_points=10000)
    print(f"✅ {len(trades)} puntos de precio generados")
    
    prices = [t["price"] for t in trades]
    print(f"   Rango: ${min(prices):.2f} - ${max(prices):.2f}")
    print(f"   Diferencia: ${max(prices) - min(prices):.2f}\n")
    
    print(f"🔨 Construyendo Range Bars ({RANGE_SIZE} puntos)...")
    bars = build_range_bars(trades, RANGE_SIZE)
    print(f"✅ {len(bars)} Range Bars generadas\n")

    slopes = []
    closes = []
    
    # Inicializar estrategia A1
    a1_strategy = A1Strategy()

    position = None
    entry_price = None
    stop_loss = None
    take_profit = None

    results = []
    trade_count = 0
    
    # Contadores para debug
    impulses_detected = 0
    setups_detected = 0

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
                impulses_detected += 1
                a1_strategy.set_impulse(impulse)
                if impulses_detected <= 5:  # Mostrar primeros 5 impulsos
                    print(f"⚡ Impulso #{impulses_detected}: {impulse} en barra #{i+1}")

        # Evaluar señal A1
        signal = a1_strategy.evaluate(
            bar=bar,
            lr_value=lr_value,
            lr_slope=lr_slope,
            keltner=kc
        )

        # --- ENTRADA ---
        if not position and signal:
            trade_count += 1
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
                
                print(f"\n🚨 TRADE #{trade_count} - {signal} @ ${entry_price:.2f}")
                print(f"   📍 Barra #{i+1}")
                print(f"   🛑 SL: ${stop_loss:.2f} (-${sl_tp['risk_distance']:.2f})")
                print(f"   🎯 TP: ${take_profit:.2f} (+${sl_tp['reward_distance']:.2f})")

        # --- GESTIÓN ---
        if position == "LONG_A1":
            if bar["low"] <= stop_loss:
                results.append(-1)  # Pérdida de 1R
                print(f"   ❌ Stop Loss alcanzado @ ${bar['low']:.2f}")
                position = None
            elif bar["high"] >= take_profit:
                results.append(2)  # Ganancia de 2R
                print(f"   ✅ Take Profit alcanzado @ ${bar['high']:.2f}")
                position = None

        if position == "SHORT_A1":
            if bar["high"] >= stop_loss:
                results.append(-1)  # Pérdida de 1R
                print(f"   ❌ Stop Loss alcanzado @ ${bar['high']:.2f}")
                position = None
            elif bar["low"] <= take_profit:
                results.append(2)  # Ganancia de 2R
                print(f"   ✅ Take Profit alcanzado @ ${bar['low']:.2f}")
                position = None

    print(f"\n📈 Estadísticas de detección:")
    print(f"   Impulsos detectados: {impulses_detected}")
    print(f"   Señales A1 generadas: {trade_count}")
    
    print_results(results)


def print_results(results):
    total = len(results)
    wins = len([r for r in results if r > 0])
    losses = len([r for r in results if r < 0])

    net = sum(results)
    
    win_rate = (wins / total * 100) if total > 0 else 0
    expectancy = (net / total) if total > 0 else 0

    print("\n" + "="*60)
    print("📊 DEMO BACKTEST - ESTRATEGIA A1 MDC (DATOS SIMULADOS)")
    print("="*60)
    print(f"Total Trades:     {total}")
    print(f"Ganadores:        {wins} ({win_rate:.1f}%)")
    print(f"Perdedores:       {losses} ({100-win_rate:.1f}%)")
    print(f"Resultado Neto:   {net:+.2f}R")
    print(f"Expectativa:      {expectancy:+.2f}R por trade")
    print("="*60)
    
    if total > 0:
        print("\n💡 Nota: Estos son datos simulados para demostración.")
        print("   Para backtest real, ejecuta: python -m backtesting.backtest")


if __name__ == "__main__":
    run_demo_backtest()
