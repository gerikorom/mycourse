import pandas as pd
from datetime import datetime, timedelta
import pandas_datareader.data as web
import matplotlib.pyplot as plt

veg = datetime.today()
kezdet = veg - timedelta(days=900)

ticker = 'AAPL'

df = web.DataReader(ticker, start=kezdet,end=veg, data_source='yahoo')['Adj Close']
print(df)

def mozgo_atlag(df, ablak):
    return df.rolling(window=ablak, center=False).mean()

def mozgo_szoras(df, ablak):
    return df.rolling(window=ablak, center=False).std()

def bollinger_bands(matlag, mszoras):
    """Return upper and lower Bollinger Bands."""
    felso_sav = matlag + mszoras * 2
    also_sav = matlag - mszoras * 2
    return felso_sav, also_sav

ablak = 20
ma_AAPL = mozgo_atlag(df, ablak)
ms_AAPL = mozgo_szoras(df, ablak)

felso_AAPL, also_AAPL = bollinger_bands(ma_AAPL, ms_AAPL)

ax = df.plot(title=ticker, label=ticker)
ma_AAPL.plot(label='Mozgó átlag', ax=ax)
felso_AAPL.plot(label='felső sáv', ax=ax)
also_AAPL.plot(label='alsó sáv', ax=ax)

# Add axis labels and legend
ax.set_xlabel("Dátum")
ax.set_ylabel("Ár")
ax.legend(loc='upper left')
plt.show()

lista = ['SPY', 'AAPL', 'TSLA', 'MSFT', 'QQQ', 'FB', 'DIS', 'UNH', 'JNJ']

for i in lista:
    df = web.DataReader(i, start=kezdet, end=veg, data_source='yahoo')['Adj Close']
    matlag = mozgo_atlag(df, ablak)
    mszoras = mozgo_szoras(df, ablak)

    felso_sav, also_sav = bollinger_bands(matlag, mszoras)

    ax = df.plot(title=i, label=i)
    matlag.plot(label='Mozgó átlag', ax=ax)
    felso_sav.plot(label='felső sáv', ax=ax)
    also_sav.plot(label='alsó sáv', ax=ax)

    # Add axis labels and legend
    ax.set_xlabel("Dátum")
    ax.set_ylabel("Ár")
    ax.legend(loc='upper left')
    plt.show()
