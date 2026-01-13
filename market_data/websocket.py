# Trades en tiempo real (Binance)
from binance import ThreadedWebsocketManager
from config.secrets import API_KEY, API_SECRET
from config.settings import (
    SYMBOL, RANGE_SIZE, RISK_PERCENTAGE, EXECUTE_TRADES, TESTNET
)
from market_data.range_builder import RangeBarBuilder

from indicators.regression import linear_regression
from indicators.keltner import keltner_channel

from strategy.impulses import detect_impulse
from strategy.entries import A1Strategy
from risk.stop_take import calculate_sl_tp
from execution.binance_client import BinanceFuturesClient


def start_trade_stream():
    range_builder = RangeBarBuilder(RANGE_SIZE)
    bars = []
    slopes = []
    
    # Inicializar estrategia A1
    a1_strategy = A1Strategy()
    
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
            slopes.append(lr_slope)

            # Calcular Keltner Channel 52 (3.5)
            kc = keltner_channel(bars)

            # Detectar impulsos (cambio de pendiente)
            impulse = None
            if len(slopes) >= 2:
                impulse = detect_impulse(slopes[-2], slopes[-1])
                if impulse:
                    a1_strategy.set_impulse(impulse)

            # Evaluar señal A1
            signal = a1_strategy.evaluate(
                bar=completed_bar,
                lr_value=lr_value,
                lr_slope=lr_slope,
                keltner=kc
            )

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
                print(f"\n⏳ Esperando retroceso a banda media para: {a1_strategy.waiting_pullback}")

            # Ejecutar señal A1
            if signal and not has_open_position:
                signal_emoji = "🟢" if "LONG" in signal else "🔴"
                print(f"\n{signal_emoji} {'='*66}")
                print(f"🚨 SEÑAL A1 DETECTADA: {signal}")
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

    twm = ThreadedWebsocketManager(
        api_key=API_KEY,
        api_secret=API_SECRET,
        testnet=TESTNET
    )

    twm.start()

    twm.start_trade_socket(
        symbol=SYMBOL,
        callback=handle_trade
    )

    mode = "🔴 LIVE TRADING" if EXECUTE_TRADES else "🟡 DEMO (Solo Señales)"
    network = "🧪 TESTNET" if TESTNET else "⚠️ MAINNET"
    
    print("\n" + "="*70)
    print("🤖 MDC TRADING BOT - ESTRATEGIA A1")
    print("="*70)
    print(f"  Símbolo:        {SYMBOL}")
    print(f"  Range Size:     {RANGE_SIZE} puntos")
    print(f"  Riesgo:         {RISK_PERCENTAGE*100}%")
    print(f"  Modo:           {mode}")
    print(f"  Network:        {network}")
    print("="*70)
    print("\n✅ Conectado al WebSocket de Binance")
    print("📊 Construyendo Range Bars en tiempo real...")
    print("⏳ Esperando primera Range Bar completa...\n")

    twm.join()

    twm.join()
