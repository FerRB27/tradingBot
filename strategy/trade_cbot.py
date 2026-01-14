"""
TRADE CBOT - Confirmación de Breakout (MDC)
============================================
Trade de rompimiento en mercados balanceados (Fase 3) confirmado por 2+ anclas.
"""

class TradeCBOT:
    """
    Estrategia TRADE CBOT para rompimientos confirmados por anclas.
    
    Condiciones:
    - Mercado en Fase 3 (lateralizado)
    - Área de soporte/resistencia definida por 2+ anclas
    - Entrada a 3 ticks del pivote extremo del área
    """
    
    def __init__(self, tick_size=1.0, breakout_ticks=3):
        """
        Args:
            tick_size: Tamaño del tick del instrumento
            breakout_ticks: Ticks arriba/abajo del pivote para entrada
        """
        self.tick_size = tick_size
        self.breakout_ticks = breakout_ticks
        
        # Estado del último CBOT detectado
        self.last_cbot = None
        self.waiting_confirmation = False
        self.breakout_direction = None
    
    def evaluate(self, bar, current_phase, resistance_area, support_area):
        """
        Evalúa si hay setup CBOT válido.
        
        Args:
            bar: Barra actual con OHLC
            current_phase: Fase actual del mercado
            resistance_area: Área de resistencia con anclas (o None)
            support_area: Área de soporte con anclas (o None)
            
        Returns:
            dict con señal o None
        """
        # Solo en Fase 3 (lateralización)
        if current_phase != "PHASE_3":
            return None
        
        close_price = bar['close']
        high_price = bar['high']
        low_price = bar['low']
        
        # CBOT LONG: Rompe resistencia con 2+ anclas
        if resistance_area and resistance_area['anchor_count'] >= 2:
            highest_pivot = resistance_area['highest_pivot']
            breakout_level = highest_pivot + (self.breakout_ticks * self.tick_size)
            
            # Entrada si el precio rompe 3 ticks arriba del pivote más alto
            if high_price >= breakout_level and close_price >= breakout_level:
                
                # Calcular stop y target
                risk_distance = abs(close_price - resistance_area['lowest_level'])
                stop_loss = resistance_area['lowest_level'] - (1 * self.tick_size)
                take_profit = close_price + (risk_distance * 2)  # R:R 1:2
                
                # Registrar CBOT para Trade 20
                self.last_cbot = {
                    'direction': 'LONG',
                    'breakout_price': close_price,
                    'area_level': highest_pivot,
                    'anchor_count': resistance_area['anchor_count']
                }
                
                return {
                    'type': 'CBOT',
                    'direction': 'LONG',
                    'entry': close_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'risk': risk_distance,
                    'reward': risk_distance * 2,
                    'ratio': 2,
                    'anchor_count': resistance_area['anchor_count'],
                    'breakout_level': breakout_level,
                    'pivot_level': highest_pivot
                }
        
        # CBOT SHORT: Rompe soporte con 2+ anclas
        if support_area and support_area['anchor_count'] >= 2:
            lowest_pivot = support_area['lowest_pivot']
            breakout_level = lowest_pivot - (self.breakout_ticks * self.tick_size)
            
            # Entrada si el precio rompe 3 ticks abajo del pivote más bajo
            if low_price <= breakout_level and close_price <= breakout_level:
                
                # Calcular stop y target
                risk_distance = abs(support_area['highest_level'] - close_price)
                stop_loss = support_area['highest_level'] + (1 * self.tick_size)
                take_profit = close_price - (risk_distance * 2)  # R:R 1:2
                
                # Registrar CBOT para Trade 20
                self.last_cbot = {
                    'direction': 'SHORT',
                    'breakout_price': close_price,
                    'area_level': lowest_pivot,
                    'anchor_count': support_area['anchor_count']
                }
                
                return {
                    'type': 'CBOT',
                    'direction': 'SHORT',
                    'entry': close_price,
                    'stop_loss': stop_loss,
                    'take_profit': take_profit,
                    'risk': risk_distance,
                    'reward': risk_distance * 2,
                    'ratio': 2,
                    'anchor_count': support_area['anchor_count'],
                    'breakout_level': breakout_level,
                    'pivot_level': lowest_pivot
                }
        
        return None
    
    def get_last_cbot(self):
        """Retorna el último CBOT detectado (para Trade 20)."""
        return self.last_cbot
    
    def reset_cbot(self):
        """Resetea el CBOT (después de que Trade 20 lo use)."""
        self.last_cbot = None
