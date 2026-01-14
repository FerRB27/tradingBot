# 🔄 Las 4 Fases del Mercado según MDC Trading Academy

## 📖 Teoría Fundamental

El mercado no se mueve de forma aleatoria, sino que sigue ciclos definidos de 4 fases que se repiten constantemente. Identificar correctamente estas fases permite:
- ✅ Entrar en el momento óptimo
- ✅ Evitar zonas de bajo rendimiento
- ✅ Mejorar el timing de las operaciones
- ✅ Aumentar la probabilidad de éxito

---

## 🔢 Las 4 Fases

### Fase 1: TENDENCIAL 📈📉
**Descripción:** Movimiento direccional, tendencia o imbalance a favor de una dirección.

**Características:**
- LR con pendiente fuerte (slope > 1.0)
- Precio consistentemente alejado de banda media Keltner
- Impulsos sostenidos en la misma dirección
- Alta momentum

**Indicadores en código:**
```python
strong_slope = abs(lr_slope) > 1.0
away_from_basis = price alejado de keltner["basis"]
sustained_direction = impulsos en misma dirección
```

**Estrategias aplicables:**
- ⚠️ **A1/A2**: Con precaución (solo en pullbacks limpios)
- ❌ **A3**: No aplicable (requiere LR plana)
- ✅ **Continuación de tendencia**: Ideal

---

### Fase 2: CAMBIO DE RITMO 🔄
**Descripción:** Entrada de órdenes pasivas que inicialmente detienen el movimiento direccional previo. Se establecen las áreas del rango.

**Características:**
- Impulso contrario detectado (cambio de dirección)
- Pendiente de LR comenzando a moderarse
- Precio alcanzando extremos de Keltner
- Inicio del establecimiento de soporte/resistencia

**Indicadores en código:**
```python
impulse_change = impulso diferente al previo
slope_moderating = abs(lr_slope) < 1.0
at_extremes = precio en upper o lower Keltner
coming_from_phase_1 = fase anterior fue tendencial
```

**Estrategias aplicables:**
- ✅ **A1**: Muy efectiva (setup ideal)
- ✅ **A2**: Muy efectiva
- ❌ **A3**: No aplicable aún
- ❌ **FOBO**: No hay rango establecido

**Importancia:** Esta es la fase donde se "dibujan" los límites del futuro rango.

---

### Fase 3: LATERALIZACIÓN ↔️
**Descripción:** Movimiento lateral o balance. Movimiento alrededor de las áreas establecidas en la fase de parada.

**Características:**
- LR relativamente plana (|slope| <= 0.5)
- Precio oscilando entre bandas de Keltner
- Rango establecido con soporte y resistencia claros
- Consolidación de precio

**Indicadores en código:**
```python
flat_lr = abs(lr_slope) <= 0.5
in_range = precio entre keltner lower y upper
range_established = rango confirmado con 3+ barras
respecting_range = precio respetando límites
```

**Estrategias aplicables:**
- ⚠️ **A1/A2**: No recomendado (no hay tendencia clara)
- ✅ **A3**: Ideal (requiere LR plana)
- ✅ **FOBO**: Muy efectivo (rompimientos fallidos)

**Zona clave para:** Entradas A3 y detección de FOBOs.

---

### Fase 4: TRANSICIÓN 🚀
**Descripción:** El precio rompe el rango o balance (con confirmación) e inicia una nueva tendencia o imbalance en búsqueda de una nueva zona de valor.

**Características:**
- Ruptura confirmada del rango establecido en Fase 3
- Nuevo impulso direccional (BULLISH o BEARISH)
- Cierre fuera del rango con convicción
- Puede ser cambio o continuación de tendencia

**Indicadores en código:**
```python
breakout_confirmed = cierre fuera del rango
new_impulse = impulso direccional detectado
from_phase_3 = estaba en lateralización
volume_confirmation = aceleración en movimiento
```

**Estrategias aplicables:**
- ✅ **A1**: Muy efectiva (nuevo impulso)
- ✅ **A2**: Efectiva
- ⚠️ **A3**: No (ya no hay LR plana)
- ❌ **FOBO**: No (ruptura real, no falsa)

**Importancia:** Inicio de nuevo ciclo → Vuelve a Fase 1

---

## 🎯 Sub-Fase: FOBO dentro de Fase 3

### ¿Qué es un FOBO?
**FOBO = Fake Out Break Out** (Rompimiento Falso)

Durante la Fase 3 (lateralización), a veces el precio intenta romper el rango pero fracasa y regresa.

### 📊 Estadística MDC
**80% de probabilidad:** Cuando hay un FOBO en un lado del rango, el precio testeará el lado opuesto.

### Tipos de FOBO

#### 1. FOBO en Resistencia
```
Resistencia ══════════════════
         ↑
         │ Intento de ruptura (FOBO)
         │ ↓ Regresa al rango
         │   ↓ Acelera hacia soporte
Soporte ════════════════════ ← 80% probabilidad de testear
```

**Señal:** SHORT (operar en corto)  
**Objetivo:** Soporte del rango  
**Requisito:** Aceleración confirmada hacia abajo

#### 2. FOBO en Soporte
```
Resistencia ════════════════════ ← 80% probabilidad de testear
         ↑ Acelera hacia resistencia
         │ ↑ Regresa al rango
         │
         ↓ Intento de ruptura (FOBO)
Soporte ══════════════════
```

