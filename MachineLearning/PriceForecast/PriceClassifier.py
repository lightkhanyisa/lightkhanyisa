import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split



file='../Datasets/^NDX.csv'
data=pd.read_csv(file)
#data['Date']=pd.to_datetime(data['Date'])
#predict the x number of days
future=25
#create target data shifted x units to the future
data=data[['Close']]
data['Prediction']=data[["Close"]].shift(-future)

#create the feature set 
X=np.array(data.drop(['Prediction'],1))[:-future]
#create the target data set (y)
y=np.array(data)[:-future]
#split the data
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.25)
#create the model
tree=DecisionTreeRegressor().fit(X_train,y_train)
lr=LinearRegression().fit(X_train,y_train)
#Last x-row of the feature dataset
x_future=data.drop(['Prediction'],1)[:-future]
x_future=x_future.tail(future)
x_future=np.array(x_future)
##############
#show model predictions
tree_preds=tree.predict(x_future)
print(tree_preds)
print()
lr_preds=lr.predict(x_future)
print(lr_preds)
############
actual=data[X.shape[0]:]
actual['Prediction']=lr_preds
plt.title('Nasdaq Stock')
plt.xlabel("Date")
plt.ylabel('Close Prices')
plt.plot(data['Close'])
plt.plot(actual[['Close','Prediction']])
plt.legend(['Original','Validation','Predictions'])

'''
plt.figure(figsize=(16,8))
plt.title('Nasdaq Stock')
plt.xlabel("Date")
plt.ylabel('Close Prices')
plt.plot(data['Close'])
'''
plt.show()