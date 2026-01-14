"""
Backtesting Completo - Sistema MDC
===================================
Descarga datos históricos de Binance y ejecuta backtest de todas las estrategias.
"""

import requests
from datetime import datetime, timedelta
import time
from collections import defaultdict

from market_data.range_builder import RangeBarBuilder
from indicators.regression import linear_regression
from indicators.keltner import keltner_channel
from indicators.ema import ema
from strategy.signals import TradingSignalGenerator


class BacktestResults:
    """Clase para almacenar y calcular resultados del backtest"""
    
    def __init__(self, initial_balance=10000):
        self.initial_balance = initial_balance
        self.balance = initial_balance
        self.trades = []
        self.equity_curve = [initial_balance]
        self.strategy_stats = defaultdict(lambda: {
            'total': 0, 'wins': 0, 'losses': 0, 
            'profit': 0, 'loss': 0
        })
        
    def add_trade(self, trade):
        """Registra un trade"""
        self.trades.append(trade)
        
        # Actualizar balance
        pnl = trade['pnl']
        self.balance += pnl
        self.equity_curve.append(self.balance)
        
        # Estadísticas por estrategia
        strategy = trade['strategy']
        stats = self.strategy_stats[strategy]
        stats['total'] += 1
        
        if pnl > 0:
            stats['wins'] += 1
            stats['profit'] += pnl
        else:
            stats['losses'] += 1
            stats['loss'] += abs(pnl)
    
    def print_summary(self):
        """Imprime resumen de resultados"""
        print("\n" + "="*80)
        print("📊 RESUMEN DEL BACKTEST")
        print("="*80)
        
        total_trades = len(self.trades)
        wins = sum(1 for t in self.trades if t['pnl'] > 0)
        losses = total_trades - wins
        
        total_profit = sum(t['pnl'] for t in self.trades if t['pnl'] > 0)
        total_loss = abs(sum(t['pnl'] for t in self.trades if t['pnl'] < 0))
        
        net_profit = self.balance - self.initial_balance
        return_pct = (net_profit / self.initial_balance) * 100
        
        print(f"\n💰 Rendimiento General:")
        print(f"  Balance Inicial:    ${self.initial_balance:,.2f}")
        print(f"  Balance Final:      ${self.balance:,.2f}")
        print(f"  Ganancia/Pérdida:   ${net_profit:,.2f} ({return_pct:+.2f}%)")
        
        print(f"\n📈 Estadísticas de Trading:")
        print(f"  Total Trades:       {total_trades}")
        print(f"  Operaciones Ganadoras: {wins} ({wins/total_trades*100:.1f}%)")
        print(f"  Operaciones Perdedoras: {losses} ({losses/total_trades*100:.1f}%)")
        
        if total_loss > 0:
            profit_factor = total_profit / total_loss
            print(f"  Profit Factor:      {profit_factor:.2f}")
        
        if wins > 0:
            avg_win = total_profit / wins
            print(f"  Ganancia Promedio:  ${avg_win:.2f}")
        
        if losses > 0:
            avg_loss = total_loss / losses
            print(f"  Pérdida Promedio:   ${avg_loss:.2f}")
        
        # Estadísticas por estrategia
        print(f"\n🎯 Rendimiento por Estrategia:")
        print(f"  {'Estrategia':<12} {'Trades':<8} {'Wins':<6} {'W%':<8} {'Profit':<12} {'Loss':<12} {'Net':<12}")
        print(f"  {'-'*78}")
        
        for strategy in ['CBOT', 'TRADE_20', 'FOBO', 'TRADE_80', 'A1', 'A2', 'A3']:
            stats = self.strategy_stats.get(strategy)
            if stats and stats['total'] > 0:
                win_rate = (stats['wins'] / stats['total']) * 100
                net = stats['profit'] - stats['loss']
                print(f"  {strategy:<12} {stats['total']:<8} {stats['wins']:<6} "
                      f"{win_rate:<7.1f}% ${stats['profit']:<11.2f} "
                      f"${stats['loss']:<11.2f} ${net:<11.2f}")
        
        # Drawdown
        max_balance = self.initial_balance
        max_drawdown = 0
        for balance in self.equity_curve:
            if balance > max_balance:
                max_balance = balance
            drawdown = ((max_balance - balance) / max_balance) * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        print(f"\n📉 Riesgo:")
        print(f"  Drawdown Máximo:    {max_drawdown:.2f}%")
        
        print("="*80)


