import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 




file='../Datasets/SPY.csv'
data=pd.read_csv(file)


def candle_type(open_price,close_price):
	if close_price >= open_price:
		return 'bullish'
	elif close_price < open_price:
		return 'bearish'
	else:
		return 'doji'

data['candle_type']=np.vectorize(candle_type)(data['Open'],data['Close'])

#Now to create the 3-candle setup strategy

data['candle-1']=data['candle_type'].shift(1)
data['candle-2']=data['candle_type'].shift(2)
data['candle-3']=data['candle_type'].shift(3)
data['prev-close']=data['Close'].shift(1)


#filter the candle setups 

new_data=data[(data['candle-1']=='bullish') & (data['candle-2']=='bullish') & (data['candle-3']=='bullish')].copy()
new_data['points']=new_data['Close'] - data['prev-close']

#Evaluate the results of the strategy statistically
new_data['counts']=1

#valuating the results

last_data=new_data.groupby('candle_type').agg({
					'counts':'count',
					'points':'mean'
	}).reset_index()

last_data['total_points']=last_data['counts']* last_data['points']
new_data['cummulative_returns']=new_data['points'].cumsum()

new_data['cummulative_returns'].plot()

plt.show()
