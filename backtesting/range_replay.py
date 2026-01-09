# Construye Range Bars offline
from market_data.range_builder import RangeBarBuilder


def build_range_bars(trades, range_size):
    builder = RangeBarBuilder(range_size)
    bars = []

    for trade in trades:
        bar = builder.process_trade(trade["price"])
        if bar:
            bars.append(bar)

    return bars
