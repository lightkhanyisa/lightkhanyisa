import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import statsmodels.api as stats 
#computing the daily returns of the SP500 

file='../Datasets/SPY.csv'
def get_data(file):
    #accessing returns 
	df=pd.read_csv(file)
	df=df['Close'].pct_change()*100
	return df

df=get_data(file)

df=df.rename('Current-Day')
df=df.reset_index()


def lags(data):
	for i in range(1,6):
		data['Lag-'+str(i)]=data['Current-Day'].shift(i)
	return data


df=lags(df)

loc='../Datasets/SPY.csv'
def get_volumes(loc):
#get the volume data for further analysis
	df=pd.read_csv(loc)
	df['Volume']=df.Volume.shift(1).values/1000_000_000
	df.dropna(inplace=True)
	df['Regime']=[1 if i > 0 else 0 for i in df['Current-Day']]

vol_df=get_volumes(loc)

def model(df):
	#In this section we create our features and target variables

	df=stats.add_constant(df)#Adds an intercept to our current data

	X=df[['const','Lag-1','Lag-2','Lag-3','Lag-4','Lag-5','Volume']]
	y=df.Regime
    #fit the model on the X,y data 
	model=stats.Logit(y,X)
	result=model.fit()
	print(result.summary())
	print(preds)
	return X,y

X,y=model(vol_df)


def predictions(X):
	preds=result.predict(X)
	return preds
preds=predictions(X)

#Now a confusion matrix to measure the performance of the model

def confusion_matrix(actual,preds):
	pred_trans=['Up' if i > 0.5 else 'Down' for i in preds]
	actuals=['Up' if i > 0 else 'Down' for i in actual]
	confusion_matrix=pd.crosstab(pd.Series(actuals),
								pd.Series(pred_trans),
								rownames=['Actuals'],
								colnames=['Predicted'])
	return confusion_matrix


matrix=confusion_matrix(y,preds)
print(matrix)
#Evaluate the model
#print(len(vol_df))

'''
//This can be a way for you to measure accuracy based on 
	your data set

model_accuracy=(73+3095)/5883
print(model_accuracy)

'''
