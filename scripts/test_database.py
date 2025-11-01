"""
数据库测试脚本

验证数据库的所有基本功能：
- 创建表
- 插入数据
- 查询数据
- 更新数据
- 删除数据
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径（重要！）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 现在可以正常导入 app 模块了
from app.database.connection import SessionLocal, init_db, engine
from app.database.models import Stock, AlertHistory
from datetime import datetime


def test_connection():
    """测试 1: 连接数据库"""
    print("\n" + "=" * 50)
    print("测试 1: 数据库连接")
    print("=" * 50)

    try:
        connection = engine.connect()
        print("✅ 数据库连接成功")
        connection.close()
        return True
    except Exception as e:
        print(f"❌ 连接失败: {e}")
        return False


def test_create_tables():
    """测试 2: 创建表"""
    print("\n" + "=" * 50)
    print("测试 2: 创建数据库表")
    print("=" * 50)

    try:
        init_db()
        print("✅ 所有表创建成功")
        return True
    except Exception as e:
        print(f"❌ 创建表失败: {e}")
        return False


def test_insert_stock():
    """测试 3: 插入股票数据"""
    print("\n" + "=" * 50)
    print("测试 3: 插入股票数据")
    print("=" * 50)

    db = SessionLocal()

    try:
        # 创建一个股票对象
        apple = Stock(
            symbol="AAPL",
            name="Apple Inc.",
            current_price=178.50,
            is_active=True
        )

        # 添加到会话
        db.add(apple)

        # 提交到数据库
        db.commit()

        # 刷新对象，获取数据库生成的 ID
        db.refresh(apple)

        print(f"✅ 成功插入股票: {apple}")
        print(f"   - ID: {apple.id}")
        print(f"   - 代码: {apple.symbol}")
        print(f"   - 价格: ${apple.current_price}")
        print(f"   - 更新时间: {apple.last_updated}")

        return True
    except Exception as e:
        print(f"❌ 插入失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_query_stocks():
    """测试 4: 查询股票数据"""
    print("\n" + "=" * 50)
    print("测试 4: 查询股票数据")
    print("=" * 50)

    db = SessionLocal()

    try:
        # 查询所有股票
        stocks = db.query(Stock).all()
        print(f"✅ 找到 {len(stocks)} 只股票:")

        for stock in stocks:
            print(f"   - {stock.symbol}: ${stock.current_price}")

        # 查询特定股票
        apple = db.query(Stock).filter(Stock.symbol == "AAPL").first()
        if apple:
            print(f"\n✅ 找到 AAPL: {apple}")

        return True
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return False
    finally:
        db.close()


def test_insert_alert():
    """测试 5: 插入提醒记录"""
    print("\n" + "=" * 50)
    print("测试 5: 插入提醒记录")
    print("=" * 50)

    db = SessionLocal()

    try:
        # 创建提醒记录
        alert = AlertHistory(
            symbol="AAPL",
            signal="BUY",
            price=178.50,
            strategy_params='{"period": 20, "strategy": "turtle"}',
            message="AAPL 突破20日高点，建议买入",
            sent=True
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        print(f"✅ 成功插入提醒: {alert}")
        print(f"   - ID: {alert.id}")
        print(f"   - 信号: {alert.signal}")
        print(f"   - 消息: {alert.message}")
        print(f"   - 创建时间: {alert.created_at}")

        return True
    except Exception as e:
        print(f"❌ 插入失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_update_stock():
    """测试 6: 更新股票价格"""
    print("\n" + "=" * 50)
    print("测试 6: 更新股票价格")
    print("=" * 50)

    db = SessionLocal()

    try:
        # 查找 AAPL
        apple = db.query(Stock).filter(Stock.symbol == "AAPL").first()

        if not apple:
            print("❌ 找不到 AAPL")
            return False

        old_price = apple.current_price
        new_price = 180.00

        # 更新价格
        apple.current_price = new_price
        db.commit()

        print(f"✅ 成功更新价格:")
        print(f"   - 旧价格: ${old_price}")
        print(f"   - 新价格: ${new_price}")

        return True
    except Exception as e:
        print(f"❌ 更新失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def test_delete_stock():
    """测试 7: 删除股票（软删除）"""
    print("\n" + "=" * 50)
    print("测试 7: 软删除股票")
    print("=" * 50)

    db = SessionLocal()

    try:
        # 查找 AAPL
        apple = db.query(Stock).filter(Stock.symbol == "AAPL").first()

        if not apple:
            print("❌ 找不到 AAPL")
            return False

        # 软删除（不真正删除，只是标记为不活跃）
        apple.is_active = False
        db.commit()

        print(f"✅ 成功软删除 AAPL")
        print(f"   - is_active: {apple.is_active}")

        # 恢复（为了后续测试）
        apple.is_active = True
        db.commit()
        print(f"✅ 已恢复 AAPL")

        return True
    except Exception as e:
        print(f"❌ 删除失败: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🐢" * 25)
    print("海龟交易系统 - 数据库测试")
    print("🐢" * 25)

    tests = [
        ("连接测试", test_connection),
        ("创建表", test_create_tables),
        ("插入股票", test_insert_stock),
        ("查询股票", test_query_stocks),
        ("插入提醒", test_insert_alert),
        ("更新股票", test_update_stock),
        ("删除股票", test_delete_stock),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} 发生异常: {e}")
            results.append((name, False))

    # 总结
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status} - {name}")

    print(f"\n总计: {passed}/{total} 测试通过")

    if passed == total:
        print("\n🎉 所有测试通过！数据库工作正常！")
    else:
        print("\n⚠️ 部分测试失败，请检查错误信息")


if __name__ == "__main__":
    run_all_tests()