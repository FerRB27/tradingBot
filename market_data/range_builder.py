# Construcción de Range Bars
class RangeBarBuilder:
    def __init__(self, range_size):
        self.range_size = range_size
        self.current_bar = None
        self.bars = []

    def process_trade(self, price):
        if price <= 0:
            # Silenciosamente ignorar precios inválidos (mensajes de control del WebSocket)
            return None
            
        if self.current_bar is None:
            self._start_new_bar(price)
            return None

        # Actualizar high, low, close de la barra actual
        self.current_bar["high"] = max(self.current_bar["high"], float(price))
        
        # Protección contra valores 0 en low
        if self.current_bar["low"] <= 0:
            self.current_bar["low"] = float(price)
        else:
            self.current_bar["low"] = min(self.current_bar["low"], float(price))
            
        self.current_bar["close"] = float(price)

        if self._range_completed():
            # Validar que la barra esté completa antes de retornarla
            if self.current_bar["low"] <= 0 or self.current_bar["open"] <= 0:
                print(f"⚠️ WARNING: Barra con valores inválidos detectada:")
                print(f"   Open: {self.current_bar['open']}, High: {self.current_bar['high']}, Low: {self.current_bar['low']}, Close: {self.current_bar['close']}")
                # Corregir valores inválidos
                if self.current_bar["low"] <= 0:
                    self.current_bar["low"] = min(self.current_bar["open"], self.current_bar["close"])
                if self.current_bar["open"] <= 0:
                    self.current_bar["open"] = self.current_bar["close"]
            
            # Crear copia de la barra completada para evitar mutaciones
            finished_bar = {
                "open": float(self.current_bar["open"]),
                "high": float(self.current_bar["high"]),
                "low": float(self.current_bar["low"]),
                "close": float(self.current_bar["close"])
            }
            self.bars.append(finished_bar)
            self._start_new_bar(price)
            return finished_bar

        return None

    def _start_new_bar(self, price):
        """Inicia una nueva barra con todos los valores inicializados al precio actual"""
        if price <= 0:
            print(f"⚠️ WARNING: Intentando iniciar barra con precio inválido: {price}")
            return
            
        self.current_bar = {
            "open": float(price),
            "high": float(price),
            "low": float(price),
            "close": float(price)
        }

    def _range_completed(self):
        return (
            self.current_bar["high"] - self.current_bar["low"]
            >= self.range_size
        )
