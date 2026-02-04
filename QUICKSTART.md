# 🚀 Inicio Rápido - Bot OrderBlocks

## ✅ Paso 1: Verificar instalación

```bash
pip install websocket-client binance
```

## ✅ Paso 2: Probar el detector (offline)

```bash
python demo_order_blocks.py
```

Esto ejecutará 3 casos de prueba sin conexión a internet.

## ✅ Paso 3: Ejecutar backtesting

```bash
python backtest_orderblocks.py
```

Analiza 500 velas históricas y muestra estadísticas de OrderBlocks detectados.

## ✅ Paso 4: Ejecutar el bot en vivo

```bash
python main.py
```

El bot se conectará a Binance y comenzará a:
- 📊 Recibir velas de 5 minutos de BTCUSDT
- 🔍 Detectar OrderBlocks alcistas (🟢) y bajistas (🔴)
- 📝 Registrar todas las detecciones en `logs/order_blocks.log`

## 📋 Salida Esperada

```
======================================================================
🚀 Iniciando Bot de Trading - Detección de OrderBlocks
======================================================================
📊 Símbolo: BTCUSDT
⏱️  Temporalidad: 5 minutos
🎯 Modo: Detección de OrderBlocks (Sin ejecución de trades)
======================================================================

======================================================================
🕯️  VELA #1 | BTCUSDT | 5m
======================================================================
  Timestamp: 2026-02-04 14:35:00
  Open:      $72,450.00
  High:      $72,580.00
  Low:       $72,420.00
  Close:     $72,550.00
  Volume:    12.4567
======================================================================
```

Cuando se detecte un OrderBlock, verás:

```
======================================================================
🟢 ORDER BLOCK ALCISTA (Bullish) DETECTADO!
======================================================================
  Vela OB - Open:  $72,200.00
  Vela OB - High:  $72,250.00
  Vela OB - Low:   $72,150.00
  Vela OB - Close: $72,240.00
  Rango OB:        $100.00
======================================================================
```

## 📁 Archivos de Log

El bot creará automáticamente:

- `logs/order_blocks.log` - Todas las detecciones de OB
- `logs/errors.log` - Errores del bot
- `logs/bot.log` - Log general

## ⚙️ Cambiar Símbolo

Edita `config/settings.py`:

```python
SYMBOL = "ETHUSDT"  # Cambiar a Ethereum
```

## ⚙️ Cambiar Temporalidad

Edita `main.py` línea 47:

```python
kline_stream = KlineStream(symbol=SYMBOL, interval="15m")  # Cambiar a 15 minutos
```

Temporalidades soportadas: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d

## 🛑 Detener el Bot

Presiona `Ctrl + C` en la terminal.

## ⚠️ Notas Importantes

1. **El bot NO ejecuta trades** - Solo detecta OrderBlocks
2. **Requiere conexión a internet** - Se conecta a Binance WebSocket
3. **Espera 3 velas** - Los OrderBlocks se detectan después de tener al menos 3 velas completas (15 minutos con temporalidad de 5m)
4. **No requiere API key** - Usa datos públicos de Binance

## 📚 Más Información

Lee [ORDER_BLOCKS.md](ORDER_BLOCKS.md) para documentación completa.
