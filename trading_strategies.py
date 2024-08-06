def implement_trading_strategy(history):
    if not history.empty:
        most_recent_price = history.tail(1).price_history.iloc[0]
        lower_quantile = history.price_history.quantile(0.1)
        upper_quantile = history.price_history.quantile(0.9)
        if most_recent_price <= lower_quantile:
            return 'buy', 1
        if most_recent_price >= upper_quantile:
            return 'sell', 1
    return 'hold', 0
