# 📊 Estrategias A1 vs A2 - MDC Trading Academy

## Comparación Rápida

| Característica | A1 | A2 |
|----------------|----|----|
| **Fortaleza** | 🟢 Más fuerte | 🟡 Moderada |
| **Requisito LR** | Precio EN o EN CONTACTO con LR | Precio SIN CONTACTO con LR |
| **Frecuencia** | Menos común | Más común |
| **Win Rate esperado** | Mayor | Moderado |
| **SL/TP** | Mismo (Keltner, 2:1) | Mismo (Keltner, 2:1) |

---

## 🟢 Estrategia A1 (Más Fuerte)

### LONG A1
1. ✅ Impulso alcista inmediato (LR negativo → positivo)
2. ✅ Precio en canal **superior** de Keltner
3. ✅ LR con dirección alcista (slope > 0)
4. ✅ Primera barra de retroceso toca banda media
5. ✅ **Precio ≥ LR** (está EN o EN CONTACTO con la línea)

**Interpretación**: El precio retrocede pero encuentra soporte en la LR, mostrando fuerza.

### SHORT A1
1. ✅ Impulso bajista inmediato (LR positivo → negativo)
2. ✅ Precio en canal **inferior** de Keltner
3. ✅ LR con dirección bajista (slope < 0)
4. ✅ Primera barra de retroceso toca banda media
5. ✅ **Precio ≤ LR** (está EN o EN CONTACTO con la línea)

**Interpretación**: El precio retrocede pero encuentra resistencia en la LR, mostrando debilidad.

---

## 🟡 Estrategia A2 (Moderada)

### LONG A2
1. ✅ Impulso alcista inmediato (LR negativo → positivo)
2. ✅ Precio en canal **superior** de Keltner
3. ✅ LR con dirección alcista (slope > 0)
4. ✅ Primera barra de retroceso toca banda media
5. ✅ **Precio < LR** y **SIN contacto** con la línea (High < LR)

**Interpretación**: El precio retrocede más profundo, sin tocar la LR. Entrada más conservadora.

### SHORT A2
1. ✅ Impulso bajista inmediato (LR positivo → negativo)
2. ✅ Precio en canal **inferior** de Keltner
3. ✅ LR con dirección bajista (slope < 0)
4. ✅ Primera barra de retroceso toca banda media
5. ✅ **Precio > LR** y **SIN contacto** con la línea (Low > LR)

**Interpretación**: El precio retrocede más profundo, sin tocar la LR. Entrada más conservadora.

---

## 🎯 Diferencia Clave

```
Setup: Precio en canal superior + Impulso alcista + LR alcista
       ↓
Retroceso a banda media...

┌─────────────────────────────────────────────────┐
│                                                 │
│  Precio toca/supera LR                         │
│  ✅ LONG A1 (Más fuerte)                       │
│                                                 │
│  ────────── LR (Linear Regression) ──────────  │
│                                                 │
│  Precio NO toca LR (queda debajo)              │
│  ✅ LONG A2 (Más conservadora)                 │
│                                                 │
│  ══════════ KC Basis (banda media) ══════════  │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 📋 Validación Técnica

### Validación A1 LONG
```python
# En el retroceso a banda media:
if price >= lr_value:  # Precio en o sobre LR
    return "LONG_A1"
```

### Validación A2 LONG
```python
# En el retroceso a banda media:
if price < lr_value and high < lr_value:  # Precio debajo y sin contacto
    return "LONG_A2"
```

### Validación A1 SHORT
```python
# En el retroceso a banda media:
if price <= lr_value:  # Precio en o bajo LR
    return "SHORT_A1"
```

### Validación A2 SHORT
```python
# En el retroceso a banda media:
if price > lr_value and low > lr_value:  # Precio arriba y sin contacto
    return "SHORT_A2"
```

---

## 🎲 Gestión de Riesgo (Igual para A1 y A2)

### LONG (A1 y A2)
- **Entry**: Precio de cierre de la barra señal
- **Stop Loss**: Banda **inferior** de Keltner
- **Take Profit**: Entry + (2 × distancia SL)
- **Ratio**: 1:2

### SHORT (A1 y A2)
- **Entry**: Precio de cierre de la barra señal
- **Stop Loss**: Banda **superior** de Keltner
- **Take Profit**: Entry - (2 × distancia SL)
- **Ratio**: 1:2

---

## 💡 Prioridad de Señales

Si en la misma barra se cumplen condiciones para A1 y A2:
```python
signal = signal_a1 or signal_a2  # A1 tiene prioridad
```

**Razón**: A1 es más fuerte porque el precio muestra mejor respecto a la LR.

---

## 📊 Expectativas

### A1 (Setup Ideal)
- Ocurrencia: **Menos frecuente**
- Win Rate: **60-70%** (con buena gestión)
- Señal: **Más confiable**

### A2 (Setup Alternativo)
- Ocurrencia: **Más frecuente**
- Win Rate: **50-60%** (con buena gestión)
- Señal: **Moderada confiabilidad**

---

## ✅ Bot Actualizado

El bot ahora detecta **ambas estrategias** automáticamente:

1. Cuando detecta impulso, configura ambas estrategias (A1 y A2)
2. Espera retroceso a banda media de Keltner
3. Evalúa condiciones específicas de cada una
4. Genera señal A1 o A2 según corresponda
5. Muestra SL/TP calculados (mismo método para ambas)

---

**Recuerda**: A1 tiene prioridad porque es más fuerte. Si se cumplen ambas, siempre tomará A1.
