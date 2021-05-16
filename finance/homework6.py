import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import norm
from math import sqrt, exp, pi
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

class BSclass:
    def __init__(self, call, S, K, T, r, vol, div):
        self.call = call
        self.stock = S
        self.strike = K
        self.maturity = T
        self.interest = r
        self.volatility = vol
        self.dividend = div
        self.d1 = (self.volatility * sqrt(self.maturity)) ** (-1) * (np.log(self.stock / self.strike) + (self.interest - self.dividend + self.volatility ** 2 / 2) * self.maturity)
        self.d2 = self.d1 - self.volatility * sqrt(self.maturity)

    def price(self):
        if self.call:
            return exp(-self.dividend * self.maturity) * norm.cdf(self.d1) * self.stock - norm.cdf(self.d2) * self.strike * exp(-self.interest * self.maturity)
        else:
            return norm.cdf(-self.d2) * self.strike * exp(-self.interest * self.maturity) - norm.cdf(-self.d1) * self.stock * exp(-self.dividend * self.maturity)

    def delta(self):
        if self.call:
            return norm.cdf(self.d1) * exp(-self.dividend * self.maturity)
        else:
            return (norm.cdf(self.d1) - 1) * exp(-self.dividend * self.maturity)

    def gamma(self):
        return exp(-self.dividend * self.maturity) * norm.pdf(self.d1) / (self.stock * self.volatility * sqrt(self.maturity))

    def vega(self):
        return self.stock * norm.pdf(self.d1) * sqrt(self.maturity) * exp(-self.dividend * self.maturity)

    def theta(self):
        if self.call:
            return -exp(-self.dividend * self.maturity) * (self.stock * norm.pdf(self.d1) * self.volatility) / (2 * sqrt(self.maturity)) - self.interest * self.strike * exp(
                -self.interest * sqrt(self.maturity)) * norm.cdf(self.d2) + self.dividend * self.stock * exp(-self.dividend * self.maturity) * norm.cdf(self.d1)
        else:
            return -exp(-self.dividend * self.maturity) * (self.stock * norm.pdf(self.d1) * self.volatility) / (2 * sqrt(self.maturity)) + self.interest * self.strike * exp(
                -self.interest * sqrt(self.maturity)) * norm.cdf(-self.d2) - self.dividend * self.stock * exp(-self.dividend * self.maturity) * norm.cdf(-self.d1)

    def rho(self):
        if self.call:
            return self.strike * self.maturity * exp(-self.interest * self.maturity) * norm.cdf(self.d2)
        else:
            return -self.strike * self.maturity * exp(-self.interest * self.maturity) * norm.cdf(-self.d2)

    def vanna(self):
        return exp(-self.dividend * self.maturity) * norm.pdf(self.d1) * (self.d2 / self.volatility)

call = True
put = False
S = 100
K = 100
K2 = 105
binaryMultiplier = K2-K
T = 1
r = .05
vol = .2
div = 0.01

stockPriceList = np.linspace(80,120,41)

#Flat volatility
df = pd.DataFrame(list(zip(BSclass(put, stockPriceList, K, T, r, vol, div).price(),
                    BSclass(put, stockPriceList, K2, T, r, vol, div).price(),
                    BSclass(put, stockPriceList, K2, T, r, vol, div).price()-BSclass(put, stockPriceList, K, T, r, vol, div).price(),
                    norm.cdf(-BSclass(put, stockPriceList, K, T, r, vol, div).d2) * exp(-r*T) * binaryMultiplier,
                    )),
                   index=stockPriceList, columns=('Put 1', 'Put 2', 'Portfolio', 'Binary'))
df['Absolute diff'] = df['Portfolio'] - df['Binary']
df['Relative diff'] = ((df['Portfolio'] - df['Binary']) / df['Binary']) * 100
print('Flat volatility:')
print(df)

print('Put 1 price:', df.iat[20,0])
print('Put 2 price:', df.iat[20,1])
print('Portfolio cost:', df.iat[20,2])
print('Binary B-S price:', df.iat[20,3])


ax = df['Put 1'].plot(title='With flat vol', label='Put 1')
df['Put 2'].plot(ax=ax)
df['Binary'].plot(ax=ax)
df['Portfolio'].plot(ax=ax)

