import numpy as np 
import pandas as pd 

file='../Datasets/SPY.csv'
def get_data(loc):
	df=pd.read_csv(file)
	return df

df=get_data(file)
daily_ret=df['Close'].pct_change(1)

volatily=daily_ret.std()

print('Daily volatily: SPY',volatily)
stock_price=df['Close'].iloc[-1]

strike=stock_price

risk_free_rate=0.04
maturity=1.0

def european_option(S0,K,r,v,T,n_sim,flag):
	z=np.random.standard_normal(n_sim)
	S_forward=S0*np.exp(r-0.5*v**2)*T + v*np.sqrt(T)*z

	if flag=='C':
		payoff=np.maximum(S_forward-K,0)
	elif flag=='P':
		payoff=np.maximum(K-S_forward,0)
	else:
		print("False flag")
		return
	return np.exp(-r*T) * np.sum(payoff)/n_sim

n_sim=100000
call_price=european_option(stock_price,strike,risk_free_rate,volatily,maturity,n_sim,'P')
print("Option price:",call_price)

