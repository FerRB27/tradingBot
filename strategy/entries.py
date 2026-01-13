# A1, A2, A3 - MDC Trading Academy
class A1Strategy:
    def __init__(self):
        self.waiting_pullback = None  # 'LONG' o 'SHORT'
        self.impulse_detected = None
        
    def evaluate(self, bar, lr_value, lr_slope, keltner):
        """
        Evalúa condiciones A1 según MDC Trading Academy
        
        A1 LONG:
        1. Impulso alcista inmediato
        2. Precio en canal superior Keltner
        3. LR con dirección alcista
        4. Primera barra de retroceso que toca banda media + precio >= LR
        
        A1 SHORT:
        1. Impulso bajista inmediato
        2. Precio en canal inferior Keltner
        3. LR con dirección bajista
        4. Primera barra de retroceso que toca banda media + precio <= LR
        """
        if not lr_value or not lr_slope or not keltner:
            return None
            
        price = bar["close"]
        high = bar["high"]
        low = bar["low"]
        
        # LONG: Detectar setup alcista
        if (
            self.impulse_detected == "BULLISH"
            and self.waiting_pullback is None
            and lr_slope > 0  # LR alcista
            and price > keltner["upper"]  # Precio en canal superior
        ):
            self.waiting_pullback = "LONG"
            
        # SHORT: Detectar setup bajista
        elif (
            self.impulse_detected == "BEARISH"
            and self.waiting_pullback is None
            and lr_slope < 0  # LR bajista
            and price < keltner["lower"]  # Precio en canal inferior
        ):
            self.waiting_pullback = "SHORT"
        
        # LONG: Primera barra que toca banda media después del setup
        if self.waiting_pullback == "LONG":
            # Verificar si la barra toca o cruza la banda media
            if low <= keltner["basis"] <= high:
                # Validar que precio esté en o sobre la LR
                if price >= lr_value:
                    self.waiting_pullback = None
                    self.impulse_detected = None
                    return "LONG_A1"
                else:
                    # No cumple condición, cancelar setup
                    self.waiting_pullback = None
                    self.impulse_detected = None
            # Si cae por debajo de la banda media sin tocarla, cancelar
            elif price < keltner["basis"]:
                self.waiting_pullback = None
                self.impulse_detected = None
                
        # SHORT: Primera barra que toca banda media después del setup
        if self.waiting_pullback == "SHORT":
            # Verificar si la barra toca o cruza la banda media
            if low <= keltner["basis"] <= high:
                # Validar que precio esté en o bajo la LR
                if price <= lr_value:
                    self.waiting_pullback = None
                    self.impulse_detected = None
                    return "SHORT_A1"
                else:
                    # No cumple condición, cancelar setup
                    self.waiting_pullback = None
                    self.impulse_detected = None
            # Si sube por encima de la banda media sin tocarla, cancelar
            elif price > keltner["basis"]:
                self.waiting_pullback = None
                self.impulse_detected = None
                
        return None
    
    def set_impulse(self, impulse):
        """Registra cuando se detecta un nuevo impulso"""
        self.impulse_detected = impulse
