"""
Demo del sistema integrado de detección de fases y señales MDC

Este script demuestra cómo usar:
1. Detección de las 4 fases del mercado
2. Detección de FOBOs (rompimientos fallidos)
3. Generación de señales A1, A2, A3 según fase apropiada
"""

from strategy.signals import TradingSignalGenerator


def demo_phase_detection():
    """
    Simulación de cómo el sistema detecta fases y genera señales
    """
    
    # Inicializar generador de señales
    signal_gen = TradingSignalGenerator()
    
    # Simulación de barras de mercado
    # En producción, estas vendrían de RangeBarBuilder
    market_bars = [
        # Fase 1: Tendencia alcista fuerte
        {"open": 50000, "high": 50100, "low": 50000, "close": 50090},
        {"open": 50090, "high": 50200, "low": 50080, "close": 50195},
        {"open": 50195, "high": 50300, "low": 50190, "close": 50285},
        
        # Fase 2: Cambio de ritmo (impulso bajista detectado)
        {"open": 50285, "high": 50290, "low": 50150, "close": 50160},  # Impulso bajista
        
        # Fase 3: Lateralización (rango establecido)
        {"open": 50160, "high": 50220, "low": 50140, "close": 50180},
        {"open": 50180, "high": 50230, "low": 50165, "close": 50170},
        {"open": 50170, "high": 50225, "low": 50145, "close": 50200},
        {"open": 50200, "high": 50235, "low": 50155, "close": 50160},
        {"open": 50160, "high": 50240, "low": 50150, "close": 50190},
        
        # FOBO en resistencia (intenta romper pero falla)
        {"open": 50190, "high": 50250, "low": 50185, "close": 50200},  # Intento de ruptura
        {"open": 50200, "high": 50210, "low": 50140, "close": 50145},  # Regresa con aceleración
        
        # Fase 4: Transición (ruptura real alcista)
        {"open": 50180, "high": 50280, "low": 50175, "close": 50275},  # Ruptura confirmada
        {"open": 50275, "high": 50350, "low": 50270, "close": 50340},
    ]
    
    print("=" * 80)
    print("SIMULACIÓN: Detección de Fases del Mercado y Señales MDC")
    print("=" * 80)
    print()
    
    # Procesar cada barra
    for i, bar in enumerate(market_bars):
        print(f"\n📊 BARRA #{i+1}")
        print(f"   OHLC: O={bar['open']:.2f} H={bar['high']:.2f} L={bar['low']:.2f} C={bar['close']:.2f}")
        
        # Calcular indicadores (simulados para demo)
        # En producción, estos se calculan con ventanas deslizantes
        lr_value, lr_slope = simulate_lr(i, market_bars)
        keltner = simulate_keltner(bar)
        
        # Generar señal
        signal = signal_gen.generate_signal(bar, lr_value, lr_slope, keltner)
        
        # Mostrar contexto de mercado
        context = signal_gen.get_market_context()
        phase_info = context["phase_info"]
        
        print(f"\n   🔄 FASE: {phase_info['phase_description']}")
        print(f"      Barras en fase: {phase_info['bars_in_phase']}")
        
        if phase_info['range_established']:
            print(f"      Rango: [{phase_info['range_low']:.2f} - {phase_info['range_high']:.2f}]")
        
        # Mostrar señal si existe
        if signal:
            print(f"\n   🎯 SEÑAL DETECTADA: {signal['type']} {signal['direction']}")
            print(f"      Entry: {signal['entry']:.2f}")
            print(f"      SL: {signal['stop_loss']:.2f}")
            print(f"      TP: {signal['take_profit']:.2f}")
            print(f"      Risk: {signal['risk']:.2f}")
            print(f"      Reward: {signal['reward']:.2f}")
            print(f"      Ratio: 1:{signal['ratio']}")
            
            # Info adicional de FOBO
            if 'fobo_info' in signal:
                fobo = signal['fobo_info']
                print(f"\n      ⚠️ FOBO DETECTADO:")
                print(f"         Tipo: {fobo['type']}")
                print(f"         Probabilidad: {fobo['probability']*100:.0f}%")
                print(f"         Target: {fobo['target_area']} @ {fobo['target_level']:.2f}")
        else:
            print(f"   ⏳ Sin señal en esta barra")
        
        print(f"   {'-'*70}")


