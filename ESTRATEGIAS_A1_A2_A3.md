# 📊 Estrategias A1, A2 y A3 - MDC Trading Academy

## Resumen Comparativo

| Característica | A1 🟢 | A2 🟡 | A3 🟠 |
|----------------|-------|-------|-------|
| **Fortaleza** | Muy fuerte | Moderada | Especial (LR plana) |
| **Relación precio-LR** | EN o CON contacto | SIN contacto | DEBAJO/ARRIBA sin contacto |
| **Requisito LR** | Dirección alcista/bajista | Dirección alcista/bajista | **PLANA** (slope ≈ 0) |
| **Validación adicional** | - | - | Reward >= 2x Risk |
| **Frecuencia** | Baja | Media | Baja |
| **Complejidad** | Media | Media | Alta |

---

## 🟢 A1 - La Más Fuerte

### Setup Inicial (común para LONG y SHORT)
1. ✅ Impulso inmediato (cambio de pendiente LR)
2. ✅ Precio en canal extremo de Keltner (superior/inferior)
3. ✅ **LR con dirección** (alcista para LONG, bajista para SHORT)

### LONG A1
- **Condición inicial**: Precio en canal **superior** Keltner
- **En retroceso a banda media**: Precio **≥ LR** (está EN o CON la línea)
- **Interpretación**: El precio respeta la LR como soporte → Muy fuerte

### SHORT A1
- **Condición inicial**: Precio en canal **inferior** Keltner  
- **En retroceso a banda media**: Precio **≤ LR** (está EN o CON la línea)
- **Interpretación**: El precio respeta la LR como resistencia → Muy fuerte

---

## 🟡 A2 - Entrada Alternativa

### Setup Inicial
1. ✅ Impulso inmediato (cambio de pendiente LR)
2. ✅ Precio en canal extremo de Keltner
3. ✅ **LR con dirección** (alcista para LONG, bajista para SHORT)

### LONG A2
- **Condición inicial**: Precio en canal **superior** Keltner
- **En retroceso a banda media**: Precio **< LR** Y High **< LR** (SIN contacto)
- **Interpretación**: El precio retrocede más profundo pero LR sigue alcista

### SHORT A2
- **Condición inicial**: Precio en canal **inferior** Keltner
- **En retroceso a banda media**: Precio **> LR** Y Low **> LR** (SIN contacto)
- **Interpretación**: El precio retrocede más profundo pero LR sigue bajista

---

## 🟠 A3 - Setup Especial (LR Plana)

### Setup Inicial (DIFERENTE)
1. ✅ Impulso inmediato (cambio de pendiente LR)
2. ✅ Precio en canal extremo de Keltner
3. ✅ **Precio DEBAJO/ARRIBA de LR** (no importa dirección de LR inicial)

### LONG A3
- **Condición inicial**: 
  - Precio en canal **superior** Keltner
  - Precio **< LR** (DEBAJO de la línea)
- **En retroceso a banda media**:
  - LR debe estar **PLANA** (|slope| <= 0.5)
  - Distancia **(LR - KC Basis) >= 2x Riesgo**

**Validación matemática**:
```
Risk = KC Basis - KC Lower
Reward = LR - KC Basis
Condición: Reward >= 2 × Risk
```

### SHORT A3
- **Condición inicial**:
  - Precio en canal **inferior** Keltner
  - Precio **> LR** (ENCIMA de la línea)
- **En retroceso a banda media**:
  - LR debe estar **PLANA** (|slope| <= 0.5)
  - Distancia **(KC Basis - LR) >= 2x Riesgo**

**Validación matemática**:
```
Risk = KC Upper - KC Basis
Reward = KC Basis - LR
Condición: Reward >= 2 × Risk
```

---

## 📐 Diagrama Visual - Comparación

