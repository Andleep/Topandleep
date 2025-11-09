import datetime

def log_trade(pair, result, pnl):
    with open("trade_history.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | {pair} | {result} | {pnl}\n")

def update_cumulative_profit(value):
    with open("cumulative_profit.txt", "w") as f:
        f.write(str(value))