def simulate_lr(index, bars):
    """
    Simula cálculo de Linear Regression
    En producción, usar calculate_linear_regression()
    """
    # Valores simulados que reflejan las fases
    lr_values = [
        (50050, 15.0),   # Tendencia alcista fuerte
        (50150, 18.0),
        (50250, 20.0),
        (50200, 5.0),    # Cambio de ritmo
        (50190, 0.3),    # Lateralización
        (50195, 0.2),
        (50200, -0.1),
        (50198, 0.4),
        (50196, -0.2),
        (50200, 0.1),    # FOBO
        (50180, -0.5),
        (50250, 12.0),   # Transición
        (50300, 15.0),
    ]
    
    if index < len(lr_values):
        return lr_values[index]
    return (50000, 0.0)


def simulate_keltner(bar):
    """
    Simula cálculo de Keltner Channels
    En producción, usar calculate_keltner()
    """
    # Simulación simple basada en el precio actual
    basis = (bar["high"] + bar["low"] + bar["close"]) / 3
    atr = 40  # ATR simulado
    multiplier = 1.5
    
    return {
        "upper": basis + (multiplier * atr),
        "basis": basis,
        "lower": basis - (multiplier * atr)
    }


def demo_phase_compatibility():
    """
    Muestra qué estrategias son compatibles con cada fase
    """
    print("\n" + "=" * 80)
    print("COMPATIBILIDAD: Estrategias vs Fases del Mercado")
    print("=" * 80)
    print()
    
    from strategy.market_phases import MarketPhaseDetector
    
    detector = MarketPhaseDetector()
    
    strategies = ["A1", "A2", "A3", "FOBO_REVERSAL"]
    phases = ["PHASE_1", "PHASE_2", "PHASE_3", "PHASE_4"]
    phase_names = {
        "PHASE_1": "Tendencial",
        "PHASE_2": "Cambio de Ritmo",
        "PHASE_3": "Lateralización",
        "PHASE_4": "Transición"
    }
    
    print(f"{'Estrategia':<20} | {'Fase 1':<15} | {'Fase 2':<15} | {'Fase 3':<15} | {'Fase 4':<15}")
    print("-" * 95)
    
    for strategy in strategies:
        row = f"{strategy:<20} |"
        for phase in phases:
            # Simular compatibilidad
            detector.current_phase = phase
            is_compatible = detector.is_suitable_for_entries(strategy)
            status = "✅ Sí" if is_compatible else "❌ No"
            row += f" {status:<15}|"
        print(row)
    
    print()
    print("RECOMENDACIONES:")
    print("  • A1/A2: Usar en Fase 2 (cambio de ritmo) y Fase 4 (transición)")
    print("  • A3: Usar SOLO en Fase 3 (lateralización con LR plana)")
    print("  • FOBO: Usar SOLO en Fase 3 (rango establecido)")
    print()


def demo_fobo_detection():
    """
    Ejemplo específico de detección de FOBO
    """
    print("\n" + "=" * 80)
    print("EJEMPLO: Detección de FOBO (Rompimiento Fallido)")
    print("=" * 80)
    print()
    
    print("Escenario: Mercado en Fase 3 (lateralización)")
    print("Rango establecido: [50150 - 50250]")
    print()
    
    fobo_scenario = [
        {
            "bar": {"open": 50200, "high": 50235, "low": 50190, "close": 50210},
            "desc": "Precio dentro del rango",
            "expected": None
        },
        {
            "bar": {"open": 50210, "high": 50260, "low": 50205, "close": 50220},
            "desc": "Intento de ruptura alcista (high > 50250)",
            "expected": "Potencial FOBO en resistencia"
        },
        {
            "bar": {"open": 50220, "high": 50230, "low": 50150, "close": 50155},
            "desc": "Regresa al rango con aceleración bajista",
            "expected": "FOBO CONFIRMADO → Señal SHORT hacia soporte"
        }
    ]
    
    for i, scenario in enumerate(fobo_scenario, 1):
        bar = scenario["bar"]
        print(f"Paso {i}: {scenario['desc']}")
        print(f"   OHLC: O={bar['open']} H={bar['high']} L={bar['low']} C={bar['close']}")
        print(f"   → {scenario['expected'] or 'Sin señal'}")
        print()
    
    print("📊 Resultado: FOBO en resistencia detectado")
    print("   Dirección: SHORT")
    print("   Probabilidad: 80% (según MDC)")
    print("   Objetivo: Testear soporte en 50150")
    print()


if __name__ == "__main__":
    # Ejecutar demos
    demo_phase_detection()
    demo_phase_compatibility()
    demo_fobo_detection()
    
    print("\n" + "=" * 80)
    print("✅ Demo completado")
    print("=" * 80)
    print("\n💡 Próximos pasos:")
    print("   1. Integrar con tu sistema de backtesting")
    print("   2. Ajustar parámetros según instrumento y timeframe")
    print("   3. Realizar backtesting con datos históricos")
    print("   4. Validar tasas de éxito por fase y estrategia")
    print()
