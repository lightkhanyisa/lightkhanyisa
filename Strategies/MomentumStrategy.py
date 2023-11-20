import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 



file='../Datasets/^NDX.csv'
data=pd.read_csv(file)
data.drop(columns=['Adj Close','Volume'],inplace=True)
data=data[['Open','High','Low','Close']]
##create the indicators e.g moving averages
data['9-day-ma']=data['Close'].rolling(window=9).mean()
data['21-day-ma']=data['Close'].rolling(window=21).mean()
##create the signal columns
data['Signal']=np.where(data['9-day-ma'] > data['21-day-ma'],1,0)
data['Signal']=np.where(data['9-day-ma'] < data['21-day-ma'],-1,data['Signal'])

#calculate the returns
data['Returns']=np.log(data['Close']).diff()
data['Model_Returns']=data['Signal']*data['Returns']
data['Trade_Entries']=data['Signal'].diff()

#visualise the positions
'''
plt.grid(True,alpha=.3)
plt.plot(data.iloc[+10:]['Close'],label='NDX')
plt.plot(data.iloc[+10:]['9-day-ma'],label='9-day-ma')
plt.plot(data.iloc[+10:]['21-day-ma'],label='21-day-ma')
plt.plot(data[+10:].loc[data.Trade_Entries==2].index,data[+10:]['9-day-ma'][data.Trade_Entries==2],'^',
		 color='green',markersize=12)
plt.plot(data[+10:].loc[data.Trade_Entries==-2].index,data[+10:]['21-day-ma'][data.Trade_Entries==-2],'v',
		 color='red',markersize=12)

'''
plt.plot(np.exp(data.Returns).cumprod(),label='Buy/Hold',color='green')
plt.plot(np.exp(data.Model_Returns).cumprod(),label='Model_Returns',color='red')
plt.legend(loc=2)
plt.show()
data.dropna(inplace=True)
last_return=np.exp(data.Returns).cumprod()-1
last_model_return=np.exp(data.Model_Returns).cumprod()-1
print(last_return)
print(last_model_return)


