import pandas as pd
from datetime import datetime, timedelta
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm


veg = datetime.today()
kezdet = veg - timedelta(days=900)

ticker = 'AAPL'

df = web.DataReader(ticker, start=kezdet,end=veg, data_source='yahoo')['Adj Close']
print(df.head())

def compute_daily_returns(df):
    """Compute and return the daily return values."""
    daily_returns = df.copy()
    daily_returns[1:] = (df[1:] / df[:-1].values) - 1
    daily_returns = (df / df.shift(1)) - 1
    daily_returns.ix[0, :] = 0
    return daily_returns

logReturns = np.log(df/df.shift(1))
logReturns = logReturns.dropna()
print(logReturns)
mean = logReturns.mean()
print("Mean return: {}".format(float(mean)))
var = logReturns.var()
print("Variance: {}".format(float(var)))


drift = mean - (var * 0.5)
print("Drift: {}".format(float(drift)))
stdev = logReturns.std()
print("Std: {}".format(float(stdev)))

intervals = 1000
iterations = 10

daily_returns = np.exp(drift + stdev * norm.ppf(np.random.rand(intervals, iterations)))

print(daily_returns)

S0 = df.iloc[-1]

#Return an array of zeros with the same shape and type as a given array.
price_list = np.zeros_like(daily_returns)

price_list[0] = S0

for t in range(1, intervals):
    price_list[t] = price_list[t-1] * daily_returns[t]

print(price_list)

plt.figure(figsize=(10,6))
plt.plot(price_list)
plt.show()


average = np.mean(price_list, axis=1)
print(average)
plt.figure(figsize=(10,6))
plt.plot(average)
plt.show()