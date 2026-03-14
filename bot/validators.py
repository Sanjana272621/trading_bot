from decimal import Decimal, InvalidOperation
from .exceptions import ValidationError


VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}


def normalize_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not symbol or not symbol.isalnum():
        raise ValidationError("Symbol must be a non-empty alphanumeric value like BTCUSDT.")
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError("Side must be BUY or SELL.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError("Order type must be MARKET or LIMIT.")
    return order_type


def validate_positive_decimal(value: str, field_name: str) -> str:
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError):
        raise ValidationError(f"{field_name} must be a valid number.")

    if dec <= 0:
        raise ValidationError(f"{field_name} must be greater than 0.")

    # Return as clean string to avoid float precision issues
    return format(dec.normalize(), "f")


def validate_inputs(symbol: str, side: str, order_type: str, quantity: str, price: str | None):
    symbol = normalize_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity = validate_positive_decimal(quantity, "Quantity")

    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        price = validate_positive_decimal(price, "Price")
    else:
        if price is not None:
            # not fatal, but better to reject cleanly
            raise ValidationError("Price should not be provided for MARKET orders.")

    return {
        "symbol": symbol,
        "side": side,
        "order_type": order_type,
        "quantity": quantity,
        "price": price,
    }