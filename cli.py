import argparse
import os
import sys

from dotenv import load_dotenv

from bot.client import BinanceFuturesClient
from bot.exceptions import BinanceAPIError, NetworkError, ValidationError
from bot.logging_config import setup_logger
from bot.orders import build_order_payload, extract_order_summary
from bot.validators import validate_inputs


def parse_args():
    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")

    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Price required for LIMIT orders")

    return parser.parse_args()


def main():
    load_dotenv()
    logger = setup_logger()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BINANCE_BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        print("Error: BINANCE_API_KEY and BINANCE_API_SECRET must be set in environment variables.")
        sys.exit(1)

    args = parse_args()

    try:
        validated = validate_inputs(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )

        payload = build_order_payload(
            symbol=validated["symbol"],
            side=validated["side"],
            order_type=validated["order_type"],
            quantity=validated["quantity"],
            price=validated["price"],
        )

        print("\n=== ORDER REQUEST SUMMARY ===")
        for k, v in payload.items():
            print(f"{k}: {v}")

        client = BinanceFuturesClient(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            logger=logger,
        )

        response = client.place_order(payload)
        summary = extract_order_summary(response)

        print("\n=== ORDER RESPONSE DETAILS ===")
        for k, v in summary.items():
            print(f"{k}: {v}")

        print("\nSUCCESS: Order placed successfully.")

    except ValidationError as exc:
        logger.error("Validation error: %s", exc)
        print(f"\nFAILED: Validation error: {exc}")
        sys.exit(2)

    except BinanceAPIError as exc:
        logger.error("Binance API error: %s", exc)
        print(f"\nFAILED: Binance API error: {exc}")
        sys.exit(3)

    except NetworkError as exc:
        logger.error("Network error: %s", exc)
        print(f"\nFAILED: Network error: {exc}")
        sys.exit(4)

    except Exception as exc:
        logger.exception("Unexpected error")
        print(f"\nFAILED: Unexpected error: {exc}")
        sys.exit(5)


if __name__ == "__main__":
    main()