# Explicación del Backtest MDC Bot

## ¿Qué hace el backtest?

El backtest simula el comportamiento de la estrategia A1 de MDC Trading Academy usando datos históricos. Aquí está el proceso:

### 1. **Carga de Datos**
```
- Se descargan datos históricos de Binance (velas de 1min)
- O se generan datos simulados para demostración
```

###  **Construcción de Range Bars**
```
- Los datos se convierten en Range Bars de 100 puntos
- Cada barra se cierra cuando el rango (High - Low) alcanza 100 puntos
```

### 3. **Análisis Técnico** (por cada barra)
```
✓ Linear Regression (89 períodos) → Valor y Pendiente
✓ Keltner Channel (52, 3.5) → Upper, Basis, Lower
✓ Detección de Impulsos → Cambio de pendiente LR
```

### 4. **Evaluación Estrategia A1**

#### **LONG A1** requiere:
1. ✅ Impulso BULLISH (LR negativo → positivo)
2. ✅ Precio en canal superior de Keltner
3. ✅ LR con pendiente alcista (slope > 0)
4. ✅ Retroceso a banda media de Keltner
5. ✅ Precio ≥ LR en momento del retroceso

#### **SHORT A1** requiere:
1. ✅ Impulso BEARISH (LR positivo → negativo)
2. ✅ Precio en canal inferior de Keltner
3. ✅ LR con pendiente bajista (slope < 0)
4. ✅ Retroceso a banda media de Keltner
5. ✅ Precio ≤ LR en momento del retroceso

### 5. **Gestión de Riesgo**
```
- Stop Loss: Banda inferior/superior de Keltner
- Take Profit: 2x la distancia del SL (Ratio 2:1)
- Por cada trade: -1R si pierde, +2R si gana
```

### 6. **Resultados**
```
Total Trades:    Cantidad de señales A1 ejecutadas
Win Rate:        % de operaciones ganadoras
Resultado Neto:  Ganancia/Pérdida en múltiplos de R
Expectativa:     R promedio por operación
```

---

## ¿Por qué no genera señales?

La estrategia A1 es **MUY ESPECÍFICA**. Requiere que se cumplan 5 condiciones simultáneas:

1. **Impulso reciente** (cambio de pendiente LR)
2. **Precio en extremo del Keltner** (canal superior para LONG, inferior para SHORT)
3. **Tendencia confirmada** (pendiente LR en la dirección correcta)
4. **Retroceso controlado** (vuelve a banda media)
5. **Confirmación final** (precio vs LR correcto)

Esto es **intencional** en la metodología MDC - solo tomar las mejores configuraciones.

---

## Cómo obtener más señales para probar

### Opción 1: Usar datos reales de Binance
```python
python -m backtesting.backtest
```
Esto descargará 1500 velas de 1 minuto de BTCUSDT real.

### Opción 2: Aumentar período de backtest
Edita `backtesting/backtest.py` línea final:
```python
run_backtest(interval="1m", limit=1500)  # Cambiar a 5m o 15m
```

### Opción 3: Usar datos demo
```python
python -m backtesting.demo_backtest
```
Genera datos simulados con tendencias (puede no generar señales A1 perfectas).

---

## Métricas de un backtest exitoso

### Expectativa Positiva
- Si ganas 60% de trades con ratio 2:1:
  ```
  (0.60 × 2R) + (0.40 × -1R) = +0.80R por trade
  ```

### Win Rate Mínimo
- Con ratio 2:1, necesitas solo 34% win rate para ser rentable:
  ```
  (0.34 × 2R) + (0.66 × -1R) = +0.02R
  ```

### Ejemplo Realista
```
Total Trades:     20
Ganadores:        12 (60%)
Perdedores:       8 (40%)
Resultado Neto:   +16R
Expectativa:      +0.80R por trade
```

Con una cuenta de $1000 y riesgo de 1% ($10 por R):
- Ganancia potencial: 16R × $10 = **+$160**
- Retorno: **16%** en el período analizado

---

## Próximos pasos

1. **Prueba con datos reales**:
   ```bash
   python -m backtesting.backtest
   ```

2. **Monitorea en tiempo real** (sin ejecutar):
   ```bash
   python main.py  # EXECUTE_TRADES=False
   ```

3. **Cuando estés listo**, activa ejecución:
   - Edita `config/settings.py`
   - Cambia `EXECUTE_TRADES = True`
   - ⚠️ Usa `TESTNET = True` primero!

---

**La estrategia A1 no busca cantidad, busca CALIDAD** ✨
