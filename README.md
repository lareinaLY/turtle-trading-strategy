# 🐢 Turtle Trading Strategy - AI-Powered Stock Analysis Platform

> A full-stack web application that provides intelligent stock monitoring and trading signals based on the Turtle Trading Strategy, with AI-powered price prediction (Coming Soon).

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)

---

## 🎯 Project Overview

This project implements a **complete full-stack trading analysis system** that combines classic algorithmic trading strategies with modern web technologies and AI capabilities. It automatically monitors stock prices, generates trading signals, and sends real-time notifications to users.

**Key Features:**
- 📊 Real-time stock data fetching via yfinance API
- 🐢 Turtle Trading Strategy implementation with customizable parameters
- 📧 Automated email notifications for buy/sell signals
- 🗄️ PostgreSQL database for persistent data storage
- 🚀 RESTful API built with FastAPI
- 🤖 AI-powered price prediction (Planned - Week 8-9)

---

## 🏗️ Project Architecture

```
turtle-trading-strategy/
│
├── 📁 app/                          # Main application directory
│   ├── __init__.py                 # App package initialization
│   ├── main.py                     # Application entry point
│   │
│   ├── 📁 api/                     # API Layer
│   │   ├── __init__.py
│   │   └── routes.py               # FastAPI endpoints and request handlers
│   │
│   ├── 📁 services/                # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── fetch_data.py          # Market data fetching (yfinance)
│   │   ├── strategy.py            # Turtle Trading Strategy implementation
│   │   ├── notification.py        # Email notification system
│   │   └── history.py             # Historical data tracking
│   │
│   ├── 📁 database/                # Data Access Layer
│   │   ├── __init__.py
│   │   ├── connection.py          # Database connection & session management
│   │   └── models.py              # SQLAlchemy ORM models
│   │
│   ├── 📁 schemas/                 # Data Validation Layer
│   │   ├── __init__.py
│   │   └── stock.py               # Pydantic models for API validation
│   │
│   └── 📁 core/                    # Core Configuration
│       ├── __init__.py
│       └── config.py              # Application configuration
│
├── 📁 scripts/                     # Utility Scripts
│   ├── test_database.py           # Database integration tests
│   └── check_gitignore.sh         # Pre-commit .gitignore validator
│
├── 📁 tests/                       # Test Suite
│   ├── __init__.py
│   └── test_api.py                # API endpoint tests
│
├── 📁 data/                        # Data files (gitignored)
│   └── analysis_history.json      # Historical analysis records
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment variables template
├── 📄 .gitignore                   # Git ignore rules
└── 📄 README.md                    # Project documentation
```

### Architecture Layers

```
┌─────────────────────────────────────────────┐
│           API Layer (FastAPI)               │
│  - RESTful endpoints                        │
│  - Request/Response validation              │
│  - Error handling                           │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│        Business Logic Layer                 │
│  - Trading strategy engine                  │
│  - Data fetching & processing               │
│  - Notification service                     │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Data Access Layer (SQLAlchemy)         │
│  - ORM models                               │
│  - Database operations (CRUD)               │
│  - Session management                       │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│         PostgreSQL Database                 │
│  - stocks, alert_history                    │
│  - users, subscriptions                     │
└─────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### **Backend**
- **Framework:** FastAPI (Python 3.11+)
- **ORM:** SQLAlchemy 2.0+
- **Database:** PostgreSQL 15+
- **Data Analysis:** pandas, numpy
- **API Testing:** pytest

### **Data & Strategy**
- **Market Data:** yfinance (Yahoo Finance API)
- **Trading Strategy:** Turtle Trading Rules (20-day breakout)
- **Notifications:** SMTP email integration

### **Planned Enhancements**
- **Frontend:** React 18, TypeScript, Recharts
- **ML/AI:** TensorFlow/Keras (LSTM), Prophet
- **DevOps:** Docker, GitHub Actions CI/CD
- **Authentication:** JWT

---

## 📊 Current Progress

### ✅ Phase 1: Core Backend (Completed)
- [x] **Trading Strategy Engine**
  - Turtle Trading Rules implementation
  - Customizable period parameters
  - Historical data analysis with pandas
  
- [x] **RESTful API**
  - FastAPI framework with async support
  - Pydantic schemas for data validation
  - Comprehensive error handling and logging
  
- [x] **Database Layer**
  - PostgreSQL with SQLAlchemy ORM
  - Normalized schema design (4 tables)
  - Complete CRUD operations
  - Migration support with Alembic
  
- [x] **Notification System**
  - SMTP email integration
  - HTML template rendering
  - Asynchronous delivery

### 🚧 Phase 2: Frontend & Authentication (In Progress)
- [ ] React-based dashboard
- [ ] User authentication with JWT
- [ ] Real-time data visualization
- [ ] Personalized watchlist management

### 📋 Phase 3: ML Integration (Planned)
- [ ] LSTM neural network for price prediction
- [ ] Strategy backtesting framework
- [ ] Multi-strategy comparison
- [ ] Risk analytics dashboard

---

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.11+
PostgreSQL 15+
pip (Python package manager)
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/lareinalY/turtle-trading-strategy.git
cd turtle-trading-strategy
```

2. **Set up virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env with your configurations
```

Required `.env` variables:
```bash
# Database
DATABASE_URL=postgresql://localhost/turtle_trading

# Email (optional, for notifications)
FROM_EMAIL=your_email@gmail.com
TO_EMAIL=recipient@gmail.com
EMAIL_PASSWORD=your_app_password

