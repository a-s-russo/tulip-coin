import math
from random import choice
from statistics import mean

import matplotlib.pyplot as plt
import pandas
from matplotlib import ticker

import player

# Define coin constants
STARTING_PRICE_IN_DOLLARS = 0.1
MAXIMUM_POOL_OF_COINS = 1000000

# Define time constants
DURATION_IN_MINUTES = 60
TRADE_GAP_IN_SECONDS = 5

# Define player constants
STARTING_MONEY_IN_DOLLARS = 1000
NUM_OTHER_PLAYERS = 9

# Define simulation constants
NUM_SIMULATIONS = 50

# Initialise list to store results from each simulation
results = []

# Iterate simulations
for simulation in range(NUM_SIMULATIONS):

    # Initialise simulation parameters
    seconds_remaining = DURATION_IN_MINUTES * 60
    PRICE_FACTOR = STARTING_PRICE_IN_DOLLARS * MAXIMUM_POOL_OF_COINS
    price = PRICE_FACTOR / MAXIMUM_POOL_OF_COINS
    pool_of_coins = MAXIMUM_POOL_OF_COINS
    trade = 0

    # Initialise dictionary to store the history of prices in previous transactions
    history_dict = {
        'transaction': [0],
        'price_history': [price],
        'minutes_remaining': [DURATION_IN_MINUTES],
    }

    # Initialise players
    main_player = player.MainPlayer(money=STARTING_MONEY_IN_DOLLARS)
    players = [main_player]
    for _ in range(0, NUM_OTHER_PLAYERS):
        random_player = player.RandomPlayer(money=STARTING_MONEY_IN_DOLLARS)
        players.append(random_player)

    # Iterate trades
    while seconds_remaining > 0:

        # Extract current price (corresponding to the price of the previous transaction)
        if seconds_remaining == DURATION_IN_MINUTES * 60:
            history = pandas.DataFrame({})
        else:
            history = pandas.DataFrame(history_dict)
        current_price = history_dict['price_history'][-1]

        # Randomly select player
        selected_player = choice(players)
        trade_decision, trade_proportion = selected_player.implement_trading_strategy(history)

        # Buy coins
        if trade_decision == 'buy':
            money_to_spend = selected_player.money * trade_proportion
            coins_to_buy = int(money_to_spend // current_price)
            selected_player.coins += coins_to_buy
            pool_of_coins -= coins_to_buy
            money_spent = coins_to_buy * current_price
            selected_player.money -= money_spent

        # Sell coins
        if trade_decision == 'sell':
            coins_to_sell = int(math.floor(selected_player.coins * trade_proportion))
            selected_player.coins -= coins_to_sell
            pool_of_coins += coins_to_sell
            money_earned = coins_to_sell * current_price
            selected_player.money += money_earned

        # Update price
        try:
            price = PRICE_FACTOR / pool_of_coins
        except ZeroDivisionError:
            price = price

        # Update history
        trade += 1
        seconds_remaining -= TRADE_GAP_IN_SECONDS
        minutes_remaining = seconds_remaining // 60
        history_dict['transaction'].append(trade)
        history_dict['price_history'].append(price)
        history_dict['minutes_remaining'].append(minutes_remaining)

    # Store results of simulation
    for p in players:
        p.total_assets = p.money + p.coins * price
    results.append(players[0].total_assets)

# Calculate mean of results
mean_total_assets = mean(results)

# Plot results
x = list(range(1, NUM_SIMULATIONS + 1))
y = results
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(x, y, marker='o', linestyle='-')
plt.title(f'Total assets for each of {NUM_SIMULATIONS} simulations\nMean across runs: ${mean_total_assets:,.0f}')
plt.xlabel('Simulation run')
ax.set_xlim(xmin=1, xmax=NUM_SIMULATIONS)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
plt.grid(axis='y', linestyle='--')
plt.show()
fig.savefig('plot.png', bbox_inches='tight')
