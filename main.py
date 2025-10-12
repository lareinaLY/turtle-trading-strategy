# ============================================================================
# main.py - 海龟法则股票提醒系统主程序
# 整合所有模块：数据获取 + 策略分析 + 邮件通知
# ============================================================================

from fetch_data import fetch_data
from strategy import turtle_strategy
from notification import send_trading_signal
from datetime import datetime
from history import save_analysis, get_history, search_by_symbol, get_statistics
from config import config

EMAIL_CONFIG = {
    'from_email': config.FROM_EMAIL,      # ← 修改：你的 Gmail 地址
    'to_email': config.TO_EMAIL,        # ← 修改：接收邮件的地址（可以是同一个）
    'password': config.EMAIL_PASSWORD   # ← 修改：Gmail 应用专用密码（16位，无空格）
}

# ============================================================================
# 主要功能函数
# ============================================================================


def analyze_single_stock(symbol, to_email="trader@example.com"):
    """
    分析单只股票并发送通知

    参数:
    symbol (str): 股票代码
    to_email (str): 接收通知的邮箱

    返回:
    dict: 分析结果
    """

    print(f"\n🐢 海龟法则股票分析系统")
    print("=" * 60)
    print(f"分析股票: {symbol}")
    print(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # 步骤1：获取数据
    print(f"\n📊 步骤1：获取股票数据")
    print("-" * 40)

    data = fetch_data(symbol, period="2mo")

    if data is None or data.empty:
        print(f"❌ 无法获取 {symbol} 的数据")
        return {
            'symbol': symbol,
            'status': 'failed',
            'reason': '数据获取失败'
        }

    print(f"✅ 成功获取 {len(data)} 天的数据")

    # 步骤2：执行策略分析
    print(f"\n🧮 步骤2：执行海龟法则策略分析")
    print("-" * 40)

    signal = turtle_strategy(data)

    # 步骤3：准备价格信息
    print(f"\n📈 步骤3：提取价格信息")
    print("-" * 40)

    current_price = float(data['Close'].iloc[-1])
    high_20 = float(data['High'].iloc[-20:].max())
    low_10 = float(data['Low'].iloc[-10:].min())

    price_info = {
        'current': current_price,
        'high_20': high_20,
        'low_10': low_10
    }

    print(f"当前价格: ${current_price:.2f}")
    print(f"20日最高: ${high_20:.2f}")
    print(f"10日最低: ${low_10:.2f}")

    # 步骤4：发送通知（只在有信号时发送）
    print(f"\n📧 步骤4：发送通知")
    print("-" * 40)

    if signal in ["BUY", "SELL"]:
        print(f"检测到 {signal} 信号，发送邮件通知...")
        success = send_trading_signal(symbol, signal, price_info, to_email)

        if success:
            notification_status = "已发送"
        else:
            notification_status = "发送失败"
    else:
        print(f"信号为 HOLD，不发送通知")
        notification_status = "无需发送"

    # 返回分析结果
    result = {
        'symbol': symbol,
        'signal': signal,
        'current_price': current_price,
        'high_20': high_20,
        'low_10': low_10,
        'notification': notification_status,
        'status': 'success',
        'analysis_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    # 🆕 保存历史
    save_analysis(symbol, result)

    return result


def analyze_multiple_stocks(symbols, to_email="trader@example.com"):
    """
    批量分析多只股票

    参数:
    symbols (list): 股票代码列表
    to_email (str): 接收通知的邮箱

    返回:
    dict: 所有股票的分析结果
    """

    print(f"\n🐢 海龟法则批量分析")
    print("=" * 60)
    print(f"分析股票数量: {len(symbols)}")
    print(f"股票列表: {', '.join(symbols)}")
    print("=" * 60)

    results = {}

    for symbol in symbols:
        result = analyze_single_stock(symbol, to_email)
        results[symbol] = result
        print(f"\n{'=' * 60}\n")

    # 汇总报告
    print(f"\n📊 批量分析汇总")
    print("=" * 60)

    buy_signals = [s for s, r in results.items() if r.get('signal') == 'BUY']
    sell_signals = [s for s, r in results.items() if r.get('signal') == 'SELL']
    hold_signals = [s for s, r in results.items() if r.get('signal') == 'HOLD']

    print(f"🟢 买入信号 ({len(buy_signals)}): {', '.join(buy_signals) if buy_signals else '无'}")
    print(f"🔴 卖出信号 ({len(sell_signals)}): {', '.join(sell_signals) if sell_signals else '无'}")
    print(f"🟡 持有信号 ({len(hold_signals)}): {', '.join(hold_signals) if hold_signals else '无'}")

    return results


def main():
    """主程序入口"""

    print("""
    ╔═══════════════════════════════════════════╗
    ║   🐢 海龟法则股票提醒系统 v1.0               ║
    ║   Turtle Trading Strategy Alert System    ║
    ╚═══════════════════════════════════════════╝
    """)

    # 用户输入
    print(f"\n请选择分析模式：")
    print(f"1. 分析单只股票")
    print(f"2. 批量分析多只股票")
    print(f"3. 查看历史记录")  # 🆕
    print(f"4. 搜索股票历史")  # 🆕
    print(f"5. 查看统计信息")  # 🆕

    choice = input("\n请输入选项 (1 或 2): ").strip()

    if choice == "1":
        # 单只股票分析
        symbol = input("\n请输入股票代码 (如 AAPL): ").strip().upper()

        if symbol:
            result = analyze_single_stock(symbol)

            print(f"\n✅ 分析完成！")
            print(f"最终信号: {result.get('signal', 'N/A')}")
        else:
            print(f"❌ 股票代码不能为空")

    elif choice == "2":
        # 批量分析
        print(f"\n请输入股票代码，用逗号分隔")
        symbols_input = input("例如: AAPL,TSLA,MSFT\n请输入: ").strip().upper()

        if symbols_input:
            symbols = [s.strip() for s in symbols_input.split(',')]
            results = analyze_multiple_stocks(symbols)

            print(f"\n✅ 批量分析完成！")
            print(f"共分析 {len(results)} 只股票")
        else:
            print(f"❌ 输入不能为空")

    elif choice == "3":
        history = get_history(20)
        print("\n📜 最近20条记录")
        for r in history:
            print(f"{r['timestamp'][:19]}: {r['symbol']} - {r['signal']} (${r['current_price']:.2f})")

    elif choice == "4":
        symbol = input("输入股票代码: ").strip().upper()
        records = search_by_symbol(symbol)
        print(f"\n{symbol} 的历史记录：")
        for r in records:
            print(f"{r['timestamp'][:19]}: {r['signal']}")

    elif choice == "5":
        stats = get_statistics()
        print("\n📊 统计信息")
        print(f"总分析次数: {stats['total_analyses']}")
        print(f"买入信号: {stats['buy_count']}")
        print(f"卖出信号: {stats['sell_count']}")
        print(f"持有信号: {stats['hold_count']}")

    else:
        print(f"❌ 无效选项")

    print(f"\n感谢使用海龟法则股票提醒系统！")


# ============================================================================
# 程序入口
# ============================================================================

if __name__ == "__main__":
    # 快速测试模式（不需要用户输入）
    QUICK_TEST = False

    if QUICK_TEST:
        print(f"🚀 快速测试模式")
        print("=" * 60)
        print(f"自动测试 AAPL、TSLA、MSFT 三只股票\n")

        # 自动测试
        test_symbols = ["AAPL", "TSLA", "MSFT"]
        results = analyze_multiple_stocks(test_symbols)

        print(f"\n🎉 快速测试完成！")
        print(f"\n💡 要使用交互模式：")
        print(f"   将 QUICK_TEST 改为 False，重新运行")

    else:
        # 交互模式
        main()