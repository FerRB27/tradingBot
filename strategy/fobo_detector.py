# Detector de FOBO (Fake Out Break Out) según MDC Trading Academy

class FOBODetector:
    """
    Detecta rompimientos fallidos (FOBO) durante la Fase 3 de lateralización
    
    Según MDC:
    - FOBO en soporte → Alta probabilidad (80%) de testear resistencia
    - FOBO en resistencia → Alta probabilidad (80%) de testear soporte
    - Debe estar acompañado de aceleración hacia área opuesta
    """
    
    def __init__(self, acceleration_threshold=1.5, min_bars_in_range=5):
        """
        Args:
            acceleration_threshold: Multiplicador de velocidad para detectar aceleración
            min_bars_in_range: Mínimo de barras para considerar rango establecido
        """
        self.acceleration_threshold = acceleration_threshold
        self.min_bars_in_range = min_bars_in_range
        
        # Estado del detector
        self.potential_fobo = None  # "SUPPORT" o "RESISTANCE"
        self.fobo_bar = None
        self.acceleration_confirmed = False
        
        # Tracking de velocidad
        self.recent_bar_ranges = []
        self.max_recent_ranges = 10
        
    def detect_fobo(self, bar, market_phase_info):
        """
        Detecta si hay un FOBO (rompimiento fallido)
        
        Args:
            bar: Barra actual
            market_phase_info: Información de la fase del mercado (dict)
            
        Returns:
            dict: Información del FOBO detectado o None
        """
        # Solo buscar FOBOs en Fase 3 (lateralización)
        if market_phase_info["current_phase"] != "PHASE_3":
            self._reset()
            return None
        
        # Verificar que el rango esté bien establecido
        if not market_phase_info["range_established"]:
            return None
        
        if market_phase_info["bars_in_phase"] < self.min_bars_in_range:
            return None
        
        range_high = market_phase_info["range_high"]
        range_low = market_phase_info["range_low"]
        
        if not range_high or not range_low:
            return None
        
        # Actualizar tracking de velocidad
        self._update_bar_velocity(bar)
        
        # Detectar ruptura inicial (potencial FOBO)
        if not self.potential_fobo:
            self.potential_fobo = self._detect_breakout(bar, range_high, range_low)
            if self.potential_fobo:
                self.fobo_bar = bar.copy()
        
        # Si ya detectamos ruptura, verificar si es FOBO
        elif self.potential_fobo:
            fobo_signal = self._confirm_fobo(bar, range_high, range_low)
            if fobo_signal:
                return fobo_signal
            
            # Si la ruptura se confirma (no es falsa), resetear
            if self._breakout_confirmed(bar, range_high, range_low):
                self._reset()
        
        return None
    
    def _detect_breakout(self, bar, range_high, range_low):
        """
        Detecta si hay una ruptura del rango (potencial FOBO)
        """
        # Ruptura de resistencia (upper bound)
        if bar["high"] > range_high and bar["close"] < range_high:
            return "RESISTANCE"
        
        # Ruptura de soporte (lower bound)
        if bar["low"] < range_low and bar["close"] > range_low:
            return "SUPPORT"
        
        return None
    
    def _confirm_fobo(self, bar, range_high, range_low):
        """
        Confirma si la ruptura fue falsa (FOBO) verificando:
        1. Retorno al rango
        2. Aceleración hacia lado opuesto
        """
        # FOBO en resistencia → Precio vuelve al rango y acelera hacia soporte
        if self.potential_fobo == "RESISTANCE":
            # Verificar retorno al rango
            back_in_range = bar["close"] < range_high
            
            # Verificar movimiento hacia soporte
            moving_to_support = bar["close"] < self.fobo_bar["close"]
            
            # Verificar aceleración
            acceleration = self._detect_acceleration()
            
            if back_in_range and moving_to_support and acceleration:
                fobo_signal = {
                    "type": "FOBO_RESISTANCE",
                    "direction": "SHORT",  # Operar en corto
                    "target_area": "SUPPORT",  # Objetivo es testear soporte
                    "probability": 0.80,  # 80% según teoría MDC
                    "entry": bar["close"],
                    "fobo_level": range_high,
                    "target_level": range_low
                }
                self._reset()
                return fobo_signal
        
        # FOBO en soporte → Precio vuelve al rango y acelera hacia resistencia
        elif self.potential_fobo == "SUPPORT":
            # Verificar retorno al rango
            back_in_range = bar["close"] > range_low
            
            # Verificar movimiento hacia resistencia
            moving_to_resistance = bar["close"] > self.fobo_bar["close"]
            
            # Verificar aceleración
            acceleration = self._detect_acceleration()
            
            if back_in_range and moving_to_resistance and acceleration:
                fobo_signal = {
                    "type": "FOBO_SUPPORT",
                    "direction": "LONG",  # Operar en largo
                    "target_area": "RESISTANCE",  # Objetivo es testear resistencia
                    "probability": 0.80,  # 80% según teoría MDC
                    "entry": bar["close"],
                    "fobo_level": range_low,
                    "target_level": range_high
                }
                self._reset()
                return fobo_signal
        
        return None
    
    def _breakout_confirmed(self, bar, range_high, range_low):
        """
        Verifica si la ruptura se confirma (no es FOBO)
        - Cierre sostenido fuera del rango
        """
        if self.potential_fobo == "RESISTANCE":
            return bar["close"] > range_high
        elif self.potential_fobo == "SUPPORT":
            return bar["close"] < range_low
        return False
    
    def _update_bar_velocity(self, bar):
        """
        Actualiza el tracking de velocidad de las barras
        Velocidad = rango de la barra (high - low)
        """
        bar_range = bar["high"] - bar["low"]
        self.recent_bar_ranges.append(bar_range)
        
        # Mantener solo las últimas N barras
        if len(self.recent_bar_ranges) > self.max_recent_ranges:
            self.recent_bar_ranges.pop(0)
    
    def _detect_acceleration(self):
        """
        Detecta si hay aceleración en el movimiento
        Compara el rango de la barra actual vs promedio reciente
        """
        if len(self.recent_bar_ranges) < 3:
            return False
        
        current_range = self.recent_bar_ranges[-1]
        avg_range = sum(self.recent_bar_ranges[:-1]) / len(self.recent_bar_ranges[:-1])
        
        # Aceleración detectada si rango actual > threshold × promedio
        return current_range > (avg_range * self.acceleration_threshold)
    
    def _reset(self):
        """
        Resetea el estado del detector
        """
        self.potential_fobo = None
        self.fobo_bar = None
        self.acceleration_confirmed = False
    
    def get_fobo_info(self):
        """
        Retorna información del estado actual del detector
        """
        return {
            "potential_fobo": self.potential_fobo,
            "waiting_confirmation": self.potential_fobo is not None,
            "average_velocity": (
                sum(self.recent_bar_ranges) / len(self.recent_bar_ranges)
                if self.recent_bar_ranges else 0
            )
        }
