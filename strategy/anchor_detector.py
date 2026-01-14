"""
Detector de Anclas - Teoría MDC
================================
Las anclas son pivotes que generaron cambio de impulso (puntos de fallo).
Son importantes para identificar áreas clave de soporte/resistencia.
"""

class AnchorDetector:
    """
    Detecta anclas (pivotes de cambio de impulso) para identificar
    áreas importantes de soporte y resistencia.
    """
    
    def __init__(self, tick_size=1.0, anchor_lookback=20):
        """
        Args:
            tick_size: Tamaño del tick del instrumento
            anchor_lookback: Barras hacia atrás para detectar anclas
        """
        self.tick_size = tick_size
        self.anchor_lookback = anchor_lookback
        
        # Almacenar anclas detectadas
        self.resistance_anchors = []  # Anclas de resistencia
        self.support_anchors = []     # Anclas de soporte
        
        # Historial de pendiente de LR para detectar cambios de impulso
        self.slope_history = []
        
    def update(self, bar, lr_slope):
        """
        Actualiza el detector con nueva barra y pendiente LR.
        
        Args:
            bar: Barra actual con OHLC
            lr_slope: Pendiente actual de Linear Regression
        """
        if lr_slope is None:
            return
            
        self.slope_history.append(lr_slope)
        
        # Mantener solo las últimas barras necesarias
        if len(self.slope_history) > self.anchor_lookback:
            self.slope_history.pop(0)
        
        # Detectar cambio de impulso (ancla)
        if len(self.slope_history) >= 3:
            # Cambio de bajista a alcista = Ancla de soporte
            if (self.slope_history[-3] < 0 and 
                self.slope_history[-2] < 0 and 
                self.slope_history[-1] > 0):
                
                anchor = {
                    'level': bar['low'],
                    'type': 'SUPPORT',
                    'bar_high': bar['high'],
                    'bar_low': bar['low'],
                    'timestamp': bar.get('timestamp', None)
                }
                self.support_anchors.append(anchor)
                
                # Mantener solo anclas recientes
                if len(self.support_anchors) > 10:
                    self.support_anchors.pop(0)
            
            # Cambio de alcista a bajista = Ancla de resistencia
            elif (self.slope_history[-3] > 0 and 
                  self.slope_history[-2] > 0 and 
                  self.slope_history[-1] < 0):
                
                anchor = {
                    'level': bar['high'],
                    'type': 'RESISTANCE',
                    'bar_high': bar['high'],
                    'bar_low': bar['low'],
                    'timestamp': bar.get('timestamp', None)
                }
                self.resistance_anchors.append(anchor)
                
                # Mantener solo anclas recientes
                if len(self.resistance_anchors) > 10:
                    self.resistance_anchors.pop(0)
    
    def get_resistance_area(self, tolerance_ticks=5):
        """
        Identifica área de resistencia con 2 o más anclas agrupadas.
        
        Args:
            tolerance_ticks: Tolerancia en ticks para agrupar anclas
            
        Returns:
            dict con información del área o None
        """
        if len(self.resistance_anchors) < 2:
            return None
        
        tolerance = tolerance_ticks * self.tick_size
        
        # Buscar grupo de anclas cercanas
        for i in range(len(self.resistance_anchors) - 1):
            anchor1 = self.resistance_anchors[i]
            nearby_anchors = [anchor1]
            
            for j in range(i + 1, len(self.resistance_anchors)):
                anchor2 = self.resistance_anchors[j]
                
                # Si está dentro de la tolerancia, agregar al grupo
                if abs(anchor1['level'] - anchor2['level']) <= tolerance:
                    nearby_anchors.append(anchor2)
            
            # Si encontramos 2+ anclas, definir área
            if len(nearby_anchors) >= 2:
                levels = [a['level'] for a in nearby_anchors]
                highest_pivot = max(levels)
                
                return {
                    'type': 'RESISTANCE',
                    'anchor_count': len(nearby_anchors),
                    'highest_pivot': highest_pivot,
                    'lowest_level': min(levels),
                    'anchors': nearby_anchors
                }
        
        return None
    
    def get_support_area(self, tolerance_ticks=5):
        """
        Identifica área de soporte con 2 o más anclas agrupadas.
        
        Args:
            tolerance_ticks: Tolerancia en ticks para agrupar anclas
            
        Returns:
            dict con información del área o None
        """
        if len(self.support_anchors) < 2:
            return None
        
        tolerance = tolerance_ticks * self.tick_size
        
        # Buscar grupo de anclas cercanas
        for i in range(len(self.support_anchors) - 1):
            anchor1 = self.support_anchors[i]
            nearby_anchors = [anchor1]
            
            for j in range(i + 1, len(self.support_anchors)):
                anchor2 = self.support_anchors[j]
                
                # Si está dentro de la tolerancia, agregar al grupo
                if abs(anchor1['level'] - anchor2['level']) <= tolerance:
                    nearby_anchors.append(anchor2)
            
            # Si encontramos 2+ anclas, definir área
            if len(nearby_anchors) >= 2:
                levels = [a['level'] for a in nearby_anchors]
                lowest_pivot = min(levels)
                
                return {
                    'type': 'SUPPORT',
                    'anchor_count': len(nearby_anchors),
                    'lowest_pivot': lowest_pivot,
                    'highest_level': max(levels),
                    'anchors': nearby_anchors
                }
        
        return None
    
    def get_info(self):
        """Retorna información sobre anclas detectadas."""
        return {
            'resistance_anchors_count': len(self.resistance_anchors),
            'support_anchors_count': len(self.support_anchors),
            'has_resistance_area': self.get_resistance_area() is not None,
            'has_support_area': self.get_support_area() is not None
        }
