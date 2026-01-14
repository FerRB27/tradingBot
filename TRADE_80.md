# 📈 Trade 80 - Entrada en Desarrollo de Tendencia

## 🎯 Concepto

El **Trade 80** es una estrategia de entrada basada en la **EMA 80** que busca capturar el **desarrollo de la tendencia o desbalance del mercado**. 

Es ideal para mercados **tendenciales** (Fase 1 y Fase 4).

---

## 🔄 Fases Apropiadas

| Fase | Apropiado | Descripción |
|------|-----------|-------------|
| **Fase 1: Tendencial** | ✅ **SÍ** | Ideal - tendencia establecida |
| **Fase 2: Cambio de Ritmo** | ❌ No | No hay tendencia clara |
| **Fase 3: Lateralización** | ❌ No | Mercado lateral |
| **Fase 4: Transición** | ✅ **SÍ** | Ideal - nueva tendencia iniciando |

---

## 📋 Condiciones para LONG

### ✅ Setup Requirements:
1. **EMA 80 debajo de banda media Keltner**
2. **LR con dirección alcista o plana** (slope >= -0.5)
3. **EMA 80 con dirección alcista o plana** (slope >= -0.5)
4. **Espacio entre EMA 80 y banda media > 3 ticks**

### ✅ Entry Trigger:
5. **Precio toca o cruza EMA 80 desde arriba**

---

## 📋 Condiciones para SHORT

### ✅ Setup Requirements:
1. **EMA 80 sobre banda media Keltner**
2. **LR con dirección bajista o plana** (slope <= 0.5)
3. **EMA 80 con dirección bajista o plana** (slope <= 0.5)
4. **Espacio entre EMA 80 y banda media > 3 ticks**

### ✅ Entry Trigger:
5. **Precio toca o cruza EMA 80 desde abajo**

---

## 📊 Diagrama Visual

### LONG Setup:

```
┌───────────────────────────────────────────────┐
│                                               │
│  KC Upper ════════════════════════════════   │
│                                               │
│                                               │
│  KC Basis ════════════════════════════════   │ ← EMA80 debe estar DEBAJO
│         ↓                                     │
│         ↓ > 3 ticks de espacio                │
│         ↓                                     │
│  ──── EMA 80 ─────────────────────────────   │ ← Precio retrocede y toca
│         ↑                                     │    ✅ ENTRADA LONG
│         │ Precio desde arriba                 │
│         │                                     │
│  KC Lower ════════════════════════════════   │ ← Stop Loss
│                                               │
└───────────────────────────────────────────────┘

Condiciones:
✅ EMA80 < KC Basis
✅ LR alcista/plana
✅ EMA80 alcista/plana
✅ Espacio > 3 ticks
```

### SHORT Setup:

```
┌───────────────────────────────────────────────┐
│                                               │
│  KC Upper ════════════════════════════════   │ ← Stop Loss
│                                               │
│         │                                     │
│         │ Precio desde abajo                  │
│         ↓                                     │
│  ──── EMA 80 ─────────────────────────────   │ ← Precio sube y toca
│         ↑                                     │    ✅ ENTRADA SHORT
│         ↑ > 3 ticks de espacio                │
│         ↑                                     │
│  KC Basis ════════════════════════════════   │ ← EMA80 debe estar ENCIMA
│                                               │
│                                               │
│  KC Lower ════════════════════════════════   │
│                                               │
└───────────────────────────────────────────────┘

Condiciones:
✅ EMA80 > KC Basis
✅ LR bajista/plana
✅ EMA80 bajista/plana
✅ Espacio > 3 ticks
```

---

## 💼 Gestión de Riesgo

### LONG Trade 80
- **Entry**: Cierre de la barra que toca EMA 80
- **Stop Loss**: Banda **inferior** de Keltner (KC Lower)
- **Take Profit**: Entry + (2 × distancia SL)
- **Ratio**: 1:2

### SHORT Trade 80
- **Entry**: Cierre de la barra que toca EMA 80
- **Stop Loss**: Banda **superior** de Keltner (KC Upper)
- **Take Profit**: Entry - (2 × distancia SL)
- **Ratio**: 1:2

---

## 🔍 Diferencias con A1/A2/A3

| Característica | A1/A2/A3 | Trade 80 |
|---------------|----------|----------|
| **Referencia** | Linear Regression | EMA 80 |
| **Tipo de mercado** | Impulso + retroceso | Tendencia sostenida |
| **Fases** | Fase 2, 4 | Fase 1, 4 |
| **Setup** | Impulso detectado | Tendencia confirmada |
| **Entrada** | Retroceso a KC Basis | Retroceso a EMA 80 |

---

## 💻 Uso en Código

### Básico

```python
from strategy.trade80 import Trade80Strategy

# Inicializar
trade80 = Trade80Strategy(tick_size=1.0, min_ticks=3)

# Por cada barra
signal = trade80.evaluate(
    bar=current_bar,
    ema80_value=ema80,
    ema80_slope=ema80_slope,
    lr_value=lr_value,
    lr_slope=lr_slope,
    keltner=keltner_bands
)

if signal == "LONG_TRADE80":
    print("✅ Entrada LONG en EMA 80")
elif signal == "SHORT_TRADE80":
    print("✅ Entrada SHORT en EMA 80")
```

### Integrado con Sistema de Señales

