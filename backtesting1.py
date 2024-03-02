from backtesting import Backtest, Strategy
from backtesting.test import GOOG

from backtesting.lib import crossover, resample_apply

import talib

print(GOOG)

class RsiOscillator(Strategy): 
  upper_bound = 70
  lower_bound = 30
  rsi_window = 14

  def init(self):
    self.daily_rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

    # self.weekly_rsi = resample_apply('W-SUN', talib.RSI, self.data.Close, self.rsi_window)

  # mixing in higher time frame indicators
  # def next(self):
  #   if (crossover(self.daily_rsi, self.upper_bound) and self.weekly_rsi[-1] > self.upper_bound): 
  #     self.position.close()
  #   elif (crossover(self.lower_bound, self.daily_rsi) and self.weekly_rsi[-1] < self.lower_bound):
  #     self.buy()

  def next(self):
    if crossover(self.daily_rsi, self.upper_bound): 
      if self.position.is_long:
        print(self.position.size)
        print(self.position.pl_pct)

        self.position.close()
        self.sell()

    elif crossover(self.lower_bound, self.daily_rsi):
      if self.position.is_short or not self.position:
        self.position.close()
        self.buy()      

bt = Backtest(GOOG, RsiOscillator, cash = 10_000)

# optimizing your strategy parameters to get a better desired metric
# stats = bt.optimize(upper_bound = range(50, 85, 5), lower_bound = range(10, 45, 5), rsi_window = range(10,30, 2), maximize = 'Sharpe Ratio')



stats = bt.run()
print(stats)

bt.plot()