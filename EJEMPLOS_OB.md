# 📊 Ejemplos Visuales de OrderBlocks

## 🟢 Ejemplo 1: Bullish OrderBlock

### Condición
```
high[2] < low[0]
```

El **high de hace 2 velas** está por debajo del **low de la vela actual**.

### Representación Visual

```
Precio
  │
  │                    ┌─────┐
  │                    │ [0] │  ← Vela ACTUAL
110 │                  │     │     Low = 110
  │                    └─────┘
  │          ┌─────┐
  │          │ [1] │            ← Vela ANTERIOR
105 │        │     │
  │          └─────┘
  │
  │   ┌─────┐                  ← Vela hace 2 (OB)
100 │   │  X  │ ← HIGH = 100      ✅ 100 < 110
  │   │     │                      BULLISH OB!
95  │   └─────┘
  │
  └────────────────────────────────────────► Tiempo
      [2]     [1]     [0]
```

### Datos del Ejemplo
```
Vela [2] (hace 2):  Open=95   High=100  Low=90   Close=98
Vela [1] (anterior): Open=98   High=105  Low=97   Close=104
Vela [0] (actual):   Open=104  High=115  Low=110  Close=113

Condición: high[2]=100 < low[0]=110 ✅ TRUE
Resultado: BULLISH ORDER BLOCK detectado en vela [2]
```

### Interpretación
- El precio ha **saltado hacia arriba**
- Dejó un "hueco" entre 100 y 110
- La vela [2] es un **bloque de órdenes de compra** institucional
- Posible zona de **soporte futuro**

---

## 🔴 Ejemplo 2: Bearish OrderBlock

### Condición
```
low[2] > high[0]
```

El **low de hace 2 velas** está por encima del **high de la vela actual**.

### Representación Visual

```
Precio
  │
  │   ┌─────┐                  ← Vela hace 2 (OB)
110 │   │     │
  │   │     │
105 │   └─────┘ ← LOW = 100     ✅ 100 > 90
  │        │  X  │                  BEARISH OB!
100 │      └─────┘
  │          ┌─────┐
  │          │ [1] │            ← Vela ANTERIOR
95  │        │     │
  │          └─────┘
  │                    ┌─────┐
  │                    │ [0] │  ← Vela ACTUAL
90  │                  │     │     High = 90
  │                    └─────┘
  │
  └────────────────────────────────────────► Tiempo
      [2]     [1]     [0]
```

### Datos del Ejemplo
```
Vela [2] (hace 2):  Open=105  High=110  Low=100  Close=102
Vela [1] (anterior): Open=102  High=103  Low=95   Close=96
Vela [0] (actual):   Open=96   High=90   Low=85   Close=87

Condición: low[2]=100 > high[0]=90 ✅ TRUE
Resultado: BEARISH ORDER BLOCK detectado en vela [2]
```

### Interpretación
- El precio ha **caído abruptamente**
- Dejó un "hueco" entre 100 y 90
- La vela [2] es un **bloque de órdenes de venta** institucional
- Posible zona de **resistencia futuro**

---

## ❌ Ejemplo 3: Sin OrderBlock

### Representación Visual

```
Precio
  │
  │                    ┌─────┐
  │                    │ [0] │  ← Vela ACTUAL
108 │                  │     │     Low = 104
  │                    └─────┘     High = 108
  │
  │          ┌─────┐
  │          │ [1] │            ← Vela ANTERIOR
105 │        │     │
  │          └─────┘
  │
  │   ┌─────┐                  ← Vela hace 2
  │   │     │ ← HIGH = 105        ❌ 105 NO < 104
100 │   │     │                   ❌ 98 NO > 108
  │   └─────┘ ← LOW = 98          Sin OB
  │
  └────────────────────────────────────────► Tiempo
      [2]     [1]     [0]
```

### Datos del Ejemplo
```
Vela [2] (hace 2):  Open=100  High=105  Low=98   Close=103
Vela [1] (anterior): Open=103  High=107  Low=101  Close=105
Vela [0] (actual):   Open=105  High=108  Low=104  Close=106

Condición Bullish: high[2]=105 < low[0]=104 ❌ FALSE (105 no es < 104)
Condición Bearish: low[2]=98 > high[0]=108 ❌ FALSE (98 no es > 108)
Resultado: NO se detectó OrderBlock
```

