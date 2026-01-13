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

from strategy.impulses import detect_impulse
from strategy.entries import A1Strategy, A2Strategy, A3Strategy
from risk.stop_take import calculate_sl_tp
from execution.binance_client import BinanceFuturesClient
from visualization.chart_view import LiveChart


def start_trade_stream():
    range_builder = RangeBarBuilder(RANGE_SIZE)
    bars = []
    slopes = []
    
    # Listas para almacenar indicadores historicos
    lr_history = []
    keltner_history = {'upper': [], 'basis': [], 'lower': []}
    ema20_history = []
    ema80_history = []
    
    # Inicializar estrategias A1, A2 y A3
    a1_strategy = A1Strategy()
    a2_strategy = A2Strategy()
    a3_strategy = A3Strategy()
    
    # Inicializar cliente de Binance (si está habilitado)
    binance_client = BinanceFuturesClient(testnet=TESTNET) if EXECUTE_TRADES else None
    
    # Variable para evitar múltiples operaciones
    has_open_position = False
    
    # Inicializar grafico en tiempo real (DESHABILITADO)
    chart = None
    # try:
    #     chart = LiveChart()
    #     print("✅ Gráfico en tiempo real inicializado\n")
    # except Exception as e:
    #     print(f"⚠️  No se pudo inicializar el gráfico: {e}")
    #     print("   El bot continuará sin visualización\n")
    #     chart = None
    
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
            slopes.append(lr_slope)
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

            # Calcular Keltner Channel 52 (3.5)
            kc = keltner_channel(bars)

            # Detectar impulsos (cambio de pendiente)
            impulse = None
            if len(slopes) >= 2:
                impulse = detect_impulse(slopes[-2], slopes[-1])
                if impulse:
                    a1_strategy.set_impulse(impulse)
                    a2_strategy.set_impulse(impulse)
                    a3_strategy.set_impulse(impulse)

            # Evaluar señales A1, A2 y A3
            signal_a1 = a1_strategy.evaluate(
                bar=completed_bar,
                lr_value=lr_value,
                lr_slope=lr_slope,
                keltner=kc
            )
            
            signal_a2 = a2_strategy.evaluate(
                bar=completed_bar,
                lr_value=lr_value,
                lr_slope=lr_slope,
                keltner=kc
            )
            
            signal_a3 = a3_strategy.evaluate(
                bar=completed_bar,
                lr_value=lr_value,
                lr_slope=lr_slope,
                keltner=kc
            )
            
            # Priorizar A1 > A2 > A3
            signal = signal_a1 or signal_a2 or signal_a3

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

            if impulse:
                impulse_emoji = "🟢" if impulse == "BULLISH" else "🔴"
                print(f"\n{impulse_emoji} ⚡ IMPULSO DETECTADO: {impulse}")
                
            if a1_strategy.waiting_pullback:
                print(f"\n⏳ [A1] Esperando retroceso a banda media para: {a1_strategy.waiting_pullback}")
                
            if a2_strategy.waiting_pullback:
                print(f"\n⏳ [A2] Esperando retroceso a banda media para: {a2_strategy.waiting_pullback}")
                
            if a3_strategy.waiting_pullback:
                print(f"\n⏳ [A3] Esperando retroceso a banda media para: {a3_strategy.waiting_pullback}")

            # Ejecutar señal A1 o A2
            if signal and not has_open_position:
                signal_emoji = "🟢" if "LONG" in signal else "🔴"
                if "A1" in signal:
                    signal_type = "A1"
                elif "A2" in signal:
                    signal_type = "A2"
                else:
                    signal_type = "A3"
                print(f"\n{signal_emoji} {'='*66}")
                print(f"🚨 SEÑAL {signal_type} DETECTADA: {signal}")
                print(f"{'='*70}")
                
                # Calcular SL y TP
                sl_tp = calculate_sl_tp(
                    entry_price=completed_bar["close"],
                    signal_type=signal,
                    keltner=kc,
                    risk_percentage=RISK_PERCENTAGE
                )
                
                if sl_tp:
                    print(f"\n📋 Detalles de la operación:")
                    print(f"  Entry Price:   ${completed_bar['close']:.2f}")
                    print(f"  Stop Loss:     ${sl_tp['stop_loss']:.2f} (${sl_tp['risk_distance']:.2f})")
                    print(f"  Take Profit:   ${sl_tp['take_profit']:.2f} (+${sl_tp['reward_distance']:.2f})")
                    print(f"  Ratio R:R:     1:2")
                    print(f"  Riesgo:        {RISK_PERCENTAGE*100}% de la cuenta")
                    
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
                            
                            print(f"  Balance:       ${balance:.2f}")
                            print(f"  Cantidad:      {quantity} BTC")
                            
                            order = binance_client.place_order_a1(
                                signal=signal,
                                entry_price=completed_bar["close"],
                                stop_loss=sl_tp["stop_loss"],
                                take_profit=sl_tp["take_profit"],
                                quantity=quantity
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
            
            # Actualizar grafico en tiempo real
            if chart and len(bars) > 0:
                try:
                    indicators_data = {
                        'lr_values': lr_history,
                        'lr_slope': lr_slope if lr_slope else 0,
                        'keltner_upper': keltner_history['upper'],
                        'keltner_basis': keltner_history['basis'],
                        'keltner_lower': keltner_history['lower'],
                        'ema20': ema20_history,
                        'ema80': ema80_history
                    }
                    
                    # Preparar datos de señal si existe
                    signal_data = None
                    if signal and sl_tp:
                        signal_type_chart = 'LONG' if 'LONG' in signal else 'SHORT'
                        strategy_name = 'A1' if 'A1' in signal else 'A2' if 'A2' in signal else 'A3'
                        
                        signal_data = {
                            'type': signal_type_chart,
                            'price': completed_bar["close"],
                            'sl': sl_tp['stop_loss'],
                            'tp': sl_tp['take_profit'],
                            'strategy': strategy_name
                        }
                    
                    # Actualizar grafico
                    chart.update(bars, indicators_data, signal_data)
                    
                except Exception as e:
                    print(f"⚠️  Error actualizando gráfico: {e}")

    # WebSocket URL según testnet o mainnet
    if TESTNET:
        ws_url = f"wss://testnet.binance.vision/ws/{SYMBOL.lower()}@trade"
    else:
        ws_url = f"wss://stream.binance.com:9443/ws/{SYMBOL.lower()}@trade"

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
        print("🤖 MDC TRADING BOT - ESTRATEGIAS A1, A2 & A3")
        print("="*70)
        print(f"  Símbolo:        {SYMBOL}")
        print(f"  Range Size:     {RANGE_SIZE} puntos")
        print(f"  Riesgo:         {RISK_PERCENTAGE*100}%")
        print(f"  Estrategias:    A1, A2, A3 (MDC Trading Academy)")
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
