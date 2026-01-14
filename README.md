# 🤖 MDC Trading Bot - Estrategias A1, A2 & A3 + Detección de Fases

Bot de trading automatizado para Binance Futures basado en la metodología **MDC Trading Academy**.

## 📋 Características

- ✅ **Estrategias A1, A2 y A3** implementadas según MDC Trading Academy
- ✅ **Detección de las 4 Fases del Mercado** MDC (NUEVO ⭐)
- ✅ **Detección de FOBOs** (Fake Out Break Outs) con 80% probabilidad (NUEVO ⭐)
- ✅ **Range Bars** de 100 puntos
- ✅ **Indicadores técnicos**: Linear Regression 89, Keltner Channel 52 (3.5)
- ✅ **Risk Management**: Stop Loss y Take Profit con ratio 2:1
- ✅ **Backtesting** con datos históricos
- ✅ **Trading en tiempo real** vía WebSocket
- ✅ **Modo DEMO** y modo LIVE

## 🎯 Estrategias MDC

### A1 - Más Fuerte 🟢
**LONG**: Precio en/con LR + LR alcista  
**SHORT**: Precio en/con LR + LR bajista  
**Fases apropiadas**: Fase 2 (Cambio de Ritmo), Fase 4 (Transición)

### A2 - Alternativa 🟡
**LONG**: Precio sin tocar LR (debajo) + LR alcista  
**SHORT**: Precio sin tocar LR (encima) + LR bajista  
**Fases apropiadas**: Fase 2 (Cambio de Ritmo), Fase 4 (Transición)

### A3 - LR Plana 🟠
**LONG**: LR plana + espacio LR-Basis >= 2x riesgo  
**SHORT**: LR plana + espacio Basis-LR >= 2x riesgo  
**Fases apropiadas**: Fase 3 (Lateralización) solamente

### Trade 80 - Desarrollo de Tendencia 📈 (NUEVO)
**LONG**: EMA80 debajo KC Basis + espacio > 3 ticks + precio toca EMA80  
**SHORT**: EMA80 sobre KC Basis + espacio > 3 ticks + precio toca EMA80  
**Fases apropiadas**: Fase 1 (Tendencial), Fase 4 (Transición)

### FOBO - Rompimientos Fallidos ⚠️ (NUEVO)
Detecta rompimientos falsos en rangos establecidos con 80% probabilidad de reversión según MDC.
**Fases apropiadas**: Fase 3 (Lateralización) solamente

Ver [ESTRATEGIAS_A1_A2_A3.md](ESTRATEGIAS_A1_A2_A3.md) para detalles completos de A1/A2/A3.  
Ver [TRADE_80.md](TRADE_80.md) para detalles completos del Trade 80.

## 🔄 Las 4 Fases del Mercado MDC (NUEVO)

El sistema ahora detecta automáticamente las 4 fases de actividad del mercado:

### Fase 1: TENDENCIAL 📈📉
Movimiento direccional sostenido, tendencia o imbalance.

### Fase 2: CAMBIO DE RITMO 🔄
Detención del movimiento direccional, establecimiento de áreas de soporte/resistencia.  
**✅ Momento ideal para entradas A1 y A2**

### Fase 3: LATERALIZACIÓN ↔️
Movimiento lateral dentro de un rango establecido, LR plana.  
**✅ Momento ideal para entradas A3 y detección de FOBOs**

### Fase 4: TRANSICIÓN 🚀
Ruptura confirmada del rango, inicio de nueva tendencia.  
**✅ Momento ideal para entradas A1 y A2**

**Ver documentación completa**: [FASES_MERCADO_MDC.md](FASES_MERCADO_MDC.md)

**Resumen ejecutivo**: [RESUMEN_FASES_MDC.md](RESUMEN_FASES_MDC.md)

**Guía de implementación**: [IMPLEMENTACION_FASES.md](IMPLEMENTACION_FASES.md)

## 🚀 Uso

### 1. Configuración

Edita `config/settings.py` para ajustar parámetros:

```python
RANGE_SIZE = 100          # Tamaño de Range Bars
RISK_PERCENTAGE = 0.01    # 1% de riesgo por trade
EXECUTE_TRADES = False    # True para ejecutar órdenes reales
TESTNET = True            # True para red de pruebas
```

### 2. Demo del Sistema de Fases

Prueba el sistema de detección de fases y FOBOs:

```bash
python demo_phases.py
```

Esto mostrará:
- Simulación de las 4 fases del mercado
- Detecció por estrategia y fase
- Resultado neto en R (múltiplos de riesgo)
- Expectativa por trade
- Rendimiento de FOBOs vs teoría (80%)

### 4
### 3. Backtesting

Prueba la estrategia con datos históricos:

```bash
python backtesting/backtest.py
```

