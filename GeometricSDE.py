import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 


file='../Datasets/SPY.csv'

def get_data(file):
	data=pd.read_csv(file)
	return data

data=get_data(file)

n_t=len(data)
n_mc=10000
sigma=0.25#(volatility)
mu=0.08#drift term(business cycles,growth)
dt=2./(n_t-1)

def calculate(df,n_t,n_mc,sigma,mu,dt):
	#This part is for the calculation of the SDE 
	S_t=pd.DataFrame(0.,index=df.index,columns=list(range(1,n_mc+1)))
	S_t.iloc[0]=df.Close.iloc[0]

	print('Daily Vol:',sigma*np.sqrt(dt))

	for i in range(1,n_t):
		ds2_t=mu*dt+sigma*np.sqrt(dt)*np.random.randn(n_mc)
		S_t.iloc[i]=S_t.iloc[i-1] + S_t.iloc[i-1]*ds2_t

	return S_t

S_t=calculate(data,n_t,n_mc,sigma,mu,dt)



def plot_S_t(data,S_t,n_mc,n_t):
	#Here we have our visualisations
	fig=plt.figure()
	ax1=fig.add_subplot(111)

	for i in np.random.choice(np.array(range(1,n_mc+1)),size=20):
		ax1.plot(S_t[i],'b',lw=0.5)

	ax1.plot(data['Close'],'r',lw=1)

	S_t_mean=S_t.mean(axis=1)
	S_t_theoretical_mean=data['Close'].iloc[0] * np.exp(mu*np.arange(n_t)/n_t*2.)
	S_t_theoretical_mean=pd.DataFrame(S_t_theoretical_mean,index=S_t_mean.index)
	print('Expected Value:==',S_t_mean.iloc[-1])
	print('Theoretical expected value:==',S_t_theoretical_mean.iloc[-1])


	plt.plot(S_t_mean,'r',label='Mean value of the MC simulation')
	plt.plot(S_t_theoretical_mean,'g',label='Theoretical Mean of the MC')
	plt.xlabel('Price Series as a function of time')
	plt.ylabel('Theoretical mean Compared to MC mean(St)')
plot_S_t(data,S_t,n_mc,n_t)
plt.show()
