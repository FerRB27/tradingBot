"""
Demo del Trade 80 - Entrada en desarrollo de tendencia

Este script demuestra cómo funciona el Trade 80 en Fase 1 y Fase 4
"""

from strategy.signals import TradingSignalGenerator


def demo_trade80_long():
    """
    Ejemplo de entrada LONG con Trade 80
    """
    print("=" * 80)
    print("DEMO: Trade 80 LONG - Desarrollo de Tendencia Alcista")
    print("=" * 80)
    print()
    
    # Inicializar generador
    signal_gen = TradingSignalGenerator(tick_size=1.0)
    
    # Escenario: Tendencia alcista establecida (Fase 1)
    print("📊 ESCENARIO: Tendencia alcista establecida (Fase 1)")
    print()
    
    bars = [
        # Fase 1: Tendencia alcista
        {"open": 50000, "high": 50100, "low": 50000, "close": 50095},
        {"open": 50095, "high": 50200, "low": 50090, "close": 50190},
        {"open": 50190, "high": 50250, "low": 50185, "close": 50240},
        
        # Retroceso a EMA 80
        {"open": 50240, "high": 50250, "low": 50150, "close": 50160},  # Toca EMA80
    ]
    
    # Valores simulados
    scenarios = [
        {
            "lr": (50050, 15.0),
            "keltner": {"upper": 50280, "basis": 50150, "lower": 50020},
            "ema80": (50080, 2.5),  # EMA80 debajo de basis con slope alcista
        },
        {
            "lr": (50150, 18.0),
            "keltner": {"upper": 50350, "basis": 50200, "lower": 50050},
            "ema80": (50110, 3.0),
        },
        {
            "lr": (50220, 20.0),
            "keltner": {"upper": 50400, "basis": 50250, "lower": 50100},
            "ema80": (50140, 3.2),
        },
        {
            "lr": (50200, 8.0),
            "keltner": {"upper": 50380, "basis": 50240, "lower": 50100},
            "ema80": (50155, 1.5),  # Precio retrocede y toca EMA80
        }
    ]
    
    for i, (bar, scenario) in enumerate(zip(bars, scenarios), 1):
        print(f"\n{'='*70}")
        print(f"BARRA #{i}")
        print(f"{'='*70}")
        print(f"OHLC: O={bar['open']:.0f} H={bar['high']:.0f} L={bar['low']:.0f} C={bar['close']:.0f}")
        
        lr_value, lr_slope = scenario["lr"]
        keltner = scenario["keltner"]
        ema80_value, ema80_slope = scenario["ema80"]
        
        print(f"\nIndicadores:")
        print(f"  LR: {lr_value:.0f} (slope: {lr_slope:.1f})")
        print(f"  KC: Upper={keltner['upper']:.0f} | Basis={keltner['basis']:.0f} | Lower={keltner['lower']:.0f}")
        print(f"  EMA80: {ema80_value:.0f} (slope: {ema80_slope:.1f})")
        
        # Verificar condiciones Trade 80 LONG
        espacio = keltner['basis'] - ema80_value
        print(f"\n✓ Análisis Trade 80:")
        print(f"  • EMA80 < KC Basis: {ema80_value < keltner['basis']} ({'✅' if ema80_value < keltner['basis'] else '❌'})")
        print(f"  • LR alcista/plana: {lr_slope > -0.5} ({'✅' if lr_slope > -0.5 else '❌'})")
        print(f"  • EMA80 alcista/plana: {ema80_slope > -0.5} ({'✅' if ema80_slope > -0.5 else '❌'})")
        print(f"  • Espacio > 3 ticks: {espacio:.0f} puntos ({'✅' if espacio > 3 else '❌'})")
        print(f"  • Precio toca EMA80: {bar['low'] <= ema80_value <= bar['high']} ({'✅' if bar['low'] <= ema80_value <= bar['high'] else '❌'})")
        
        # Generar señal
        signal = signal_gen.generate_signal(
            bar=bar,
            lr_value=lr_value,
            lr_slope=lr_slope,
            keltner=keltner,
            ema80_value=ema80_value
        )
        
        if signal:
            print(f"\n🎯 SEÑAL DETECTADA: {signal['type']} {signal['direction']}")
            print(f"   Fase: {signal['phase_description']}")
            print(f"   Entry: {signal['entry']:.0f}")
            print(f"   Stop Loss: {signal['stop_loss']:.0f}")
            print(f"   Take Profit: {signal['take_profit']:.0f}")
            print(f"   Risk: {signal['risk']:.0f}")
            print(f"   Reward: {signal['reward']:.0f}")
            print(f"   Ratio: 1:{signal['ratio']:.0f}")
        else:
            print(f"\n⏳ Sin señal (esperando setup o entrada)")