def download_binance_klines(symbol, interval='1m', days=7):
    """
    Descarga datos históricos de Binance
    
    Args:
        symbol: Par de trading (ej: BTCUSDT)
        interval: Intervalo de velas (1m, 5m, 15m, 1h)
        days: Días hacia atrás
    
    Returns:
        Lista de precios (solo closes para construir range bars)
    """
    print(f"\n📥 Descargando datos históricos de Binance...")
    print(f"   Símbolo: {symbol}")
    print(f"   Intervalo: {interval}")
    print(f"   Período: últimos {days} días")
    
    url = "https://api.binance.com/api/v3/klines"
    
    end_time = int(time.time() * 1000)
    start_time = int((time.time() - (days * 24 * 60 * 60)) * 1000)
    
    all_trades = []
    
    # Binance limita a 1000 velas por request
    while start_time < end_time:
        params = {
            'symbol': symbol,
            'interval': interval,
            'startTime': start_time,
            'endTime': end_time,
            'limit': 1000
        }
        
        try:
            response = requests.get(url, params=params)
            data = response.json()
            
            if not data:
                break
            
            # Extraer precios (open, high, low, close)
            for candle in data:
                all_trades.append({
                    'timestamp': candle[0],
                    'open': float(candle[1]),
                    'high': float(candle[2]),
                    'low': float(candle[3]),
                    'close': float(candle[4]),
                    'volume': float(candle[5])
                })
            
            # Actualizar start_time para siguiente batch
            start_time = data[-1][0] + 1
            
            print(f"   Descargadas {len(all_trades)} velas...", end='\r')
            
        except Exception as e:
            print(f"\n❌ Error descargando datos: {e}")
            break
    
    print(f"\n✅ Descarga completa: {len(all_trades)} velas")
    return all_trades


def klines_to_range_bars(klines, range_size):
    """
    Convierte velas de Binance a Range Bars
    
    Args:
        klines: Lista de velas con OHLC
        range_size: Tamaño del range bar
    
    Returns:
        Lista de range bars completas
    """
    print(f"\n🔨 Construyendo Range Bars de {range_size} puntos...")
    
    range_builder = RangeBarBuilder(range_size)
    bars = []
    
    # Simular trades usando OHLC de cada vela
    for i, kline in enumerate(klines):
        # Generar precios intermedios para simular movimiento real
        prices = [
            kline['open'],
            kline['high'],
            kline['low'],
            kline['close']
        ]
        
        for price in prices:
            completed_bar = range_builder.process_trade(price)
            if completed_bar:
                bars.append(completed_bar)
        
        if (i + 1) % 1000 == 0:
            print(f"   Procesadas {i+1} velas → {len(bars)} range bars", end='\r')
    
    print(f"\n✅ Range Bars construidas: {len(bars)}")
    return bars


