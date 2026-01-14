# Parámetros de configuración MDC Bot

# === TRADING ===
SYMBOL = "BTCUSDT"
RANGE_SIZE = 100  # Tamaño de las Range Bars

# === RIESGO ===
RISK_PERCENTAGE = 0.01  # 1% de riesgo por operación
LEVERAGE = 10  # Apalancamiento en Futures

# === INDICADORES ===
# Linear Regression
LR_PERIOD = 89

# Keltner Channel
KC_PERIOD = 52
KC_MULTIPLIER = 3.5

# EMAs (para análisis adicional si se requiere)
EMA_FAST = 20
EMA_SLOW = 80

# === EJECUCIÓN ===
EXECUTE_TRADES = True  # True = Ejecutar órdenes reales | False = Solo señales
TESTNET = False  # True = Red de pruebas | False = Red principal

# === BACKTEST ===
BACKTEST_LIMIT = 1000  # Cantidad de trades históricos a cargar