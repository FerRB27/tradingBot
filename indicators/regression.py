# Linear Regression 89
import numpy as np


def linear_regression(values, period):
    if len(values) < period:
        return None

    y = np.array(values[-period:])
    x = np.arange(period)

    slope, intercept = np.polyfit(x, y, 1)
    lr_value = intercept + slope * (period - 1)

    return lr_value, slope
