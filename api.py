# ============================================================================
# api.py - 股票分析 API 主程序
# 整合 fetch_data, strategy, models 模块
# ============================================================================

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from models import (
    StockDataResponse,
    StrategyResponse,
    BatchAnalysisResponse,
    BatchAnalysisResult
)
from fetch_data import fetch_data
from strategy import turtle_strategy
from datetime import datetime
from history import get_history, search_by_symbol, get_statistics

# 创建 FastAPI 应用
app = FastAPI(
    title="海龟法则股票分析 API",
    description="提供股票数据获取、策略分析和批量监控的 REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS（允许前端访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发环境允许所有来源，生产环境要改成具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# 基础端点
# ============================================================================

@app.get("/", tags=["基础"])
def root():
    """API 根路径 - 欢迎页面"""
    return {
        "name": "海龟法则股票分析 API",
        "version": "1.0.0",
        "description": "提供股票数据和交易策略分析",
        "endpoints": {
            "文档": "/docs",
            "健康检查": "/health",
            "股票数据": "/api/stock/{symbol}",
            "策略分析": "/api/analyze/{symbol}",
            "批量分析": "/api/stocks/batch"
        },
        "author": "Turtle Trading System",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/health", tags=["基础"])
def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "Stock Analysis API",
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# 股票数据端点
# ============================================================================

@app.get("/api/stock/{symbol}", response_model=StockDataResponse, tags=["股票数据"])
def get_stock_data(
        symbol: str,
        period: str = Query("2mo", description="时间周期：1d, 5d, 1mo, 3mo, 6mo, 1y等")
):
    """
    获取股票的详细数据

    参数:
    - symbol: 股票代码（如 AAPL, TSLA, MSFT）
    - period: 数据时间范围（默认2个月）

    返回:
    - 股票当前价格
    - 20日最高价
    - 10日最低价
    - 平均价格
    - 数据点数等
    """

    try:
        # 获取股票数据
        data = fetch_data(symbol, period=period)

        # 检查数据是否有效
        if data is None or data.empty:
            raise HTTPException(
                status_code=404,
                detail=f"无法获取股票 {symbol.upper()} 的数据，请检查股票代码是否正确"
            )

        # 检查数据量是否足够
        if len(data) < 20:
            raise HTTPException(
                status_code=400,
                detail=f"数据不足：只有 {len(data)} 天数据，需要至少 20 天"
            )

        # 计算各项指标
        current_price = float(data['Close'].iloc[-1])
        high_20d = float(data['High'].iloc[-20:].max())
        low_10d = float(data['Low'].iloc[-10:].min())
        avg_price = float(data['Close'].mean())

        # 返回结构化数据
        return StockDataResponse(
            symbol=symbol.upper(),
            current_price=round(current_price, 2),
            high_20d=round(high_20d, 2),
            low_10d=round(low_10d, 2),
            avg_price=round(avg_price, 2),
            data_points=len(data),
            period=period,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        # 重新抛出 HTTP 异常
        raise

    except Exception as e:
        # 捕获其他所有错误
        raise HTTPException(
            status_code=500,
            detail=f"服务器内部错误: {str(e)}"
        )


# ============================================================================
# 策略分析端点
# ============================================================================

@app.get("/api/analyze/{symbol}", response_model=StrategyResponse, tags=["策略分析"])
def analyze_strategy(
        symbol: str,
        period: str = Query("2mo", description="数据时间范围"),
        entry_period: int = Query(20, description="入场周期（突破天数）"),
        exit_period: int = Query(10, description="出场周期（突破天数）")
):
    """
    分析股票的交易策略信号

    参数:
    - symbol: 股票代码
    - period: 数据时间范围
    - entry_period: 买入突破周期（默认20天）
    - exit_period: 卖出突破周期（默认10天）

    返回:
    - 交易信号（BUY/SELL/HOLD）
    - 当前价格和技术指标
    - 操作建议
    """

    try:
        # 获取数据
        data = fetch_data(symbol, period=period)

        if data is None or data.empty:
            raise HTTPException(
                status_code=404,
                detail=f"无法获取股票 {symbol.upper()} 的数据"
            )

        if len(data) < entry_period:
            raise HTTPException(
                status_code=400,
                detail=f"数据不足：只有 {len(data)} 天，需要至少 {entry_period} 天"
            )

        # 执行策略分析
        signal = turtle_strategy(data, entry_period=entry_period, exit_period=exit_period)

        # 提取价格信息
        current_price = float(data['Close'].iloc[-1])
        high_period = float(data['High'].iloc[-entry_period:].max())
        low_period = float(data['Low'].iloc[-exit_period:].min())

        # 生成操作建议
        recommendations = {
            "BUY": f"价格突破{entry_period}日最高点，建议买入",
            "SELL": f"价格跌破{exit_period}日最低点，建议卖出",
            "HOLD": f"价格在 ${low_period:.2f} - ${high_period:.2f} 通道内，建议持有观望"
        }

        return StrategyResponse(
            symbol=symbol.upper(),
            signal=signal,
            current_price=round(current_price, 2),
            high_20d=round(high_period, 2),
            low_10d=round(low_period, 2),
            recommendation=recommendations.get(signal, "无建议"),
            analysis_time=datetime.now().isoformat()
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"策略分析失败: {str(e)}"
        )


# ============================================================================
# 批量分析端点
# ============================================================================

@app.get("/api/stocks/batch", response_model=BatchAnalysisResponse, tags=["批量操作"])
def analyze_multiple_stocks(
        symbols: str = Query(..., description="股票代码列表，逗号分隔", example="AAPL,TSLA,MSFT")
):
    """
    批量分析多只股票

    参数:
    - symbols: 股票代码列表，用逗号分隔（如：AAPL,TSLA,MSFT）

    返回:
    - 每只股票的分析结果
    - 成功和失败的统计
    """

    try:
        # 解析股票代码列表
        symbol_list = [s.strip().upper() for s in symbols.split(',') if s.strip()]

        if not symbol_list:
            raise HTTPException(
                status_code=400,
                detail="股票代码列表不能为空"
            )

        if len(symbol_list) > 10:
            raise HTTPException(
                status_code=400,
                detail="一次最多分析10只股票"
            )

        results = []

        # 逐个分析股票
        for symbol in symbol_list:
            try:
                # 获取数据
                data = fetch_data(symbol, period="2mo")

                if data is not None and not data.empty and len(data) >= 20:
                    # 执行策略
                    signal = turtle_strategy(data)
                    current_price = float(data['Close'].iloc[-1])

                    results.append(
                        BatchAnalysisResult(
                            symbol=symbol,
                            signal=signal,
                            current_price=round(current_price, 2),
                            status="success",
                            error=None
                        )
                    )
                else:
                    results.append(
                        BatchAnalysisResult(
                            symbol=symbol,
                            signal=None,
                            current_price=None,
                            status="failed",
                            error="无法获取数据或数据不足"
                        )
                    )

            except Exception as e:
                results.append(
                    BatchAnalysisResult(
                        symbol=symbol,
                        signal=None,
                        current_price=None,
                        status="failed",
                        error=str(e)
                    )
                )

        return BatchAnalysisResponse(
            total=len(symbol_list),
            results=results,
            timestamp=datetime.now().isoformat()
        )

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"批量分析失败: {str(e)}"
        )


# ============================================================================
# 获取历史数据端点
# ============================================================================
@app.get("/api/history", tags=["历史记录"])
def get_analysis_history(limit: int = Query(10, ge=1, le=100)):
    """
    获取分析历史记录

    参数:
    - limit: 返回最近N条记录
    """
    history = get_history(limit)
    return {
        "count": len(history),
        "records": history
    }


@app.get("/api/history/{symbol}", tags=["历史记录"])
def get_symbol_history(symbol: str):
    """
    获取特定股票的历史记录

    参数:
    - symbol: 股票代码
    """
    records = search_by_symbol(symbol.upper())
    return {
        "symbol": symbol.upper(),
        "count": len(records),
        "records": records
    }


@app.get("/api/statistics", tags=["统计信息"])
def get_analysis_statistics():
    """获取分析统计信息"""
    stats = get_statistics()
    return stats


# ============================================================================
# 测试运行说明
# ============================================================================

if __name__ == "__main__":
    print("🚀 API 服务器启动说明")
    print("=" * 60)
    print("\n运行命令：")
    print("  uvicorn api:app --reload")
    print("\n访问地址：")
    print("  主页：http://localhost:8000")
    print("  文档：http://localhost:8000/docs")
    print("  健康检查：http://localhost:8000/health")
    print("\n可用端点：")
    print("  GET  /api/stock/AAPL")
    print("  GET  /api/analyze/TSLA")
    print("  GET  /api/stocks/batch?symbols=AAPL,TSLA,MSFT")
    print("=" * 60)