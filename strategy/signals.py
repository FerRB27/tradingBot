# Sistema integrado de señales MDC con detección de fases del mercado
from .market_phases import MarketPhaseDetector
from .fobo_detector import FOBODetector
from .entries import A1Strategy, A2Strategy, A3Strategy
from .trade80 import Trade80Strategy
from .anchor_detector import AnchorDetector
from .trade_cbot import TradeCBOT
from .trade_20 import Trade20Strategy
from .impulses import detect_impulse


class TradingSignalGenerator:
    """
    Generador de señales de trading que integra:
    - Detección de las 4 fases del mercado MDC
    - Estrategias A1, A2, A3
    - Trade 80 (entrada en tendencia con EMA 80)
    - Trade CBOT (breakout confirmado por anclas)
    - Trade 20 (entrada en EMA 20 después de CBOT)
    - Detección de FOBOs (rompimientos fallidos)
    - Detector de Anclas (puntos de cambio de impulso)
    """
    
    def __init__(self, tick_size=1.0):
        # Detectores de mercado
        self.phase_detector = MarketPhaseDetector(
            slope_threshold=1.0,
            flat_slope_threshold=0.5
        )
        self.fobo_detector = FOBODetector(
            acceleration_threshold=1.5,
            min_bars_in_range=5
        )
        self.anchor_detector = AnchorDetector(
            tick_size=tick_size,
            anchor_lookback=20
        )
        
        # Estrategias de entrada
        self.a1_strategy = A1Strategy()
        self.a2_strategy = A2Strategy()
        self.a3_strategy = A3Strategy()
        self.trade80_strategy = Trade80Strategy(tick_size=tick_size, min_ticks=3)
        self.trade_cbot = TradeCBOT(tick_size=tick_size, breakout_ticks=3)
        self.trade20_strategy = Trade20Strategy(tick_size=tick_size, min_distance_ticks=4)
        
        # Tracking
        self.previous_lr_slope = None
        self.previous_ema80 = None
    
    def generate_signal(self, bar, lr_value, lr_slope, keltner, ema80_value=None, ema20_value=None):
        """
        Genera señales de trading considerando fase del mercado
        
        Args:
            bar: Barra actual (dict)
            lr_value: Valor de Linear Regression
            lr_slope: Pendiente de LR
            keltner: Bandas Keltner (dict con upper, basis, lower)
            ema80_value: Valor de EMA 80 (opcional, para Trade 80)
            ema20_value: Valor de EMA 20 (opcional, para Trade 20)
            
        Returns:
            dict: Señal completa con tipo, dirección, fase, etc.
        """
        if not lr_value or not lr_slope or not keltner:
            return None
        
        # Calcular pendiente de EMA 80 si está disponible
        ema80_slope = None
        if ema80_value and self.previous_ema80:
            ema80_slope = ema80_value - self.previous_ema80
        
        # 1. Detectar impulso
        impulse = detect_impulse(self.previous_lr_slope, lr_slope)
        if impulse:
            self.a1_strategy.set_impulse(impulse)
            self.a2_strategy.set_impulse(impulse)
            self.a3_strategy.set_impulse(impulse)
            self.phase_detector.update_impulse(impulse)
        
        # 2. Actualizar detector de anclas
        self.anchor_detector.update(bar, lr_slope)
        
        # 3. Detectar fase del mercado
        current_phase = self.phase_detector.detect_phase(
            bar, lr_value, lr_slope, keltner, impulse
        )
        
        # 4. Obtener info de fase para contexto
        phase_info = self.phase_detector.get_phase_info()
        
        # 5. Obtener áreas de anclas
        resistance_area = self.anchor_detector.get_resistance_area()
        support_area = self.anchor_detector.get_support_area()
        
        # 6. Evaluar TRADE CBOT (solo en Fase 3 con 2+ anclas)
        signal_cbot = self.trade_cbot.evaluate(
            bar, current_phase, resistance_area, support_area
        )
        if signal_cbot:
            # Si detecta CBOT, resetear Trade 20 para nueva secuencia
            self.trade20_strategy.reset_for_new_cbot()
            return self._build_signal(
                signal_type=signal_cbot["type"],
                direction=signal_cbot["direction"],
                entry=signal_cbot["entry"],
                phase=current_phase,
                keltner=keltner,
                lr_value=lr_value,
                cbot_info=signal_cbot
            )
        
        # 7. Evaluar TRADE 20 (después de CBOT)
        if ema20_value:
            last_cbot = self.trade_cbot.get_last_cbot()
            signal_trade20 = self.trade20_strategy.evaluate(
                bar, current_phase, ema20_value, keltner, last_cbot
            )
            if signal_trade20:
                return self._build_signal(
                    signal_type=signal_trade20["type"],
                    direction=signal_trade20["direction"],
                    entry=signal_trade20["entry"],
                    phase=current_phase,
                    keltner=keltner,
                    lr_value=lr_value,
                    trade20_info=signal_trade20
                )
        
        # 8. Detectar FOBOs (solo en Fase 3)
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
        
        # 9. Evaluar Trade 80 (Fase 1 y Fase 4 - tendencial)
        if ema80_value and self.phase_detector.is_suitable_for_entries("TRADE_80"):
            signal_trade80 = self.trade80_strategy.evaluate(
                bar, ema80_value, ema80_slope, lr_value, lr_slope, keltner
            )
            if signal_trade80:
                direction = "LONG" if "LONG" in signal_trade80 else "SHORT"
                # Actualizar tracking de EMA80
                self.previous_ema80 = ema80_value
                return self._build_signal(
                    signal_type="TRADE_80",
                    direction=direction,
                    entry=bar["close"],
                    phase=current_phase,
                    keltner=keltner,
                    lr_value=lr_value,
                    ema80_value=ema80_value
                )
        
        # 10. Evaluar estrategias A1, A2, A3 según fase apropiada
        
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
        
        # Actualizar EMA80 previo
        if ema80_value:
            self.previous_ema80 = ema80_value
        
        return None
    
    def _build_signal(self, signal_type, direction, entry, phase, keltner, lr_value, 
                     fobo_info=None, ema80_value=None, cbot_info=None, trade20_info=None):
        """
        Construye el objeto de señal completo
        """
        # Si es CBOT o Trade 20, usar sus propios stops/targets
        if cbot_info:
            signal = {
                "type": signal_type,
                "direction": direction,
                "entry": cbot_info["entry"],
                "stop_loss": cbot_info["stop_loss"],
                "take_profit": cbot_info["take_profit"],
                "risk": cbot_info["risk"],
                "reward": cbot_info["reward"],
                "ratio": cbot_info["ratio"],
                "phase": phase,
                "phase_description": self.phase_detector._get_phase_description(),
                "keltner_basis": keltner["basis"],
                "lr_value": lr_value,
                "cbot_info": cbot_info
            }
            return signal
        
        if trade20_info:
            signal = {
                "type": signal_type,
                "direction": direction,
                "entry": trade20_info["entry"],
                "stop_loss": trade20_info["stop_loss"],
                "take_profit": trade20_info["take_profit"],
                "risk": trade20_info["risk"],
                "reward": trade20_info["reward"],
                "ratio": trade20_info["ratio"],
                "phase": phase,
                "phase_description": self.phase_detector._get_phase_description(),
                "keltner_basis": keltner["basis"],
                "lr_value": lr_value,
                "trade20_info": trade20_info
            }
            return signal
        
        # Para otras estrategias, calcular stop/take profit estándar
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
        
        # Añadir info adicional si es Trade 80
        if ema80_value:
            signal["ema80_value"] = ema80_value
        
        return signal
    
    def get_market_context(self):
        """
        Retorna contexto completo del mercado
        """
        return {
            "phase_info": self.phase_detector.get_phase_info(),
            "fobo_info": self.fobo_detector.get_fobo_info(),
            "anchor_info": self.anchor_detector.get_info(),
            "resistance_area": self.anchor_detector.get_resistance_area(),
            "support_area": self.anchor_detector.get_support_area()
        }
