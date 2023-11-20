import numpy as np 
import yfinance as yf 
import pandas as pd
import matplotlib.pyplot as plt 
import datetime as dt 



def get_data(stocks):
	start=dt.datetime.today()-dt.timedelta(365)
	end=dt.datetime.today()
	data=yf.download(stocks,start,end)
	return data


stocks_1="AMZN"
stocks_2="^NDX"

goog_data=get_data(stocks_1)
spy_data=get_data(stocks_1)

spy_data['Returns']=np.log(spy_data.Close).diff
goog_data['Returns']=np.log(goog_data.Close).diff

def get_corr(data:pd.DataFrame()):
	corr=data.corr()
	return corr

def get_sample(data:pd.DataFrame(),n=60):
	sample=data.sample(n)
	return sample


def train_reg(x1,y1,deg=1):
	regression=np.polyfit(x1,y1,deg)
	trend=np.polyval(reg,y1)
	return trend

spy_sample=get_sample(spy_data['Returns'],65)
goog_sample=get_sample(goog_data['Returns'],65)
reg=train_reg(spy_sample,goog_sample)

plt.scatter(x=spy_sample,y=goog_sample)
plt.plot(goog_sample,reg,'r')

def predict(t=1,deg=1):
	new_data=yf.download(stocks,start,end)
	time=np.arange(1,len(data)+t)
	new_data['Date']=time
	new_data=round(data,2)
	new_reg=np.ployfit(new_data['Date'],new_data['Close'],deg=1)
	reg=np.polyval()
	return new_data.tail()

data_test=predict(1)

plt.show()

