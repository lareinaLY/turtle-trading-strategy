import pytest
import pandas as pd
from strategy import turtle_strategy


def test_signal():
    """简单测试"""
    data = pd.DataFrame({
        'Close': [240, 245, 250, 255, 260],
        'High': [242, 247, 252, 257, 261],
        'Low': [238, 243, 248, 253, 258]
    })

    signal = turtle_strategy(data)
    assert signal in ["BUY", "SELL", "HOLD"]
    print(f"测试通过！信号: {signal}")