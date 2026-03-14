import hashlib
import hmac
import time
from urllib.parse import urlencode

import requests

from .exceptions import BinanceAPIError, NetworkError


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str, logger, timeout: int = 10):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url.rstrip("/")
        self.logger = logger
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key
        })

    def _sign_params(self, params: dict) -> str:
        query_string = urlencode(params, doseq=True)
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return signature

    def _send_signed_request(self, method: str, path: str, params: dict) -> dict:
        url = f"{self.base_url}{path}"
        params = params.copy()
        params["timestamp"] = int(time.time() * 1000)

        signature = self._sign_params(params)
        params["signature"] = signature

        self.logger.info("REQUEST %s %s | params=%s", method, url, {k: v for k, v in params.items() if k != "signature"})

        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            self.logger.exception("Network error during request")
            raise NetworkError(f"Network error: {exc}") from exc

        text_preview = response.text[:1000]
        self.logger.info(
            "RESPONSE %s | status_code=%s | body=%s",
            url,
            response.status_code,
            text_preview,
        )

        try:
            data = response.json()
        except ValueError:
            self.logger.exception("Non-JSON response received")
            raise BinanceAPIError(f"Non-JSON response from Binance: {text_preview}")

        if response.status_code >= 400:
            msg = data.get("msg", "Unknown Binance API error")
            code = data.get("code", "N/A")
            self.logger.error("Binance API error | code=%s | msg=%s", code, msg)
            raise BinanceAPIError(f"Binance API error {code}: {msg}")

        return data

    def place_order(self, payload: dict) -> dict:
        return self._send_signed_request("POST", "/fapi/v1/order", payload)