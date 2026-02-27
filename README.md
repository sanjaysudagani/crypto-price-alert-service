# 🚀 Crypto Price Alert Service

A production-ready, Dockerized cryptocurrency alerting service that monitors market prices and sends Telegram notifications based on configurable rules.

---

## 📌 Overview

This service:
- Fetches live crypto prices
- Evaluates configurable alert rules
- Sends Telegram notifications
- Avoids alert spam with intelligent throttling
- Runs continuously in Docker

Designed with production best practices:
- Environment variable secret management
- Clean logging
- Retry mechanisms
- Config-driven rules
- Containerized deployment

---

## 🏗 Architecture

Price Fetcher → Rule Engine → Notifier → Telegram

- `price_fetcher.py` → Fetches live market data
- `rule_engine.py` → Evaluates alert conditions
- `notifier.py` → Sends alerts
- `main.py` → Orchestrates the workflow

---

## ⚙️ Features

- 24h percentage change alerts
- Rapid price movement detection
- Daily summary (optional)
- Dockerized deployment
- Config-driven rules
- Safe secret handling (.env)
- Graceful retry logic
- Alert deduplication

---

## 🔐 Environment Variables

Secrets are stored using environment variables:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

Never commit `.env`.

---

## 🐳 Run with Docker

Build image:

```
docker build -t crypto-alert-service .
```

Run container:

```
docker run -d \
  --name crypto-alert \
  --restart unless-stopped \
  --env-file .env \
  crypto-alert-service
```

---

## 📂 Project Structure

```
app/
  main.py
  price_fetcher.py
  rule_engine.py
  notifier.py
config/
  alert_config.json
Dockerfile
requirements.txt
```

---

## 🛡 Production Considerations

- Secrets are not stored in code
- Retry strategy for API failures
- Alert throttling prevents spam
- Docker restart policy ensures availability
- Logging is centralized via stdout (Docker logs)

---

## 🔮 Future Improvements

- Persistent state (Redis / DB)
- Rate limiting
- AWS deployment (ECS / EC2)
- Metrics + Prometheus integration
- Slack / Email notifications
- Kubernetes deployment

---

## 👨‍💻 Author

Built as a production-grade monitoring microservice.