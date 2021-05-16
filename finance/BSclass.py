import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.stats import norm
from math import sqrt, exp, pi
from mpl_toolkits.mplot3d import Axes3D

print(norm.cdf(-0.1))

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
S = 100
K = 100
T = 5
r = .01
vol = .15
div = 0 # dividend yield


timeToMaturityList = np.linspace(0.01, T, 100)
strikePriceList = np.linspace(50,150,100)
stockPriceList = np.linspace(50,150,100)


print(BSclass(call, 100, 100, 1/12, 0, 0.3, 0).delta())

# Calculate delta for different stock price and time to maturity
d = np.array([])
for t in timeToMaturityList:
    d = np.append(d, BSclass(call, stockPriceList, K, t, r, vol, div).delta(), axis=0)
d = d.reshape(len(stockPriceList), len(timeToMaturityList))


X, Y = np.meshgrid(stockPriceList, timeToMaturityList)
figd = plt.figure()
ax = Axes3D(figd)
ax.plot_surface(X, Y, d, rstride=1, cstride=1, cmap=cm.coolwarm, shade='interp')
plt.title('Put Option Delta')
ax.view_init(25, -120)
ax.set_xlabel('Stock Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Delta')
#plt.show()

# Calculate delta for different strike price and time to maturity
d = np.array([])
for t in timeToMaturityList:
    d = np.append(d, BSclass(call, S, strikePriceList, t, r, vol, div).delta(), axis=0)
d = d.reshape(len(strikePriceList), len(timeToMaturityList))

X, Y = np.meshgrid(strikePriceList, timeToMaturityList)
figd = plt.figure()
ax = Axes3D(figd)
ax.plot_surface(X, Y, d, rstride=1, cstride=1, cmap=cm.coolwarm, shade='interp')
plt.title('Put Option Delta')
ax.view_init(25, -120)
ax.set_xlabel('Strike Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Delta')


# Calculate gamma for different stock price and time to maturity
g = np.array([])
for t in timeToMaturityList:
    g = np.append(g, BSclass(call, stockPriceList, K, t, r, vol, div).gamma(), axis=0)

print(g.shape)
print(g)
g = g.reshape(len(stockPriceList), len(timeToMaturityList))
print(g.shape)

X, Y = np.meshgrid(stockPriceList, timeToMaturityList)
figg = plt.figure()
ax = Axes3D(figg)
ax.plot_surface(X, Y, g, rstride=1, cstride=1, cmap=cm.coolwarm, shade='interp')
plt.title('Call Option Gamma')
ax.view_init(25, -120)
ax.set_xlabel('Stock Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Gamma')


# Calculate gamma for different strike price and time to maturity
g = np.array([])
for t in timeToMaturityList:
    g = np.append(g, BSclass(call, S, strikePriceList, t, r, vol, div).gamma(), axis=0)

print(g.shape)
print(g)
g = g.reshape(len(strikePriceList), len(timeToMaturityList))
print(g.shape)

X, Y = np.meshgrid(strikePriceList, timeToMaturityList)
figg = plt.figure()
ax = Axes3D(figg)
ax.plot_surface(X, Y, g, rstride=1, cstride=1, cmap=cm.coolwarm, shade='interp')
plt.title('Call Option Gamma')
ax.view_init(25, -120)
ax.set_xlabel('Strike Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Gamma')


# Calculate theta for different stock price and time to maturity
t = np.array([])
for i in timeToMaturityList:
    t = np.append(t, BSclass(call, stockPriceList, K, i, r, vol, div).theta(), axis=0)
t = t.reshape(len(stockPriceList), len(timeToMaturityList))

X, Y = np.meshgrid(stockPriceList, timeToMaturityList)
figt = plt.figure()
ax = Axes3D(figt)
ax.plot_surface(X, Y, t, rstride=1, cstride=1, cmap=cm.coolwarm, shade='interp')
ax.view_init(27, -125)
plt.title('Call Option Theta')
ax.set_xlabel('Strike Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Theta')


v = np.array([])
for i in timeToMaturityList:
    v = np.append(v, BSclass(call, stockPriceList, K, i, r, vol, div).vega(), axis=0)
v = v.reshape(len(stockPriceList), len(timeToMaturityList))
X, Y = np.meshgrid(stockPriceList, timeToMaturityList)
figv = plt.figure()
ax = Axes3D(figv)
ax.plot_surface(X, Y, v, rstride=1, cstride=1, cmap=cm.coolwarm, shade='interp')
plt.title('Call Option Vega')
ax.view_init(27, -125)
ax.set_xlabel('Stock Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Vega')


va = np.array([])
for i in timeToMaturityList:
    va = np.append(va, BSclass(call, stockPriceList, K, i, r, vol, div).vanna(), axis=0)
va = va.reshape(len(stockPriceList), len(timeToMaturityList))
X, Y = np.meshgrid(stockPriceList, timeToMaturityList)
figva = plt.figure()
ax = Axes3D(figva)
ax.plot_surface(X, Y, va, rstride=1, cstride=1, cmap=cm.coolwarm, shade='interp')
plt.title('Call Option Vanna')
ax.view_init(27, -125)
ax.set_xlabel('Stock Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Vanna')
plt.show()