"""
TRADE 20 - Entrada en EMA 20 después de CBOT (MDC)
===================================================
Trade de impulso después del rompimiento de un mercado lateral.
Se anticipa retroceso pequeño con entrada en la EMA 20.
"""

class Trade20Strategy:
    """
    Estrategia TRADE 20 para entradas en EMA 20 después de CBOT.
    
    Condiciones:
    - Idealmente en Fase 4 (después de lateralización)
    - CBOT previo válido en la dirección
    - Primera barra de retroceso que toca EMA 20
    - Distancia >= 4 ticks entre EMA 20 y banda superior/inferior de Keltner
    """
    
    def __init__(self, tick_size=1.0, min_distance_ticks=4):
        """
        Args:
            tick_size: Tamaño del tick del instrumento
            min_distance_ticks: Distancia mínima entre EMA 20 y Keltner
        """
        self.tick_size = tick_size
        self.min_distance_ticks = min_distance_ticks
        
        # Track si ya tocó la 20 para evitar múltiples entradas
        self.has_touched_ema20 = False
        self.waiting_for_pullback = False
        self.cbot_direction = None
    
    def evaluate(self, bar, current_phase, ema20_value, keltner, last_cbot):
        """
        Evalúa si hay setup Trade 20 válido.
        
        Args:
            bar: Barra actual con OHLC
            current_phase: Fase actual del mercado
            ema20_value: Valor actual de EMA 20
            keltner: Dict con bandas de Keltner {upper, basis, lower}
            last_cbot: Último CBOT detectado (de TradeCBOT)
            
        Returns:
            dict con señal o None
        """
        # Validar que tenemos todos los datos
        if not ema20_value or not keltner or not last_cbot:
            return None
        
        # Idealmente en Fase 4, pero puede darse en otras fases
        # (no es restricción estricta, solo preferencia)
        
        close_price = bar['close']
        high_price = bar['high']
        low_price = bar['low']
        
        cbot_direction = last_cbot['direction']
        
        # TRADE 20 LONG (después de CBOT alcista)
        if cbot_direction == 'LONG':
            # Verificar distancia mínima entre EMA 20 y banda superior de Keltner
            distance_to_upper = keltner['upper'] - ema20_value
            distance_in_ticks = distance_to_upper / self.tick_size
            
            if distance_in_ticks < self.min_distance_ticks:
                return None
            
            # Detectar si la barra toca o cruza la EMA 20 en retroceso
            if low_price <= ema20_value <= high_price:
                
                # Evitar múltiples entradas en la misma secuencia
                if self.has_touched_ema20 and self.cbot_direction == cbot_direction:
                    return None
                
                # Entrada en el cierre de la barra que toca la 20
                entry_price = close_price
                
                # Stop debajo de la EMA 20
                risk_distance = abs(entry_price - (ema20_value - (2 * self.tick_size)))
                stop_loss = ema20_value - (2 * self.tick_size)
                take_profit = entry_price + (risk_distance * 3)  # R:R 1:3
                
                # Marcar que ya tocó la 20
                self.has_touched_ema20 = True
                self.cbot_direction = cbot_direction
                
                return {
                    'type': 'TRADE_20',
                    'direction': 'LONG',
                    'entry': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'risk': risk_distance,
                    'reward': risk_distance * 3,
                    'ratio': 3,
                    'ema20_value': ema20_value,
                    'keltner_distance': distance_in_ticks,
                    'cbot_info': last_cbot
                }
        
        # TRADE 20 SHORT (después de CBOT bajista)
        elif cbot_direction == 'SHORT':
            # Verificar distancia mínima entre EMA 20 y banda inferior de Keltner
            distance_to_lower = ema20_value - keltner['lower']
            distance_in_ticks = distance_to_lower / self.tick_size
            
            if distance_in_ticks < self.min_distance_ticks:
                return None
            
            # Detectar si la barra toca o cruza la EMA 20 en retroceso
            if low_price <= ema20_value <= high_price:
                
                # Evitar múltiples entradas en la misma secuencia
                if self.has_touched_ema20 and self.cbot_direction == cbot_direction:
                    return None
                
                # Entrada en el cierre de la barra que toca la 20
                entry_price = close_price
                
                # Stop arriba de la EMA 20
                risk_distance = abs((ema20_value + (2 * self.tick_size)) - entry_price)
                stop_loss = ema20_value + (2 * self.tick_size)
                take_profit = entry_price - (risk_distance * 3)  # R:R 1:3
                
                # Marcar que ya tocó la 20
                self.has_touched_ema20 = True
                self.cbot_direction = cbot_direction
                
                return {
                    'type': 'TRADE_20',
                    'direction': 'SHORT',
                    'entry': entry_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'risk': risk_distance,
                    'reward': risk_distance * 3,
                    'ratio': 3,
                    'ema20_value': ema20_value,
                    'keltner_distance': distance_in_ticks,
                    'cbot_info': last_cbot
                }
        
        return None
    
    def reset_for_new_cbot(self):
        """Resetea el estado cuando hay nuevo CBOT."""
        self.has_touched_ema20 = False
        self.cbot_direction = None
