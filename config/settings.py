# Parámetros de configuración Bot de Scalping con OrderBlocks

# === TRADING ===
SYMBOL = "BTCUSDT"
TIMEFRAME = "5m"  # Temporalidad de las velas japonesas

# === RIESGO ===
RISK_PERCENTAGE = 0.01  # 1% de riesgo por operación
LEVERAGE = 10  # Apalancamiento en Futures

# === INDICADORES ===
# (Solo OrderBlocks - otros indicadores removidos)

# === ORDER BLOCKS ===
DETECT_ORDER_BLOCKS = True  # Detección de OrderBlocks habilitada

# === EJECUCIÓN ===
EXECUTE_TRADES = False  # True = Ejecutar órdenes reales | False = Solo señales
TESTNET = False  # True = Red de pruebas | False = Red principal

# === BACKTEST ===
BACKTEST_LIMIT = 500  # Cantidad de velas a cargar para backtesting