ax.set_xlabel("Stock price")
ax.legend(loc='upper right')
plt.show()


ax2 = df['Binary'].plot(title='With flat vol', label='Binary')
df['Portfolio'].plot(ax=ax2)
df['Absolute diff'].plot(ax=ax2)
ax2.set_xlabel("Stock price")
ax2.legend(loc='upper right')
plt.show()


#Non-flat volatility
vol = 0.19
vol2 = 0.195
df2 = pd.DataFrame(list(zip(BSclass(put, stockPriceList, K, T, r, vol, div).price(),
                    BSclass(put, stockPriceList, K2, T, r, vol2, div).price(),
                    BSclass(put, stockPriceList, K2, T, r, vol2, div).price()-BSclass(put, stockPriceList, K, T, r, vol, div).price(),
                    norm.cdf(-BSclass(put, stockPriceList, K, T, r, vol, div).d2) * exp(-r*T) * binaryMultiplier,
                    )),
                   index=stockPriceList, columns=('Put 1', 'Put 2', 'Portfolio', 'Binary'))
df2['Absolute diff'] = df2['Portfolio'] - df2['Binary']
df2['Relative diff'] = ((df2['Portfolio'] - df2['Binary']) / df2['Binary']) * 100
print('Non-flat volatility:')
print(df2)

ax3 = df2['Put 1'].plot(title='With non-flat vol', label='Put 1')
df2['Put 2'].plot(ax=ax3)
df2['Binary'].plot(ax=ax3)
df2['Portfolio'].plot(ax=ax3)

ax3.set_xlabel("Stock price")
ax3.legend(loc='upper right')
plt.show()

print('Put 1 price:', df2.iat[20,0])
print('Put 2 price:', df2.iat[20,1])
print('Portfolio cost:', df2.iat[20,2])
print('Binary B-S price:', df2.iat[20,3])


ax4 = df2['Binary'].plot(title='With non-flat vol', label='Binary')
df2['Portfolio'].plot(ax=ax4)
df2['Absolute diff'].plot(ax=ax4)

ax4.set_xlabel("Stock price")
ax4.legend(loc='upper right')
plt.show()

ax5 = df['Relative diff'].plot(title='Relative difference in %', label='Flat vol')
df2['Relative diff'].plot(ax=ax5, label='Non-flat vol')
ax5.set_xlabel("Stock price")
ax5.legend(loc='upper left')
plt.show()


#More strikes
K = 100
K2 = 101
vol = 0.19
vol2 = 0.191
binaryMultiplier = K2-K
df3 = pd.DataFrame(list(zip(BSclass(put, stockPriceList, K, T, r, vol, div).price(),
                    BSclass(put, stockPriceList, K2, T, r, vol2, div).price(),
                    BSclass(put, stockPriceList, K2, T, r, vol2, div).price()-BSclass(put, stockPriceList, K, T, r, vol, div).price(),
                    norm.cdf(-BSclass(put, stockPriceList, K, T, r, vol, div).d2) * exp(-r*T) * binaryMultiplier,
                    )),
                   index=stockPriceList, columns=('Put 1', 'Put 2', 'Portfolio', 'Binary'))
df3['Absolute diff'] = df3['Portfolio'] - df3['Binary']
df3['Relative diff'] = ((df3['Portfolio'] - df3['Binary']) / df3['Binary']) * 100
print('Non-flat volatility:')
print(df3)

ax3 = df3['Put 1'].plot(title='Continuous strikes K2 = ' + str(K2), label='Put 1')
df3['Put 2'].plot(ax=ax3)
df3['Binary'].plot(ax=ax3)
df3['Portfolio'].plot(ax=ax3)

ax3.set_xlabel("Stock price")
ax3.legend(loc='upper right')
plt.show()

print('Put 1 price:', df3.iat[20,0])
print('Put 2 price:', df3.iat[20,1])
print('Portfolio cost:', df3.iat[20,2])
print('Binary B-S price:', df3.iat[20,3])

ax4 = df3['Binary'].plot(title='Continuous strikes K2 = ' + str(K2), label='Binary')
df3['Portfolio'].plot(ax=ax4)
df3['Absolute diff'].plot(ax=ax4)

ax4.set_xlabel("Stock price")
ax4.legend(loc='upper right')
plt.show()


