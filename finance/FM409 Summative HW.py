import pandas as pd
from datetime import datetime, timedelta
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import numpy as np
from pandas.plotting import autocorrelation_plot
from statsmodels.graphics.tsaplots import plot_acf
from matplotlib import pyplot
from scipy import stats
from scipy.stats import norm


end = '2021-03-15'
start = '2011-03-15'

ticker = 'GME'

df = web.DataReader(ticker, start=start,end=end, data_source='yahoo')['Adj Close']
print(df)


daily_returns = df.copy()
daily_returns = np.log(df / df.shift(1)) * 100
daily_returns = daily_returns[1:]

daily_returns_squared = (daily_returns) ** 2

print(daily_returns)
print(daily_returns_squared)

print('Mean: ', round(daily_returns.mean(),4))
print('Std: ', round(daily_returns.std(),4))
print('Skew: ', round(daily_returns.skew(),4))
print('Kurtosis: ', round(daily_returns.kurtosis(),4))
autocorr = []
for i in range(1,21):
    autocorr.append(daily_returns.autocorr(lag=i))
    print('Autocorr(',i, '): ', daily_returns.autocorr(lag=i))


ma = daily_returns_squared.rolling(window=25, center=False).mean()
print('MA')
ma = ma.dropna()
print(ma)
lamb = 0.96
ewma = ma.copy()
for i in range(0, ewma.__len__()-1):
    ewma[i+1] = (1-lamb)*daily_returns_squared[i+24] + lamb * ewma[i]

print('EWMA')
print(ewma)



#garch
h1 = 30.05677
garch = df.copy()
garch[0] = h1
print(garch)
for i in range(0, df.__len__()-1):
    garch[i+1] = 0.41221 + 0.13434 * daily_returns_squared[i] + 0.85988 * garch[i]

print(garch)

cvols = pd.DataFrame()
cvols['ma'] = np.sqrt(ma*252)
cvols['ewma'] = np.sqrt(ewma*252)
cvols['garch'] = np.sqrt(garch[24:]*252)
print(cvols.head())
print(cvols.corr())



#VaR

VaR = pd.DataFrame()
VaR['ma'] = np.sqrt(ma) * stats.norm.ppf(0.05)
VaR['ewma'] = np.sqrt(ewma) * stats.norm.ppf(0.05)
VaR['garch'] = np.sqrt(garch) * stats.norm.ppf(0.05)

print(stats.norm.ppf(0.05))




#HS VaR
HSVaR = daily_returns.copy()
for i in range(251, len(daily_returns)):
    helpnp = daily_returns[i-251:i-1]
    HSVaR[i] = np.sort(helpnp)[int(0.05*251)-1]

HSVaR = HSVaR[251:]
VaR2 = VaR[227:]
VaR = VaR2
VaR['HS'] = HSVaR
print(VaR)


print('****VaR Corr****')
print(VaR.corr())


print('****VaR****')
violation = [0,0,0,0]
probaR = 0
probaVaR = 0
for i in range(0, len(VaR)):
    if VaR['ma'][i] > daily_returns[251+i]:
        violation[0] = violation[0] + 1
        probaR = daily_returns[251+i]
        probaVaR = VaR['ma'][i]
    if VaR['ewma'][i] > daily_returns[251+i]:
        violation[1] = violation[1] + 1
    if VaR['garch'][i] > daily_returns[251+i]:
        violation[2] = violation[2] + 1
    if VaR['HS'][i] > daily_returns[251+i]:
        violation[3] = violation[3] + 1

print(probaR)
print(probaVaR)
print('****VaR Violations ALL****')
print(violation)


