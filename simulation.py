import math
from random import choice
from statistics import mean

import matplotlib.pyplot as plt
import pandas
from matplotlib import ticker

import player

# Define coin constants
#   Starting (or maximum) pool of coins X is arbitrary.
#   Slope and intercept terms come from fitting a straight line between the following two points:
#   (1) when there are X coins in the pool, the price should be $0.10;
#   (2) when there are 10% of the coins left in the pool, the price should be $10.
#   When there are 0 coins in the pool, the price will be the intercept term.
STARTING_POOL_OF_COINS = 100000
SLOPE = -0.00011
INTERCEPT = 11.1

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


# Define function to calculate price based on pool of coins
def calculate_price(slope, intercept, pool):
    return round(slope * pool + intercept, 2)


# Iterate simulations
for simulation in range(NUM_SIMULATIONS):

    # Initialise simulation parameters
    seconds_remaining = DURATION_IN_MINUTES * 60
    minutes_remaining = DURATION_IN_MINUTES
    pool_of_coins = STARTING_POOL_OF_COINS
    trade_number = 1

    # Initialise dictionary and dataframe to store the history of prices in previous transactions
    history_dict = {
        'transaction': [],
        'price_history': [],
        'minutes_remaining': [],
    }

    # Initialise players
    main_player = player.MainPlayer(money=STARTING_MONEY_IN_DOLLARS)
    players = [main_player]
    for _ in range(0, NUM_OTHER_PLAYERS):
        random_player = player.RandomPlayer(money=STARTING_MONEY_IN_DOLLARS)
        players.append(random_player)

    # Iterate trades
    while seconds_remaining > 0:

        # Calculate current price
        current_price = calculate_price(SLOPE, INTERCEPT, pool_of_coins)

        # Randomly select player
        selected_player = choice(players)
        trade_decision, trade_proportion = selected_player.implement_trading_strategy(pandas.DataFrame(history_dict))

        # Buy coins
        if trade_decision == 'buy':
            money_to_spend = selected_player.money * trade_proportion
            coins_to_buy = min(int(money_to_spend // current_price), pool_of_coins)
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

        # Do not buy or sell coins
        if trade_decision == 'hold' and trade_number > 1:
            current_price = history_dict['price_history'][-1]

        # Update history
        history_dict['transaction'].append(trade_number)
        history_dict['price_history'].append(current_price)
        history_dict['minutes_remaining'].append(minutes_remaining)

        # Update simulation parameters
        trade_number += 1
        seconds_remaining -= TRADE_GAP_IN_SECONDS
        minutes_remaining = seconds_remaining // 60

    # Store results of simulation
    closing_price = calculate_price(SLOPE, INTERCEPT, pool_of_coins)
    for p in players:
        p.total_assets = p.money + p.coins * closing_price
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
if NUM_SIMULATIONS == 1:
    ax.xaxis.set_major_locator(ticker.FixedLocator(x))
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(list(map(str, x))))
else:
    ax.set_xlim(xmin=1, xmax=NUM_SIMULATIONS)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
ax.yaxis.set_major_formatter(ticker.StrMethodFormatter('${x:,.0f}'))
plt.grid(axis='y', linestyle='--')
plt.show()
fig.savefig('plot.png', bbox_inches='tight')