# Strategy parameters
ENTRY_PERIOD=20
EXIT_PERIOD=10
```

5. **Set up database**
```bash
# Create database
createdb turtle_trading

# Run tests to verify setup
python test_database.py
```

6. **Start the server**
```bash
python main.py
```

Server will run at `http://localhost:8000`

---

## 📖 API Documentation

Once the server is running, access interactive API docs at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

#### Analyze Stock
```http
POST /analyze
Content-Type: application/json

{
  "symbol": "AAPL",
  "period": "2mo",
  "entry_period": 20,
  "exit_period": 10
}
```

Response:
```json
{
  "symbol": "AAPL",
  "current_price": 178.50,
  "signal": "BUY",
  "entry_price": 175.20,
  "exit_price": 172.80,
  "timestamp": "2024-10-13T15:30:00Z"
}
```

#### Get History
```http
GET /history?symbol=AAPL&limit=10
```

---

## 🗄️ Database Schema

### Tables

**stocks**
- Primary table for stock information
- Stores current prices and metadata
- Auto-updated timestamps

**alert_history**
- Logs all generated trading signals
- Tracks notification status
- Stores strategy parameters used

**users**
- User authentication and profile data
- Encrypted password storage

**subscriptions**
- User watchlist management
- Custom strategy parameters per stock

---

## 🧪 Testing

Run comprehensive test suite:
```bash
# Database tests
python test_database.py

# API tests
pytest tests/

# Coverage report
pytest --cov=. tests/
```

---

## 🎓 Turtle Trading Strategy

The [Turtle Trading Strategy](https://en.wikipedia.org/wiki/Turtle_trading) is a trend-following system developed in the 1980s. 

**Key Rules:**
- **Entry Signal:** Buy when price breaks above 20-day high
- **Exit Signal:** Sell when price breaks below 10-day low
- **Position Sizing:** Risk-based position calculation
- **Stop Loss:** 2 ATR (Average True Range)

**Implementation:**
```python
def turtle_strategy(data: pd.DataFrame, entry_period=20, exit_period=10):
    entry_price = data['High'].rolling(entry_period).max()
    exit_price = data['Low'].rolling(exit_period).min()
    
    if current_price >= entry_price:
        return "BUY"
    elif current_price <= exit_price:
        return "SELL"
    return "HOLD"
```

---

## 🔮 Future Enhancements

### Advanced ML Features
- **Price Prediction:** LSTM neural network for multi-day forecasts
- **Strategy Optimization:** Genetic algorithms for parameter tuning
- **Sentiment Analysis:** News and social media impact analysis
- **Risk Management:** Portfolio optimization with Modern Portfolio Theory

### Technical Improvements
- WebSocket support for real-time updates
- Caching layer with Redis
- Kubernetes deployment
- Multi-timeframe analysis

---

## 📂 Project Structure

```
turtle-trading-strategy/
│
├── 📁 app/                          # Main application package
│   ├── __init__.py                 # Package initialization
│   ├── main.py                     # Application entry point
│   │
│   ├── 📁 api/                     # API Layer
│   │   ├── __init__.py
│   │   └── routes.py               # FastAPI endpoints
│   │
│   ├── 📁 services/                # Business Logic Layer
│   │   ├── __init__.py
│   │   ├── fetch_data.py          # Market data fetching
│   │   ├── strategy.py            # Trading strategy logic
│   │   ├── notification.py        # Email notifications
│   │   └── history.py             # Historical tracking
│   │
│   ├── 📁 database/                # Data Access Layer
│   │   ├── __init__.py
│   │   ├── connection.py          # DB connection & session
│   │   └── models.py              # SQLAlchemy ORM models
│   │
│   ├── 📁 schemas/                 # Data Validation Layer
│   │   ├── __init__.py
│   │   └── stock.py               # Pydantic models
│   │
│   └── 📁 core/                    # Core Configuration
│       ├── __init__.py
│       └── config.py              # App configuration
│
├── 📁 scripts/                     # Utility scripts
│   ├── test_database.py           # Database tests
│   └── check_gitignore.sh         # Pre-commit checker
│
├── 📁 tests/                       # Test suite
│   ├── __init__.py
│   └── test_api.py                # API tests
│
├── 📁 data/                        # Data files (gitignored)
│   └── analysis_history.json      # Historical records
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .gitignore                   # Git ignore rules
└── 📄 README.md                    # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

not yet

---

## 👤 Author

**YingLu**
- GitHub: [@lareinalY](https://github.com/lareinalY)
- Email: lareina6145@gmail.com

---

## 🙏 Acknowledgments

- Turtle Trading methodology by Richard Dennis and William Eckhardt
- [FastAPI](https://fastapi.tiangolo.com/) for the excellent web framework
- [yfinance](https://github.com/ranaroussi/yfinance) for market data access
- Northeastern University CS Align Program

---

## 📈 Development Roadmap

```
Phase 1: Backend Infrastructure        ✅ Complete
  └── Trading strategy engine
  └── RESTful API (FastAPI)
  └── Database layer (PostgreSQL + SQLAlchemy)
  └── Email notification system

Phase 2: Frontend & User Management    🚧 In Progress
  └── React dashboard
  └── JWT authentication
  └── Real-time data visualization
  └── User watchlist features

Phase 3: ML & Advanced Analytics       📋 Planned
  └── LSTM price prediction
  └── Strategy backtesting
  └── Risk management tools
  └── Performance optimization
```

**Project Status:** Phase 1 Complete, actively developing Phase 2  
**Last Updated:** October 2024