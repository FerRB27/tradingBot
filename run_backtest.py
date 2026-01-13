"""
Script para ejecutar backtesting de estrategias A1, A2 y A3
"""
from backtesting.backtest import run_backtest

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔬 BACKTEST - ESTRATEGIAS A1, A2 & A3 (MDC Trading Academy)")
    print("="*70 + "\n")
    
    # Configurar parámetros del backtest
    # Intervalos disponibles: 1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d
    # Limit: máximo 1500 velas
    
    # Ejemplo 1: 1000 velas de 1 minuto (aprox. 16 horas de datos)
    print("📊 Configuración:")
    print("   Intervalo: 1m (1 minuto)")
    print("   Velas:     1000")
    print("   Range:     100 puntos")
    print("   Ratio R:R: 1:2 (SL en Keltner, TP = 2x distancia SL)")
    print("\n")
    
    run_backtest(interval="1m", limit=1000)
    
    print("\n" + "="*70)
    print("💡 TIP: Para más datos históricos, aumenta 'limit' o usa intervalos mayores:")
    print("   - interval='5m', limit=1500  → 5 días de datos")
    print("   - interval='15m', limit=1500 → 15 días de datos")
    print("   - interval='1h', limit=1500  → 62 días de datos")
    print("="*70 + "\n")
