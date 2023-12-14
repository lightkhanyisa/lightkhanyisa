import yfinance as yf 
import numpy as np 
import pandas as pd 
from sklearn.linear_model import LogisticRegression 
import matplotlib.pyplot as plt

file='../Datasets/^NDX.csv'
data=pd.read_csv(file)
##get returns or relative price changes 
data['ret']=data.Close.pct_change()
##calculate the lagged returns [t-1...t-2]
def lagged(data,lags):
	for i in range(1,lags+1):
		data['lags'+str(i)]=data['ret'].shift(i)
	return['lags'+str(i) for i in range(1,lags+1)]

data['regime']=np.where(data.ret > 0,1,0)
##data.regime.value_counts() to see the imbalance in data

features=lagged(data,3)
data.dropna(inplace=True)
print(features)
##now lets build our model

X=data[features]
y=data['regime']

model=LogisticRegression(class_weight='balanced')

model.fit(X,y)
data['predicted_vals']=model.predict(X)

data['alpha']=data['predicted_vals']*data['ret']
##retrieve the cummulated product of the two values

print((data[['alpha','ret']]+1).cumprod()-1)
##(data[['alpha','ret']]+1).cumprod().plot()
##test again by splitting the data to see if the results are the same 
from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,shuffle=False)
model.fit(X_train,y_train)
X_test['predicted_vals']=model.predict(X_test)
X_test['ret']=data.ret[X_test.index[0]:]
X_test['alpha']=X_test.predicted_vals*X_test.ret
(X_test[['alpha','ret']]+1).cumprod().plot()
print(X_test)
plt.show()
