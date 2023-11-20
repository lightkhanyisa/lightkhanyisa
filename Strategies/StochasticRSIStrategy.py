import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt


def load_data(loc:str):
	data=pd.read_csv(loc)
	data_frame=pd.DataFrame(data)
	return data_frame

file='../TestData/^NDX.csv'##use a more smaller data set and to avoid caveats


data=load_data(file)

data=data.set_index(pd.DatetimeIndex(data['Date'].values))

def mov_avrg(data,period=12,column='Close'):
	return data[column].ewm(span=period,adjust=False).mean()

def stoch_rsi(data,period=14,column='Close'):
	delta=data[column].diff(1)#discrete difference of the column value and let it be = 1
	delta=delta.dropna()
	up_bound=delta.copy()
	low_bound=delta.copy()
	up_bound[up_bound<0]=0
	low_bound[low_bound>0]=0
	data['upper']=up_bound##form the upper  bounds 
	data['lower']=low_bound#form  the lower bounds 

	avrg_gain=mov_avrg(data,period,column='upper')
	avrg_loss=abs(mov_avrg(data,period,column='lower'))

	rel_strength=avrg_gain/avrg_loss
	rel_strength=100.0-(100.0/(1.0+rel_strength))
     ##applying the formula to retrieve the stoch rsi value 
	stoch_rsi_value=(rel_strength-rel_strength.rolling(period).min())/(rel_strength.rolling(period).max()-rel_strength.rolling(period).min())

	return stoch_rsi_value


##parse the data into columns 

data['StochRsi']=stoch_rsi(data)
data['MovingAvrg']=mov_avrg(data)

##visualise the data 
fig,(ax1,ax2,ax3)=plt.subplots(nrows=3,sharex=True)
plt.subplots_adjust(hspace=0)

ax1.plot(data.index,data['Close'],color='b')
ax2.plot(data.index,data['StochRsi'],color='r',linestyle='--')
ax3.plot(data.index,data['MovingAvrg'],color='g',linestyle='--')

##create the upper and lower bounds 

ax2.axhline(0.20,color='r')##the oversold level 
ax2.axhline(0.80,color='b')##the overbought level 

plt.xticks(rotation=45)

plt.show()
