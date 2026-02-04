# Backtesting de OrderBlocks con velas de 5 minutos
from backtesting.data_loader import load_klines
from indicators.order_blocks import OrderBlockDetector
from datetime import datetime


def run_backtest_orderblocks(symbol="BTCUSDT", interval="5m", limit=500):
    """
    Ejecuta backtest de detección de OrderBlocks
    
    Args:
        symbol: Par de trading (ej: BTCUSDT)
        interval: Intervalo de velas (5m, 15m, 1h, etc.)
        limit: Cantidad de velas a cargar (max 1500)
    """
    print("="*70)
    print("📊 BACKTESTING - Detección de OrderBlocks")
    print("="*70)
    print(f"Símbolo: {symbol}")
    print(f"Intervalo: {interval}")
    print(f"Velas a analizar: {limit}")
    print("="*70)
    
    print(f"\n📥 Cargando datos históricos de Binance...")
    candles = load_klines(symbol=symbol, interval=interval, limit=limit)
    print(f"✅ {len(candles)} velas cargadas\n")
    
    if len(candles) < 3:
        print("❌ Error: Se necesitan al menos 3 velas para detectar OrderBlocks")
        return
    
    # Inicializar detector
    detector = OrderBlockDetector()
    
    # Estadísticas
    total_bullish = 0
    total_bearish = 0
    ob_list = []
    
    print(f"{'='*70}")
    print(f"🔍 Analizando velas...")
    print(f"{'='*70}\n")
    
    # Analizar vela por vela
    for i in range(2, len(candles)):
        # Obtener últimas 3 velas
        candles_slice = candles[i-2:i+1]
        
        # Detectar OrderBlock
        ob = detector.detect(candles_slice)
        
        if ob:
            ob_type = ob['type']
            ob_candle = ob['candle']
            
            if ob_type == 'bullish':
                total_bullish += 1
                emoji = "🟢"
                tipo_texto = "BULLISH"
            else:
                total_bearish += 1
                emoji = "🔴"
                tipo_texto = "BEARISH"
            
            # Guardar en lista
            ob_info = {
                'index': i,
                'type': ob_type,
                'timestamp': candles[i]['timestamp'],
                'candle': ob_candle,
                'range': ob['range']
            }
            ob_list.append(ob_info)
            
            # Mostrar detección
            print(f"{emoji} OrderBlock {tipo_texto} #{len(ob_list)}")
            print(f"   Vela #{i} | Tiempo: {candles[i]['timestamp'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   OB → O: ${ob_candle['open']:.2f} | H: ${ob_candle['high']:.2f} | L: ${ob_candle['low']:.2f} | C: ${ob_candle['close']:.2f}")
            print(f"   Rango: ${ob['range']:.2f}\n")
    
    # Resumen estadístico
    print(f"\n{'='*70}")
    print(f"📊 RESUMEN DE RESULTADOS")
    print(f"{'='*70}")
    print(f"Total de velas analizadas: {len(candles)}")
    print(f"OrderBlocks detectados: {len(ob_list)}")
    print(f"  🟢 Bullish: {total_bullish}")
    print(f"  🔴 Bearish: {total_bearish}")
    
    if len(ob_list) > 0:
        frecuencia = len(candles) / len(ob_list)
        print(f"\nFrecuencia: 1 OB cada {frecuencia:.1f} velas")
        
        # Calcular tiempo promedio
        if interval == "5m":
            minutos_por_vela = 5
        elif interval == "15m":
            minutos_por_vela = 15
        elif interval == "1h":
            minutos_por_vela = 60
        else:
            minutos_por_vela = 5
        
        tiempo_entre_obs = frecuencia * minutos_por_vela
        print(f"Tiempo promedio entre OBs: {tiempo_entre_obs:.1f} minutos ({tiempo_entre_obs/60:.1f} horas)")
    
    print(f"{'='*70}\n")
    
    return {
        'total_candles': len(candles),
        'total_obs': len(ob_list),
        'bullish': total_bullish,
        'bearish': total_bearish,
        'ob_list': ob_list
    }


if __name__ == "__main__":
    # Ejecutar backtest con configuración por defecto
    run_backtest_orderblocks(symbol="BTCUSDT", interval="5m", limit=500)
