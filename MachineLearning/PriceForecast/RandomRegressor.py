import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.ensemble import RandomForestRegressor

file='../Datasets/^NDX.csv'
def get_data(file):

	data=pd.read_csv(file)
	return data

df=get_data(file)
def model(df):
	model=RandomForestRegressor()
	#train the model using X and y data
	X=data[['Open','High','Low','Volume']]
	X=X[:int(len(data)-1)]
	#create the target set 
	y=data['Close']
	y=y[:int(len(data)-1)]

	#fit the regressor
	model.fit(X,y)
	#Get the model predictions
	predictions=model.predict(X)
	print('Model accuracy is :',model.score(X,y))

#Test the predictions of the model
	new_data=data[['Open','High','Low','Volume']].tail(1)
	preds=model.predict(new_data)
	print('Model Predictions for the last day of price')
	print()
	print('Model Predictions:',preds)
	print()
	print('Actuality of the price data seems to be :',data[['Close']].tail(1).values[0][0])


model(df)