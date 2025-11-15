"""
API 路由 - 集成数据库版本

这个文件定义了所有的 API 端点，现在所有操作都会保存到数据库
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from datetime import datetime
import json

# 更新导入路径（使用新的模块化结构）
from app.schemas.stock import StockRequest, StockResponse, HistoryResponse
from app.services.fetch_data import fetch_data
from app.services.strategy import turtle_strategy
from app.database.connection import get_db
from app.database.models import Stock, AlertHistory

router = APIRouter()

@router.get("/")
def root():
    """根路径 - API 信息"""
    return {
        "message": "海龟交易策略 API",
        "version": "2.0.0",
        "features": ["数据库存储", "历史查询", "股票管理"],
        "endpoints": {
            "分析股票": "POST /analyze",
            "查询历史": "GET /history",
            "股票列表": "GET /stocks",
            "API文档": "/docs"
        }
    }


@router.post("/analyze", response_model=StockResponse)
def analyze_stock(
        request: StockRequest,
        db: Session = Depends(get_db)
):
    """
    分析股票并保存结果到数据库

    参数:
        request: 股票分析请求（symbol, period等）
        db: 数据库会话（自动注入）

    返回:
        分析结果，包括信号、价格等信息
    """
    try:
        # 自动转大写，用户友好
        symbol = request.symbol.upper()

        # 1. 获取股票数据（使用你原来的函数）
        data = fetch_data(
            symbol,
            request.period  # 只传两个参数
        )

        if data is None or data.empty:  # 先检查是否是 None
            raise HTTPException(
                status_code=404,
                detail=f"无法获取 {symbol} 的数据，请检查股票代码是否正确"
            )

        # 2. 运行海龟策略（只返回信号字符串）
        signal = turtle_strategy(
            data,
            request.entry_period,
            request.exit_period
        )

        # 3. 手动计算需要的价格信息
        current_price = float(data['Close'].iloc[-1])
        high_20d = float(data['High'].iloc[-request.entry_period:].max())
        low_10d = float(data['Low'].iloc[-request.exit_period:].min())

        # 4. 更新或创建股票记录
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()

        if stock:
            # 更新现有股票
            stock.current_price = current_price
            stock.last_updated = datetime.now()
        else:
            # 创建新股票
            stock = Stock(
                symbol=symbol,
                name=symbol,  # 可以后续从 API 获取完整名称
                current_price=current_price,
                is_active=True
            )
            db.add(stock)

        # 5. 保存提醒历史
        alert = AlertHistory(
            symbol=symbol,
            signal=signal,  # 直接使用字符串
            price=current_price,
            strategy_params=json.dumps({
                'entry_period': request.entry_period,
                'exit_period': request.exit_period,
                'entry_price': high_20d,
                'exit_price': low_10d
            }),
            message=f"{symbol} 当前信号: {signal}",
            sent=False  # 还没发送邮件
        )
        db.add(alert)

        # 6. 提交到数据库
        db.commit()
        db.refresh(stock)
        db.refresh(alert)

        # 7. 返回结果
        return StockResponse(
            symbol=symbol,
            current_price=current_price,
            signal=signal,
            entry_price=high_20d,
            exit_price=low_10d,
            high_20d=high_20d,
            low_10d=low_10d,
            timestamp=datetime.now(),
            alert_id=alert.id  # 返回提醒记录的 ID
        )

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()  # 出错回滚
        raise HTTPException(status_code=500, detail=f"分析失败: {str(e)}")


@router.get("/history", response_model=List[HistoryResponse])
def get_history(
        symbol: Optional[str] = None,
        limit: int = 10,
        db: Session = Depends(get_db)
):
    """
    查询历史提醒记录

    参数:
        symbol: 股票代码（可选，不提供则查询所有，自动转大写）
        limit: 返回记录数量（默认10条）
        db: 数据库会话（自动注入）

    返回:
        历史记录列表
    """
    try:
        # 构建查询
        query = db.query(AlertHistory)

        # 如果指定了股票代码，添加过滤（自动转大写）
        if symbol:
            symbol = symbol.upper()
            query = query.filter(AlertHistory.symbol == symbol)

        # 按时间倒序，取最新的 N 条
        alerts = query.order_by(AlertHistory.created_at.desc()).limit(limit).all()

        # 转换为响应格式
        return [
            HistoryResponse(
                id=alert.id,
                symbol=alert.symbol,
                signal=alert.signal,
                price=alert.price,
                message=alert.message,
                created_at=alert.created_at,
                sent=alert.sent
            )
            for alert in alerts
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/stocks")
def get_stocks(
        active_only: bool = True,
        db: Session = Depends(get_db)
):
    """
    获取所有股票列表

    参数:
        active_only: 只返回活跃的股票（默认 True）
        db: 数据库会话（自动注入）

    返回:
        股票列表
    """
    try:
        query = db.query(Stock)

        if active_only:
            query = query.filter(Stock.is_active == True)

        stocks = query.order_by(Stock.symbol).all()

        return {
            "total": len(stocks),
            "stocks": [
                {
                    "symbol": stock.symbol,
                    "name": stock.name,
                    "current_price": stock.current_price,
                    "last_updated": stock.last_updated,
                    "is_active": stock.is_active
                }
                for stock in stocks
            ]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.get("/stocks/{symbol}")
def get_stock_detail(
        symbol: str,
        db: Session = Depends(get_db)
):
    """
    获取单个股票的详细信息

    参数:
        symbol: 股票代码（自动转大写）
        db: 数据库会话（自动注入）

    返回:
        股票详情 + 最近的提醒记录
    """
    try:
        # 自动转大写，用户友好
        symbol = symbol.upper()

        # 查找股票
        stock = db.query(Stock).filter(Stock.symbol == symbol).first()

        if not stock:
            raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")

        # 查询最近 5 条提醒
        recent_alerts = db.query(AlertHistory) \
            .filter(AlertHistory.symbol == symbol) \
            .order_by(AlertHistory.created_at.desc()) \
            .limit(5) \
            .all()

        return {
            "stock": {
                "symbol": stock.symbol,
                "name": stock.name,
                "current_price": stock.current_price,
                "last_updated": stock.last_updated,
                "is_active": stock.is_active
            },
            "recent_alerts": [
                {
                    "signal": alert.signal,
                    "price": alert.price,
                    "created_at": alert.created_at,
                    "sent": alert.sent
                }
                for alert in recent_alerts
            ]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")


@router.delete("/stocks/{symbol}")
def delete_stock(
        symbol: str,
        db: Session = Depends(get_db)
):
    """
    软删除股票（标记为不活跃）

    参数:
        symbol: 股票代码（自动转大写）
        db: 数据库会话（自动注入）

    返回:
        操作结果
    """
    try:
        # 自动转大写，用户友好
        symbol = symbol.upper()

        stock = db.query(Stock).filter(Stock.symbol == symbol).first()

        if not stock:
            raise HTTPException(status_code=404, detail=f"股票 {symbol} 不存在")

        # 软删除
        stock.is_active = False
        db.commit()

        return {
            "message": f"股票 {symbol} 已标记为不活跃",
            "symbol": symbol,
            "is_active": False
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    健康检查 - 检查 API 和数据库是否正常

    返回:
        系统状态
    """
    try:
        # 测试数据库连接（修复 SQL 警告）
        db.execute(text("SELECT 1"))

        # 统计数据
        stock_count = db.query(Stock).count()
        alert_count = db.query(AlertHistory).count()

        return {
            "status": "healthy",
            "database": "connected",
            "statistics": {
                "total_stocks": stock_count,
                "total_alerts": alert_count
            },
            "timestamp": datetime.now()
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.now()
        }