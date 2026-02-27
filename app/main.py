import time
import json
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

from app.logger import setup_logger
from app.price_fetcher import fetch_prices
from app.rule_engine import evaluate_rules
from app.notifier import send_alert


def load_config():
    with open("config/alert_config.json", "r") as f:
        return json.load(f)


def send_daily_summary(prices):
    """
    Sends a formatted daily summary message.
    """
    if not prices:
        logging.warning("No prices available for daily summary.")
        return

    message_lines = ["📊 Daily Crypto Summary (UTC)\n"]

    for coin, data in prices.items():
        name = data.get("name")
        price = data.get("current_price")
        change = data.get("price_change_24h")

        message_lines.append(
            f"{name}: ${price} | 24h Change: {change:.2f}%"
        )

    summary_message = "\n".join(message_lines)
    logging.info("Sending daily summary.")
    send_alert(summary_message)


def main():
    load_dotenv()
    setup_logger()

    logging.info("Starting Crypto Alert Service...")

    last_summary_date = None  # Track last summary sent

    try:
        config = load_config()

        coins = config["coins"]
        rules = config["rules"]
        interval = config.get("interval_seconds", 60)

        rapid_threshold = rules["rapid_movement"]["threshold"]
        summary_enabled = config.get("daily_summary", {}).get("enabled", False)
        summary_hour = config.get("daily_summary", {}).get("hour_utc", 12)

        while True:
            prices = fetch_prices(coins)
            logging.info(f"Fetched prices: {prices}")

            # 1️⃣ Rapid movement alerts
            alerts = evaluate_rules(prices, rapid_threshold)
            logging.info(f"Generated alerts: {alerts}")

            for alert in alerts:
                logging.info(f"Sending alert: {alert}")
                send_alert(alert)

            # 2️⃣ Daily summary logic
            if summary_enabled:
                now = datetime.utcnow()

                if now.hour == summary_hour:
                    if last_summary_date != now.date():
                        send_daily_summary(prices)
                        last_summary_date = now.date()

            time.sleep(interval)

    except KeyboardInterrupt:
        logging.info("Service interrupted by user.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")

    finally:
        logging.info("Crypto Alert Service stopped.")


if __name__ == "__main__":
    main()