import time
import json
import logging
import threading
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Response
import uvicorn

from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

from app.logger import setup_logger
from app.price_fetcher import fetch_prices
from app.rule_engine import evaluate_rules
from app.notifier import send_alert


app = FastAPI()

# ==============================
# Service State
# ==============================

service_state = {
    "last_run": None,
    "last_success": None,
    "last_error": None,
}

# ==============================
# Prometheus Metrics
# ==============================

alerts_counter = Counter(
    "crypto_alerts_sent_total",
    "Total number of alerts sent"
)

last_run_gauge = Gauge(
    "crypto_last_run_timestamp",
    "Last execution timestamp (unix)"
)


# ==============================
# Config Loader
# ==============================

def load_config():
    with open("config/alert_config.json", "r") as f:
        return json.load(f)


# ==============================
# Background Alert Loop
# ==============================

def alert_loop():
    load_dotenv()
    setup_logger()

    logging.info("Starting Crypto Alert Background Loop...")

    config = load_config()
    coins = config["coins"]
    rules = config["rules"]
    interval = config.get("interval_seconds", 60)

    while True:
        try:
            now = datetime.utcnow().isoformat()
            service_state["last_run"] = now
            last_run_gauge.set(time.time())

            prices = fetch_prices(coins)
            logging.info(f"Fetched prices: {prices}")

            alerts = evaluate_rules(prices, rules)
            logging.info(f"Generated alerts: {alerts}")

            for alert in alerts:
                logging.info(f"Sending alert: {alert}")
                send_alert(alert)
                alerts_counter.inc()

            service_state["last_success"] = datetime.utcnow().isoformat()

        except Exception as e:
            logging.error(f"Error in alert loop: {e}")
            service_state["last_error"] = str(e)

        time.sleep(interval)


# ==============================
# API Endpoints
# ==============================

@app.get("/health")
def health():
    return {
        "status": "running",
        "last_run": service_state["last_run"],
        "last_success": service_state["last_success"],
        "last_error": service_state["last_error"],
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# ==============================
# Entry Point
# ==============================

if __name__ == "__main__":
    thread = threading.Thread(target=alert_loop, daemon=True)
    thread.start()

    uvicorn.run(app, host="0.0.0.0", port=8000)