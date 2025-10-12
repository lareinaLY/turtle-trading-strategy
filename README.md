# 🐢 海龟法则股票分析系统

基于海龟法则的智能股票监控和交易信号系统

## 🎯 功能特点

- 📊 实时股票数据获取
- 🐢 海龟法则策略分析
- 📧 邮件通知（买入/卖出信号）
- 🌐 REST API 接口
- 📜 历史记录追踪
- 📈 批量股票分析

## 🛠️ 技术栈

- **后端**: FastAPI, Python 3.11+
- **数据**: yfinance, pandas
- **测试**: pytest
- **数据模型**: Pydantic

## 📦 安装
```bash
# 1. 克隆仓库
git clone <your-repo-url>
cd project1_turtle_strategy

# 2. 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置邮箱（可选）
cp .env.example .env
# 编辑 .env 文件，填写你的邮箱配置