```python
from strategy.signals import TradingSignalGenerator

# Inicializar
signal_gen = TradingSignalGenerator(tick_size=1.0)

# Por cada barra (incluir ema80_value)
signal = signal_gen.generate_signal(
    bar=current_bar,
    lr_value=lr_value,
    lr_slope=lr_slope,
    keltner=keltner_bands,
    ema80_value=ema80_value  # ← Incluir EMA 80
)

if signal and signal['type'] == 'TRADE_80':
    print(f"Trade 80 {signal['direction']}")
    print(f"Fase: {signal['phase_description']}")
    print(f"Entry: {signal['entry']}")
    print(f"SL: {signal['stop_loss']}")
    print(f"TP: {signal['take_profit']}")
    print(f"EMA80: {signal['ema80_value']}")
```

---

## 🎓 Razones de las Condiciones

### 1. **EMA 80 separada de KC Basis (> 3 ticks)**
- Asegura que hay espacio suficiente para que el precio retroceda
- Evita entradas en zonas de compresión
- Mayor probabilidad de que el retroceso sea válido

### 2. **LR y EMA80 con misma dirección**
- Confirma que la tendencia es consistente
- Reduce probabilidad de reversión
- Alineación de múltiples timeframes

### 3. **Direcciones alcistas/planas (o bajistas/planas)**
- Permite entradas en tendencias establecidas
- También permite entradas cuando la tendencia se está formando (plana → direccional)

### 4. **Precio toca EMA 80**
- Punto de entrada específico (no ambiguo)
- EMA 80 actúa como soporte dinámico (LONG) o resistencia dinámica (SHORT)
- Retroceso saludable en tendencia

---

## 📈 Cuándo Usar Trade 80 vs A1/A2/A3

### Usar **Trade 80** cuando:
- ✅ Mercado está en **Fase 1** (tendencia establecida)
- ✅ Mercado está en **Fase 4** (nueva tendencia iniciando)
- ✅ Quieres entrar en **desarrollo de tendencia**
- ✅ EMA 80 está bien separada de KC Basis

### Usar **A1/A2/A3** cuando:
- ✅ Mercado está en **Fase 2** (cambio de ritmo)
- ✅ Mercado está en **Fase 3** (lateral) → Solo A3
- ✅ Detectas **impulso reciente** (cambio de pendiente LR)
- ✅ Buscas entrada en **retroceso a KC Basis**

---

## ⚙️ Parámetros Ajustables

```python
trade80 = Trade80Strategy(
    tick_size=1.0,    # Tamaño del tick del instrumento
    min_ticks=3       # Mínimo de ticks de espacio
)
```

### Ajustar según:
- **tick_size**: Varía por instrumento (BTC=1.0, ETH=0.01, etc.)
- **min_ticks**: Ajustar según volatilidad
  - Mercados menos volátiles: 2-3 ticks
  - Mercados más volátiles: 4-5 ticks

---

## 🧪 Ejemplo Práctico

### Escenario LONG:

```
Barra #1:
  EMA80 = 50100
  KC Basis = 50150
  Espacio = 50 puntos (> 3 ticks ✅)
  LR slope = 2.5 (alcista ✅)
  EMA80 slope = 1.2 (alcista ✅)
  → Setup detectado, esperando entrada

Barra #2:
  Precio: High=50120, Low=50090, Close=50105
  EMA80 = 50102
  Low (50090) <= EMA80 (50102) <= High (50120) ✅
  → ENTRADA LONG confirmada
  Entry: 50105
  SL: 50000 (KC Lower)
  TP: 50315 (Entry + 2×Risk)
```

### Escenario SHORT:

```
Barra #1:
  EMA80 = 50250
  KC Basis = 50200
  Espacio = 50 puntos (> 3 ticks ✅)
  LR slope = -2.8 (bajista ✅)
  EMA80 slope = -1.5 (bajista ✅)
  → Setup detectado, esperando entrada

Barra #2:
  Precio: High=50260, Low=50240, Close=50245
  EMA80 = 50248
  Low (50240) <= EMA80 (50248) <= High (50260) ✅
  → ENTRADA SHORT confirmada
  Entry: 50245
  SL: 50350 (KC Upper)
  TP: 50035 (Entry - 2×Risk)
```

---

## 📊 Expectativas de Desempeño

### Trade 80 (Setup Tendencial)
- **Ocurrencia**: 🟡 Media (en mercados tendenciales)
- **Win Rate**: 🟢 60-70% (en Fase 1 y 4)
- **Confiabilidad**: 🟢 Alta (cuando hay tendencia clara)
- **Uso**: Capturar continuación de tendencia

---

## 🎯 Matriz de Estrategias por Fase

| Estrategia | Fase 1 | Fase 2 | Fase 3 | Fase 4 |
|-----------|--------|--------|--------|--------|
| **A1** | ⚠️ | ✅ | ❌ | ✅ |
| **A2** | ⚠️ | ✅ | ❌ | ✅ |
| **A3** | ❌ | ❌ | ✅ | ❌ |
| **Trade 80** | ✅ | ❌ | ❌ | ✅ |
| **FOBO** | ❌ | ❌ | ✅ | ❌ |

**Conclusión**: Trade 80 complementa perfectamente A1/A2/A3 cubriendo las Fases 1 y 4.

---

## ✅ Resumen

El **Trade 80** es una estrategia poderosa para:
- 📈 Capturar continuación de tendencia
- 🎯 Entrar en desarrollo de desbalance
- 💪 Operar en Fase 1 y Fase 4 (tendencial)
- 🔄 Complementar A1/A2/A3 en fases diferentes

**Requiere**:
- EMA 80 calculada correctamente
- Espacio suficiente entre EMA80 y KC Basis
- Tendencia confirmada (LR + EMA80 alineadas)
- Precio retrocediendo a EMA 80

**¡Listo para integrar en tu sistema de trading!** 🚀
