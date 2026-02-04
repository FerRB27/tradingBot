# 🤖 Bot de Trading - Detección de OrderBlocks

## 📊 Versión 2.0 - OrderBlocks Edition

Bot de **scalping** para Binance que detecta **OrderBlocks** (bloques de órdenes institucionales) en velas japonesas de **5 minutos**.

---

## 🎯 ¿Qué son los OrderBlocks?

Los **OrderBlocks** son zonas de precio donde instituciones (bancos, fondos de inversión) han colocado órdenes grandes. Se detectan mediante patrones específicos en las velas:

- 🟢 **Bullish OrderBlock**: El precio salta hacia arriba dejando un "hueco" → Zona de soporte
- 🔴 **Bearish OrderBlock**: El precio cae abruptamente dejando un "hueco" → Zona de resistencia

**Basado en:** Indicador de TradingView (PineScript) - Ver archivo `indicadorOB.txt`

---

## ✨ Características

- ✅ **Detección automática** de OrderBlocks en tiempo real
- ✅ **Velas de 5 minutos** desde Binance WebSocket
- ✅ **Alertas visuales** en consola (🟢 Bullish / 🔴 Bearish)
- ✅ **Sistema de logging** especializado
- ✅ **Sin ejecución de trades** (solo detección por ahora)
- ✅ **Sin API key requerida** (usa datos públicos)
- ✅ **Demo offline** incluido para pruebas

---

## 🚀 Inicio Rápido

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

O manualmente:
```bash
pip install websocket-client python-binance
```

### 2. Probar el detector (sin internet)

```bash
python demo_order_blocks.py
```

Resultado esperado:
```
✅ BULLISH OrderBlock detectado!
✅ BEARISH OrderBlock detectado!
❌ No se detectó OrderBlock (correcto)
```

### 3. Ejecutar el bot en vivo

```bash
python main.py
```

El bot comenzará a:
- 📡 Conectarse a Binance WebSocket
- 🕯️ Recibir velas de 5 minutos de BTCUSDT
- 🔍 Detectar OrderBlocks automáticamente
- 📝 Registrar alertas en logs/

---

## 📁 Estructura del Proyecto

```
tradingBot/
├── main.py                          # 🎯 Programa principal
├── demo_order_blocks.py             # 🧪 Demo sin conexión
├── requirements.txt                 # 📦 Dependencias
│
├── indicators/
│   └── order_blocks.py             # 🔍 Detector de OrderBlocks
│
├── market_data/
│   └── kline_stream.py             # 📊 Stream de velas 5m
│
├── utils/
│   └── logger.py                   # 📝 Sistema de logging
│
├── config/
│   └── settings.py                 # ⚙️ Configuración
│
├── logs/
│   ├── order_blocks.log            # 📋 Log de OrderBlocks
│   ├── errors.log                  # ❌ Log de errores
│   └── bot.log                     # ℹ️ Log general
│
└── docs/
    ├── ORDER_BLOCKS.md             # 📚 Documentación completa
    ├── QUICKSTART.md               # ⚡ Guía rápida
    ├── EJEMPLOS_OB.md              # 📊 Ejemplos visuales
    ├── FLUJO_SISTEMA.md            # 🔄 Diagrama de flujo
    └── CAMBIOS_REALIZADOS.md       # 📝 Historial de cambios
```

---

## 📊 Ejemplo de Salida

```
======================================================================
🚀 Iniciando Bot de Trading - Detección de OrderBlocks
======================================================================
📊 Símbolo: BTCUSDT
⏱️  Temporalidad: 5 minutos
🎯 Modo: Detección de OrderBlocks (Sin ejecución de trades)
======================================================================

======================================================================
🕯️  VELA #3 | BTCUSDT | 5m
======================================================================
  Timestamp: 2026-02-04 14:40:00
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

## 🎓 Documentación

### Para Usuarios
- [QUICKSTART.md](QUICKSTART.md) - Inicio rápido en 3 pasos
- [ORDER_BLOCKS.md](ORDER_BLOCKS.md) - Documentación completa
- [EJEMPLOS_OB.md](EJEMPLOS_OB.md) - Ejemplos visuales de detección

### Para Desarrolladores
- [FLUJO_SISTEMA.md](FLUJO_SISTEMA.md) - Diagramas de arquitectura
- [CAMBIOS_REALIZADOS.md](CAMBIOS_REALIZADOS.md) - Historial de cambios
- `indicadorOB.txt` - Código PineScript original

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

### Cambiar a otro par
```python
SYMBOL = "ETHUSDT"  # Ethereum
SYMBOL = "BNBUSDT"  # Binance Coin
```

### Cambiar temporalidad
En `main.py` línea 47:
```python
kline_stream = KlineStream(symbol=SYMBOL, interval="15m")
```

Opciones: `1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `4h`, `1d`