def demo_trade80_short():
    """
    Ejemplo de entrada SHORT con Trade 80
    """
    print("\n\n" + "=" * 80)
    print("DEMO: Trade 80 SHORT - Desarrollo de Tendencia Bajista")
    print("=" * 80)
    print()
    
    signal_gen = TradingSignalGenerator(tick_size=1.0)
    
    print("📊 ESCENARIO: Tendencia bajista establecida (Fase 1)")
    print()
    
    bars = [
        # Fase 1: Tendencia bajista
        {"open": 50000, "high": 50010, "low": 49900, "close": 49905},
        {"open": 49905, "high": 49920, "low": 49800, "close": 49810},
        {"open": 49810, "high": 49820, "low": 49700, "close": 49710},
        
        # Retroceso a EMA 80
        {"open": 49710, "high": 49850, "low": 49700, "close": 49840},  # Toca EMA80
    ]
    
    scenarios = [
        {
            "lr": (49950, -15.0),
            "keltner": {"upper": 50050, "basis": 49900, "lower": 49750},
            "ema80": (49950, -2.5),  # EMA80 sobre basis con slope bajista
        },
        {
            "lr": (49850, -18.0),
            "keltner": {"upper": 49980, "basis": 49820, "lower": 49660},
            "ema80": (49910, -3.0),
        },
        {
            "lr": (49750, -20.0),
            "keltner": {"upper": 49880, "basis": 49730, "lower": 49580},
            "ema80": (49870, -3.2),
        },
        {
            "lr": (49780, -8.0),
            "keltner": {"upper": 49910, "basis": 49760, "lower": 49610},
            "ema80": (49845, -1.5),  # Precio retrocede y toca EMA80
        }
    ]
    
    for i, (bar, scenario) in enumerate(zip(bars, scenarios), 1):
        print(f"\n{'='*70}")
        print(f"BARRA #{i}")
        print(f"{'='*70}")
        print(f"OHLC: O={bar['open']:.0f} H={bar['high']:.0f} L={bar['low']:.0f} C={bar['close']:.0f}")
        
        lr_value, lr_slope = scenario["lr"]
        keltner = scenario["keltner"]
        ema80_value, ema80_slope = scenario["ema80"]
        
        print(f"\nIndicadores:")
        print(f"  LR: {lr_value:.0f} (slope: {lr_slope:.1f})")
        print(f"  KC: Upper={keltner['upper']:.0f} | Basis={keltner['basis']:.0f} | Lower={keltner['lower']:.0f}")
        print(f"  EMA80: {ema80_value:.0f} (slope: {ema80_slope:.1f})")
        
        # Verificar condiciones Trade 80 SHORT
        espacio = ema80_value - keltner['basis']
        print(f"\n✓ Análisis Trade 80:")
        print(f"  • EMA80 > KC Basis: {ema80_value > keltner['basis']} ({'✅' if ema80_value > keltner['basis'] else '❌'})")
        print(f"  • LR bajista/plana: {lr_slope < 0.5} ({'✅' if lr_slope < 0.5 else '❌'})")
        print(f"  • EMA80 bajista/plana: {ema80_slope < 0.5} ({'✅' if ema80_slope < 0.5 else '❌'})")
        print(f"  • Espacio > 3 ticks: {espacio:.0f} puntos ({'✅' if espacio > 3 else '❌'})")
        print(f"  • Precio toca EMA80: {bar['low'] <= ema80_value <= bar['high']} ({'✅' if bar['low'] <= ema80_value <= bar['high'] else '❌'})")
        
        # Generar señal
        signal = signal_gen.generate_signal(
            bar=bar,
            lr_value=lr_value,
            lr_slope=lr_slope,
            keltner=keltner,
            ema80_value=ema80_value
        )
        
        if signal:
            print(f"\n🎯 SEÑAL DETECTADA: {signal['type']} {signal['direction']}")
            print(f"   Fase: {signal['phase_description']}")
            print(f"   Entry: {signal['entry']:.0f}")
            print(f"   Stop Loss: {signal['stop_loss']:.0f}")
            print(f"   Take Profit: {signal['take_profit']:.0f}")
            print(f"   Risk: {signal['risk']:.0f}")
            print(f"   Reward: {signal['reward']:.0f}")
            print(f"   Ratio: 1:{signal['ratio']:.0f}")
        else:
            print(f"\n⏳ Sin señal (esperando setup o entrada)")


def demo_estrategias_por_fase():
    """
    Muestra qué estrategia usar en cada fase
    """
    print("\n\n" + "=" * 80)
    print("MATRIZ: Estrategias por Fase del Mercado")
    print("=" * 80)
    print()
    
    print(f"{'Estrategia':<15} | {'Fase 1':<12} | {'Fase 2':<12} | {'Fase 3':<12} | {'Fase 4':<12}")
    print("-" * 80)
    print(f"{'A1':<15} | {'⚠️  Precaución':<12} | {'✅ IDEAL':<12} | {'❌ No':<12} | {'✅ IDEAL':<12}")
    print(f"{'A2':<15} | {'⚠️  Precaución':<12} | {'✅ IDEAL':<12} | {'❌ No':<12} | {'✅ IDEAL':<12}")
    print(f"{'A3':<15} | {'❌ No':<12} | {'❌ No':<12} | {'✅ IDEAL':<12} | {'❌ No':<12}")
    print(f"{'Trade 80':<15} | {'✅ IDEAL':<12} | {'❌ No':<12} | {'❌ No':<12} | {'✅ IDEAL':<12}")
    print(f"{'FOBO':<15} | {'❌ No':<12} | {'❌ No':<12} | {'✅ IDEAL':<12} | {'❌ No':<12}")
    print()
    print("📌 OBSERVACIÓN:")
    print("   • Trade 80 complementa A1/A2/A3 perfectamente")
    print("   • Trade 80 opera en Fases 1 y 4 (tendencial)")
    print("   • A1/A2 operan en Fases 2 y 4 (impulsos + retrocesos)")
    print("   • A3 opera en Fase 3 (lateral)")
    print("   • FOBO opera en Fase 3 (rompimientos fallidos)")
    print()


if __name__ == "__main__":
    demo_trade80_long()
    demo_trade80_short()
    demo_estrategias_por_fase()
    
    print("\n" + "=" * 80)
    print("✅ Demo Trade 80 completado")
    print("=" * 80)
    print("\n💡 Próximos pasos:")
    print("   1. Revisar documentación completa en TRADE_80.md")
    print("   2. Integrar EMA 80 en tu sistema de cálculo de indicadores")
    print("   3. Realizar backtesting con datos históricos")
    print("   4. Comparar rendimiento Trade 80 vs A1/A2/A3 por fase")
    print()
