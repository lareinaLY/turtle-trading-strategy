# history.py - 历史记录管理模块

import json
from datetime import datetime
from pathlib import Path

HISTORY_FILE = "data/analysis_history.json"


def ensure_data_dir():
    """确保 data 目录存在"""
    Path("").mkdir(exist_ok=True)


def save_analysis(symbol, result):
    """
    保存分析记录

    参数:
    symbol: 股票代码
    result: 分析结果字典
    """
    ensure_data_dir()

    # 读取现有历史
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
    except FileNotFoundError:
        history = []

    # 创建新记录
    record = {
        "symbol": symbol,
        "signal": result.get('signal'),
        "current_price": result.get('current_price'),
        "high_20d": result.get('high_20d'),
        "low_10d": result.get('low_10d'),
        "timestamp": datetime.now().isoformat(),
        "analysis_id": len(history) + 1  # 简单的 ID
    }

    history.append(record)

    # 保存
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

    print(f"✅ 记录已保存（ID: {record['analysis_id']}）")
    return record


def get_history(limit=10):
    """
    获取历史记录

    参数:
    limit: 返回最近N条记录
    """
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        return history[-limit:]
    except FileNotFoundError:
        return []


def search_by_symbol(symbol):
    """搜索特定股票的历史"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)
        return [r for r in history if r['symbol'] == symbol]
    except FileNotFoundError:
        return []


def get_statistics():
    """获取统计信息"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history = json.load(f)

        total = len(history)
        buy_signals = len([r for r in history if r['signal'] == 'BUY'])
        sell_signals = len([r for r in history if r['signal'] == 'SELL'])
        hold_signals = len([r for r in history if r['signal'] == 'HOLD'])

        return {
            "total_analyses": total,
            "buy_count": buy_signals,
            "sell_count": sell_signals,
            "hold_count": hold_signals
        }
    except FileNotFoundError:
        return {
            "total_analyses": 0,
            "buy_count": 0,
            "sell_count": 0,
            "hold_count": 0
        }


def clear_history():
    """清空所有历史记录"""
    try:
        Path(HISTORY_FILE).unlink()
        print("✅ 历史记录已清空")
        return True
    except FileNotFoundError:
        print("没有历史记录")
        return False