---

## 📝 Sistema de Logs

El bot genera 3 archivos de log automáticamente:

### 1. `logs/order_blocks.log`
Todas las detecciones de OrderBlocks con timestamp completo.

**Ejemplo:**
```
2026-02-04 14:40:22 - 🟢 ORDER BLOCK ALCISTA detectado | O: $72200.00 H: $72250.00 L: $72150.00 C: $72240.00 | Rango: $100.00
```

### 2. `logs/errors.log`
Errores del sistema (conexión, parsing, etc.)

### 3. `logs/bot.log`
Log general de actividad

---

## 🧪 Pruebas

### Demo Offline
```bash
python demo_order_blocks.py
```

Ejecuta 3 casos de prueba sin conexión a internet:
1. ✅ Bullish OrderBlock
2. ✅ Bearish OrderBlock
3. ❌ Sin OrderBlock

### Test en Vivo
```bash
python main.py
```

Conecta a Binance y detecta OrderBlocks en tiempo real.

---

## 🔧 Lógica de Detección

### Bullish OrderBlock 🟢
```python
Condición: high[2] < low[0]
```
- `high[2]`: High de hace 2 velas
- `low[0]`: Low de la vela actual
- **Resultado**: El precio saltó hacia arriba

### Bearish OrderBlock 🔴
```python
Condición: low[2] > high[0]
```
- `low[2]`: Low de hace 2 velas
- `high[0]`: High de la vela actual
- **Resultado**: El precio cayó abruptamente

---

## 🛠️ Tecnologías

- **Python 3.8+**
- **websocket-client** - Conexión WebSocket a Binance
- **python-binance** - Cliente de Binance (para futuras ejecuciones)
- **logging** - Sistema de logs
- **datetime** - Manejo de timestamps

---

## 🚦 Estado del Proyecto

| Componente | Estado | Notas |
|------------|--------|-------|
| Detección de OB | ✅ Completo | Funcionando correctamente |
| Stream de velas 5m | ✅ Completo | WebSocket de Binance |
| Sistema de logging | ✅ Completo | 3 archivos de log |
| Visualización | ✅ Completo | Console output con emojis |
| Estrategia de entrada | ⏳ Pendiente | Próxima fase |
| Backtesting | ⏳ Pendiente | Próxima fase |
| Ejecución de trades | ⏳ Pendiente | Próxima fase |

---

## 📈 Próximos Pasos

1. ⏳ **Estrategia de entrada** basada en OrderBlocks
2. ⏳ **Confirmaciones adicionales** (volumen, estructura de mercado)
3. ⏳ **Backtesting** con datos históricos
4. ⏳ **Gestión de riesgo** (SL/TP automáticos)
5. ⏳ **Ejecución automática** de trades

---

## ❓ Preguntas Frecuentes

### ¿Necesito API key de Binance?
**No**, el bot usa datos públicos de Binance WebSocket para recibir velas.

### ¿El bot ejecuta trades automáticamente?
**No**, actualmente solo detecta y alerta OrderBlocks. La ejecución está deshabilitada.

### ¿Cuánto tarda en detectar el primer OrderBlock?
Necesita al menos **3 velas completadas** (15 minutos con timeframe de 5m). Los OrderBlocks son eventos relativamente raros.

### ¿Puedo usar otros timeframes?
**Sí**, modifica el parámetro `interval` en `main.py`. Opciones: 1m, 3m, 5m, 15m, 30m, 1h, 4h, 1d.

### ¿Funciona con otros pares?
**Sí**, cambia `SYMBOL` en `config/settings.py` a cualquier par de Binance (ETHUSDT, BNBUSDT, etc.).

---

## 🆘 Solución de Problemas

### Error de conexión WebSocket
- Verifica tu conexión a internet
- Algunas regiones tienen restricciones (usa VPN)

### No detecta OrderBlocks
- Espera al menos 15 minutos (3 velas de 5m)
- Los OrderBlocks son eventos raros (1-5 por día típicamente)

### Logs no se crean
- Verifica permisos de escritura en `logs/`
- El bot crea el directorio automáticamente

---

## 📄 Licencia

Este proyecto es de código abierto para uso educativo.

---

## 🙏 Referencias

- **Indicador Original**: `indicadorOB.txt` (PineScript de TradingView)
- **Smart Money Concepts**: Metodología de trading institucional
- **Binance API**: https://binance-docs.github.io/apidocs/

---

## 📧 Soporte

Para documentación completa, consulta:
- [ORDER_BLOCKS.md](ORDER_BLOCKS.md)
- [QUICKSTART.md](QUICKSTART.md)
- [EJEMPLOS_OB.md](EJEMPLOS_OB.md)

---

**Versión:** 2.0  
**Última actualización:** 2026-02-04  
**Autor:** MDC Trading Bot Team
