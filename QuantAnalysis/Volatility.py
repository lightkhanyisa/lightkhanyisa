import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from py_vollib.black_scholes.greeks.analytical import delta


file='../Datasets/SPY.csv'

def get_data(loc):
	data=pd.read_csv(file)
	stock_price=data['Close']
	log_returns=np.log(stock_price/stock_price.shift(1)).dropna()
	return stock_price,log_returns

#Calculate the Volatility
stock_price,log_returns=get_data(file)

def calculate(log_returns):	
	trading_days=252
	trading_days_monthly=21
	Volatility=log_returns.rolling(window=trading_days_monthly).std()*np.sqrt(trading_days)
	return Volatility

Volatility=calculate(log_returns)

def plots(stock_price,Volatility):

	#Plot the insights

	fig,ax=plt.subplots()

	ax.plot(stock_price,color='red')
	ax.set_xlabel('Date',fontsize=12)
	ax.set_ylabel('Stock Price',color='red',fontsize=11)

	ax2=ax.twinx()
	ax2.plot(Volatility,color='blue')
	ax2.set_ylabel('Volatility',color='blue',fontsize=11)


plots(stock_price,Volatility)

plt.show()
