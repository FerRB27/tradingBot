# Detector de Order Blocks
# Basado en la lógica de TradingView (indicadorOB.txt)

class OrderBlockDetector:
    """
    Detecta Order Blocks (OB) siguiendo la lógica:
    - Bullish OB: high de hace 2 velas < low de la vela actual
    - Bearish OB: low de hace 2 velas > high de la vela actual
    """
    
    def __init__(self):
        self.order_blocks = []
        
    def detect(self, candles):
        """
        Detecta OrderBlocks en una lista de velas
        
        Args:
            candles: Lista de velas con formato {'open', 'high', 'low', 'close', 'timestamp'}
            
        Returns:
            dict o None: {'type': 'bullish'/'bearish', 'candle': candle_data, 'index': index}
        """
        if len(candles) < 3:
            return None
            
        # Vela actual (última)
        current = candles[-1]
        # Vela anterior
        previous = candles[-2]
        # Vela de hace 2 barras
        two_ago = candles[-3]
        
        # Detectar Bullish Order Block
        # Condición: high de hace 2 velas < low actual
        is_bullish_ob = two_ago['high'] < current['low']
        
        # Detectar Bearish Order Block
        # Condición: low de hace 2 velas > high actual
        is_bearish_ob = two_ago['low'] > current['high']
        
        if is_bullish_ob:
            ob_data = {
                'type': 'bullish',
                'candle': {
                    'open': two_ago['open'],
                    'high': two_ago['high'],
                    'low': two_ago['low'],
                    'close': two_ago['close'],
                    'timestamp': two_ago.get('timestamp', None)
                },
                'middle': abs(two_ago['high'] - two_ago['low']) / 2,
                'range': abs(two_ago['high'] - two_ago['low'])
            }
            self.order_blocks.append(ob_data)
            return ob_data
            
        elif is_bearish_ob:
            ob_data = {
                'type': 'bearish',
                'candle': {
                    'open': two_ago['open'],
                    'high': two_ago['high'],
                    'low': two_ago['low'],
                    'close': two_ago['close'],
                    'timestamp': two_ago.get('timestamp', None)
                },
                'middle': abs(two_ago['high'] - two_ago['low']) / 2,
                'range': abs(two_ago['high'] - two_ago['low'])
            }
            self.order_blocks.append(ob_data)
            return ob_data
            
        return None
    
    def get_all_order_blocks(self):
        """Retorna todos los OrderBlocks detectados"""
        return self.order_blocks
    
    def get_last_order_block(self):
        """Retorna el último OrderBlock detectado"""
        if self.order_blocks:
            return self.order_blocks[-1]
        return None
