# Sistema integrado de señales MDC con detección de fases del mercado
from .market_phases import MarketPhaseDetector
from .fobo_detector import FOBODetector
from .entries import A1Strategy, A2Strategy, A3Strategy
from .impulses import detect_impulse


class TradingSignalGenerator:
    """
    Generador de señales de trading que integra:
    - Detección de las 4 fases del mercado MDC
    - Estrategias A1, A2, A3
    - Detección de FOBOs (rompimientos fallidos)
    """
    
    def __init__(self):
        # Detectores de mercado
        self.phase_detector = MarketPhaseDetector(
            slope_threshold=1.0,
            flat_slope_threshold=0.5
        )
        self.fobo_detector = FOBODetector(
            acceleration_threshold=1.5,
            min_bars_in_range=5
        )
        
        # Estrategias de entrada
        self.a1_strategy = A1Strategy()
        self.a2_strategy = A2Strategy()
        self.a3_strategy = A3Strategy()
        
        # Tracking
        self.previous_lr_slope = None
    
    def generate_signal(self, bar, lr_value, lr_slope, keltner):
        """
        Genera señales de trading considerando fase del mercado
        
        Args:
            bar: Barra actual (dict)
            lr_value: Valor de Linear Regression
            lr_slope: Pendiente de LR
            keltner: Bandas Keltner (dict con upper, basis, lower)
            
        Returns:
            dict: Señal completa con tipo, dirección, fase, etc.
        """
        if not lr_value or not lr_slope or not keltner:
            return None
        
        # 1. Detectar impulso
        impulse = detect_impulse(self.previous_lr_slope, lr_slope)
        if impulse:
            self.a1_strategy.set_impulse(impulse)
            self.a2_strategy.set_impulse(impulse)
            self.a3_strategy.set_impulse(impulse)
            self.phase_detector.update_impulse(impulse)
        
        # 2. Detectar fase del mercado
        current_phase = self.phase_detector.detect_phase(
            bar, lr_value, lr_slope, keltner, impulse
        )
        
        # 3. Obtener info de fase para contexto
        phase_info = self.phase_detector.get_phase_info()
        
        # 4. Detectar FOBOs (solo en Fase 3)
        fobo_signal = self.fobo_detector.detect_fobo(bar, phase_info)
        if fobo_signal:
            return self._build_signal(
                signal_type=fobo_signal["type"],
                direction=fobo_signal["direction"],
                entry=fobo_signal["entry"],
                phase=current_phase,
                keltner=keltner,
                lr_value=lr_value,
                fobo_info=fobo_signal
            )
        
        # 5. Evaluar estrategias A1, A2, A3 según fase apropiada
        
        # A1 y A2: Mejor en Fase 2 (cambio de ritmo) y Fase 4 (transición)
        if self.phase_detector.is_suitable_for_entries("A1"):
            signal_a1 = self.a1_strategy.evaluate(bar, lr_value, lr_slope, keltner)
            if signal_a1:
                direction = "LONG" if "LONG" in signal_a1 else "SHORT"
                return self._build_signal(
                    signal_type="A1",
                    direction=direction,
                    entry=bar["close"],
                    phase=current_phase,
                    keltner=keltner,
                    lr_value=lr_value
                )
        
        if self.phase_detector.is_suitable_for_entries("A2"):
            signal_a2 = self.a2_strategy.evaluate(bar, lr_value, lr_slope, keltner)
            if signal_a2:
                direction = "LONG" if "LONG" in signal_a2 else "SHORT"
                return self._build_signal(
                    signal_type="A2",
                    direction=direction,
                    entry=bar["close"],
                    phase=current_phase,
                    keltner=keltner,
                    lr_value=lr_value
                )
        
        # A3: Solo en Fase 3 (lateralización con LR plana)
        if self.phase_detector.is_suitable_for_entries("A3"):
            signal_a3 = self.a3_strategy.evaluate(bar, lr_value, lr_slope, keltner)
            if signal_a3:
                direction = "LONG" if "LONG" in signal_a3 else "SHORT"
                return self._build_signal(
                    signal_type="A3",
                    direction=direction,
                    entry=bar["close"],
                    phase=current_phase,
                    keltner=keltner,
                    lr_value=lr_value
                )
        
        # Actualizar slope previo
        self.previous_lr_slope = lr_slope
        
        return None
    
    def _build_signal(self, signal_type, direction, entry, phase, keltner, lr_value, fobo_info=None):
        """
        Construye el objeto de señal completo
        """
        # Calcular stop loss y take profit
        if direction == "LONG":
            stop_loss = keltner["lower"]
            risk = entry - stop_loss
            take_profit = entry + (2 * risk)  # Ratio 1:2
        else:  # SHORT
            stop_loss = keltner["upper"]
            risk = stop_loss - entry
            take_profit = entry - (2 * risk)  # Ratio 1:2
        
        signal = {
            "type": signal_type,
            "direction": direction,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk": risk,
            "reward": abs(take_profit - entry),
            "ratio": 2.0,
            "phase": phase,
            "phase_description": self.phase_detector._get_phase_description(),
            "keltner_basis": keltner["basis"],
            "lr_value": lr_value
        }
        
        # Añadir info adicional si es FOBO
        if fobo_info:
            signal["fobo_info"] = fobo_info
        
        return signal
    
    def get_market_context(self):
        """
        Retorna contexto completo del mercado
        """
        return {
            "phase_info": self.phase_detector.get_phase_info(),
            "fobo_info": self.fobo_detector.get_fobo_info()
        }