import requests
import logging
import time


def fetch_prices(coins, retries=3, backoff_factor=2):
    url = "https://api.coingecko.com/api/v3/coins/markets"

    params = {
        "vs_currency": "usd",
        "ids": ",".join(coins),
        "price_change_percentage": "24h"
    }

    attempt = 0

    while attempt < retries:
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            prices = {}

            for coin in data:
                prices[coin["id"]] = {
                    "name": coin["name"],
                    "current_price": coin["current_price"],
                    "price_change_24h": coin.get("price_change_percentage_24h", 0)
                }

            return prices

        except requests.exceptions.RequestException as e:
            attempt += 1
            logging.warning(
                f"Attempt {attempt} failed: {e}. Retrying..."
            )
            time.sleep(backoff_factor ** attempt)

    logging.error("All retries failed. Returning empty price data.")
    return {}