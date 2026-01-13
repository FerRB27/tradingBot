# SL / TP dinámicos - Ratio 2:1 (MDC Trading Academy)

def calculate_sl_tp(entry_price, signal_type, keltner, risk_percentage=0.01):
    """
    Calcula Stop Loss y Take Profit para señales A1 y A2
    
    LONG (A1 y A2):
    - SL: Debajo de la banda inferior Keltner
    - TP: 2x la distancia del SL (ratio 2:1)
    
    SHORT (A1 y A2):
    - SL: Encima de la banda superior Keltner
    - TP: 2x la distancia del SL (ratio 2:1)
    
    Args:
        entry_price: Precio de entrada
        signal_type: "LONG_A1", "SHORT_A1", "LONG_A2", "SHORT_A2"
        keltner: Dict con 'upper', 'lower', 'basis'
        risk_percentage: % de riesgo por operación (default 1%)
    
    Returns:
        dict: {"stop_loss": float, "take_profit": float, "risk_amount": float}
    """
    if not keltner:
        return None
    
    if "LONG" in signal_type:  # LONG_A1 o LONG_A2
        # Stop Loss debajo de la banda inferior
        stop_loss = keltner["lower"]
        risk_distance = entry_price - stop_loss
        
        # Take Profit: 2x la distancia de riesgo
        take_profit = entry_price + (risk_distance * 2)
        
    elif "SHORT" in signal_type:  # SHORT_A1 o SHORT_A2
        # Stop Loss encima de la banda superior
        stop_loss = keltner["upper"]
        risk_distance = stop_loss - entry_price
        
        # Take Profit: 2x la distancia de riesgo
        take_profit = entry_price - (risk_distance * 2)
        
    else:
        return None
    
    return {
        "stop_loss": round(stop_loss, 2),
        "take_profit": round(take_profit, 2),
        "risk_distance": round(risk_distance, 2),
        "reward_distance": round(risk_distance * 2, 2)
    }