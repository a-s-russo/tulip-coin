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
            return 'buy', 1.0
        current_price = history.tail(1).price_history.iloc[0]
        mean_price = sum(history.price_history) / len(history.price_history)
        if current_price <= mean_price:
            return 'buy', 1.0
        return 'sell', 1.0
