# A1, A2, A3 - MDC Trading Academy
class A1Strategy:
    def __init__(self):
        self.waiting_pullback = None  # 'LONG' o 'SHORT'
        self.impulse_detected = None
        
    def evaluate(self, bar, lr_value, lr_slope, keltner):
        """
        Evalua condiciones A1 segun MDC Trading Academy
        
        A1 LONG:
        1. Impulso alcista inmediato
        2. Precio en canal superior Keltner
        3. LR con direccion alcista
        4. Primera barra de retroceso que toca banda media + precio >= LR (EN CONTACTO)
        
        A1 SHORT:
        1. Impulso bajista inmediato
        2. Precio en canal inferior Keltner
        3. LR con direccion bajista
        4. Primera barra de retroceso que toca banda media + precio <= LR (EN CONTACTO)
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
        
        # LONG: Primera barra que toca banda media despues del setup
        if self.waiting_pullback == "LONG":
            # Verificar si la barra toca o cruza la banda media
            if low <= keltner["basis"] <= high:
                # A1: Validar que precio este en o sobre la LR (EN CONTACTO)
                if price >= lr_value:
                    self.waiting_pullback = None
                    self.impulse_detected = None
                    return "LONG_A1"
                else:
                    # No cumple condicion, cancelar setup
                    self.waiting_pullback = None
                    self.impulse_detected = None
            # Si cae por debajo de la banda media sin tocarla, cancelar
            elif price < keltner["basis"]:
                self.waiting_pullback = None
                self.impulse_detected = None
                
        # SHORT: Primera barra que toca banda media despues del setup
        if self.waiting_pullback == "SHORT":
            # Verificar si la barra toca o cruza la banda media
            if low <= keltner["basis"] <= high:
                # A1: Validar que precio este en o bajo la LR (EN CONTACTO)
                if price <= lr_value:
                    self.waiting_pullback = None
                    self.impulse_detected = None
                    return "SHORT_A1"
                else:
                    # No cumple condicion, cancelar setup
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


class A2Strategy:
    def __init__(self):
        self.waiting_pullback = None  # 'LONG' o 'SHORT'
        self.impulse_detected = None
        
    def evaluate(self, bar, lr_value, lr_slope, keltner):
        """
        Evalua condiciones A2 segun MDC Trading Academy
        
        A2 LONG:
        1. Impulso alcista inmediato
        2. Precio en canal superior Keltner
        3. LR con direccion alcista
        4. Primera barra de retroceso que toca banda media + precio < LR (SIN CONTACTO)
        
        A2 SHORT:
        1. Impulso bajista inmediato
        2. Precio en canal inferior Keltner
        3. LR con direccion bajista
        4. Primera barra de retroceso que toca banda media + precio > LR (SIN CONTACTO)
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
        
        # LONG: Primera barra que toca banda media despues del setup
        if self.waiting_pullback == "LONG":
            # Verificar si la barra toca o cruza la banda media
            if low <= keltner["basis"] <= high:
                # A2: Validar que precio este DEBAJO de LR y SIN CONTACTO
                # Verificar que ni el close, ni high, ni low toquen la LR
                if price < lr_value and high < lr_value:
                    self.waiting_pullback = None
                    self.impulse_detected = None
                    return "LONG_A2"
                else:
                    # No cumple condicion, cancelar setup
                    self.waiting_pullback = None
                    self.impulse_detected = None
            # Si cae por debajo de la banda media sin tocarla, cancelar
            elif price < keltner["basis"]:
                self.waiting_pullback = None
                self.impulse_detected = None
                
        # SHORT: Primera barra que toca banda media despues del setup
        if self.waiting_pullback == "SHORT":
            # Verificar si la barra toca o cruza la banda media
            if low <= keltner["basis"] <= high:
                # A2: Validar que precio este ENCIMA de LR y SIN CONTACTO
                # Verificar que ni el close, ni high, ni low toquen la LR
                if price > lr_value and low > lr_value:
                    self.waiting_pullback = None
                    self.impulse_detected = None
                    return "SHORT_A2"
                else:
                    # No cumple condicion, cancelar setup
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


