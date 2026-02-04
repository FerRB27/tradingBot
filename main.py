# Bot de Trading con detección de OrderBlocks en velas de 5 minutos
from market_data.kline_stream import KlineStream
from indicators.order_blocks import OrderBlockDetector
from utils.logger import log_order_block, log_error, log_info
from config.settings import SYMBOL


def main():
    """
    Bot de scalping con detección de OrderBlocks en velas de 5 minutos
    """
    log_info("="*70)
    log_info("🚀 Iniciando Bot de Trading - Detección de OrderBlocks")
    log_info("="*70)
    log_info(f"📊 Símbolo: {SYMBOL}")
    log_info(f"⏱️  Temporalidad: 5 minutos")
    log_info(f"🎯 Modo: Detección de OrderBlocks (Sin ejecución de trades)")
    log_info("="*70)
    
    # Inicializar detector de OrderBlocks
    ob_detector = OrderBlockDetector()
    
    # Almacenamiento de velas
    candles = []
    
    def on_candle_completed(candle):
        """
        Callback que se ejecuta cuando se completa una vela de 5 minutos
        """
        try:
            # Agregar vela a la lista
            candles.append(candle)
            
            # Mostrar información de la vela
            print(f"\n{'='*70}")
            print(f"🕯️  VELA #{len(candles)} | {SYMBOL} | 5m")
            print(f"{'='*70}")
            print(f"  Timestamp: {candle['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Open:      ${candle['open']:.2f}")
            print(f"  High:      ${candle['high']:.2f}")
            print(f"  Low:       ${candle['low']:.2f}")
            print(f"  Close:     ${candle['close']:.2f}")
            print(f"  Volume:    {candle['volume']:.4f}")
            
            # Detectar OrderBlocks (necesitamos al menos 3 velas)
            if len(candles) >= 3:
                ob_result = ob_detector.detect(candles)
                
                if ob_result:
                    # OrderBlock detectado!
                    ob_type = ob_result['type']
                    ob_candle = ob_result['candle']
                    
                    # Registrar en logs
                    log_order_block(
                        ob_type=ob_type,
                        candle=ob_candle,
                        additional_info={
                            'range': ob_result['range'],
                            'timestamp': candle['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                    
                    # Mostrar en consola con formato visual
                    emoji = "🟢" if ob_type == "bullish" else "🔴"
                    tipo_texto = "ALCISTA (Bullish)" if ob_type == "bullish" else "BAJISTA (Bearish)"
                    
                    print(f"\n{'='*70}")
                    print(f"{emoji} ORDER BLOCK {tipo_texto} DETECTADO!")
                    print(f"{'='*70}")
                    print(f"  Vela OB - Open:  ${ob_candle['open']:.2f}")
                    print(f"  Vela OB - High:  ${ob_candle['high']:.2f}")
                    print(f"  Vela OB - Low:   ${ob_candle['low']:.2f}")
                    print(f"  Vela OB - Close: ${ob_candle['close']:.2f}")
                    print(f"  Rango OB:        ${ob_result['range']:.2f}")
                    print(f"{'='*70}\n")
                    
            print(f"{'='*70}\n")
            
        except Exception as e:
            log_error(f"Error procesando vela: {e}", exception=e)
    
    # Configurar y iniciar stream de velas
    try:
        kline_stream = KlineStream(symbol=SYMBOL, interval="5m")
        kline_stream.set_callback(on_candle_completed)
        
        log_info("📡 Conectando a Binance WebSocket...")
        kline_stream.start()
        
    except KeyboardInterrupt:
        log_info("\n🛑 Bot detenido por el usuario")
    except Exception as e:
        log_error(f"Error crítico en el bot: {e}", exception=e)


if __name__ == "__main__":
    main()
