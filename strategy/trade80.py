# Trade 80 - Entrada basada en EMA 80 (MDC Trading Academy)

class Trade80Strategy:
    """
    Estrategia Trade 80: Entrada en desarrollo de tendencia/desbalance
    
    Idealmente para Fase 1 (Tendencial) y Fase 4 (Transición)
    
    LONG:
    - EMA 80 debajo de banda media Keltner
    - LR con dirección alcista o plana
    - EMA 80 con dirección alcista o plana
    - Espacio entre EMA 80 y banda media > 3 ticks
    - Precio toca o cruza EMA 80 desde arriba
    
    SHORT:
    - EMA 80 sobre banda media Keltner
    - LR con dirección bajista o plana
    - EMA 80 con dirección bajista o plana
    - Espacio entre EMA 80 y banda media > 3 ticks
    - Precio toca o cruza EMA 80 desde abajo
    """
    
    def __init__(self, tick_size=1.0, min_ticks=3):
        """
        Args:
            tick_size: Tamaño del tick (default 1.0 para BTC)
            min_ticks: Mínimo de ticks de espacio entre EMA80 y banda media
        """
        self.tick_size = tick_size
        self.min_ticks = min_ticks
        self.min_distance = tick_size * min_ticks
        
        # Estado para tracking
        self.setup_detected = None  # 'LONG' o 'SHORT'
        self.previous_ema80 = None
        self.previous_ema80_slope = None
        
    def evaluate(self, bar, ema80_value, ema80_slope, lr_value, lr_slope, keltner):
        """
        Evalúa condiciones para Trade 80
        
        Args:
            bar: Barra actual (dict con open, high, low, close)
            ema80_value: Valor actual de EMA 80
            ema80_slope: Pendiente de EMA 80 (calculada entre valor actual y anterior)
            lr_value: Valor de Linear Regression
            lr_slope: Pendiente de LR
            keltner: Bandas Keltner (upper, basis, lower)
            
        Returns:
            str: "LONG_TRADE80", "SHORT_TRADE80" o None
        """
        if not ema80_value or not lr_value or not keltner:
            return None
        
        # Si no tenemos slope de EMA80, calcularlo
        if ema80_slope is None and self.previous_ema80 is not None:
            ema80_slope = ema80_value - self.previous_ema80
        
        if ema80_slope is None:
            # Primera barra, guardar y continuar
            self.previous_ema80 = ema80_value
            return None
        
        price = bar["close"]
        high = bar["high"]
        low = bar["low"]
        
        # Umbral para considerar pendiente plana (ajustable)
        FLAT_THRESHOLD = 0.5
        
        # ==================== SETUP LONG ====================
        long_ema_position = ema80_value < keltner["basis"]  # EMA80 debajo de banda media
        long_lr_direction = lr_slope > -FLAT_THRESHOLD  # LR alcista o plana
        long_ema_direction = ema80_slope > -FLAT_THRESHOLD  # EMA80 alcista o plana
        long_distance = (keltner["basis"] - ema80_value) >= self.min_distance  # Espacio > 3 ticks
        
        if (long_ema_position and long_lr_direction and 
            long_ema_direction and long_distance and 
            self.setup_detected != "LONG"):
            # Setup detectado, esperar que precio toque EMA80
            self.setup_detected = "LONG"
        
        # Verificar entrada LONG: precio toca/cruza EMA80 desde arriba
        if self.setup_detected == "LONG":
            # Precio toca o cruza EMA80
            price_touches_ema = low <= ema80_value <= high
            
            if price_touches_ema:
                # Entrada confirmada
                self.setup_detected = None
                self._update_tracking(ema80_value, ema80_slope)
                return "LONG_TRADE80"
            
            # Cancelar setup si precio cae muy por debajo de EMA80
            if price < ema80_value - self.min_distance:
                self.setup_detected = None
        
        # ==================== SETUP SHORT ====================
        short_ema_position = ema80_value > keltner["basis"]  # EMA80 sobre banda media
        short_lr_direction = lr_slope < FLAT_THRESHOLD  # LR bajista o plana
        short_ema_direction = ema80_slope < FLAT_THRESHOLD  # EMA80 bajista o plana
        short_distance = (ema80_value - keltner["basis"]) >= self.min_distance  # Espacio > 3 ticks
        
        if (short_ema_position and short_lr_direction and 
            short_ema_direction and short_distance and 
            self.setup_detected != "SHORT"):
            # Setup detectado, esperar que precio toque EMA80
            self.setup_detected = "SHORT"
        
        # Verificar entrada SHORT: precio toca/cruza EMA80 desde abajo
        if self.setup_detected == "SHORT":
            # Precio toca o cruza EMA80
            price_touches_ema = low <= ema80_value <= high
            
            if price_touches_ema:
                # Entrada confirmada
                self.setup_detected = None
                self._update_tracking(ema80_value, ema80_slope)
                return "SHORT_TRADE80"
            
            # Cancelar setup si precio sube muy por encima de EMA80
            if price > ema80_value + self.min_distance:
                self.setup_detected = None
        
        # Actualizar tracking
        self._update_tracking(ema80_value, ema80_slope)
        
        return None
    
    def _update_tracking(self, ema80_value, ema80_slope):
        """
        Actualiza valores previos para cálculo de pendiente
        """
        self.previous_ema80 = ema80_value
        self.previous_ema80_slope = ema80_slope
    
    def get_setup_info(self):
        """
        Retorna información del estado actual
        """
        return {
            "setup_detected": self.setup_detected,
            "waiting_entry": self.setup_detected is not None
        }
