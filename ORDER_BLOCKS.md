# Detección de OrderBlocks - Bot de Scalping 5m

## 📋 Resumen de Cambios

El bot ha sido transformado para trabajar con **velas japonesas de 5 minutos** en lugar de Range Bars, con enfoque en la detección de **OrderBlocks** (Bloques de Órdenes).

### Cambios Principales

1. **❌ Range Bars eliminadas** → ✅ **Velas japonesas 5m**
2. **✅ Nuevo detector de OrderBlocks** basado en TradingView (PineScript)
3. **✅ Sistema de logging mejorado** para errores y alertas OB
4. **⏸️ Ejecución de trades deshabilitada** (solo detección por ahora)

---

## 🎯 ¿Qué son los OrderBlocks?

Los **OrderBlocks** son zonas donde instituciones han colocado órdenes grandes. Se detectan mediante:

### 🟢 Bullish OrderBlock (Alcista)
- **Condición**: El `high` de hace 2 velas está por debajo del `low` de la vela actual
- **Interpretación**: Indica que el precio ha saltado hacia arriba, dejando un "bloque" de órdenes de compra
- **Color**: Verde en la consola

### 🔴 Bearish OrderBlock (Bajista)
- **Condición**: El `low` de hace 2 velas está por encima del `high` de la vela actual
- **Interpretación**: Indica que el precio ha caído, dejando un "bloque" de órdenes de venta
- **Color**: Rojo en la consola

---

## 🏗️ Arquitectura Actualizada

```
tradingBot/
├── main.py                          # ✅ NUEVO - Bot principal con OrderBlocks
├── indicators/
│   └── order_blocks.py             # ✅ NUEVO - Detector de OrderBlocks
├── market_data/
│   └── kline_stream.py             # ✅ NUEVO - Stream de velas 5m desde Binance
├── utils/
│   ├── __init__.py                 # ✅ NUEVO
│   └── logger.py                   # ✅ NUEVO - Sistema de logging mejorado
├── logs/
│   ├── order_blocks.log            # ✅ Registro de todos los OB detectados
│   ├── errors.log                  # ✅ Registro de errores
│   └── bot.log                     # ✅ Registro general
└── config/
    └── settings.py                 # ✅ ACTUALIZADO - Nueva configuración
```

---

## 🚀 Cómo Usar

### 1. Instalar dependencias

```bash
pip install websocket-client binance
```

### 2. Ejecutar el bot

```bash
python main.py
```

### 3. Observar la consola

El bot mostrará:
- 🕯️ Información de cada vela de 5 minutos
- 🟢 Alertas de OrderBlocks alcistas (Bullish)
- 🔴 Alertas de OrderBlocks bajistas (Bearish)

### Ejemplo de salida:

```
======================================================================
🕯️  VELA #45 | BTCUSDT | 5m
======================================================================
  Timestamp: 2026-02-04 14:35:00
  Open:      $72,450.00
  High:      $72,580.00
  Low:       $72,420.00
  Close:     $72,550.00
  Volume:    12.4567

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

---

## 📊 Logs

El bot genera 3 archivos de log:

### 1. `logs/order_blocks.log`
Registra todas las detecciones de OrderBlocks con timestamp y detalles completos.

### 2. `logs/errors.log`
Registra cualquier error que ocurra durante la ejecución.

### 3. `logs/bot.log`
Registro general de actividad del bot.

---

## ⚙️ Configuración

Archivo: `config/settings.py`

```python
# Símbolo a operar
SYMBOL = "BTCUSDT"

# Temporalidad de las velas
TIMEFRAME = "5m"

# Detección de OrderBlocks
DETECT_ORDER_BLOCKS = True

# Ejecución de trades (deshabilitado por ahora)
EXECUTE_TRADES = False
```

---

## 🔧 Módulos Principales

### `indicators/order_blocks.py`
Clase `OrderBlockDetector` que implementa la lógica de detección de OB basada en el código PineScript de TradingView.

**Métodos:**
- `detect(candles)`: Detecta OB en las últimas 3 velas
- `get_all_order_blocks()`: Retorna todos los OB detectados
- `get_last_order_block()`: Retorna el último OB

### `market_data/kline_stream.py`
Clase `KlineStream` que se conecta al WebSocket de Binance para recibir velas en tiempo real.

**Características:**
- Conexión a Binance WebSocket público (no requiere API key)
- Soporte para múltiples temporalidades (1m, 3m, 5m, 15m, etc.)
- Callback al completarse cada vela

### `utils/logger.py`
Sistema de logging con 3 loggers especializados:
- `log_order_block()`: Registra alertas de OB
- `log_error()`: Registra errores
- `log_info()`: Registra información general

---

## 📈 Próximos Pasos

1. ✅ **Completado**: Detección de OrderBlocks en consola
2. ⏳ **Pendiente**: Estrategia de entrada basada en OB
3. ⏳ **Pendiente**: Integración con sistema de riesgo y take profit/stop loss
4. ⏳ **Pendiente**: Backtesting con velas históricas

---

## 📝 Notas Técnicas

### Diferencias con el bot anterior:
- ❌ Ya no se construyen Range Bars
- ❌ Estrategias A1, A2, A3, Trade 80, CBOT deshabilitadas
- ✅ Nuevo enfoque: Scalping con velas de 5m
- ✅ Detección de OrderBlocks como base para futuras estrategias

### Lógica de OrderBlocks (del PineScript):
```javascript
// Bullish OB
is_bullish_order_block = high[2] < low[0]

// Bearish OB
is_bearish_order_block = low[2] > high[0]
```

Esta lógica está implementada en Python en el módulo `order_blocks.py`.

---

## 🆘 Solución de Problemas

### El bot no detecta OrderBlocks
- Espera al menos 3 velas completadas (15 minutos)
- Los OB son eventos relativamente raros, puede tomar tiempo detectar uno

### Error de conexión WebSocket
- Verifica tu conexión a internet
- Binance puede tener restricciones regionales (usa VPN si es necesario)

### Logs no se crean
- Verifica que el directorio `logs/` tenga permisos de escritura
- El bot crea el directorio automáticamente si no existe

---

## 📚 Referencias

- **Indicador Original**: `indicadorOB.txt` (PineScript de TradingView)
- **Documentación Binance WebSocket**: https://binance-docs.github.io/apidocs/spot/en/#websocket-market-streams
- **Order Blocks**: Concepto de trading institucional usado en Smart Money Concepts (SMC)
