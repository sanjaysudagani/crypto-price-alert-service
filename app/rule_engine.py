coin_state = {}

def evaluate_rules(data, rules):
    alerts = []

    # If rules is dictionary format
    if isinstance(rules, dict):
        percentage_rule = rules.get("percentage_change_24h")

        if not percentage_rule or not percentage_rule.get("enabled", True):
            return alerts

        threshold = percentage_rule.get("threshold", 5)

        for coin, values in data.items():
            price = values.get("current_price")
            change = values.get("price_change_24h")

            if change is None:
                continue

            current_state = coin_state.get(coin, "NORMAL")

            if abs(change) >= threshold:
                if current_state == "NORMAL":
                    alerts.append(
                        f"{coin.upper()} moved {change:.2f}% in 24h. Current price: ${price}"
                    )
                    coin_state[coin] = "ALERTING"
            else:
                coin_state[coin] = "NORMAL"

        return alerts

    # If rules is list format
    if isinstance(rules, list):
        for rule in rules:
            if rule.get("type") != "percentage_change_24h":
                continue
            if not rule.get("enabled", True):
                continue

            threshold = rule.get("threshold", 5)

            for coin, values in data.items():
                price = values.get("current_price")
                change = values.get("price_change_24h")

                if change is None:
                    continue

                current_state = coin_state.get(coin, "NORMAL")

                if abs(change) >= threshold:
                    if current_state == "NORMAL":
                        alerts.append(
                            f"{coin.upper()} moved {change:.2f}% in 24h. Current price: ${price}"
                        )
                        coin_state[coin] = "ALERTING"
                else:
                    coin_state[coin] = "NORMAL"

        return alerts

    return alerts