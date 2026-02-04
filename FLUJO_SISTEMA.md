# 🔄 Flujo del Sistema - Bot OrderBlocks

## Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                     BINANCE WEBSOCKET                           │
│          wss://stream.binance.com:9443/ws/                      │
│                  btcusdt@kline_5m                               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Velas 5m en tiempo real
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   market_data/kline_stream.py                   │
│                     KlineStream Class                           │
│  - Recibe velas desde WebSocket                                 │
│  - Parsea datos JSON                                            │
│  - Detecta cuando vela se cierra (is_closed=True)               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Callback al cerrar vela
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         main.py                                 │
│                   on_candle_completed()                         │
│  - Almacena vela en lista                                       │
│  - Muestra info en consola                                      │
│  - Llama al detector de OB                                      │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Lista de velas (últimas 3+)
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              indicators/order_blocks.py                         │
│                OrderBlockDetector Class                         │
│                                                                 │
│  Lógica de detección:                                           │
│  ┌───────────────────────────────────────────────────┐          │
│  │ Bullish OB:  high[2] < low[0]                     │          │
│  │ Bearish OB:  low[2] > high[0]                     │          │
│  └───────────────────────────────────────────────────┘          │
│                                                                 │
│  Retorna:                                                       │
│  {                                                              │
│    'type': 'bullish' / 'bearish',                               │
│    'candle': {...},                                             │
│    'range': float,                                              │
│    'middle': float                                              │
│  }                                                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Resultado de detección
                         ▼
         ┌───────────────┴───────────────┐
         │                               │
         ▼                               ▼
┌─────────────────┐            ┌──────────────────┐
│   CONSOLA       │            │  utils/logger.py │
│                 │            │                  │
│ 🟢 Bullish OB   │            │ log_order_block()│
│ 🔴 Bearish OB   │            │ log_error()      │
│                 │            │ log_info()       │
└─────────────────┘            └────────┬─────────┘
                                        │
                                        │ Escribe en archivos
                                        ▼
                               ┌─────────────────────┐
                               │   logs/             │
                               │                     │
                               │ order_blocks.log    │
                               │ errors.log          │
                               │ bot.log             │
                               └─────────────────────┘
```

---

## Flujo de Datos Detallado

### 1️⃣ Recepción de Vela (cada 5 minutos)

```
WebSocket Message (JSON)
    │
    ├─ k.t  → timestamp (milisegundos)
    ├─ k.o  → open price
    ├─ k.h  → high price
    ├─ k.l  → low price
    ├─ k.c  → close price
    ├─ k.v  → volume
    └─ k.x  → is_closed (boolean)
```

### 2️⃣ Procesamiento en KlineStream

```python
if kline['x']:  # Vela cerrada
    candle = {
        'timestamp': datetime,
        'open': float,
        'high': float,
        'low': float,
        'close': float,
        'volume': float,
        'is_closed': True
    }
    
    callback(candle)  # Llamar a main.py
```

### 3️⃣ Almacenamiento y Detección

```python
# main.py
candles.append(candle)  # Guardar en lista

if len(candles) >= 3:
    ob = detector.detect(candles)
```

### 4️⃣ Lógica de Detección

```python
# order_blocks.py

# Obtener velas
current = candles[-1]    # Vela actual (índice 0)
previous = candles[-2]   # Vela anterior (índice 1)
two_ago = candles[-3]    # Hace 2 velas (índice 2)

# Bullish OrderBlock
if two_ago['high'] < current['low']:
    return {
        'type': 'bullish',
        'candle': two_ago,
        ...
    }

# Bearish OrderBlock
if two_ago['low'] > current['high']:
    return {
        'type': 'bearish',
        'candle': two_ago,
        ...
    }
```

### 5️⃣ Registro y Visualización

```python
# main.py
if ob_result:
    # 1. Mostrar en consola con emojis
    print("🟢 BULLISH OB" / "🔴 BEARISH OB")
    
    # 2. Registrar en logs
    log_order_block(
        ob_type=ob_result['type'],
        candle=ob_result['candle'],
        additional_info={...}
    )
```

---

## Estados del Sistema

```
┌──────────────────┐
│  Inicializando   │
│  - Logger        │
│  - Detector OB   │
│  - WebSocket     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Conectando      │
│  WebSocket       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Esperando       │
│  1era vela       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Esperando       │
│  2da vela        │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Esperando       │
│  3era vela       │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  Operativo       │
│  (Detectando OB) │
└──────────────────┘
         │
         │ Cada 5 minutos
         │
         ├──► Nueva vela
         │    │
         │    ├──► ¿OB detectado?
         │    │    │
         │    │    ├── Sí → Alerta 🟢/🔴 + Log
         │    │    └── No → Continuar
         │    │
         │    └──► Volver a esperar
         │
         └──────────┘
```

---

## Ejemplo de Timeline

```
Tiempo    Vela#   Acción
────────────────────────────────────────────────────
14:30     #1      📥 Vela recibida
                  ⏳ Esperando más velas...

14:35     #2      📥 Vela recibida
                  ⏳ Esperando más velas...

14:40     #3      📥 Vela recibida
                  🔍 INICIANDO DETECCIÓN DE OB
                  ❌ No se detectó OB

14:45     #4      📥 Vela recibida
                  🔍 Analizando...
                  ✅ 🟢 BULLISH OB DETECTADO!
                  📝 Registrado en logs/order_blocks.log
                  📢 Alerta en consola

14:50     #5      📥 Vela recibida
                  🔍 Analizando...
                  ❌ No se detectó OB

14:55     #6      📥 Vela recibida
                  🔍 Analizando...
                  ✅ 🔴 BEARISH OB DETECTADO!
                  📝 Registrado en logs/order_blocks.log
                  📢 Alerta en consola

... continúa indefinidamente ...
```

---

## Comparación: Antes vs Después

### ANTES (Range Bars)
```
Trade Stream (Binance)
    ↓
RangeBarBuilder
    ↓
Barra completa cuando range ≥ 100
    ↓
Estrategias A1/A2/A3/Trade80/CBOT
    ↓
Señal de trading
    ↓
Ejecutar orden (opcional)
```

### DESPUÉS (Velas 5m + OrderBlocks)
```
Kline Stream (Binance)
    ↓
KlineStream
    ↓
Vela completa cada 5 minutos
    ↓
OrderBlockDetector
    ↓
Alerta de OB (🟢/🔴)
    ↓
Console + Logs
```

---

## Próxima Evolución

```
Kline Stream
    ↓
OrderBlockDetector
    ↓
¿OB Detectado?
    ├── No → Continuar
    └── Sí → Estrategia de Entrada [FUTURO]
              ↓
              ¿Confirmaciones OK?
              ├── No → Esperar
              └── Sí → Calcular Riesgo [FUTURO]
                        ↓
                        Ejecutar Orden [FUTURO]
                        ↓
                        Gestión de Trade [FUTURO]
```

---

## Componentes Clave

| Componente | Archivo | Responsabilidad |
|------------|---------|-----------------|
| **Stream** | `kline_stream.py` | Conexión WebSocket, recibir velas |
| **Detector** | `order_blocks.py` | Lógica de detección de OB |
| **Logger** | `logger.py` | Registro de eventos y errores |
| **Main** | `main.py` | Orquestación y visualización |
| **Config** | `settings.py` | Configuración del bot |

---

## Dependencias Externas

```
websocket-client
    └── Conexión WebSocket a Binance

binance (python-binance)
    └── [Futuro] Ejecución de órdenes
```

---

**Versión:** 2.0  
**Última actualización:** 2026-02-04