def run_backtest(bars, initial_balance=10000, risk_pct=0.01):
    """
    Ejecuta backtest completo con todas las estrategias
    
    Args:
        bars: Lista de range bars
        initial_balance: Balance inicial
        risk_pct: Porcentaje de riesgo por trade
    
    Returns:
        BacktestResults con todos los resultados
    """
    print(f"\n🚀 Ejecutando Backtest...")
    print(f"   Balance inicial: ${initial_balance:,.2f}")
    print(f"   Riesgo por trade: {risk_pct*100}%")
    print(f"   Total de barras: {len(bars)}")
    
    results = BacktestResults(initial_balance)
    signal_generator = TradingSignalGenerator(tick_size=1.0)
    
    # Para almacenar indicadores
    closes = []
    
    # Estado de posición
    in_position = False
    current_trade = None
    
    for i, bar in enumerate(bars):
        closes.append(bar['close'])
        
        # Calcular indicadores (necesitan suficiente historial)
        if len(closes) < 90:
            continue
        
        lr = linear_regression(closes, 89)
        lr_value = lr[0] if lr else None
        lr_slope = lr[1] if lr else None
        
        kc = keltner_channel(bars[:i+1])
        ema20_val = ema(closes, 20)
        ema80_val = ema(closes, 80)
        
        if not lr_value or not lr_slope or not kc:
            continue
        
        # Si estamos en posición, verificar stop/take
        if in_position:
            hit_stop = False
            hit_target = False
            
            if current_trade['direction'] == 'LONG':
                if bar['low'] <= current_trade['stop_loss']:
                    hit_stop = True
                    exit_price = current_trade['stop_loss']
                elif bar['high'] >= current_trade['take_profit']:
                    hit_target = True
                    exit_price = current_trade['take_profit']
            else:  # SHORT
                if bar['high'] >= current_trade['stop_loss']:
                    hit_stop = True
                    exit_price = current_trade['stop_loss']
                elif bar['low'] <= current_trade['take_profit']:
                    hit_target = True
                    exit_price = current_trade['take_profit']
            
            # Cerrar posición si tocó stop o target
            if hit_stop or hit_target:
                # Calcular PnL
                if current_trade['direction'] == 'LONG':
                    pnl_points = exit_price - current_trade['entry']
                else:
                    pnl_points = current_trade['entry'] - exit_price
                
                # Calcular PnL en dinero (arriesgando risk_pct del balance)
                risk_amount = results.balance * risk_pct
                pnl = (pnl_points / current_trade['risk']) * risk_amount * current_trade['ratio'] if hit_target else -risk_amount
                
                # Registrar trade
                trade_record = {
                    'strategy': current_trade['strategy'],
                    'direction': current_trade['direction'],
                    'entry': current_trade['entry'],
                    'exit': exit_price,
                    'stop_loss': current_trade['stop_loss'],
                    'take_profit': current_trade['take_profit'],
                    'result': 'WIN' if hit_target else 'LOSS',
                    'pnl': pnl,
                    'bar_index': i
                }
                
                results.add_trade(trade_record)
                
                in_position = False
                current_trade = None
        
        # Si no estamos en posición, buscar nueva señal
        if not in_position:
            signal = signal_generator.generate_signal(
                bar=bar,
                lr_value=lr_value,
                lr_slope=lr_slope,
                keltner=kc,
                ema80_value=ema80_val,
                ema20_value=ema20_val
            )
            
            if signal:
                # Abrir nueva posición
                current_trade = {
                    'strategy': signal['type'],
                    'direction': signal['direction'],
                    'entry': signal['entry'],
                    'stop_loss': signal['stop_loss'],
                    'take_profit': signal['take_profit'],
                    'risk': signal['risk'],
                    'ratio': signal['ratio'],
                    'bar_index': i
                }
                in_position = True
        
        # Progreso
        if (i + 1) % 100 == 0:
            print(f"   Procesadas {i+1}/{len(bars)} barras ({(i+1)/len(bars)*100:.1f}%) | Trades: {len(results.trades)} | Balance: ${results.balance:,.2f}", end='\r')
    
    print(f"\n✅ Backtest completado: {len(results.trades)} trades ejecutados")
    
    return results


if __name__ == "__main__":
    print("="*80)
    print("🤖 BACKTESTING SISTEMA MDC - 7 ESTRATEGIAS")
    print("="*80)
    
    # Configuración
    SYMBOL = 'BTCUSDT'
    INTERVAL = '5m'  # Velas de 5 minutos (más rápido que 1m)
    DAYS = 7  # Última semana
    RANGE_SIZE = 100  # Range bars de 100 puntos
    INITIAL_BALANCE = 10000
    RISK_PCT = 0.01  # 1% por trade
    
    # 1. Descargar datos
    klines = download_binance_klines(SYMBOL, INTERVAL, DAYS)
    
    if not klines:
        print("❌ No se pudieron descargar datos")
        exit(1)
    
    # 2. Convertir a Range Bars
    bars = klines_to_range_bars(klines, RANGE_SIZE)
    
    if len(bars) < 100:
        print(f"❌ Muy pocas barras ({len(bars)}). Necesitas al menos 100.")
        exit(1)
    
    # 3. Ejecutar backtest
    results = run_backtest(bars, INITIAL_BALANCE, RISK_PCT)
    
    # 4. Mostrar resultados
    results.print_summary()
    
    # 5. Mostrar últimos 10 trades
    print(f"\n📋 Últimos 10 Trades:")
    print(f"  {'#':<4} {'Estrategia':<12} {'Dir':<6} {'Entry':<10} {'Exit':<10} {'Result':<6} {'PnL':<12}")
    print(f"  {'-'*78}")
    
    for i, trade in enumerate(results.trades[-10:], 1):
        print(f"  {i:<4} {trade['strategy']:<12} {trade['direction']:<6} "
              f"${trade['entry']:<9.2f} ${trade['exit']:<9.2f} "
              f"{trade['result']:<6} ${trade['pnl']:<11.2f}")
    
    print("\n" + "="*80)
