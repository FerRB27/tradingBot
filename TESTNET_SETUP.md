# 🧪 CONFIGURACIÓN TESTNET - GUÍA RÁPIDA

## 📋 Paso 1: Obtener API Keys de Binance Testnet

### 🌐 Binance Futures Testnet:
1. Ve a: https://testnet.binancefuture.com/
2. Click en "Login" (esquina superior derecha)
3. Inicia sesión con tu cuenta de GitHub/Google
4. Una vez dentro, ve a tu perfil → **API Management**
5. Genera nuevas API keys:
   - Copia **API Key**
   - Copia **Secret Key**

### ⚠️ Importante:
- Las Testnet API keys son **DIFERENTES** a las de producción
- **NO uses las keys de producción en testnet**
- El dinero es **VIRTUAL** - puedes perder todo sin consecuencias

---

## 📝 Paso 2: Configurar API Keys en secrets.py

Edita `config/secrets.py`:

```python
# API KEY / SECRET - TESTNET (Dinero Virtual)
API_KEY = "tu_api_key_de_testnet_aqui"
API_SECRET = "tu_secret_key_de_testnet_aqui"
```

---

## 💰 Paso 3: Obtener Balance Virtual

En Binance Testnet:
1. Ve a **Wallet** o **Transfer**
2. Busca opción "Get Test Funds" o similar
3. Te darán **USDT virtual** (normalmente 100,000)

---

## ✅ Paso 4: Verificar Configuración

En `config/settings.py` debe estar:
```python
EXECUTE_TRADES = True  # ✅ Para ejecutar órdenes
TESTNET = True         # ✅ Para usar testnet
RISK_PERCENTAGE = 0.01 # 1% por trade
```

---

## 🚀 Paso 5: Ejecutar el Bot

```bash
python main.py
```

### Lo que verás:
```
======================================================================
🤖 MDC TRADING BOT - SISTEMA COMPLETO DE ESTRATEGIAS
======================================================================
  Símbolo:        BTCUSDT
  Range Size:     100 puntos
  Riesgo:         1.0%
  Estrategias:    A1, A2, A3, Trade 80, CBOT, Trade 20, FOBO
  Detección:      4 Fases del Mercado MDC + Anclas
  Modo:           🔴 LIVE TRADING         <-- ¡ACTIVO!
  Network:        🧪 TESTNET              <-- ¡TESTNET!
======================================================================
```

---

## 📊 Monitoreo

El bot mostrará:
- ✅ Conexión a WebSocket
- 📊 Range bars construyéndose
- 🚨 Señales detectadas
- 💼 **Órdenes ejecutadas en Binance Testnet**
- ✅ Confirmación de ejecución

---

## ⚠️ Troubleshooting

### Error: "API-key format invalid"
→ Las API keys están mal copiadas o son de producción

### Error: "Insufficient balance"
→ Necesitas fondos virtuales en testnet

### Error: "Invalid signature"
→ El API Secret está incorrecto

### No ejecuta órdenes:
→ Verifica que `EXECUTE_TRADES = True`

---

## 🎯 Siguiente Paso

Una vez funcionando en TESTNET:
1. **Déjalo correr 1 semana**
2. Monitorea trades diarios
3. Verifica que stops/targets funcionan
4. Si todo va bien → **MAINNET con capital pequeño**

---

## 📞 Soporte

Si encuentras errores, revisa:
- `execution/binance_client.py` → Manejo de API
- Logs en consola → Detalles del error
