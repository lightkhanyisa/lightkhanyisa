import yfinance as yf 
import pandas as pd 
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score

file='../Datasets/^NDX.csv'
data=pd.read_csv(file)
data['Date']=pd.to_datetime(data['Date'])
data.index=data['Date']


def Analyse(data,shift=1):
	data['Tomorrow']=data.Close.shift(shift)
	data['Target']=(data.Tomorrow > data["Close"]).astype(int)
	return data[['Tomorrow','Target']]

Analyse(data)
data=data.loc['2020-01-01':].copy()

def train_model(data,n_samples):
	model=RandomForestClassifier(n_estimators=n_samples,min_samples_split=100,random_state=1)##random state for randomization in a predictable sequence
	train=data.iloc[:-100]
	test=data.iloc[-100:]
	predictors=["Close","Volume","Open","High","Low"]
	model.fit(train[predictors],train['Target'])
	yhat=model.predict(test[predictors])
	return yhat
	

output=train_model(data,100)	
print(output)