**Señal:** LONG (operar en largo)  
**Objetivo:** Resistencia del rango  
**Requisito:** Aceleración confirmada hacia arriba

### Requisitos para confirmar FOBO:
1. ✅ Estar en Fase 3 (rango establecido)
2. ✅ Mínimo 5 barras dentro del rango
3. ✅ Ruptura inicial (high/low fuera del rango)
4. ✅ Regreso al rango (cierre dentro)
5. ✅ Aceleración hacia lado opuesto (velocidad > 1.5x promedio)

---

## 🔄 Ciclo Completo del Mercado

```
Fase 1 (Tendencial)
      ↓
Fase 2 (Cambio de Ritmo)
      ↓
Fase 3 (Lateralización) ←→ [FOBO Detection]
      ↓
Fase 4 (Transición)
      ↓
Fase 1 (Nueva Tendencia)
      ↓
      ...
```

**El ciclo se repite constantemente.**

---

## 📈 Aplicación de Estrategias por Fase

| Fase | A1 | A2 | A3 | FOBO | Notas |
|------|----|----|----| -----|-------|
| **Fase 1** | ⚠️ | ⚠️ | ❌ | ❌ | Tendencia fuerte, esperar pullback |
| **Fase 2** | ✅ | ✅ | ❌ | ❌ | **IDEAL para A1/A2** |
| **Fase 3** | ❌ | ❌ | ✅ | ✅ | **IDEAL para A3 y FOBO** |
| **Fase 4** | ✅ | ✅ | ❌ | ❌ | Ruptura confirmada, nuevo impulso |

---

## 💻 Uso en Código

### Detección automática de fase:
```python
from strategy.market_phases import MarketPhaseDetector

detector = MarketPhaseDetector()
current_phase = detector.detect_phase(bar, lr_value, lr_slope, keltner, impulse)

# Resultado: "PHASE_1", "PHASE_2", "PHASE_3", "PHASE_4"
```

### Verificar si fase es apropiada para estrategia:
```python
if detector.is_suitable_for_entries("A1"):
    # Evaluar entrada A1
    signal = a1_strategy.evaluate(...)

if detector.is_suitable_for_entries("A3"):
    # Evaluar entrada A3
    signal = a3_strategy.evaluate(...)
```

### Detección de FOBO:
```python
from strategy.fobo_detector import FOBODetector

fobo = FOBODetector()
phase_info = detector.get_phase_info()
fobo_signal = fobo.detect_fobo(bar, phase_info)

if fobo_signal:
    # FOBO detectado
    direction = fobo_signal["direction"]  # LONG o SHORT
    target = fobo_signal["target_level"]
    probability = fobo_signal["probability"]  # 0.80
```

### Sistema integrado:
```python
from strategy.signals import TradingSignalGenerator

signal_gen = TradingSignalGenerator()
signal = signal_gen.generate_signal(bar, lr_value, lr_slope, keltner)

if signal:
    print(f"Señal: {signal['type']} {signal['direction']}")
    print(f"Fase: {signal['phase']} - {signal['phase_description']}")
    print(f"Entry: {signal['entry']}")
    print(f"SL: {signal['stop_loss']} | TP: {signal['take_profit']}")
```

---

## 🎓 Mejores Prácticas

### ✅ DO (Hacer):
1. **Respetar las fases** - No forzar estrategias incompatibles
2. **Esperar confirmaciones** - Especialmente en FOBOs
3. **Usar fase como filtro** - Complemento a las estrategias A1/A2/A3
4. **Monitorear transiciones** - Los cambios de fase son oportunidades

### ❌ DON'T (No hacer):
1. **Operar A3 en Fase 1** - Requiere LR plana (Fase 3)
2. **Buscar FOBOs en Fase 1** - Necesita rango establecido
3. **Ignorar la fase** - Es contexto fundamental
4. **Operar contra la fase** - Reduce probabilidad de éxito

---

## 📊 Parámetros Ajustables

```python
# MarketPhaseDetector
slope_threshold = 1.0           # Umbral para tendencia fuerte
flat_slope_threshold = 0.5      # Umbral para LR plana

# FOBODetector
acceleration_threshold = 1.5    # Multiplicador de velocidad
min_bars_in_range = 5          # Mínimo barras para rango válido
```

Ajusta según:
- Timeframe utilizado
- Volatilidad del instrumento
- Backtesting results

---

## 🔍 Debugging y Monitoreo

### Obtener información de fase actual:
```python
phase_info = detector.get_phase_info()
print(phase_info)
```

Salida:
```python
{
    "current_phase": "PHASE_3",
    "bars_in_phase": 8,
    "range_established": True,
    "range_high": 50250.5,
    "range_low": 50100.2,
    "phase_description": "Lateralización - Movimiento en rango"
}
```

### Obtener contexto completo:
```python
context = signal_gen.get_market_context()
print(context)
```

Salida:
```python
{
    "phase_info": {...},
    "fobo_info": {
        "potential_fobo": "SUPPORT",
        "waiting_confirmation": True,
        "average_velocity": 25.3
    }
}
```

---

## 🎯 Conclusión

El sistema de detección de fases añade una **capa de contexto crucial** al trading:

- ✅ Filtra señales de baja calidad
- ✅ Mejora el timing de entradas
- ✅ Identifica oportunidades FOBO (80% probabilidad)
- ✅ Se integra perfectamente con A1, A2, A3

**Resultado:** Mayor tasa de éxito y mejor gestión de riesgo.
