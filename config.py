# config.py - 配置管理

import os
from pathlib import Path


class Config:
    """应用配置"""

    # 邮件配置
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    FROM_EMAIL = os.getenv("FROM_EMAIL", "lareina6145@gmail.com")
    TO_EMAIL = os.getenv("TO_EMAIL", "lareina6145@gmail.com")
    EMAIL_PASSWORD = os.getenv("jyzwmckgordxikab")

    # 股票分析配置
    DEFAULT_PERIOD = "2mo"
    ENTRY_PERIOD = 20
    EXIT_PERIOD = 10

    # 历史记录配置
    HISTORY_FILE = "data/analysis_history.json"
    MAX_HISTORY = 1000  # 最多保存1000条

    # API 配置
    API_HOST = "0.0.0.0"
    API_PORT = 8000

    @classmethod
    def load_from_env(cls):
        """从 .env 文件加载配置"""
        env_file = Path(".env")
        if env_file.exists():
            with open(env_file) as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        os.environ[key] = value


# 使用
config = Config()