```
LONG Setup:

┌───────────────────────────────────────────────┐
│                                               │
│  KC Upper ════════════════════════════════   │
│                                               │
│        ╔═══ Precio en canal superior ═══╗    │
│        ║                                 ║    │
│  ──── LR (Regression Line) ────────────  │    │ A1: Precio alcanza/toca LR ✅
│        │                          A2 │   │    │ A2: Precio bajo LR sin tocar ✅
│        │     A1                      │   │    │ A3: LR plana + espacio 2:1 ✅
│        ↓                             ↓   │    │
│  KC Basis ════════════════════════════   │    │ ← Retroceso aquí
│                                               │
│  KC Lower ════════════════════════════════   │
│                                               │
└───────────────────────────────────────────────┘
```

---

## 🎯 Priorización de Señales

El bot evalúa las tres estrategias simultáneamente pero prioriza:

```python
signal = signal_a1 or signal_a2 or signal_a3
```

**Orden de prioridad**:
1. **A1** (más fuerte - precio con LR)
2. **A2** (moderada - precio sin LR pero LR direccional)
3. **A3** (especial - LR plana con espacio 2:1)

---

## 💼 Gestión de Riesgo (Igual para todas)

### LONG (A1, A2, A3)
- **Entry**: Precio de cierre cuando se detecta señal
- **Stop Loss**: Banda **inferior** de Keltner
- **Take Profit**: Entry + (2 × distancia SL)
- **Ratio**: 1:2

### SHORT (A1, A2, A3)
- **Entry**: Precio de cierre cuando se detecta señal
- **Stop Loss**: Banda **superior** de Keltner
- **Take Profit**: Entry - (2 × distancia SL)
- **Ratio**: 1:2

---

## 🔍 Diferencias Clave en Código

### A1: Precio EN/CON LR
```python
if price >= lr_value:  # LONG
    return "LONG_A1"
```

### A2: Precio SIN contacto con LR
```python
if price < lr_value and high < lr_value:  # LONG
    return "LONG_A2"
```

### A3: LR Plana + Validación de espacio
```python
if abs(lr_slope) <= 0.5:  # LR plana
    risk = entry - keltner["lower"]
    reward = lr_value - keltner["basis"]
    if reward >= (2 * risk):  # Espacio suficiente
        return "LONG_A3"
```

---

## 📊 Expectativas de Desempeño

### A1 (Setup Ideal)
- **Ocurrencia**: 🔴 Baja (más selectiva)
- **Win Rate**: 🟢 60-70%
- **Confiabilidad**: 🟢 Alta
- **Uso**: Setup principal

### A2 (Setup Alternativo)
- **Ocurrencia**: 🟡 Media
- **Win Rate**: 🟡 50-60%
- **Confiabilidad**: 🟡 Moderada
- **Uso**: Cuando A1 no califica

### A3 (Setup Especial)
- **Ocurrencia**: 🔴 Baja (requiere LR plana)
- **Win Rate**: 🟡 50-60%
- **Confiabilidad**: 🟡 Moderada-Alta
- **Uso**: Mercados en consolidación/laterales

---

## ⚙️ Parámetro Ajustable

### Umbral de LR "Plana" (A3)
```python
FLAT_SLOPE_THRESHOLD = 0.5
```

Si la LR está muy inclinada, A3 no se activará. Puedes ajustar este valor en [strategy/entries.py](strategy/entries.py) para hacerlo más o menos estricto:

- **0.3**: Más estricto (LR muy plana)
- **0.5**: Equilibrado (default)
- **0.8**: Más permisivo (LR casi plana)

---

## ✅ Bot Actualizado

El bot ahora detecta automáticamente las **3 estrategias**:

1. ✅ A1: Precio en/con LR + LR direccional
2. ✅ A2: Precio sin LR + LR direccional  
3. ✅ A3: Precio lejos de LR + LR plana + espacio 2:1

Todas con el mismo sistema de SL/TP (ratio 2:1 usando bandas Keltner).

---

**Recuerda**: El bot prioriza automáticamente A1 > A2 > A3 cuando múltiples condiciones se cumplen.
