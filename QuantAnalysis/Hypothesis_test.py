import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_pacf

from statsmodels.graphics.tsaplots import plot_acf
file='../Datasets/AAPL.csv'

def get_data(file):

	data=pd.read_csv(file,parse_dates=True)
	data['Date']=pd.to_datetime(data['Date'])
	data.index=data['Date'].values
	close_data=data['Close'].copy()

	return close_data

data=get_data(file)

def adfuller_test(df):
	result=adfuller(df)
	print(f'ADF Stats:{result[0]}')
	print(f'p-value:{result[1]}')


adfuller_test(data)

def acf_test(df):
#Autocorrelation Function
	fig,(ax1,ax2)=plt.subplots(1,2,figsize=(16,8))
	ax1.plot(df)
	ax1.set_title('Close Price Data')
	plot_acf(df,ax=ax2)


acf_test(data)

def differencing(df):
	#Perform differencing on the price data 
	diff=df.diff().dropna()
	fig,(ax3,ax4)=plt.subplots(1,2,figsize=(16,8))
	ax3.plot(diff)
	ax3.set_title("Differenced Data")
	plot_acf(diff,ax=ax4)
	return diff



diff=differencing(data)

def pcf_test(diff):
	#Perform PartialAutoCorrelation
	fig,(ax3,ax4)=plt.subplots(1,2,figsize=(16,8))
	ax3.plot(diff)
	ax3.set_title("Differenced Data")
	plot_pacf(diff,ax=ax4)
pcf_test(diff)


plt.show()


