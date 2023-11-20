import pandas as pd 
import mplfinance as mpf 
import numpy as np 
from sklearn.linear_model import LinearRegression





file='../TestData/^NDX.csv'
data=pd.read_csv(file)
data['Date']=pd.to_datetime(data['Date'])
data.index=data['Date']

channel_width=.2
sma_period=20


data['sma']=data['Close'].rolling(window=sma_period).mean()
data['Upper_Channel']=data['sma']*(1+channel_width)
data['Lower_Channel']=data['sma']*(1-channel_width)

data['Breakout']=data['Close'].shift(1) < data['Upper_Channel'].shift(1)
data.dropna(inplace=True)

#calculate the triangle breakout channel
x=np.arange(len(data)).reshape(-1,1)
y=data['High'].values.reshape(-1,1)

reg=LinearRegression().fit(x,y)

upper_trend=reg.predict(x)*(1+channel_width)
lower_trend=reg.predict(x)*(1-channel_width)

data['Upper_Trend']=upper_trend.flatten()
data['Lower_Trend']=lower_trend.flatten()

ind=mpf.make_addplot(data[['Upper_Channel','Lower_Channel']])
mpf.plot(data,type='candle',addplot=ind,title='Stock-Breakout')
ind=mpf.make_addplot(data[['Upper_Trend','Lower_Trend']],type='line')
mpf.plot(data,type='candle',addplot=ind,title='Stock-Breakout')



