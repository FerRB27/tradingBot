# Construcción de Range Bars
class RangeBarBuilder:
    def __init__(self, range_size):
        self.range_size = range_size
        self.current_bar = None
        self.bars = []

    def process_trade(self, price):
        if self.current_bar is None:
            self._start_new_bar(price)
            return None

        self.current_bar["high"] = max(self.current_bar["high"], price)
        self.current_bar["low"] = min(self.current_bar["low"], price)
        self.current_bar["close"] = price

        if self._range_completed():
            finished_bar = self.current_bar
            self.bars.append(finished_bar)
            self._start_new_bar(price)
            return finished_bar

        return None

    def _start_new_bar(self, price):
        self.current_bar = {
            "open": price,
            "high": price,
            "low": price,
            "close": price
        }

    def _range_completed(self):
        return (
            self.current_bar["high"] - self.current_bar["low"]
            >= self.range_size
        )
