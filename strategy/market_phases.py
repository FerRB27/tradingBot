# Detección de las 4 Fases del Mercado según MDC Trading Academy

class MarketPhaseDetector:
    """
    Detecta las 4 fases de actividad del mercado según MDC:
    
    Fase 1 - Tendencial: Movimiento direccional, tendencia o imbalance
    Fase 2 - Cambio de Ritmo: Entrada de órdenes pasivas que detienen el movimiento
    Fase 3 - Lateralización: Movimiento lateral o balance dentro del rango
    Fase 4 - Transición: Ruptura confirmada del rango, inicio de nueva tendencia
    """
    
    def __init__(self, slope_threshold=1.0, flat_slope_threshold=0.5):
        """
        Args:
            slope_threshold: Umbral para considerar LR como tendencial
            flat_slope_threshold: Umbral para considerar LR como plana
        """
        self.slope_threshold = slope_threshold
        self.flat_slope_threshold = flat_slope_threshold
        
        # Estado del mercado
        self.current_phase = None
        self.phase_history = []
        
        # Rangos detectados (para Fase 3)
        self.range_high = None
        self.range_low = None
        self.range_established = False
        
        # Tracking de barras en fase
        self.bars_in_phase = 0
        self.previous_impulse = None
        
    def detect_phase(self, bar, lr_value, lr_slope, keltner, impulse=None):
        """
        Detecta la fase actual del mercado
        
        Args:
            bar: Barra actual (dict con open, high, low, close)
            lr_value: Valor de la Linear Regression
            lr_slope: Pendiente de la LR
            keltner: Bandas Keltner (upper, basis, lower)
            impulse: Impulso actual detectado (BULLISH/BEARISH/None)
            
        Returns:
            str: Fase actual ("PHASE_1", "PHASE_2", "PHASE_3", "PHASE_4")
        """
        if not lr_value or not lr_slope or not keltner:
            return None
            
        price = bar["close"]
        high = bar["high"]
        low = bar["low"]
        
        # Detectar Fase 1: TENDENCIAL
        # - LR con pendiente fuerte
        # - Precio consistentemente fuera de banda media
        # - Impulsos en misma dirección
        if self._is_phase_1(price, lr_slope, keltner, impulse):
            if self.current_phase != "PHASE_1":
                self._transition_to_phase("PHASE_1")
                # Resetear rangos al salir de lateralización
                self.range_established = False
            return "PHASE_1"
        
        # Detectar Fase 4: TRANSICIÓN (ruptura de rango previo)
        # - Debe haber estado en Fase 3 previamente
        # - Ruptura confirmada de rango establecido
        # - Nuevo impulso direccional
        if self.range_established and self._is_phase_4(bar, impulse):
            if self.current_phase != "PHASE_4":
                self._transition_to_phase("PHASE_4")
            return "PHASE_4"
        
        # Detectar Fase 3: LATERALIZACIÓN
        # - LR relativamente plana
        # - Precio oscilando entre extremos de Keltner
        # - Rango establecido
        if self._is_phase_3(price, lr_slope, keltner):
            if self.current_phase != "PHASE_3":
                self._transition_to_phase("PHASE_3")
            return "PHASE_3"
        
        # Detectar Fase 2: CAMBIO DE RITMO
        # - Transición entre Fase 1 y Fase 3
        # - Impulso contrario detectado
        # - Precio alcanzando extremos de Keltner
        if self._is_phase_2(price, lr_slope, keltner, impulse):
            if self.current_phase != "PHASE_2":
                self._transition_to_phase("PHASE_2")
                # Comenzar a establecer rangos
                self._update_range_boundaries(bar, keltner)
            return "PHASE_2"
        
        # Mantener fase actual si no hay cambios claros
        self.bars_in_phase += 1
        return self.current_phase
    
    def _is_phase_1(self, price, lr_slope, keltner, impulse):
        """
        Fase 1 - TENDENCIAL:
        - Pendiente LR fuerte (> threshold)
        - Precio consistentemente alejado de banda media
        - Impulsos sostenidos en misma dirección
        """
        strong_slope = abs(lr_slope) > self.slope_threshold
        
        # Precio alejado de banda media (tendencial)
        away_from_basis = (
            price > keltner["basis"] + (keltner["upper"] - keltner["basis"]) * 0.3 or
            price < keltner["basis"] - (keltner["basis"] - keltner["lower"]) * 0.3
        )
        
        # Si estamos en tendencia alcista
        if lr_slope > self.slope_threshold:
            uptrend_momentum = price > keltner["basis"]
            return strong_slope and uptrend_momentum
        
        # Si estamos en tendencia bajista
        elif lr_slope < -self.slope_threshold:
            downtrend_momentum = price < keltner["basis"]
            return strong_slope and downtrend_momentum
        
        return False
    
    def _is_phase_2(self, price, lr_slope, keltner, impulse):
        """
        Fase 2 - CAMBIO DE RITMO:
        - Impulso contrario detectado
        - Pendiente LR comenzando a disminuir
        - Precio alcanzando extremos de Keltner (estableciendo áreas)
        """
        # Detectar cambio de impulso
        impulse_change = False
        if impulse and self.previous_impulse:
            impulse_change = impulse != self.previous_impulse
        
        # Pendiente moderándose
        slope_moderating = abs(lr_slope) < self.slope_threshold
        
        # Precio en extremos de Keltner
        at_extremes = (
            price >= keltner["upper"] or 
            price <= keltner["lower"]
        )
        
        # Transición desde Fase 1
        coming_from_phase_1 = self.current_phase == "PHASE_1"
        
        return (impulse_change or coming_from_phase_1) and slope_moderating and at_extremes
    
    def _is_phase_3(self, price, lr_slope, keltner):
        """
        Fase 3 - LATERALIZACIÓN:
        - LR relativamente plana
        - Precio oscilando entre bandas de Keltner
        - Rango establecido
        """
        # LR plana o con poca pendiente
        flat_lr = abs(lr_slope) <= self.flat_slope_threshold
        
        # Precio dentro del rango (no en tendencia)
        in_range = keltner["lower"] <= price <= keltner["upper"]
        
        # Si ya establecimos un rango, verificar que se mantiene
        if self.range_established:
            respecting_range = (
                self.range_low is not None and 
                self.range_high is not None and
                self.range_low * 0.95 <= price <= self.range_high * 1.05  # 5% tolerancia
            )
            return flat_lr and in_range and respecting_range
        
        # Iniciar establecimiento de rango
        return flat_lr and in_range and self.current_phase == "PHASE_2"
    
    def _is_phase_4(self, bar, impulse):
        """
        Fase 4 - TRANSICIÓN:
        - Ruptura confirmada del rango establecido en Fase 3
        - Nuevo impulso direccional
        - Cierre fuera del rango con convicción
        """
        if not self.range_established or not self.range_high or not self.range_low:
            return False
        
        price = bar["close"]
        
        # Ruptura alcista confirmada
        bullish_breakout = (
            price > self.range_high and 
            impulse == "BULLISH" and
            self.current_phase == "PHASE_3"
        )
        
        # Ruptura bajista confirmada
        bearish_breakout = (
            price < self.range_low and 
            impulse == "BEARISH" and
            self.current_phase == "PHASE_3"
        )
        
        return bullish_breakout or bearish_breakout
    
    def _update_range_boundaries(self, bar, keltner):
        """
        Actualiza los límites del rango durante Fase 2 y Fase 3
        """
        if self.current_phase in ["PHASE_2", "PHASE_3"]:
            # Usar extremos de Keltner como proxy inicial
            if self.range_high is None:
                self.range_high = bar["high"]
            else:
                self.range_high = max(self.range_high, bar["high"])
            
            if self.range_low is None:
                self.range_low = bar["low"]
            else:
                self.range_low = min(self.range_low, bar["low"])
            
            # Establecer rango después de suficientes barras en Fase 3
            if self.current_phase == "PHASE_3" and self.bars_in_phase >= 3:
                self.range_established = True
    
    def _transition_to_phase(self, new_phase):
        """
        Maneja la transición a una nueva fase
        """
        # Guardar historial
        if self.current_phase:
            self.phase_history.append({
                "phase": self.current_phase,
                "bars": self.bars_in_phase
            })
        
        # Actualizar estado
        self.current_phase = new_phase
        self.bars_in_phase = 0
        
        # Resetear rango al entrar en nueva tendencia (Fase 1)
        if new_phase == "PHASE_1":
            self.range_high = None
            self.range_low = None
            self.range_established = False
        
        # Resetear rango después de transición exitosa (Fase 4)
        if new_phase == "PHASE_4":
            # Mantener el rango temporalmente para análisis
            pass
    
    def update_impulse(self, impulse):
        """
        Actualiza el tracking de impulsos
        """
        if impulse:
            self.previous_impulse = impulse
    
    def get_phase_info(self):
        """
        Retorna información detallada de la fase actual
        """
        return {
            "current_phase": self.current_phase,
            "bars_in_phase": self.bars_in_phase,
            "range_established": self.range_established,
            "range_high": self.range_high,
            "range_low": self.range_low,
            "phase_description": self._get_phase_description()
        }
    
    def _get_phase_description(self):
        """
        Retorna descripción legible de la fase actual
        """
        descriptions = {
            "PHASE_1": "Tendencial - Movimiento direccional",
            "PHASE_2": "Cambio de Ritmo - Estableciendo áreas",
            "PHASE_3": "Lateralización - Movimiento en rango",
            "PHASE_4": "Transición - Ruptura de rango",
            None: "Indefinida - Analizando mercado"
        }
        return descriptions.get(self.current_phase, "Desconocida")
    
    def is_suitable_for_entries(self, entry_type):
        """
        Determina si la fase actual es adecuada para un tipo de entrada
        
        Args:
            entry_type: Tipo de entrada ("A1", "A2", "A3", "TRADE_80", "FOBO_REVERSAL", etc.)
            
        Returns:
            bool: True si la fase es adecuada para ese tipo de entrada
        """
        phase_entry_compatibility = {
            "A1": ["PHASE_2", "PHASE_4"],  # Impulsos fuertes con retroceso
            "A2": ["PHASE_2", "PHASE_4"],  # Similar a A1 pero menos restrictivo
            "A3": ["PHASE_3"],              # Requiere lateralización (LR plana)
            "TRADE_80": ["PHASE_1", "PHASE_4"],  # Tendencial - desarrollo de tendencia
            "FOBO_REVERSAL": ["PHASE_3"],   # Rompimientos fallidos en rango
            "TREND_CONTINUATION": ["PHASE_1"], # Continuación de tendencia
        }
        
        compatible_phases = phase_entry_compatibility.get(entry_type, [])
        return self.current_phase in compatible_phases
