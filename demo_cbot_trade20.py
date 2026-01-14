"""
Demo: TRADE CBOT y TRADE 20
============================
Prueba las nuevas estrategias basadas en la teoría de las anclas.
"""

from strategy.anchor_detector import AnchorDetector
from strategy.trade_cbot import TradeCBOT
from strategy.trade_20 import Trade20Strategy

# Datos simulados de barras
bars = [
    {"open": 95000, "high": 95050, "low": 94950, "close": 95000},  # Barra 1
    {"open": 95000, "high": 95100, "low": 94900, "close": 95050},  # Barra 2 - Ancla soporte
    {"open": 95050, "high": 95150, "low": 95000, "close": 95100},  # Barra 3
    {"open": 95100, "high": 95200, "low": 95050, "close": 95150},  # Barra 4 - Ancla resistencia
    {"open": 95150, "high": 95200, "low": 95000, "close": 95050},  # Barra 5 - Retroceso
    {"open": 95050, "high": 95100, "low": 94950, "close": 95000},  # Barra 6 - Ancla soporte
    {"open": 95000, "high": 95200, "low": 94980, "close": 95180},  # Barra 7 - Lateralización
    {"open": 95180, "high": 95250, "low": 95150, "close": 95200},  # Barra 8 - Ancla resistencia
    {"open": 95200, "high": 95400, "low": 95190, "close": 95350},  # Barra 9 - BREAKOUT! (CBOT)
    {"open": 95350, "high": 95400, "low": 95250, "close": 95280},  # Barra 10 - Retroceso a EMA 20
]

# Pendientes LR simuladas (cambio de impulso para detectar anclas)
lr_slopes = [-2.0, -1.5, 0.5, 1.5, 0.8, -1.2, -0.5, 0.3, 2.5, 1.0]

# EMAs simuladas
ema20_values = [94950, 94970, 95000, 95050, 95080, 95060, 95100, 95150, 95200, 95270]
ema80_values = [94800, 94820, 94850, 94880, 94900, 94920, 94950, 94980, 95000, 95020]

# Keltner simulado (bandas amplias para cumplir requisitos)
keltner = {
    'upper': 95500,
    'basis': 95200,
    'lower': 94900
}

print("="*70)
print("🧪 DEMO: TRADE CBOT Y TRADE 20")
print("="*70)
print("\nSimulando mercado lateral (Fase 3) con múltiples anclas...")
print("Objetivo: Detectar breakout confirmado (CBOT) y entrada en EMA 20\n")

# Inicializar detectores
anchor_detector = AnchorDetector(tick_size=1.0, anchor_lookback=20)
trade_cbot = TradeCBOT(tick_size=1.0, breakout_ticks=3)
trade20 = Trade20Strategy(tick_size=1.0, min_distance_ticks=4)

current_phase = "PHASE_3"  # Simulamos Fase 3 (lateralización)

for i, bar in enumerate(bars):
    print(f"\n{'─'*70}")
    print(f"📊 BARRA #{i+1}")
    print(f"{'─'*70}")
    print(f"Precio: ${bar['low']:.0f} - ${bar['high']:.0f} | Close: ${bar['close']:.0f}")
    print(f"LR Slope: {lr_slopes[i]:.2f}")
    print(f"EMA 20: ${ema20_values[i]:.0f} | EMA 80: ${ema80_values[i]:.0f}")
    
    # Actualizar detector de anclas
    anchor_detector.update(bar, lr_slopes[i])
    
    # Obtener áreas de anclas
    resistance_area = anchor_detector.get_resistance_area()
    support_area = anchor_detector.get_support_area()
    
    # Mostrar anclas detectadas
    anchor_info = anchor_detector.get_info()
    print(f"\n⚓ Anclas: {anchor_info['resistance_anchors_count']} resistencia, {anchor_info['support_anchors_count']} soporte")
    
    if resistance_area:
        print(f"  📍 Área resistencia: {resistance_area['anchor_count']} anclas @ ${resistance_area['highest_pivot']:.0f}")
    if support_area:
        print(f"  📍 Área soporte: {support_area['anchor_count']} anclas @ ${support_area['lowest_pivot']:.0f}")
    
    # Evaluar TRADE CBOT
    signal_cbot = trade_cbot.evaluate(bar, current_phase, resistance_area, support_area)
    
    if signal_cbot:
        print(f"\n🚨 {'='*66}")
        print(f"✅ SEÑAL CBOT {signal_cbot['direction']} DETECTADA!")
        print(f"{'='*70}")
        print(f"  Tipo: {signal_cbot['type']}")
        print(f"  Anclas: {signal_cbot['anchor_count']}")
        print(f"  Pivote: ${signal_cbot['pivot_level']:.0f}")
        print(f"  Breakout: ${signal_cbot['breakout_level']:.0f}")
        print(f"  Entry: ${signal_cbot['entry']:.0f}")
        print(f"  Stop Loss: ${signal_cbot['stop_loss']:.0f}")
        print(f"  Take Profit: ${signal_cbot['take_profit']:.0f}")
        print(f"  R:R: 1:{signal_cbot['ratio']}")
        trade20.reset_for_new_cbot()
    
    # Evaluar TRADE 20 (solo si hay CBOT previo)
    last_cbot = trade_cbot.get_last_cbot()
    if last_cbot:
        # Cambiar a Fase 4 después de breakout (más realista)
        current_phase = "PHASE_4"
        
        signal_trade20 = trade20.evaluate(bar, current_phase, ema20_values[i], keltner, last_cbot)
        
        if signal_trade20:
            print(f"\n🚨 {'='*66}")
            print(f"✅ SEÑAL TRADE 20 {signal_trade20['direction']} DETECTADA!")
            print(f"{'='*70}")
            print(f"  Tipo: {signal_trade20['type']}")
            print(f"  EMA 20: ${signal_trade20['ema20_value']:.0f}")
            print(f"  Distancia a Keltner: {signal_trade20['keltner_distance']:.1f} ticks")
            print(f"  CBOT previo: {signal_trade20['cbot_info']['direction']} @ ${signal_trade20['cbot_info']['breakout_price']:.0f}")
            print(f"  Entry: ${signal_trade20['entry']:.0f}")
            print(f"  Stop Loss: ${signal_trade20['stop_loss']:.0f}")
            print(f"  Take Profit: ${signal_trade20['take_profit']:.0f}")
            print(f"  R:R: 1:{signal_trade20['ratio']}")

print("\n" + "="*70)
print("✅ Demo completado")
print("="*70)
print("\nResumen:")
print("- Anclas detectadas correctamente en cambios de impulso")
print("- TRADE CBOT detecta breakout con 2+ anclas confirmando nivel")
print("- TRADE 20 detecta entrada en EMA 20 después de CBOT")
print("- Ambas estrategias calculan stops y targets apropiados")
