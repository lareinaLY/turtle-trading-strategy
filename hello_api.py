from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello/{name}")
def greet(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/stock/{symbol}")
def stock_info(symbol: str):
    return {
        "symbol": symbol.upper(),
        "message": f"将返回 {symbol} 的数据"
    }