class A3Strategy:
    def __init__(self):
        self.waiting_pullback = None  # 'LONG' o 'SHORT'
        self.impulse_detected = None
        
    def evaluate(self, bar, lr_value, lr_slope, keltner):
        """
        Evalua condiciones A3 segun MDC Trading Academy
        
        A3 LONG:
        1. Impulso alcista inmediato
        2. Precio en canal superior Keltner
        3. Precio DEBAJO de LR
        4. Primera barra de retroceso que toca banda media:
           - LR debe estar PLANA (slope cerca de 0)
           - Distancia (LR - KC Basis) >= 2x riesgo
        
        A3 SHORT:
        1. Impulso bajista inmediato
        2. Precio en canal inferior Keltner
        3. Precio ENCIMA de LR
        4. Primera barra de retroceso que toca banda media:
           - LR debe estar PLANA (slope cerca de 0)
           - Distancia (KC Basis - LR) >= 2x riesgo
        """
        if not lr_value or not lr_slope or not keltner:
            return None
            
        price = bar["close"]
        high = bar["high"]
        low = bar["low"]
        
        # Umbral para considerar LR "plana" (ajustable segun volatilidad)
        FLAT_SLOPE_THRESHOLD = 0.5
        
        # LONG: Detectar setup alcista
        if (
            self.impulse_detected == "BULLISH"
            and self.waiting_pullback is None
            and price > keltner["upper"]  # Precio en canal superior
            and price < lr_value  # Precio DEBAJO de LR
        ):
            self.waiting_pullback = "LONG"
            
        # SHORT: Detectar setup bajista
        elif (
            self.impulse_detected == "BEARISH"
            and self.waiting_pullback is None
            and price < keltner["lower"]  # Precio en canal inferior
            and price > lr_value  # Precio ENCIMA de LR
        ):
            self.waiting_pullback = "SHORT"
        
        # LONG: Primera barra que toca banda media despues del setup
        if self.waiting_pullback == "LONG":
            # Verificar si la barra toca o cruza la banda media
            if low <= keltner["basis"] <= high:
                # A3: Validar LR plana
                if abs(lr_slope) <= FLAT_SLOPE_THRESHOLD:
                    # Calcular riesgo y recompensa potencial
                    entry_approx = keltner["basis"]
                    risk = entry_approx - keltner["lower"]  # Distancia al SL
                    reward_potential = lr_value - keltner["basis"]  # Distancia LR-Basis
                    
                    # Validar que reward >= 2x risk
                    if reward_potential >= (2 * risk):
                        self.waiting_pullback = None
                        self.impulse_detected = None
                        return "LONG_A3"
                
                # Si no cumple, cancelar setup
                self.waiting_pullback = None
                self.impulse_detected = None
                
            # Si cae por debajo de la banda media sin tocarla, cancelar
            elif price < keltner["basis"]:
                self.waiting_pullback = None
                self.impulse_detected = None
                
        # SHORT: Primera barra que toca banda media despues del setup
        if self.waiting_pullback == "SHORT":
            # Verificar si la barra toca o cruza la banda media
            if low <= keltner["basis"] <= high:
                # A3: Validar LR plana
                if abs(lr_slope) <= FLAT_SLOPE_THRESHOLD:
                    # Calcular riesgo y recompensa potencial
                    entry_approx = keltner["basis"]
                    risk = keltner["upper"] - entry_approx  # Distancia al SL
                    reward_potential = keltner["basis"] - lr_value  # Distancia Basis-LR
                    
                    # Validar que reward >= 2x risk
                    if reward_potential >= (2 * risk):
                        self.waiting_pullback = None
                        self.impulse_detected = None
                        return "SHORT_A3"
                
                # Si no cumple, cancelar setup
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
