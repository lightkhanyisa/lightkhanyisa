import pandas as pd
import numpy as np 
import yfinance as yf 
import matplotlib.pyplot as plt


file='../Datasets/^NDX.csv'

data=pd.read_csv(file)

data=pd.DataFrame(data)
data=data.set_index(pd.DatetimeIndex(data['Date'].values))

def SMA20(data,period):
	data['SMA']=data.Close.rolling(window=period).mean()
	return data['SMA']

data['SMA']=SMA20(data,7)

def Std(data,period):
	data['Std']=data.Close.rolling(window=period).std()
	return data['Std']

data['Std']=Std(data,7)

def BB_Bands(data):
	data['Upper']=data.SMA + 2 * data.Std
	data['Lower']=data.SMA - 2 * data.Std
	return data.Upper,data.Lower

bands=BB_Bands(data)
data['Upper']=bands[0]
data['Lower']=bands[1]

data.dropna()

def Strategy(data):
	buys=[]
	sells=[]
	open_pos=False

	for i in range(len(data)):
		if data.Lower[i] > data.Close[i]:
			if open_pos==False:
				buys.append(i)
				open_pos=True
		elif data.Upper[i] < data.Close[i]:
			if open_pos:
				sells.append(i)
				open_pos=False
	return buys,sells


regime=Strategy(data)

BuySignals=regime[0]
SellSignals=regime[1]

print(BuySignals)
print(SellSignals)

'''
To get a data set of the positions taken so we can be able to calculate our PNL we will merge our dataset and create
a new one to house those results
'''


def BackTest(data):
	plt.plot(data[['Close','SMA','Upper','Lower']])
	#plt.fill_between(data.index,data.Upper,data.Lower,color='g',alpha=0.5)
	plt.scatter(data.iloc[BuySignals].index,data.iloc[BuySignals].Close,marker='*',color='g')
	plt.scatter(data.iloc[SellSignals].index,data.iloc[SellSignals].Close,marker='*',color='r')
	plt.show()

def AverageGain(merged_data):
	totalgains=merged_data.shift(-1).SellPos - merged_data.BuyPos
	rel_gains=(merged_data.shift(-1).SellPos - merged_data.BuyPos)/merged_data.BuyPos

	print('Mean Value For Avrg Gains:',totalgains)
	print('Mean Value For Relative Gains:',rel_gains)

buy=regime[0]
sell=regime[1]

merged=pd.concat([data.iloc[buy].Close,data.iloc[sell].Close],axis=1)
merged.columns=['BuyPos','SellPos']

BackTest(data)
#AverageGain(merged)





