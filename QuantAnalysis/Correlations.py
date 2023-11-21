import pandas as pd 
import datetime as dt 
import yfinance as yf  
import matplotlib.pyplot as plt 
import seaborn as sns


start=dt.datetime(2018,1,1)
end=dt.datetime.now()
tickers=['FB','NVDA','MSFT','BA','AAPL']


def get_data(start,end,tickers):
	for ticker in tickers:
		data=yf.download(tickers,start,end)['Close']
	return data

data=get_data(start,end)

def heatmap(df):
	corr_data=df.pct_change().corr(method='pearson')
	sns.heatmap(corr_data,annot=True,cmaps='coolwarm')
	print(corr_data)

heatmap(data)

plt.show()