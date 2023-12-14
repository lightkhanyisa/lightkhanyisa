import math
import pandas as pd 
import numpy as np 
from sklearn.preprocessing import MinMaxScaler
from keras.layers import Dense,LSTM
from keras.models import Sequential
import matplotlib.pyplot as plt 


file='../DataSets/^NDX.csv'
data=pd.read_csv(file)
##create the features
dataset=pd.DataFrame()
dataset=data.filter(['Close'])
dataset=dataset.values
#create the train set
train_len=math.ceil(len(dataset)*0.8)
scaler=MinMaxScaler(feature_range=(0,1))
scaled_data=scaler.fit_transform(dataset)
train_data=scaled_data[0:train_len,:]
x_train=[]
y_train=[]

train_days=60

for i in range(train_days,len(train_data)):
	x_train.append(train_data[i-60:i,0])
	y_train.append(train_data[i,0])
	'''
	if i <= train_days+1:
		print(x_train)
		print()
		print(y_train)
    '''

#convert our data to numpy arrays 
x_train,y_train=np.array(x_train),np.array(y_train)
#reshape the data for the data to be 3D dataset
x_train=np.reshape(x_train,(x_train.shape[0],x_train.shape[1],1))
##build the model
model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(x_train.shape[1],1)))
model.add(LSTM(50,return_sequences=False))
model.add(Dense(25))
model.add(Dense(1))
model.compile(optimizer='adam',loss='mean_squared_error')
model.fit(x_train,y_train,batch_size=10,epochs=1)


#create the test dataset
test_data=scaled_data[train_len-60:,:]
x_test=[]
y_test=dataset[train_len:,:]
for i in range(train_days,len(test_data)):
	x_test.append(test_data[i-train_days:i,0])
x_test=np.array(x_test)
x_test=np.reshape(x_test,(x_test.shape[0],x_test.shape[1],1))

predictions=model.predict(x_train)
predictions=scaler.inverse_transform(predictions)
##evaluate the model predictions using rmse for model accuracy and std of the residuals
plt.plot(data['Close'],color='green',label='Actual-Close Prices')
plt.plot(predictions,color='red',label='Predicitions')
plt.legend()
plt.show()