Esto mostrará:
- Total de trades ejecutados
- Win rate
- Resultado neto en R (múltiplos de riesgo)
- Expectativa por trade

### 3. Trading en Tiempo Real (DEMO)

Ejecuta el bot en modo DEMO (solo señales, sin ejecutar órdenes):

```bash
python main.py
```

El bot mostrará:
- Range Bars completadas en tiempo real
- **Fase actual del mercado** (NUEVO ⭐)
- Detección de impulsos
- **Señales A1/A2/A3 filtradas por fase** (NUEVO ⭐)
- **Señales FOBO en Fase 3** (NUEVO ⭐)
- SL y TP calculados

### 5
### 4. Trading en VIVO

⚠️ **PRECAUCIÓN**: Esto ejecutará órdenes reales en Binance

1. Edita `config/settings.py`:
```python
EXECUTE_TRADES = True
TESTNET = True  # Usa testnet primero para probar
```

2. Ejecuta:
```bash
python main.py y Sistemas

| Componente | Configuración | Descripción |
|-----------|---------------|-------------|
| Linear Regression | 89 períodos | Dirección de tendencia |
| Keltner Channel | 52 períodos, 3.5x | Bandas de volatilidad |
| EMA (opcional) | 20, 80 | Promedios móviles |
| **Detector de Fases** | **Automático** | **Identifica las 4 fases MDC** ⭐ |
| **Detector de FOBO** | **Automático** | **Rompimientos fallidos** ⭐------|
| Linear Regression | 89 | - |
| Keltner Channel | 52 | 3.5 |
| EMA (opcional) | 20, 80 | - |

## 🛠️ Estructura del Proyecto
demo_phases.py             # Demo del sistema de fases (NUEVO) ⭐
├── config/
│   ├── settings.py           # Configuración general
│   └── secrets.py            # API keys de Binance
├── market_data/
│   ├── websocket.py          # Conexión WebSocket con Binance
│   └── range_builder.py      # Construcción de Range Bars
├── indicators/
│   ├── trade80.py            # Lógica de Trade 80 (NUEVO) ⭐
│   ├── regression.py         # Linear Regression 89
│   ├── keltner.py            # Keltner Channel 52 (3.5)
│   └── ema.py                # EMAs 20 y 80
├── strategy/
│   ├── impulses.py           # Detección de cambios de impulso
│   ├── entries.py            # Lógica de entrada A1, A2, A3
│   ├── signals.py            # Sistema integrado de señales (ACTUALIZADO) ⭐
│   ├── market_phases.py      # Detector de las 4 fases MDC (NUEVO) ⭐
│   └── fobo_detector.py      # Detector de FOBOs (NUEVO) ⭐3.5)
│   └── ema.py                # EMAs 20 y 80
├── strategy/
│   ├── impulses.py           # Detección de cambios de impulso
│   └── entries.py            # Lógica de entrada A1
├── risk/
│   └── stop_take.py          # Cálculo de SL/TP (ratio 2:1)
├── execution/
│   └── binance_client.py     # Ejecución de órdenes en Binance
└── backtesting/
    ├── backtest.py           # Motor de backtesting
    ├── data_loader.py        # Carga datos históricos
    └── range_replay.py       # Reproduce Range Bars
```Sistema de Fases MDC**: El bot ahora detecta automáticamente las 4 fases del mercado y filtra señales según la fase apropiada, mejorando significativamente la tasa de éxito.

4. **Detección de FOBOs**: En Fase 3, el sistema detecta rompimientos fallidos con 80% de probabilidad de reversión según la teoría MDC.

5. **Risk Management**: El sistema calcula automáticamente el tamaño de posición basado en el porcentaje de riesgo configurado.

6# 📝 Notas Importantes

1. **Range Bars vs Velas Temporales**: Este bot usa Range Bars de 100 puntos. En TradingView, asegúrate de usar el mismo tipo de gráfico (Range 100) para comparar resultados.

2. **Indicadores corregidos**: Los indicadores (ATR, EMA) ahora replican exactamente el comportamiento de TradingView usando EMA en lugar de promedios simples.

3. **Risk Management**: El sistema calcula automáticamente el tamaño de posición basado en el porcentaje de riesgo configurado.

4. **Testnet**: Siempre prueba primero en la red de pruebas de Binance antes de usar fondos reales.

## ⚠️ Advertencias

- El trading de criptomonedas conlleva riesgos significativos
- No inviertas más de lo que puedas permitirte perder
- Este bot es para fines educativos y de investigación
- Prueba exhaustivamente en testnet antes de usar fondos reales
- Los resultados pasados no garantizan resultados futuros

## 📚 Recursos

- [MDC Trading Academy](https://mdctradingacademy.com/)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/futures/en/)
- [TradingView Pine Script](https://www.tradingview.com/pine-script-docs/)

---

**Desarrollado con ❤️ siguiendo la metodología MDC Trading Academy**
