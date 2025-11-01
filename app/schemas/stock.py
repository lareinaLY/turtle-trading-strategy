"""
Pydantic 模型 - API 数据验证

定义 API 请求和响应的数据结构
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class StockRequest(BaseModel):
    """股票分析请求模型"""
    symbol: str = Field(..., description="股票代码", example="AAPL")
    period: str = Field(default="2mo", description="数据周期", example="2mo")
    interval: str = Field(default="1d", description="数据间隔", example="1d")
    entry_period: int = Field(default=20, description="入场周期（天）", example=20)
    exit_period: int = Field(default=10, description="离场周期（天）", example=10)


class StockResponse(BaseModel):
    """股票分析响应模型"""
    symbol: str = Field(..., description="股票代码")
    current_price: float = Field(..., description="当前价格")
    signal: str = Field(..., description="交易信号：BUY/SELL/HOLD")
    entry_price: Optional[float] = Field(None, description="入场价格（20日最高）")
    exit_price: Optional[float] = Field(None, description="离场价格（10日最低）")
    high_20d: Optional[float] = Field(None, description="20日最高价")
    low_10d: Optional[float] = Field(None, description="10日最低价")
    timestamp: datetime = Field(..., description="分析时间")
    alert_id: Optional[int] = Field(None, description="提醒记录ID")

    class Config:
        json_schema_extra = {
            "example": {
                "symbol": "AAPL",
                "current_price": 178.50,
                "signal": "BUY",
                "entry_price": 175.20,
                "exit_price": 172.80,
                "timestamp": "2024-10-13T15:30:00",
                "alert_id": 1
            }
        }


class HistoryResponse(BaseModel):
    """历史记录响应模型"""
    id: int = Field(..., description="记录ID")
    symbol: str = Field(..., description="股票代码")
    signal: str = Field(..., description="交易信号")
    price: float = Field(..., description="触发价格")
    message: Optional[str] = Field(None, description="提醒消息")
    created_at: datetime = Field(..., description="创建时间")
    sent: bool = Field(..., description="是否已发送")

    class Config:
        from_attributes = True  # 允许从 ORM 模型创建
        json_schema_extra = {
            "example": {
                "id": 1,
                "symbol": "AAPL",
                "signal": "BUY",
                "price": 178.50,
                "message": "AAPL 当前信号: BUY",
                "created_at": "2024-10-13T15:30:00",
                "sent": False
            }
        }