import math
from random import randint
from statistics import median

import matplotlib.pyplot as plt
import pandas
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter

from trading_strategies import implement_trading_strategy

# Define constants
STARTING_PRICE = 0.1
DURATION_IN_MINS = 60
TRADE_GAP_IN_SECS = 5
NUM_SIMULATIONS = 50
NUM_PLAYERS = 10
NUM_TRADES = int(60.0 / TRADE_GAP_IN_SECS * DURATION_IN_MINS)

# Initialise list to store results from each simulation
results = []

# Iterate simulations
for simulation in range(NUM_SIMULATIONS):
    # Initialise dictionary to store the history of prices in previous transactions
    history_dict = {
        'transaction': [0],
        'price_history': [STARTING_PRICE],
        'minutes_remaining': [DURATION_IN_MINS],
    }

    # Initialise starting amount of money and coins
    money = 1000
    coins = 0

    # Iterate trades
    for trade in range(1, NUM_TRADES + 1):

        # Calculate new price
        current_price = history_dict['price_history'][-1]
        price_fluctuation = randint(-10, 10)
        new_price = round(max(current_price + price_fluctuation / 100, 0.01), 2)

        # Update history
        revised_minutes_remaining = history_dict['minutes_remaining'][-1]
        if trade % 12 == 0:
            revised_minutes_remaining -= 1
        history_dict['transaction'].append(trade)
        history_dict['price_history'].append(new_price)
        history_dict['minutes_remaining'].append(revised_minutes_remaining)
        history = pandas.DataFrame(history_dict)

        # Determine ability to trade
        selected_player = randint(1, NUM_PLAYERS)
        if selected_player == 1:
            trade_decision, trade_proportion = implement_trading_strategy(history)

            # Buy coins
            if trade_decision == 'buy':
                money_to_spend = money * trade_proportion
                coins_to_buy = int(money_to_spend // new_price)
                coins += coins_to_buy
                money_spent = coins_to_buy * new_price
                money -= money_spent

            if trade_decision == 'sell':
                coins_to_sell = int(math.floor(coins * trade_proportion))
                coins -= coins_to_sell
                money_earned = coins_to_sell * new_price
                money += money_earned

    # Store results of simulation
    total_assets = money + coins * new_price
    results.append(total_assets)

# Calculate average result
median_total_assets = median(results)


# Define formatting function for y-axis
def human_format(num, pos):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '$%.1f%s' % (num, ['', 'K', 'M', 'B'][magnitude])


# Plot results
x = list(range(1, NUM_SIMULATIONS + 1))
y = results
fig, ax = plt.subplots()
ax.plot(x, y, marker='o', linestyle='-')
plt.title(f'Simulations of total assets\nMedian: ${median_total_assets:,.0f}')
plt.xlabel('Simulation run')
ax.xaxis.set_major_locator(ticker.FixedLocator(x))
ax.xaxis.set_major_formatter(ticker.FixedFormatter(list(map(str, x))))
formatter = FuncFormatter(human_format)
ax.yaxis.set_major_formatter(formatter)
plt.show()
