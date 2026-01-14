# TRADE CBOT y TRADE 20 - Teoría de las Anclas

## 📚 Teoría de las Anclas

Las **anclas** son pivotes especiales que generaron cambio de impulso en el mercado:
- Son los llamados **puntos de fallo**
- Permiten diferenciar pivotes importantes de los que no lo son
- Nos permiten anticipar áreas de precio desde el corto plazo

### ⚓ Detección de Anclas
Se detectan cuando hay cambio de pendiente en Linear Regression:
- **Ancla de Resistencia**: Cuando LR cambia de alcista a bajista
- **Ancla de Soporte**: Cuando LR cambia de bajista a alcista

---

## 🎯 TRADE CBOT (Confirmación de Breakout)

**Trade de Rompimiento confirmado por anclas**

### Condiciones Generales:
✅ Mercados balanceados (Fase 3 - Lateralización)  
✅ Áreas de soporte/resistencia confirmadas por **2 o más anclas**  
✅ Ideal para volatilidades altas (crisis, pandemias, guerra comercial, incertidumbre)

### Condiciones para LONG:
1. **Mercado en Fase 3** (lateralizado)
2. **Área de resistencia** definida por 2+ anclas
3. Identificar el **pivote más alto** del área
4. **Entrada**: 3 ticks arriba de ese pivote más alto, en plena corrida del mercado

### Condiciones para SHORT:
1. **Mercado en Fase 3** (lateralizado)
2. **Área de soporte** definida por 2+ anclas
3. Identificar el **pivote más bajo** del área
4. **Entrada**: 3 ticks abajo de ese pivote más bajo, en plena corrida del mercado

### Ejemplo Visual CBOT LONG:
```
Precio
  │
  │    CBOT LONG aquí! (3 ticks arriba)
  ↑    ───────────────────────────
  │         ╱
  │        ╱ Breakout
  │       ╱
  │  ────────── ← Ancla Resistencia #2 (Pivote más alto)
  │      │
  │  ────┴────── ← Ancla Resistencia #1
  │      │   MERCADO LATERAL (Fase 3)
  │  ────┬──────
  │      │
  │  ────────── ← Anclas de Soporte
  │
  └────────────────────────► Tiempo
```

### Risk Management:
- **Stop Loss**: 1 tick debajo del nivel de las anclas opuestas
- **Take Profit**: R:R 1:2
- **Risk**: Distancia desde entry hasta el área de anclas

---

## 📈 TRADE 20 (Entrada en EMA 20 después de CBOT)

**Trade de impulso después del rompimiento de mercado lateral**

### Concepto:
Se anticipa que el retroceso después del rompimiento sea pequeño, por eso buscamos entrada en la **EMA 20**.

### Condiciones Generales:
✅ **Idealmente en Fase 4** (después de lateralización)  
✅ **CBOT previo válido** en la dirección del trade  
✅ Retroceso pequeño que toca la EMA 20

### Reglas para LONG:
1. **CBOT en dirección alcista** válido
2. Entrada en la **primera barra del retroceso que toque la EMA 20**
3. **Distancia mínima**: 4 ticks entre la EMA 20 y la banda superior del Keltner Channel

### Reglas para SHORT:
1. **CBOT en dirección bajista** válido
2. Entrada en la **primera barra del retroceso que toque la EMA 20**
3. **Distancia mínima**: 4 ticks entre la EMA 20 y la banda inferior del Keltner Channel

### Ejemplo Visual TRADE 20:
```
Precio
  │
  │                    ╱
  │                   ╱ Continuación
  │                  ╱
  │                 ↑ TRADE 20 aquí!
  │                │  (Toca EMA 20)
  │               ╱│╲
  │              ╱ │ ╲ Retroceso
  │             ╱  │  ╲
  │     CBOT! ╱   │   ╲
  │    ──────╱────┴────╲─── EMA 20
  │         ╱           ╲
  │  ──────────          ╲
  │    Anclas
  │
  └───────────────────────────► Tiempo
     Fase 3  │  Fase 4
```

### Risk Management:
- **Stop Loss**: 2 ticks debajo/arriba de EMA 20
- **Take Profit**: R:R 1:3 (más agresivo que otras estrategias)
- **Risk**: Distancia desde entry hasta stop loss

---

## 🤖 Integración en el Bot

### Archivos Creados:

#### 1. `strategy/anchor_detector.py`
- Clase `AnchorDetector`
- Detecta cambios de impulso (anclas)
- Agrupa anclas cercanas (tolerancia de 5 ticks)
- Identifica áreas de soporte/resistencia con 2+ anclas

