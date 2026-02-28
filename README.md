# Crypto Price Alert Service

A production-style crypto monitoring microservice that fetches live cryptocurrency prices, evaluates alert rules, sends Telegram notifications, and exposes health and metrics endpoints for observability.

## Features

- Tracks configured cryptocurrencies using CoinGecko
- Sends Telegram alerts based on configured rules
- Retries external API calls on temporary failures
- Structured JSON logging
- FastAPI health endpoint
- Prometheus metrics endpoint
- Dockerized deployment
- GitHub Actions CI pipeline to build and push Docker images

## Architecture

The service runs two components inside one container:

1. **Background Alert Loop**
   - Loads config
   - Fetches prices from CoinGecko
   - Evaluates alert rules
   - Sends Telegram alerts
   - Updates service state and metrics

2. **FastAPI HTTP Server**
   - `/health` for health checks
   - `/metrics` for Prometheus metrics

## Endpoints

- `GET /health`
- `GET /metrics`

## Environment Variables

Create a local `.env` file (this file is not committed):

```env
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Run Locally

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -m app.main
```

### Windows (PowerShell)

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.main
```

## Run with Docker

Build the image:

```bash
docker build -t crypto-alert-service .
```

Run the container:

```bash
docker run -d \
  --name crypto-alert \
  --restart unless-stopped \
  --env-file .env \
  -p 8000:8000 \
  crypto-alert-service
```

## Observability

### Health Check

```bash
http://localhost:8000/health
```

### Metrics

```bash
http://localhost:8000/metrics
```

Prometheus metrics include:
- Python process metrics
- alert counter
- last run timestamp

## CI/CD

GitHub Actions automatically:

- builds the Docker image
- pushes the image to Docker Hub on every push to `main`

Docker Hub image:

```text
sudaganisanjay/crypto-price-alert-service
```

## Project Structure

```text
app/
  __init__.py
  logger.py
  main.py
  notifier.py
  price_fetcher.py
  rule_engine.py

config/
  alert_config.json

.github/workflows/
  docker.yml

Dockerfile
requirements.txt
README.md
```

## Security Notes

- `.env` is ignored and never committed
- Secrets are injected at runtime
- Docker image does not contain secrets
- GitHub repository contains only source code and safe configuration

## Future Improvements

- Persist alert state in Redis or database
- Add deployment to AWS EC2 / ECS
- Add continuous deployment (CD)
- Add user-configurable alert rules
- Add Slack / email notifications
- Add authentication for management endpoints