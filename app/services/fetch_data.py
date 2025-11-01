import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_data(symbol, period="1mo"):
    """
    获取股票的历史价格数据

    参数:
    symbol (str): 股票代码，例如 "AAPL", "TSLA", "MSFT"
    period (str): 数据时间范围，默认为 "1mo" (1个月)
                 可选: "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"

    返回:
    pandas.DataFrame: 包含股票历史数据的DataFrame，如果失败则返回None
    """

    try:
        # 步骤1: 创建股票对象
        # yf.Ticker() 创建一个股票对象，用于获取该股票的各种数据
        stock = yf.Ticker(symbol)

        # 步骤2: 获取历史数据
        # history() 方法获取历史价格数据
        # period参数指定时间范围，interval可以指定数据间隔（默认1天）
        data = stock.history(period=period)

        # 步骤3: 检查数据是否为空
        if data.empty:
            print(f"警告: 无法获取股票 {symbol} 的数据，请检查股票代码是否正确")
            return None

        # 步骤4: 数据清理和格式化
        # 重置索引，让日期从索引变成普通列
        data = data.reset_index()

        # 将日期列转换为日期格式（去掉时区信息，只保留日期）
        data['Date'] = data['Date'].dt.date

        # 保留我们需要的列：日期、开盘价、最高价、最低价、收盘价、成交量
        # 海龟法则主要使用收盘价和最高/最低价
        columns_to_keep = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        data = data[columns_to_keep]

        # 步骤5: 按日期排序（确保数据按时间顺序排列）
        data = data.sort_values('Date').reset_index(drop=True)

        print(f"✅ 成功获取股票 {symbol} 的数据")
        print(f"📊 数据范围: {data['Date'].min()} 到 {data['Date'].max()}")
        print(f"📈 总共 {len(data)} 个交易日的数据")

        return data

    except Exception as e:
        # 步骤6: 错误处理
        print(f"❌ 获取股票 {symbol} 数据时发生错误: {str(e)}")
        print("可能的原因:")
        print("1. 网络连接问题")
        print("2. 股票代码不正确")
        print("3. Yahoo Finance 服务暂时不可用")
        return None


def display_recent_data(data, days=20):
    """
    显示最近几天的收盘价数据

    参数:
    data (pandas.DataFrame): 股票数据
    days (int): 显示最近多少天的数据，默认20天
    """

    if data is None or data.empty:
        print("❌ 没有数据可显示")
        return

    # 获取最近N天的数据
    recent_data = data.tail(days).copy()
    # 重置索引，确保索引从0开始连续编号
    recent_data = recent_data.reset_index(drop=True)

    print(f"\n📋 最近 {len(recent_data)} 个交易日的收盘价:")
    print("-" * 50)
    print(f"{'日期':<12} {'收盘价':<10} {'涨跌':<8}")
    print("-" * 50)

    for i in range(len(recent_data)):
        row = recent_data.iloc[i]

        # 计算涨跌（与前一天比较）
        if i > 0:
            prev_close = recent_data.iloc[i - 1]['Close']
            change = row['Close'] - prev_close
            change_pct = (change / prev_close) * 100
            change_str = f"{change:+.2f} ({change_pct:+.1f}%)"
        else:
            change_str = "---"

        print(f"{str(row['Date']):<12} ${row['Close']:<9.2f} {change_str}")


# 测试代码
if __name__ == "__main__":
    print("🐢 海龟法则股票提醒系统 - 数据获取模块测试")
    print("=" * 60)

    # 测试不同的股票
    test_symbols = ["AAPL", "TSLA", "MSFT"]

    for symbol in test_symbols:
        print(f"\n🔍 正在测试股票: {symbol}")

        # 获取数据
        stock_data = fetch_data(symbol, period="1mo")

        if stock_data is not None:
            # 显示最近20天的收盘价
            display_recent_data(stock_data, days=20)

            # 显示数据统计信息
            latest_close = stock_data['Close'].iloc[-1]
            highest_20d = stock_data['Close'].tail(20).max()
            lowest_20d = stock_data['Close'].tail(20).min()

            print(f"\n📊 {symbol} 统计信息:")
            print(f"   最新收盘价: ${latest_close:.2f}")
            print(f"   20日最高价: ${highest_20d:.2f}")
            print(f"   20日最低价: ${lowest_20d:.2f}")

        print("\n" + "=" * 60)