"""
数据库连接配置

这个文件负责：
1. 创建数据库引擎（Engine）
2. 创建会话工厂（SessionLocal）
3. 提供 Base 类给所有模型继承
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取数据库 URL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/turtle_trading")

# 创建数据库引擎
# echo=True 会打印所有 SQL 语句，方便调试
engine = create_engine(
    DATABASE_URL,
    echo=True,  # 开发时设为 True，生产环境设为 False
    pool_pre_ping=True  # 检查连接是否有效
)

# 创建会话工厂
# 每次需要操作数据库时，用这个工厂创建一个新会话
SessionLocal = sessionmaker(
    autocommit=False,  # 不自动提交，手动控制事务
    autoflush=False,  # 不自动刷新，手动控制
    bind=engine  # 绑定到我们的引擎
)

# 创建基类
# 所有数据库模型都继承这个类
Base = declarative_base()


def get_db():
    """
    依赖注入函数

    用法：
        @app.get("/items/")
        def read_items(db: Session = Depends(get_db)):
            return db.query(Item).all()

    这个函数会：
    1. 创建一个数据库会话
    2. 在请求结束后自动关闭
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    初始化数据库

    创建所有定义的表
    只在第一次运行时需要调用
    """
    from app.database.models import Stock, AlertHistory  # 更新导入路径

    Base.metadata.create_all(bind=engine)
    print("✅ 数据库表创建成功！")


if __name__ == "__main__":
    # 测试连接
    print("测试数据库连接...")
    print(f"数据库 URL: {DATABASE_URL}")

    try:
        # 尝试连接
        connection = engine.connect()
        print("✅ 数据库连接成功！")
        connection.close()

        # 初始化表
        init_db()
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")