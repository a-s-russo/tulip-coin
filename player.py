from random import choice, random


class RandomPlayer:
    def __init__(self, money):
        self.money = money
        self.coins = 0
        self.total_assets = 0

    def implement_trading_strategy(self, history):
        random_trade_decision = choice(['buy', 'sell', 'hold'])
        random_trade_proportion = random()
        return random_trade_decision, random_trade_proportion


class MainPlayer(RandomPlayer):
    def __init__(self, money):
        super().__init__(money)

    def implement_trading_strategy(self, history):
        if history.empty:
            return 'buy', 1
        else:
            most_recent_price = history.tail(1).price_history.iloc[0]
            lower_quantile = history.price_history.quantile(0.1)
            upper_quantile = history.price_history.quantile(0.9)
            if most_recent_price <= lower_quantile:
                return 'buy', 1
            if most_recent_price >= upper_quantile:
                return 'sell', 1
            return 'hold', 0
