def build_order_payload(symbol: str, side: str, order_type: str, quantity: str, price: str | None) -> dict:
    payload = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
        "newOrderRespType": "RESULT",
    }

    if order_type == "LIMIT":
        payload["price"] = price
        payload["timeInForce"] = "GTC"

    return payload


def extract_order_summary(response: dict) -> dict:
    return {
        "orderId": response.get("orderId"),
        "status": response.get("status"),
        "executedQty": response.get("executedQty"),
        "avgPrice": response.get("avgPrice"),
        "symbol": response.get("symbol"),
        "side": response.get("side"),
        "type": response.get("type"),
    }