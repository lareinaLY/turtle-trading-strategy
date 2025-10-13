"""
数据库模型定义

定义数据库表的结构，就像建筑图纸一样
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, Boolean
from sqlalchemy.sql import func
from database.connection import Base


class Stock(Base):
    """
    股票表 - 存储股票的基本信息和当前价格

    类比：这是一个"商品目录"
    """
    __tablename__ = "stocks"  # 表名

    # 主键 - 每条记录的唯一标识
    id = Column(Integer, primary_key=True, index=True)

    # 股票代码（如 AAPL, TSLA）
    symbol = Column(String(10), unique=True, index=True, nullable=False)

    # 公司名称（可选）
    name = Column(String(100), nullable=True)

    # 当前价格
    current_price = Column(Float, nullable=True)

    # 最后更新时间（自动设置）
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # 是否活跃（用于软删除）
    is_active = Column(Boolean, default=True)

    def __repr__(self):
        """打印对象时显示的内容"""
        return f"<Stock(symbol='{self.symbol}', price={self.current_price})>"


class AlertHistory(Base):
    """
    提醒历史表 - 记录所有发送过的提醒

    类比：这是一个"订单历史"
    """
    __tablename__ = "alert_history"

    # 主键
    id = Column(Integer, primary_key=True, index=True)

    # 股票代码
    symbol = Column(String(10), index=True, nullable=False)

    # 信号类型（BUY, SELL, HOLD）
    signal = Column(String(10), nullable=False)

    # 触发价格
    price = Column(Float, nullable=False)

    # 策略参数（存储为 JSON 字符串）
    strategy_params = Column(Text, nullable=True)

    # 提醒内容
    message = Column(Text, nullable=True)

    # 是否已发送
    sent = Column(Boolean, default=False)

    # 创建时间（自动设置，不可修改）
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<AlertHistory(symbol='{self.symbol}', signal='{self.signal}', price={self.price})>"


class User(Base):
    """
    用户表 - 为 Week 6-7 的用户系统预留

    现在先定义，但不使用
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}')>"


class Subscription(Base):
    """
    订阅表 - 用户订阅的股票（Week 6-7 使用）
    """
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)  # 将来会加外键
    symbol = Column(String(10), nullable=False)
    strategy = Column(String(20), default="turtle")  # 策略名称
    period = Column(Integer, default=20)  # 策略参数
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Subscription(user_id={self.user_id}, symbol='{self.symbol}')>"