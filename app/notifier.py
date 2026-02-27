import os
import logging
import requests


def send_alert(message: str):
    """
    Sends alert message to Telegram using Bot API.
    Requires TELEGRAM_TOKEN and TELEGRAM_CHAT_ID
    to be set as environment variables.
    """

    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        logging.error("Telegram credentials are not set.")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        logging.info("Alert sent successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send Telegram alert: {e}")