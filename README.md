# Trade Simulator – Real-Time Market Impact and Cost Estimation

A **high-performance trade simulator** designed to estimate transaction costs, market impact, and slippage using **real-time cryptocurrency market data**.  
This project connects to WebSocket endpoints streaming full **L2 orderbook data** from exchanges like **OKX**, allowing users to simulate trades and analyze their cost impact.

---

## Objective
To create a **real-time trading simulator** that:
- Connects to a live market feed using WebSockets  
- Processes L2 orderbook data in real time  
- Estimates **slippage**, **fees**, and **market impact** using quantitative models  
- Benchmarks system **latency and performance** under real streaming conditions  

---

## Core Features

### User Interface
- **Left Panel** – Input Parameters  
  - Exchange: `OKX`  
  - Spot Asset: any available asset  
  - Order Type: `market`  
  - Quantity: ~$100 equivalent  
  - Volatility parameter (from exchange data)  
  - Fee Tier (as per OKX documentation)

- **Right Panel** – Output Metrics  
  - Expected **Slippage** *(Linear or Quantile Regression)*  
  - Expected **Fees** *(Rule-Based Fee Model)*  
  - Expected **Market Impact** *(Almgren–Chriss Model)*  
  - **Net Cost** = Slippage + Fees + Market Impact  
  - **Maker/Taker Proportion** *(Logistic Regression)*  
  - **Internal Latency** (processing time per tick)

---

## WebSocket Implementation
**WebSocket Endpoint:**
wss://ws.gomarket-cpp.goquant.io/ws/l2-orderbook/okx/BTC-USDT-SWAP


**Sample Response:**
```json
{
  "timestamp": "2025-05-04T10:39:13Z",
  "exchange": "OKX",
  "symbol": "BTC-USDT-SWAP",
  "asks": [
    ["95445.5", "9.06"],
    ["95448", "2.05"]
  ],
  "bids": [
    ["95445.4", "1104.23"],
    ["95445.3", "0.02"]
  ]
}

