# Demo de detección de OrderBlocks
# Script de prueba sin conexión a Binance

from indicators.order_blocks import OrderBlockDetector
from datetime import datetime, timedelta


def demo_order_blocks():
    """
    Demuestra la detección de OrderBlocks con datos de ejemplo
    """
    print("="*70)
    print("🧪 DEMO - Detector de OrderBlocks")
    print("="*70)
    
    # Inicializar detector
    detector = OrderBlockDetector()
    
    # Crear velas de ejemplo que generen un Bullish OrderBlock
    # Para Bullish OB: high[2] < low[0]
    print("\n📊 Caso 1: Bullish OrderBlock")
    print("-" * 70)
    
    candles_bullish = [
        # Vela hace 2 barras (índice -3): high=100
        {'open': 95, 'high': 100, 'low': 90, 'close': 98, 'timestamp': datetime.now() - timedelta(minutes=10)},
        # Vela anterior (índice -2)
        {'open': 98, 'high': 105, 'low': 97, 'close': 104, 'timestamp': datetime.now() - timedelta(minutes=5)},
        # Vela actual (índice -1): low=110 > high[2]=100 ✅ BULLISH OB!
        {'open': 104, 'high': 115, 'low': 110, 'close': 113, 'timestamp': datetime.now()},
    ]
    
    print("\nVelas:")
    for i, candle in enumerate(candles_bullish):
        print(f"  Vela {i}: O={candle['open']}, H={candle['high']}, L={candle['low']}, C={candle['close']}")
    
    result = detector.detect(candles_bullish)
    
    if result:
        print(f"\n✅ {result['type'].upper()} OrderBlock detectado!")
        print(f"   Vela OB: O={result['candle']['open']}, H={result['candle']['high']}, L={result['candle']['low']}, C={result['candle']['close']}")
        print(f"   Rango: {result['range']:.2f}")
        emoji = "🟢" if result['type'] == 'bullish' else "🔴"
        print(f"   {emoji} Tipo: {result['type'].upper()}")
    else:
        print("\n❌ No se detectó OrderBlock")
    
    # Crear velas de ejemplo que generen un Bearish OrderBlock
    # Para Bearish OB: low[2] > high[0]
    print("\n\n📊 Caso 2: Bearish OrderBlock")
    print("-" * 70)
    
    detector2 = OrderBlockDetector()
    
    candles_bearish = [
        # Vela hace 2 barras (índice -3): low=100
        {'open': 105, 'high': 110, 'low': 100, 'close': 102, 'timestamp': datetime.now() - timedelta(minutes=10)},
        # Vela anterior (índice -2)
        {'open': 102, 'high': 103, 'low': 95, 'close': 96, 'timestamp': datetime.now() - timedelta(minutes=5)},
        # Vela actual (índice -1): high=90 < low[2]=100 ✅ BEARISH OB!
        {'open': 96, 'high': 90, 'low': 85, 'close': 87, 'timestamp': datetime.now()},
    ]
    
    print("\nVelas:")
    for i, candle in enumerate(candles_bearish):
        print(f"  Vela {i}: O={candle['open']}, H={candle['high']}, L={candle['low']}, C={candle['close']}")
    
    result = detector2.detect(candles_bearish)
    
    if result:
        print(f"\n✅ {result['type'].upper()} OrderBlock detectado!")
        print(f"   Vela OB: O={result['candle']['open']}, H={result['candle']['high']}, L={result['candle']['low']}, C={result['candle']['close']}")
        print(f"   Rango: {result['range']:.2f}")
        emoji = "🟢" if result['type'] == 'bullish' else "🔴"
        print(f"   {emoji} Tipo: {result['type'].upper()}")
    else:
        print("\n❌ No se detectó OrderBlock")
    
    # Caso 3: Sin OrderBlock
    print("\n\n📊 Caso 3: Sin OrderBlock")
    print("-" * 70)
    
    detector3 = OrderBlockDetector()
    
    candles_no_ob = [
        {'open': 100, 'high': 105, 'low': 98, 'close': 103, 'timestamp': datetime.now() - timedelta(minutes=10)},
        {'open': 103, 'high': 107, 'low': 101, 'close': 105, 'timestamp': datetime.now() - timedelta(minutes=5)},
        {'open': 105, 'high': 108, 'low': 104, 'close': 106, 'timestamp': datetime.now()},
    ]
    
    print("\nVelas:")
    for i, candle in enumerate(candles_no_ob):
        print(f"  Vela {i}: O={candle['open']}, H={candle['high']}, L={candle['low']}, C={candle['close']}")
    
    result = detector3.detect(candles_no_ob)
    
    if result:
        print(f"\n✅ {result['type'].upper()} OrderBlock detectado!")
    else:
        print("\n❌ No se detectó OrderBlock (correcto)")
    
    print("\n" + "="*70)
    print("✅ Demo completada")
    print("="*70)


if __name__ == "__main__":
    demo_order_blocks()
