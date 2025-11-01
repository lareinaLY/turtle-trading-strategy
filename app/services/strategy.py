def turtle_strategy(data, entry_period=20, exit_period=10):
    """
    海龟法则策略判断

    参数:
    data: 股票历史数据 (DataFrame)
    entry_period: 入场周期（默认20天）
    exit_period: 出场周期（默认10天）

    返回:
    "BUY" / "SELL" / "HOLD"
    """

    # 检查数据是否足够
    if len(data) < entry_period:
        print(f"⚠️  数据不足：只有 {len(data)} 天数据")
        return "HOLD"

    # 获取当前价格
    current_price = float(data['Close'].iloc[-1])
    print(f"💰 当前价格: ${current_price:.2f}")

    # 计算20日最高价（突破这个价格就买入）
    high_20 = float(data['High'].iloc[-entry_period:].max())
    print(f"📈 {entry_period}日最高价: ${high_20:.2f}")

    # 计算10日最低价（跌破这个价格就卖出）
    low_10 = float(data['Low'].iloc[-exit_period:].min())
    print(f"📉 {exit_period}日最低价: ${low_10:.2f}")

    # 判断交易信号
    if current_price >= high_20:
        print(f"🟢 买入信号：价格突破{entry_period}日最高！")
        return "BUY"
    elif current_price <= low_10:
        print(f"🔴 卖出信号：价格跌破{exit_period}日最低！")
        return "SELL"
    else:
        print(f"🟡 持有信号：价格在通道内")
        return "HOLD"


# 测试代码
if __name__ == "__main__":
    print("🐢 海龟法则策略测试")
    print("=" * 50)

    import yfinance as yf

    # 测试 AAPL
    print("\n📊 测试股票: AAPL")
    print("-" * 50)

    ticker = yf.Ticker("AAPL")
    data = ticker.history(period="2mo")

    signal = turtle_strategy(data)

    print("\n" + "=" * 50)
    print(f"🎯 最终信号: {signal}")
    print("=" * 50)