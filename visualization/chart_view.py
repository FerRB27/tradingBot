"""
Visualizacion en tiempo real del bot de trading
Muestra Range Bars, Keltner, LR, EMAs y señales
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from datetime import datetime
import threading


class LiveChart:
    def __init__(self):
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        self.fig.canvas.manager.set_window_title('MDC Trading Bot - Range Bars BTCUSDT')
        
        self.bars = []
        self.indicators = {}
        self.signals = []
        
        plt.ion()  # Modo interactivo
        self.setup_chart()
        
    def setup_chart(self):
        """Configuracion inicial del grafico"""
        self.ax.set_facecolor('#0e1117')
        self.fig.patch.set_facecolor('#0e1117')
        self.ax.grid(True, alpha=0.2, color='white', linestyle='--')
        self.ax.set_xlabel('Range Bar #', color='white', fontsize=10)
        self.ax.set_ylabel('Precio (USDT)', color='white', fontsize=10)
        self.ax.tick_params(colors='white')
        
    def update(self, bars_data, indicators_data, signal_data=None):
        """
        Actualiza el grafico con nuevos datos
        
        bars_data: lista de dict con {open, high, low, close}
        indicators_data: dict con {
            'keltner_upper': [],
            'keltner_basis': [],
            'keltner_lower': [],
            'lr_values': [],
            'lr_slope': valor,
            'ema20': [],
            'ema80': []
        }
        signal_data: dict con {type, price, sl, tp} si hay señal
        """
        self.ax.clear()
        self.setup_chart()
        
        if len(bars_data) < 2:
            return
            
        # Mostrar solo las ultimas N barras para mejor visualizacion
        max_bars = 100
        start_idx = max(0, len(bars_data) - max_bars)
        bars_to_show = bars_data[start_idx:]
        
        # Dibujar Range Bars como velas japonesas
        for i, bar in enumerate(bars_to_show):
            x = start_idx + i
            open_price = bar['open']
            close_price = bar['close']
            high = bar['high']
            low = bar['low']
            
            # Color: verde si cierre > apertura, rojo si no
            color = '#00ff00' if close_price >= open_price else '#ff0000'
            
            # Dibujar mecha (high-low)
            self.ax.plot([x, x], [low, high], color=color, linewidth=1, alpha=0.8)
            
            # Dibujar cuerpo de la vela
            body_height = abs(close_price - open_price)
            body_bottom = min(open_price, close_price)
            
            rect = Rectangle(
                (x - 0.3, body_bottom),
                0.6,
                body_height if body_height > 0 else 0.01,
                facecolor=color,
                edgecolor=color,
                alpha=0.9
            )
            self.ax.add_patch(rect)
        
        # Dibujar indicadores
        x_range = list(range(start_idx, start_idx + len(bars_to_show)))
        
        # Keltner Channel
        if 'keltner_upper' in indicators_data and len(indicators_data['keltner_upper']) > start_idx:
            upper_raw = indicators_data['keltner_upper'][start_idx:]
            basis_raw = indicators_data['keltner_basis'][start_idx:]
            lower_raw = indicators_data['keltner_lower'][start_idx:]
            
            # Filtrar None values
            upper_clean = [(x_range[i], v) for i, v in enumerate(upper_raw) if v is not None]
            basis_clean = [(x_range[i], v) for i, v in enumerate(basis_raw) if v is not None]
            lower_clean = [(x_range[i], v) for i, v in enumerate(lower_raw) if v is not None]
            
            if upper_clean:
                x_upper, y_upper = zip(*upper_clean)
                self.ax.plot(x_upper, y_upper, color='#ff9800', linewidth=1.5, label='Keltner Upper', alpha=0.7)
            
            if basis_clean:
                x_basis, y_basis = zip(*basis_clean)
                self.ax.plot(x_basis, y_basis, color='#2196f3', linewidth=1.5, label='Keltner Basis (EMA)', alpha=0.7)
            
            if lower_clean:
                x_lower, y_lower = zip(*lower_clean)
                self.ax.plot(x_lower, y_lower, color='#ff9800', linewidth=1.5, label='Keltner Lower', alpha=0.7)
            
            # Rellenar area entre bandas
            if upper_clean and lower_clean:
                x_fill, y_upper_fill = zip(*upper_clean)
                _, y_lower_fill = zip(*lower_clean)
                self.ax.fill_between(x_fill, y_upper_fill, y_lower_fill, alpha=0.1, color='#ff9800')
        
        # Linear Regression
        if 'lr_values' in indicators_data and len(indicators_data['lr_values']) > start_idx:
            lr_raw = indicators_data['lr_values'][start_idx:]
            slope = indicators_data.get('lr_slope', 0)
            
            # Filtrar None values
            lr_clean = [(x_range[i], v) for i, v in enumerate(lr_raw) if v is not None]
            
            if lr_clean:
                x_lr, y_lr = zip(*lr_clean)
                # Color segun pendiente
                lr_color = '#00ff00' if slope > 0.5 else '#ff0000' if slope < -0.5 else '#ffeb3b'
                self.ax.plot(x_lr, y_lr, color=lr_color, linewidth=2, label=f'LR 89 (slope: {slope:.2f})', alpha=0.8)
        
        # EMAs
        if 'ema20' in indicators_data and len(indicators_data['ema20']) > start_idx:
            ema20_raw = indicators_data['ema20'][start_idx:]
            ema20_clean = [(x_range[i], v) for i, v in enumerate(ema20_raw) if v is not None]
            if ema20_clean:
                x_ema20, y_ema20 = zip(*ema20_clean)
                self.ax.plot(x_ema20, y_ema20, color='#9c27b0', linewidth=1, label='EMA 20', alpha=0.6, linestyle='--')
        
        if 'ema80' in indicators_data and len(indicators_data['ema80']) > start_idx:
            ema80_raw = indicators_data['ema80'][start_idx:]
            ema80_clean = [(x_range[i], v) for i, v in enumerate(ema80_raw) if v is not None]
            if ema80_clean:
                x_ema80, y_ema80 = zip(*ema80_clean)
                self.ax.plot(x_ema80, y_ema80, color='#673ab7', linewidth=1, label='EMA 80', alpha=0.6, linestyle='--')
        
        # Marcar señal si existe
        if signal_data:
            signal_x = len(bars_data) - 1
            signal_price = signal_data['price']
            signal_type = signal_data['type']
            
            # Flecha y texto de señal
            if signal_type == 'LONG':
                self.ax.annotate('▲ LONG', 
                               xy=(signal_x, signal_price),
                               xytext=(signal_x, signal_price - 200),
                               fontsize=12, color='#00ff00', weight='bold',
                               ha='center',
                               arrowprops=dict(arrowstyle='->', color='#00ff00', lw=2))
            else:
                self.ax.annotate('▼ SHORT', 
                               xy=(signal_x, signal_price),
                               xytext=(signal_x, signal_price + 200),
                               fontsize=12, color='#ff0000', weight='bold',
                               ha='center',
                               arrowprops=dict(arrowstyle='->', color='#ff0000', lw=2))
            
            # Lineas de SL y TP
            if 'sl' in signal_data:
                self.ax.axhline(y=signal_data['sl'], color='#ff0000', linestyle=':', 
                              linewidth=1.5, label=f"SL: ${signal_data['sl']:.2f}", alpha=0.8)
            
            if 'tp' in signal_data:
                self.ax.axhline(y=signal_data['tp'], color='#00ff00', linestyle=':', 
                              linewidth=1.5, label=f"TP: ${signal_data['tp']:.2f}", alpha=0.8)
            
            # Estrategia detectada
            strategy = signal_data.get('strategy', 'N/A')
            self.ax.text(0.02, 0.98, f'🎯 Señal: {strategy}', 
                        transform=self.ax.transAxes,
                        fontsize=11, color='#ffeb3b', weight='bold',
                        verticalalignment='top',
                        bbox=dict(boxstyle='round', facecolor='black', alpha=0.7))
        
        # Titulo con info actual
        current_bar = bars_to_show[-1]
        title = f"MDC Trading Bot | BTCUSDT Range Bars (100pts) | "
        title += f"O: ${current_bar['open']:.2f} H: ${current_bar['high']:.2f} "
        title += f"L: ${current_bar['low']:.2f} C: ${current_bar['close']:.2f} | "
        title += f"Total Barras: {len(bars_data)}"
        
        self.ax.set_title(title, color='white', fontsize=11, weight='bold', pad=15)
        
        # Leyenda
        self.ax.legend(loc='upper left', fontsize=8, facecolor='#1a1a1a', 
                      edgecolor='white', framealpha=0.8, labelcolor='white')
        
        # Ajustar limites del eje Y
        all_prices = [b['high'] for b in bars_to_show] + [b['low'] for b in bars_to_show]
        if all_prices:
            price_range = max(all_prices) - min(all_prices)
            self.ax.set_ylim(min(all_prices) - price_range * 0.1, 
                           max(all_prices) + price_range * 0.1)
        
        # Refrescar
        plt.tight_layout()
        plt.pause(0.01)
        
    def close(self):
        """Cerrar el grafico"""
        plt.close(self.fig)
