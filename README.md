# 🤖 MDC Trading Bot - Estrategias A1, A2 & A3

Bot de trading automatizado para Binance Futures basado en la metodología **MDC Trading Academy**.

## 📋 Características

- ✅ **Estrategias A1, A2 y A3** implementadas según MDC Trading Academy
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

### A2 - Alternativa 🟡
**LONG**: Precio sin tocar LR (debajo) + LR alcista  
**SHORT**: Precio sin tocar LR (encima) + LR bajista

### A3 - LR Plana 🟠
**LONG**: LR plana + espacio LR-Basis >= 2x riesgo  
**SHORT**: LR plana + espacio Basis-LR >= 2x riesgo

Ver [ESTRATEGIAS_A1_A2_A3.md](ESTRATEGIAS_A1_A2_A3.md) para detalles completos.

## 🚀 Uso

### 1. Configuración

Edita `config/settings.py` para ajustar parámetros:

```python
RANGE_SIZE = 100          # Tamaño de Range Bars
RISK_PERCENTAGE = 0.01    # 1% de riesgo por trade
EXECUTE_TRADES = False    # True para ejecutar órdenes reales
TESTNET = True            # True para red de pruebas
```

### 2. Backtesting

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
- Valores de indicadores (LR, Keltner)
- Detección de impulsos
- Señales A1 cuando se cumplen las condiciones
- SL y TP calculados

### 4. Trading en VIVO

⚠️ **PRECAUCIÓN**: Esto ejecutará órdenes reales en Binance

1. Edita `config/settings.py`:
```python
EXECUTE_TRADES = True
TESTNET = True  # Usa testnet primero para probar
```

2. Ejecuta:
```bash
python main.py
```

## 📊 Indicadores

| Indicador | Período | Multiplier |
|-----------|---------|------------|
| Linear Regression | 89 | - |
| Keltner Channel | 52 | 3.5 |
| EMA (opcional) | 20, 80 | - |

## 🛠️ Estructura del Proyecto

```
tradingBot/
├── main.py                    # Ejecuta el bot en tiempo real
├── config/
│   ├── settings.py           # Configuración general
│   └── secrets.py            # API keys de Binance
├── market_data/
│   ├── websocket.py          # Conexión WebSocket con Binance
│   └── range_builder.py      # Construcción de Range Bars
├── indicators/
│   ├── regression.py         # Linear Regression 89
│   ├── keltner.py            # Keltner Channel 52 (3.5)
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
```

## 📝 Notas Importantes

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
