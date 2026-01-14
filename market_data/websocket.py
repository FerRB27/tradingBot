# Trades en tiempo real (Binance)
import websocket
import json
import threading
from config.settings import (
    SYMBOL, RANGE_SIZE, RISK_PERCENTAGE, EXECUTE_TRADES, TESTNET
)
from market_data.range_builder import RangeBarBuilder

from indicators.regression import linear_regression
from indicators.keltner import keltner_channel
from indicators.ema import ema

from strategy.signals import TradingSignalGenerator
from execution.binance_client import BinanceFuturesClient


def start_trade_stream():
    range_builder = RangeBarBuilder(RANGE_SIZE)
    bars = []
    
    # Listas para almacenar indicadores historicos
    lr_history = []
    keltner_history = {'upper': [], 'basis': [], 'lower': []}
    ema20_history = []
    ema80_history = []
    
    # Inicializar sistema integrado de señales (A1, A2, A3, Trade 80, CBOT, Trade 20, FOBO)
    signal_generator = TradingSignalGenerator(tick_size=1.0)
    
    # Inicializar cliente de Binance (si está habilitado)
    binance_client = BinanceFuturesClient(testnet=TESTNET) if EXECUTE_TRADES else None
    
    # Variable para evitar múltiples operaciones
    has_open_position = False
    
    # Contador de barras
    bar_count = 0

    def handle_trade(msg):
        nonlocal has_open_position, bar_count
        
        if msg["e"] != "trade":
            return

        price = float(msg["p"])
        completed_bar = range_builder.process_trade(price)

        if completed_bar:
            bar_count += 1
            bars.append(completed_bar)

            closes = [b["close"] for b in bars]

            # Calcular Linear Regression 89
            lr = linear_regression(closes, 89)
            lr_value = lr[0] if lr else None
            lr_slope = lr[1] if lr else None
            lr_history.append(lr_value)

            # Calcular Keltner Channel 52 (3.5)
            kc = keltner_channel(bars)
            keltner_history['upper'].append(kc['upper'] if kc else None)
            keltner_history['basis'].append(kc['basis'] if kc else None)
            keltner_history['lower'].append(kc['lower'] if kc else None)
            
            # Calcular EMAs
            ema20_val = ema(closes, 20)
            ema80_val = ema(closes, 80)
            ema20_history.append(ema20_val)
            ema80_history.append(ema80_val)

            # Generar señal usando sistema integrado (A1, A2, A3, Trade 80, CBOT, Trade 20, FOBO)
            signal = signal_generator.generate_signal(
                bar=completed_bar,
                lr_value=lr_value,
                lr_slope=lr_slope,
                keltner=kc,
                ema80_value=ema80_val,  # Para Trade 80
                ema20_value=ema20_val   # Para Trade 20
            )
            
            # Obtener contexto del mercado (fase actual)
            market_context = signal_generator.get_market_context()

            # Mostrar información de la barra
            print(f"\n{'='*70}")
            print(f"🟦 RANGE BAR #{bar_count} | ${SYMBOL}")
            print(f"{'='*70}")
            print(f"  Open:   ${completed_bar['open']:.2f}")
            print(f"  High:   ${completed_bar['high']:.2f}")
            print(f"  Low:    ${completed_bar['low']:.2f}")
            print(f"  Close:  ${completed_bar['close']:.2f}")
            print(f"  Range:  ${completed_bar['high'] - completed_bar['low']:.2f}")
            
            if lr_value and lr_slope:
                slope_direction = "📈 Alcista" if lr_slope > 0 else "📉 Bajista"
                print(f"\n📊 Indicadores:")
                print(f"  LR Value:  ${lr_value:.2f}")
                print(f"  LR Slope:  {lr_slope:.6f} {slope_direction}")
            
            if kc:
                print(f"  KC Upper:  ${kc['upper']:.2f}")
                print(f"  KC Basis:  ${kc['basis']:.2f}")
                print(f"  KC Lower:  ${kc['lower']:.2f}")
            
            if ema20_val:
                print(f"  EMA 20:    ${ema20_val:.2f}")
            
            if ema80_val:
                print(f"  EMA 80:    ${ema80_val:.2f}")
            
            # Mostrar fase del mercado
            phase_info = market_context['phase_info']
            if phase_info['current_phase']:
                phase_emoji = {
                    "PHASE_1": "📈",
                    "PHASE_2": "🔄",
                    "PHASE_3": "↔️",
                    "PHASE_4": "🚀"
                }.get(phase_info['current_phase'], "❓")
                print(f"\n{phase_emoji} Fase del Mercado: {phase_info['phase_description']}")
                print(f"  Barras en fase: {phase_info['bars_in_phase']}")
                
                if phase_info['range_established']:
                    print(f"  Rango: ${phase_info['range_low']:.2f} - ${phase_info['range_high']:.2f}")
            
            # Mostrar información de anclas
            anchor_info = market_context['anchor_info']
            resistance_area = market_context['resistance_area']
            support_area = market_context['support_area']
            
            if resistance_area or support_area:
                print(f"\n⚓ Anclas detectadas:")
                if resistance_area:
                    print(f"  📍 Resistencia: {resistance_area['anchor_count']} anclas @ ${resistance_area['highest_pivot']:.2f}")
                if support_area:
                    print(f"  📍 Soporte: {support_area['anchor_count']} anclas @ ${support_area['lowest_pivot']:.2f}")
            
            # Mostrar si hay setup FOBO en espera
            fobo_info = market_context['fobo_info']
            if fobo_info['waiting_confirmation']:
                print(f"\n⚠️ FOBO potencial en: {fobo_info['potential_fobo']}")

            # Ejecutar señal (A1, A2, A3, Trade 80, CBOT, Trade 20, FOBO)
            if signal and not has_open_position:
                signal_type = signal['type']
                signal_direction = signal['direction']
                signal_emoji = "🟢" if signal_direction == "LONG" else "🔴"
                
                print(f"\n{signal_emoji} {'='*66}")
                print(f"🚨 SEÑAL {signal_type} {signal_direction} DETECTADA!")
                print(f"{'='*70}")
                print(f"  Fase: {signal['phase_description']}")
                
                # Info adicional para Trade 80
                if signal_type == "TRADE_80" and 'ema80_value' in signal:
                    print(f"  EMA 80: ${signal['ema80_value']:.2f}")
                
                # Info adicional para CBOT
                if 'cbot_info' in signal:
                    cbot = signal['cbot_info']
                    print(f"  Anclas: {cbot['anchor_count']}")
                    print(f"  Pivote: ${cbot['pivot_level']:.2f}")
                    print(f"  Breakout: ${cbot['breakout_level']:.2f}")
                
                # Info adicional para Trade 20
                if 'trade20_info' in signal:
                    t20 = signal['trade20_info']
                    print(f"  EMA 20: ${t20['ema20_value']:.2f}")
                    print(f"  Distancia KC: {t20['keltner_distance']:.1f} ticks")
                    cbot_prev = t20['cbot_info']
                    print(f"  CBOT previo: {cbot_prev['direction']} @ ${cbot_prev['breakout_price']:.2f}")
                
                # Info adicional para FOBO
                if 'fobo_info' in signal:
                    fobo = signal['fobo_info']
                    print(f"  FOBO: {fobo['type']}")
                    print(f"  Probabilidad: {fobo['probability']*100:.0f}%")
                    print(f"  Target: {fobo['target_area']} @ ${fobo['target_level']:.2f}")
                
                print(f"\n📋 Detalles de la operación:")
                print(f"  Entry Price:   ${signal['entry']:.2f}")
                print(f"  Stop Loss:     ${signal['stop_loss']:.2f} (-${signal['risk']:.2f})")
                print(f"  Take Profit:   ${signal['take_profit']:.2f} (+${signal['reward']:.2f})")
                print(f"  Ratio R:R:     1:{signal['ratio']:.0f}")
                print(f"  Riesgo:        {RISK_PERCENTAGE*100}% de la cuenta")
                
                # Preparar datos para ejecución
                sl_tp = {
                    'stop_loss': signal['stop_loss'],
                    'take_profit': signal['take_profit'],
                    'risk_distance': signal['risk'],
                    'reward_distance': signal['reward']
                }
                
                # Ejecutar la orden si está habilitado
                if EXECUTE_TRADES and binance_client:
                    print(f"\n💼 Ejecutando orden en Binance...")
                    balance = binance_client.get_balance()
                    if balance:
                        quantity = binance_client.calculate_position_size(
                            balance=balance,
                            risk_percentage=RISK_PERCENTAGE,
                            risk_distance=sl_tp['risk_distance']
                        )
                        
                        # Ejecutar orden de mercado
                        order = binance_client.place_market_order(
                            side=signal_direction,
                            quantity=quantity,
                            stop_loss=sl_tp["stop_loss"],
                            take_profit=sl_tp["take_profit"]
                        )
                        
                        if order:
                            has_open_position = True
                            print(f"\n✅ ¡Orden ejecutada exitosamente!")
                else:
                    print(f"\n⚠️  MODO DEMO - Señal detectada pero NO se ejecutó")
                    print(f"    Para ejecutar órdenes reales:")
                    print(f"    1. Edita config/settings.py")
                    print(f"    2. Cambia EXECUTE_TRADES = True")
                print(f"{'='*70}\n")

    # WebSocket URL según testnet o mainnet
    if TESTNET:
        ws_url = f"wss://stream.binancefuture.com/ws/{SYMBOL.lower()}@trade"
    else:
        ws_url = f"wss://fstream.binance.com/ws/{SYMBOL.lower()}@trade"

    def on_message(ws, message):
        try:
            msg = json.loads(message)
            # Convertir el formato del mensaje al esperado
            trade_msg = {
                "e": "trade",
                "p": msg["p"],  # precio
                "q": msg["q"],  # cantidad
                "T": msg["T"]   # timestamp
            }
            handle_trade(trade_msg)
        except Exception as e:
            print(f"Error procesando mensaje: {e}")

    def on_error(ws, error):
        print(f"WebSocket error: {error}")

    def on_close(ws, close_status_code, close_msg):
        print(f"\n⚠️ WebSocket cerrado. Código: {close_status_code}")
        print("Intentando reconectar en 5 segundos...")
        threading.Timer(5.0, start_trade_stream).start()

    def on_open(ws):
        mode = "🔴 LIVE TRADING" if EXECUTE_TRADES else "🟡 DEMO (Solo Señales)"
        network = "🧪 TESTNET" if TESTNET else "⚠️ MAINNET"
        
        print("\n" + "="*70)
        print("🤖 MDC TRADING BOT - SISTEMA COMPLETO DE ESTRATEGIAS")
        print("="*70)
        print(f"  Símbolo:        {SYMBOL}")
        print(f"  Range Size:     {RANGE_SIZE} puntos")
        print(f"  Riesgo:         {RISK_PERCENTAGE*100}%")
        print(f"  Estrategias:    A1, A2, A3, Trade 80, CBOT, Trade 20, FOBO")
        print(f"  Detección:      4 Fases del Mercado MDC + Anclas")
        print(f"  Modo:           {mode}")
        print(f"  Network:        {network}")
        print("="*70)
        print("\n✅ Conectado al WebSocket de Binance")
        print("📊 Construyendo Range Bars en tiempo real...")
        print("⏳ Esperando primera Range Bar completa...\n")

    # Crear y ejecutar WebSocket
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    
    ws.run_forever()