#### 2. `strategy/trade_cbot.py`
- Clase `TradeCBOT`
- Evalúa breakouts confirmados por anclas
- Solo activa en Fase 3
- Entry a 3 ticks del pivote extremo

#### 3. `strategy/trade_20.py`
- Clase `Trade20Strategy`
- Busca retroceso a EMA 20 después de CBOT
- Idealmente en Fase 4
- Requiere 4+ ticks de distancia a Keltner

### Actualización de `signals.py`:
```python
# Prioridad de evaluación:
1. TRADE CBOT (si hay 2+ anclas y Fase 3)
2. TRADE 20 (si hay CBOT previo y toca EMA 20)
3. FOBO (si Fase 3)
4. TRADE 80 (si Fase 1 o Fase 4)
5. A1 (si apropiado según fase)
6. A2 (si apropiado según fase)
7. A3 (si Fase 3)
```

### Actualización del WebSocket:
- Muestra **EMA 20** en indicadores
- Muestra información de **anclas detectadas**
- Muestra detalles de **CBOT** cuando se detecta
- Muestra detalles de **TRADE 20** con CBOT previo

---

## 📊 Ejemplo de Señal CBOT

```
🚨 ══════════════════════════════════════════════════════════════
✅ SEÑAL CBOT LONG DETECTADA!
══════════════════════════════════════════════════════════════
  Fase: Lateralización - Mercado plano sin dirección clara
  Anclas: 2
  Pivote: $95200.00
  Breakout: $95203.00
  Entry Price:   $95203.00
  Stop Loss:     $94999.00 (-$204.00)
  Take Profit:   $95611.00 (+$408.00)
  Ratio R:R:     1:2
  Riesgo:        1.0% de la cuenta
```

## 📊 Ejemplo de Señal TRADE 20

```
🚨 ══════════════════════════════════════════════════════════════
✅ SEÑAL TRADE_20 LONG DETECTADA!
══════════════════════════════════════════════════════════════
  Fase: Transición - Mercado saliendo de lateralización
  EMA 20: $95270.00
  Distancia KC: 5.2 ticks
  CBOT previo: LONG @ $95350.00
  Entry Price:   $95268.00
  Stop Loss:     $95268.00 (-$2.00)
  Take Profit:   $95274.00 (+$6.00)
  Ratio R:R:     1:3
  Riesgo:        1.0% de la cuenta
```

---

## 🎯 Resumen de Estrategias

| Estrategia | Fase Ideal | Indicador Clave | R:R | Condición Especial |
|-----------|-----------|----------------|-----|-------------------|
| **A1** | 2, 4 | LR + Impulso | 1:2 | Entrada en contra de impulso |
| **A2** | 2, 4 | Keltner + Impulso | 1:2 | Precio fuera de banda |
| **A3** | 3 | LR plana | 1:2 | Mercado lateral |
| **Trade 80** | 1, 4 | EMA 80 | 1:2 | Precio cerca de EMA 80 |
| **CBOT** | 3 | **Anclas (2+)** | 1:2 | Breakout confirmado |
| **Trade 20** | 4 | **EMA 20 + CBOT** | **1:3** | Después de breakout |
| **FOBO** | 3 | Aceleración | 1:2 | 80% probabilidad reversal |

---

## ✅ Ventajas de las Nuevas Estrategias

### TRADE CBOT:
✅ **Confirmación objetiva**: Requiere 2+ anclas (no subjetivo)  
✅ **Alta probabilidad**: Breakout confirmado por múltiples puntos de fallo  
✅ **Gestión clara**: Stops definidos por las anclas  
✅ **Versatilidad**: Funciona en alta volatilidad

### TRADE 20:
✅ **R:R superior**: 1:3 vs 1:2 de otras estrategias  
✅ **Momentum fuerte**: Aprovecha el impulso del breakout  
✅ **Entry precisa**: EMA 20 como nivel objetivo claro  
✅ **Secuencial**: Complementa perfectamente al CBOT

---

## 🧪 Testing

Ejecutar el demo:
```bash
python demo_cbot_trade20.py
```

Este demo simula:
1. Mercado lateral (Fase 3) con múltiples anclas
2. Detección de áreas de soporte/resistencia
3. CBOT cuando rompe con 2+ anclas
4. Trade 20 cuando retrocede a EMA 20

---

## 🚀 Próximos Pasos

1. **Backtest**: Probar CBOT y Trade 20 con datos históricos
2. **Optimización**: Ajustar tolerancia de anclas y distancia a Keltner
3. **Estadísticas**: Medir win rate de cada estrategia por fase
4. **Live Testing**: Ejecutar en TESTNET antes de MAINNET
