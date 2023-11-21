import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 

file='../Datasets/SPY.csv'
def get_data(loc):
	df=pd.read_csv(file)
	return df

df=get_data(file)
stock_price=df['Close']
log_returns=np.log(stock_price/stock_price.shift(1)).dropna()

#Calculate the Volatility

trading_days=252

trading_days_monthly=21

Volatility=log_returns.rolling(window=trading_days_monthly).std()*np.sqrt(trading_days)
T=1
n_timesteps=100

n_sim=10000
r=0.05
#Implement Geometric Brownian Motion
def gbm(Volatility,df,T,n_timesteps,n_sim,r):

	S0=stock_price.iloc[-1]
	
	vol=Volatility.iloc[-1]


	delta_t=T/n_timesteps
	S_fwd=np.zeros((n_timesteps+1,n_sim))
	S_fwd[0]=S0

	for t in range(1,n_timesteps+1):
		S_fwd[t]=S_fwd[t-1]* np.exp((r-0.5*vol**2)*delta_t+vol *np.sqrt(delta_t)*np.random.standard_normal(n_sim))

	delta_stock_price=(S_fwd[-1]-S0).mean()/S0
	delta_percent='{:.2%}'.format(delta_stock_price)
	print(delta_percent,':The stock price in %')#The higher the n_simulations the higher the values
	return S_fwd

S_fwd=gbm(Volatility,df,T,n_timesteps,n_sim,r)

def line_plot(S_fwd):

	plt.figure()
	plt.plot(S_fwd[:,0:50])
	plt.xlabel('Days in the future')
	plt.ylabel('Stock')
	plt.title('Stock Price Forecast in n-days in the Future')
def hist(S_fwd):
	plt.hist(S_fwd[-1],bins=100)


plt.show()

