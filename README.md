# Binance Futures Testnet Trading Bot

A simplified Python trading bot for Binance Futures Testnet (USDT-M) built as part of an application task.

## Features

- Place **MARKET** and **LIMIT** orders on Binance Futures Testnet
- Supports both **BUY** and **SELL**
- CLI-based input using `argparse`
- Input validation for symbol, side, order type, quantity, and price
- Structured code with separate client/API and CLI layers
- Logging of API requests, responses, and errors to log files
- Exception handling for validation errors, API errors, and network failures

## Project Structure

```text
trading_bot/
  bot/
    __init__.py
    client.py
    orders.py
    validators.py
    logging_config.py
    exceptions.py
  cli.py
  test_ping.py
  test_signed.py
  README.md
  requirements.txt
  logs/
```

## Requirements

- Python 3.10+
- Binance Futures Testnet / Demo Trading account
- Testnet API key and secret

## Setup

- Clone the repository:

```bash
git clone https://github.com/Sanjana272621/trading_bot.git
cd trading_bot
```

- Create and activate a virtual environment:
Windows
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux
```bash
python -m venv .venv
source .venv/bin/activate
```

- Install Dependencies
```bash
pip install -r requirements.txt
```

- Create a .env file in the project root:
```env
BINANCE_API_KEY=your_testnet_api_key
BINANCE_API_SECRET=your_testnet_api_secret
BINANCE_BASE_URL=https://testnet.binancefuture.com
```

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create environment variables

Create a `.env` file in the project root with the following values:

```bash
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_secret_key  
BINANCE_BASE_URL=https://testnet.binancefuture.com
```
### 3. Test API connectivity

```bash
python test_ping.py
```

This checks that the Binance Futures Testnet endpoint is reachable.

### 4. Test authenticated API access

```bash
python test_signed.py
```

This verifies that the API key, API secret, and request signing are working correctly.

### 5. Place a MARKET order

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.002
```

This prints the order request summary, order response details, and a success or failure message.

### 6. Place a LIMIT order

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 150000
```

This places a limit order on the Binance Futures Testnet.

## CLI Arguments

| Argument | Description |
|---|---|
| `--symbol` | Trading symbol, for example `BTCUSDT` |
| `--side` | `BUY` or `SELL` |
| `--type` | `MARKET` or `LIMIT` |
| `--quantity` | Order quantity |
| `--price` | Required for LIMIT orders |

## Logging

All API requests, responses, and errors are logged.

Default log file: `logs/trading_bot.log`

Sample submitted logs:

- `logs/market_order.log`
- `logs/limit_order.log`

## Assumptions

- Only **USDT-M Futures Testnet** is supported
- Only **MARKET** and **LIMIT** orders are implemented
- LIMIT orders use `timeInForce=GTC`
- Binance minimum notional rules apply, so very small quantities may be rejected

## Bonus

Implemented bonus: **Enhanced CLI UX**

This includes:
- clear validation messages
- structured order summaries
- readable success and failure output