violation = [0,0,0,0]
probaR = 0
probaVaR = 0
VaR200 = VaR[-200:]
dr200 = daily_returns[-200:]
for i in range(0, len(VaR200)):
    if VaR200['ma'][i] > dr200[i]:
        violation[0] = violation[0] + 1
        probaR = dr200[i]
        probaVaR = VaR200['ma'][i]
    if VaR200['ewma'][i] > dr200[i]:
        violation[1] = violation[1] + 1
    if VaR200['garch'][i] > dr200[i]:
        violation[2] = violation[2] + 1
    if VaR200['HS'][i] > dr200[i]:
        violation[3] = violation[3] + 1

print(probaR)
print(probaVaR)
print('****VaR Violations Last 200****')
print(violation)
print(VaR)

dummy = np.zeros((4,len(VaR)))
dummyEWMA = np.zeros((1,len(VaR)))
dummyG = np.zeros((1,len(VaR)))
dummyHS = np.zeros((1,len(VaR)))

print(dummy)

dummy = VaR.copy()


for i in range(0, len(VaR)):
    if VaR['ma'][i] > daily_returns[251+i]:
        dummy['ma'][i] = 1
    else:
        dummy['ma'][i] = 0
    if VaR['ewma'][i] > daily_returns[251+i]:
        dummy['ewma'][i] = 1
    else:
        dummy['ewma'][i] = 0
    if VaR['garch'][i] > daily_returns[251+i]:
        dummy['garch'][i] = 1
    else:
        dummy['garch'][i] = 0
    if VaR['HS'][i] > daily_returns[251+i]:
        dummy['HS'][i] = 1
    else:
        dummy['HS'][i] = 0

print('****Dummy****')
print(dummy)

print('Autocorr MA:', round(dummy['ma'].autocorr(lag=1),4))
print('Autocorr EWMA:', round(dummy['ewma'].autocorr(lag=1),4))
print('Autocorr GARCH:', round(dummy['garch'].autocorr(lag=1),4))
print('Autocorr HS:', round(dummy['HS'].autocorr(lag=1),4))





print('****VaR****')

VaR.plot(title='VaR')
plt.legend(['MA', 'EWMA', 'GARCH'])
plt.show()

HSVaR.plot(title='HS VaR')
plt.show()

print(VaR[-2:])
VaR[-200:].plot()
daily_returns[-200:].plot()
plt.legend(['MA', 'EWMA', 'GARCH', 'HS', 'Log R'])
plt.show()

print(np.sort(daily_returns)[-20:])

cvols[-50:].plot(title='Annualized conditional standard deviation')
plt.legend(['MA', 'EWMA', 'GARCH'])
plt.show()


plt.hist(daily_returns, bins = 1000, range = (-100,100), density = True)
fitted_norm=stats.norm.pdf(np.linspace(-100,100,1000),
                           daily_returns.mean(),daily_returns.std())

plt.plot(np.linspace(-100,100,1000), fitted_norm)
plt.title('Density histogram of returns')
plt.show()

ar = daily_returns_squared.plot(title='GME', label='GME')
garch.plot(label='Garch', ax=ar)
plt.show()
at = daily_returns_squared[-100:].plot(title='GME', label='GME')
garch[-100:].plot(label='Garch', ax=at)
plt.show()


df.plot(title='GME', label='GME')
plt.show()

daily_returns.plot(title='GME Daily returns', label='GME')
plt.ylabel('%')
plt.show()

ax = autocorrelation_plot(daily_returns)
ax.set_xlim([0, 20])
plt.show()
ab = autocorrelation_plot(daily_returns_squared)
ab.set_xlim([0, 20])
plt.show()
plt.plot(autocorr)
plt.show()



plot_acf(daily_returns, lags=20)
pyplot.show()
plot_acf(daily_returns_squared, lags=20)
pyplot.show()

ax = daily_returns_squared[-100:].plot(title='GME', label='GME')
ma[-100:].plot(label='Moving average', ax=ax)
plt.show()

ag = daily_returns_squared[-100:].plot(title='GME', label='GME')
ewma[-100:].plot(label='EWMoving average', ax=ag)
plt.show()


