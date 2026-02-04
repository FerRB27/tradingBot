# Stream de velas japonesas (Klines) desde Binance WebSocket
import websocket
import json
import logging
from datetime import datetime
from config.settings import SYMBOL

# Configurar logger
logger = logging.getLogger('kline_stream')


class KlineStream:
    """
    Cliente para recibir velas japonesas (Klines) en tiempo real desde Binance
    """
    
    def __init__(self, symbol="BTCUSDT", interval="5m"):
        """
        Args:
            symbol: Par de trading (ej: "BTCUSDT")
            interval: Intervalo de las velas (1m, 3m, 5m, 15m, 30m, 1h, etc.)
        """
        self.symbol = symbol.lower()
        self.interval = interval
        self.url = f"wss://stream.binance.com:9443/ws/{self.symbol}@kline_{self.interval}"
        self.ws = None
        self.candles = []
        self.on_candle_callback = None
        
    def set_callback(self, callback):
        """
        Establece una función callback que se ejecutará al completarse una vela
        
        Args:
            callback: Función que recibe un dict de vela {'open', 'high', 'low', 'close', 'timestamp'}
        """
        self.on_candle_callback = callback
        
    def start(self):
        """Inicia el stream de WebSocket"""
        logger.info(f"Iniciando stream de {self.interval} para {self.symbol.upper()}")
        self.ws = websocket.WebSocketApp(
            self.url,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self.ws.run_forever()
        
    def _on_open(self, ws):
        logger.info(f"✅ Conectado al stream de {self.interval}")
        
    def _on_message(self, ws, message):
        try:
            data = json.loads(message)
            
            if 'k' not in data:
                return
                
            kline = data['k']
            
            # Crear objeto de vela
            candle = {
                'timestamp': datetime.fromtimestamp(kline['t'] / 1000),
                'open': float(kline['o']),
                'high': float(kline['h']),
                'low': float(kline['l']),
                'close': float(kline['c']),
                'volume': float(kline['v']),
                'is_closed': kline['x']  # True cuando la vela se cierra
            }
            
            # Si la vela se cerró, llamar al callback
            if candle['is_closed'] and self.on_candle_callback:
                self.candles.append(candle)
                self.on_candle_callback(candle)
                
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            
    def _on_error(self, ws, error):
        logger.error(f"Error en WebSocket: {error}")
        
    def _on_close(self, ws, close_status_code, close_msg):
        logger.warning(f"WebSocket cerrado: {close_status_code} - {close_msg}")
        
    def get_candles(self):
        """Retorna todas las velas recopiladas"""
        return self.candles
