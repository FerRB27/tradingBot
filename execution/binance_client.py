# Cliente Futures - Ejecución de órdenes A1
from binance.client import Client
from config.secrets import API_KEY, API_SECRET


class BinanceFuturesClient:
    def __init__(self, testnet=True):
        self.client = Client(API_KEY, API_SECRET)
        
        if testnet:
            # Futures Testnet endpoints
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com'
            self.client.FUTURES_DATA_URL = 'https://testnet.binancefuture.com'
            self.client.FUTURES_COIN_URL = 'https://testnet.binancefuture.com'
            self.client.FUTURES_COIN_DATA_URL = 'https://testnet.binancefuture.com'
        
        try:
            self.client.futures_change_leverage(symbol="BTCUSDT", leverage=10)
        except Exception as e:
            print(f"⚠️ No se pudo establecer leverage: {e}")
            print("   Continuando de todas formas...")
        
    def place_order_a1(self, signal, entry_price, stop_loss, take_profit, quantity):
        """
        Coloca una orden A1 con SL y TP
        
        Args:
            signal: "LONG_A1" o "SHORT_A1"
            entry_price: Precio de entrada
            stop_loss: Precio del stop loss
            take_profit: Precio del take profit
            quantity: Cantidad a operar
        """
        try:
            side = "BUY" if signal == "LONG_A1" else "SELL"
            
            # Orden de entrada (Market)
            entry_order = self.client.futures_create_order(
                symbol="BTCUSDT",
                side=side,
                type="MARKET",
                quantity=quantity
            )
            
            print(f"✅ Orden de entrada ejecutada: {side} {quantity} BTCUSDT")
            
            # Stop Loss
            sl_side = "SELL" if signal == "LONG_A1" else "BUY"
            sl_order = self.client.futures_create_order(
                symbol="BTCUSDT",
                side=sl_side,
                type="STOP_MARKET",
                stopPrice=stop_loss,
                closePosition=True
            )
            
            print(f"✅ Stop Loss colocado: {stop_loss}")
            
            # Take Profit
            tp_order = self.client.futures_create_order(
                symbol="BTCUSDT",
                side=sl_side,
                type="TAKE_PROFIT_MARKET",
                stopPrice=take_profit,
                closePosition=True
            )
            
            print(f"✅ Take Profit colocado: {take_profit}")
            
            return {
                "entry": entry_order,
                "stop_loss": sl_order,
                "take_profit": tp_order
            }
            
        except Exception as e:
            print(f"❌ Error al ejecutar orden: {e}")
            return None
    
    def get_balance(self):
        """Obtiene el balance disponible en Futures"""
        try:
            account = self.client.futures_account()
            balance = float(account['availableBalance'])
            return balance
        except Exception as e:
            print(f"❌ Error al obtener balance: {e}")
            return None
    
    def calculate_position_size(self, balance, risk_percentage, risk_distance):
        """
        Calcula el tamaño de posición basado en el riesgo
        
        Args:
            balance: Balance disponible
            risk_percentage: % de riesgo por trade (ej: 0.01 = 1%)
            risk_distance: Distancia al stop loss en puntos
        """
        risk_amount = balance * risk_percentage
        quantity = risk_amount / risk_distance
        return round(quantity, 3)