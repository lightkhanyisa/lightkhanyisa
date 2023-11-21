import pandas as pd 
import pandas_ta as ta 
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt 
from scipy.signal import savgol_filter
from scipy.signal import find_peaks



file='../Datasets/SPY.csv'
data=pd.read_csv(file)
data['Date']=pd.to_datetime(data['Date'])
data.index=data['Date']

data['ATR']=ta.atr(high=data.High,low=data.Low,close=data.Close)
data['ATR']=data.ATR.rolling(window=20).mean()


def plot(data):
	data=data.iloc[0:1000]
	fig,ax=plt.subplots()
	plt.xticks(rotation=30)
	price=ax.plot(data.index,data.Close,c='grey')


def smoothen_data(data):
	data=data.iloc[0:2000]
	data['smoothed_data']=savgol_filter(data['Close'],50,5)
	fig,ax=plt.subplots()
	price=ax.plot(data.index,data.Close,c='grey')
	price_smooth=ax.plot(data.index,data['smoothed_data'],c='blue')

	atr=data.ATR.iloc[-1]

	peaks_idx,_=find_peaks(data.smoothed_data,distance=15,width=3,prominence=atr)
	troughs_idx,_=find_peaks(-1*data.smoothed_data,distance=15,width=3,prominence=atr)
	peaks,=ax.plot(data.index[peaks_idx],data.smoothed_data.iloc[peaks_idx],c='r')
	troughs,=ax.plot(data.index[troughs_idx],data.smoothed_data.iloc[troughs_idx],c='g')

	slope_len=0
	slope=True

	slope_down_len=0
	slope_down=False

	while slope:
		if 2 + slope_len > len(peaks_idx) or 2 + slope_len > len(troughs_idx):
			break
		if data.smoothed_data.iloc[peaks_idx[-1 - slope_len]] > data.smoothed_data.iloc[peaks_idx[-2 - slope_len]] and data.smoothed_data.iloc[troughs_idx[-1 - slope_len]] > data.smoothed_data.iloc[troughs_idx[-2 - slope_len]]:
			slope_len+=1
		else:
			slope=False
	if slope_len > 0 :
		ax.set_facecolor((150/255,255/255,159/255,0.3))
	else:
		ax.set_facecolor('white')

	while slope_down:
		if 2 + slope_down_len > len(peaks_idx) or 2 + slope_down_len > len(troughs_idx):
			break
		if data.smoothed_data.iloc[peaks_idx[-1 - slope_down_len]] < data.smoothed_data.iloc[peaks_idx[-2 - slope_down_len]] and data.smoothed_data.iloc[troughs_idx[-1 - slope_down_len]] > data.smoothed_data.iloc[troughs_idx[-2 - slope_down_len]]:
			slope_down_len+=1
		else:
			slope_down=False
	if slope_down_len > 0 :
		ax.set_facecolor((100/255,255/255,100/255,0.3))
	
	return(peaks,troughs,data['smoothed_data'])

#smoothen_data(data)
peaks,_,_=smoothen_data(data)
print(peaks)
plt.show()