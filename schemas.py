# ============================================================================
# models.py - 数据模型定义
# 使用 Pydantic 定义 API 的请求和响应格式
# ============================================================================

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StockDataResponse(BaseModel):
    """
    股票数据响应模型
    定义了 /api/stock/{symbol} 端点的返回格式
    """
    symbol: str = Field(..., description="股票代码", example="AAPL")
    current_price: float = Field(..., description="当前价格", example=255.50)
    high_20d: float = Field(..., description="20日最高价", example=260.00)
    low_10d: float = Field(..., description="10日最低价", example=240.00)
    avg_price: float = Field(..., description="平均价格", example=250.00)
    data_points: int = Field(..., description="数据点数", example=40)
    period: str = Field(..., description="时间周期", example="2mo")
    timestamp: str = Field(..., description="分析时间", example="2024-10-02T15:30:00")

    class Config:
        # 提供示例数据，在 Swagger 文档中显示
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "current_price": 255.50,
                "high_20d": 260.00,
                "low_10d": 240.00,
                "avg_price": 250.00,
                "data_points": 40,
                "period": "2mo",
                "timestamp": "2024-10-02T15:30:00"
            }
        }


class StrategyResponse(BaseModel):
    """
    策略分析响应模型
    定义了 /api/analyze/{symbol} 端点的返回格式
    """
    symbol: str = Field(..., description="股票代码")
    signal: str = Field(..., description="交易信号：BUY/SELL/HOLD")
    current_price: float = Field(..., description="当前价格")
    high_20d: float = Field(..., description="20日最高价")
    low_10d: float = Field(..., description="10日最低价")
    recommendation: str = Field(..., description="操作建议")
    analysis_time: str = Field(..., description="分析时间")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "signal": "BUY",
                "current_price": 255.50,
                "high_20d": 254.00,
                "low_10d": 240.00,
                "recommendation": "价格突破20日最高点，建议买入",
                "analysis_time": "2024-10-02T15:30:00"
            }
        }


class BatchAnalysisResult(BaseModel):
    """单只股票的批量分析结果"""
    symbol: str
    signal: Optional[str] = None
    current_price: Optional[float] = None
    status: str  # success or failed
    error: Optional[str] = None


class BatchAnalysisResponse(BaseModel):
    """批量分析响应模型"""
    total: int = Field(..., description="总股票数")
    results: list[BatchAnalysisResult] = Field(..., description="分析结果列表")
    timestamp: str = Field(..., description="分析时间")

    class Config:
        json_schema_extra = {
            "example": {
                "total": 3,
                "results": [
                    {
                        "symbol": "AAPL",
                        "signal": "BUY",
                        "current_price": 255.50,
                        "status": "success",
                        "error": None
                    },
                    {
                        "symbol": "TSLA",
                        "signal": "HOLD",
                        "current_price": 265.00,
                        "status": "success",
                        "error": None
                    }
                ],
                "timestamp": "2024-10-02T15:30:00"
            }
        }


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str = Field(..., description="错误类型")
    detail: str = Field(..., description="错误详情")
    timestamp: str = Field(..., description="错误时间")

    class Config:
        json_schema_extra = {
            "example": {
                "error": "StockNotFound",
                "detail": "无法获取股票 INVALID 的数据",
                "timestamp": "2024-10-02T15:30:00"
            }
        }


# ============================================================================
# 如果运行这个文件，会显示模型的 JSON Schema
# ============================================================================

if __name__ == "__main__":
    print("📋 数据模型 JSON Schema 示例")
    print("=" * 60)

    # 创建示例对象
    stock_data = StockDataResponse(
        symbol="AAPL",
        current_price=255.50,
        high_20d=260.00,
        low_10d=240.00,
        avg_price=250.00,
        data_points=40,
        period="2mo",
        timestamp=datetime.now().isoformat()
    )

    print("\n1. StockDataResponse 示例:")
    print(stock_data.model_dump_json(indent=2))

    strategy_result = StrategyResponse(
        symbol="AAPL",
        signal="BUY",
        current_price=255.50,
        high_20d=254.00,
        low_10d=240.00,
        recommendation="价格突破20日最高点，建议买入",
        analysis_time=datetime.now().isoformat()
    )

    print("\n2. StrategyResponse 示例:")
    print(strategy_result.model_dump_json(indent=2))

    print("\n✅ 模型定义完成！")
    print("这些模型将用于 API 的请求和响应验证")