### Interpretación
- El precio se mueve de forma **continua**
- No hay "huecos" o saltos significativos
- **Movimiento normal del mercado**

---

## 📈 Caso Real: Bitcoin

### Escenario Bullish OB

```
BTCUSDT - 5m

Hora      Vela    Open      High      Low       Close
────────────────────────────────────────────────────────
14:30     [2]     $72,150   $72,250   $72,100   $72,200  ← OB
14:35     [1]     $72,200   $72,450   $72,180   $72,400
14:40     [0]     $72,400   $72,600   $72,350   $72,550

Detección:
- high[2] = $72,250
- low[0]  = $72,350
- Condición: $72,250 < $72,350 ✅ TRUE
- Resultado: 🟢 BULLISH ORDER BLOCK

Zona de OB: $72,100 - $72,250
Rango OB: $150
```

### Escenario Bearish OB

```
BTCUSDT - 5m

Hora      Vela    Open      High      Low       Close
────────────────────────────────────────────────────────
14:30     [2]     $73,500   $73,650   $73,450   $73,550  ← OB
14:35     [1]     $73,550   $73,580   $73,200   $73,250
14:40     [0]     $73,250   $73,300   $73,100   $73,150

Detección:
- low[2]  = $73,450
- high[0] = $73,300
- Condición: $73,450 > $73,300 ✅ TRUE
- Resultado: 🔴 BEARISH ORDER BLOCK

Zona de OB: $73,450 - $73,650
Rango OB: $200
```

---

## 🎯 Uso en Trading

### Bullish OrderBlock 🟢
- **¿Qué es?** Zona donde instituciones compraron
- **Uso:** Buscar entradas LONG cuando el precio retorna a esta zona
- **Stop Loss:** Por debajo del OB
- **Confluencias:** Soportes, niveles clave, fibonacci

### Bearish OrderBlock 🔴
- **¿Qué es?** Zona donde instituciones vendieron
- **Uso:** Buscar entradas SHORT cuando el precio retorna a esta zona
- **Stop Loss:** Por encima del OB
- **Confluencias:** Resistencias, niveles clave, fibonacci

---

## 🔍 Comparación con TradingView

### PineScript (Original)
```javascript
// Vela hace 2
high_two_ago := high[2]
low_two_ago  := low[2]

// Vela actual
high_current := high
low_current  := low

// Detección
is_bullish_order_block = high_two_ago < low_current
is_bearish_order_block = low_two_ago > high_current
```

### Python (Nuestra Implementación)
```python
# Obtener velas
current = candles[-1]
two_ago = candles[-3]

# Detección
is_bullish_ob = two_ago['high'] < current['low']
is_bearish_ob = two_ago['low'] > current['high']
```

**✅ Lógica idéntica al indicador de TradingView**

---

## 📊 Estadísticas Esperadas

En un mercado volátil (como crypto):
- **Frecuencia:** 1-5 OrderBlocks por día (timeframe 5m)
- **Efectividad:** Variable (depende de contexto del mercado)
- **Mejores condiciones:** Después de noticias importantes o rupturas de rango

---

## 💡 Tips de Interpretación

### ✅ Buenos OrderBlocks
- Rango amplio (indica presión fuerte)
- En zonas clave (soportes/resistencias)
- Alineados con tendencia mayor
- Confirmados por volumen alto

### ⚠️ OrderBlocks Débiles
- Rango muy pequeño
- En medio de zona sin estructura
- Contra tendencia principal
- Bajo volumen

---

## 🧪 Verificación del Detector

Para verificar que el detector funciona correctamente:

```bash
python demo_order_blocks.py
```

Deberías ver:
```
✅ BULLISH OrderBlock detectado!   # Caso 1
✅ BEARISH OrderBlock detectado!   # Caso 2
❌ No se detectó OrderBlock        # Caso 3
```

---

**Referencia:** Este documento explica la lógica implementada en `indicators/order_blocks.py` basada en el indicador de TradingView (`indicadorOB.txt`).
