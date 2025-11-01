"""
FastAPI 应用入口文件

这是整个应用的启动入口
"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径（重要！）
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import uvicorn

if __name__ == "__main__":
    print("🐢 海龟交易策略 API 服务器启动中...")
    print("📖 API 文档: http://localhost:8000/docs")
    print("🔧 ReDoc: http://localhost:8000/redoc")
    print("\n按 Ctrl+C 停止服务器\n")

    uvicorn.run(
        "app.api.routes:app",  # 指向 app 对象的路径
        host="0.0.0.0",
        port=8000,
        reload=True  # 开发模式：代码改动自动重启
    )