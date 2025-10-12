# tests/test_api.py

from fastapi.testclient import TestClient
from api import app
import pytest

client = TestClient(app)


class TestBasicEndpoints:
    """基础端点测试"""

    def test_root(self):
        """测试根路径"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data

    def test_health_check(self):
        """测试健康检查"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"


class TestStockEndpoints:
    """股票数据端点测试"""

    def test_get_stock_data_success(self):
        """测试获取股票数据 - 成功"""
        response = client.get("/api/stock/AAPL")

        assert response.status_code == 200
        data = response.json()

        assert data["symbol"] == "AAPL"
        assert "current_price" in data
        assert "high_20d" in data
        assert data["data_points"] > 0

    def test_get_stock_data_with_period(self):
        """测试带时间周期参数"""
        response = client.get("/api/stock/AAPL?period=1y")

        assert response.status_code == 200
        data = response.json()
        assert data["period"] == "1y"

    def test_invalid_stock_symbol(self):
        """测试无效股票代码"""
        response = client.get("/api/stock/INVALID_XYZ_123")

        # 应该返回 404 或 500
        assert response.status_code in [404, 500]


class TestStrategyEndpoints:
    """策略分析端点测试"""

    def test_analyze_strategy(self):
        """测试策略分析"""
        response = client.get("/api/analyze/AAPL")

        assert response.status_code == 200
        data = response.json()

        assert data["symbol"] == "AAPL"
        assert data["signal"] in ["BUY", "SELL", "HOLD"]
        assert "recommendation" in data

    def test_custom_periods(self):
        """测试自定义周期参数"""
        response = client.get(
            "/api/analyze/AAPL?entry_period=30&exit_period=15"
        )

        assert response.status_code == 200


class TestBatchEndpoints:
    """批量分析端点测试"""

    def test_batch_analysis(self):
        """测试批量分析"""
        response = client.get("/api/stocks/batch?symbols=AAPL,TSLA,MSFT")

        assert response.status_code == 200
        data = response.json()

        assert data["total"] == 3
        assert len(data["results"]) == 3

    def test_batch_with_invalid(self):
        """测试批量分析包含无效代码"""
        response = client.get("/api/stocks/batch?symbols=AAPL,INVALID,TSLA")

        assert response.status_code == 200
        data = response.json()

        # 应该返回3个结果
        assert data["total"] == 3
        # 检查是否正确标记了失败
        statuses = [r["status"] for r in data["results"]]
        assert "failed" in statuses