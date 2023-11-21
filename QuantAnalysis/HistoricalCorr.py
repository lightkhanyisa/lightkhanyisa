import yfinance as yf 
import datetime as dt 
import matplotlib.pyplot as plt 


sp500=['AAPL','MSFT']
start=dt.datetime(2018,1,1)


def get_returns(tickers,start):
	data=yf.download(tickers,start=start)['Close']

	Returns=data.pct_change()

	print(Returns.corr())
	return Returns

returns=get_returns(sp500,start)

def plot_results(returns,period=20):
    #a plot of the company returns for selected tickers
	roll_corr=returns.rolling(window=period).corr()
	roll_corr.dropna(inplace=True)

	print(roll_corr)
	print(roll_corr.unstack()['AAPL'])
	roll_corr.unstack()['AAPL'][['TSLA','MSFT']].plot()


plt.show()


