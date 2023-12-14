import numpy as np 
import matplotlib.pyplot as plt 
import pandas as pd
import seaborn as sns
import yfinance as yf 
import datetime as dt 
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import Dense,Dropout,LSTM
from tensorflow.keras.models import Sequential

file='../Datasets/^NDX.csv'

data=pd.read_csv(file)
#data['Date']=pd.to_datetime(data['Date'])
prev_dates=pd.to_datetime(data['Date'])


scaler=StandardScaler()
features=list(data)[1:6]
train_data=data[features].astype(float)
train_scaled_data=scaler.fit_transform(train_data)


plt_data=train_data.tail(100)
#plt_data['Close'].plot()


X_train=[]
y_train=[]

n_prev=15
n_forecast=1

for i in range(n_prev,len(train_scaled_data)-n_forecast+1):
	X_train.append(train_scaled_data[i-n_prev:i,0:train_scaled_data.shape[1]])
	y_train.append(train_scaled_data[i+n_forecast-1:i+n_forecast,0])

X_train,y_train=np.array(X_train),np.array(y_train)

def Model(model):
	model.add(LSTM(64,activation='relu',input_shape=(X_train.shape[1],X_train.shape[2]),return_sequences=True))
	model.add(LSTM(32,activation='relu',return_sequences=False))
	model.add(Dense(y_train.shape[1]))
	model.add(Dropout(0.5))
	model.compile(optimizer='adam',loss='mse')
    return model



hist=model.fit(X_train,y_train,epochs=10,batch_size=16)
plt.plot(hist.history['loss'],label='Train Loss')








