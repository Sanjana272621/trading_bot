class ValidationError(Exception):
    """Raised when CLI input is invalid."""


class BinanceAPIError(Exception):
    """Raised when Binance returns an API error."""


class NetworkError(Exception):
    """Raised when a network/transport error occurs."""