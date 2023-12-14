import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split




file='../TestData/^NDX.csv'
data=pd.read_csv(file)
forecast_preds=20#days in the future to predict
#create the target column to be shifted n units up
#will be used to validate the actual predictions
data=data[['Adj Close']]
data['Prediction']=data[["Adj Close"]].shift(-forecast_preds)
#create the feature set 
X=np.array(data.drop(['Prediction'],1))
X=X[:-forecast_preds]
#create the target data set (y)
y=np.array(data['Prediction'])
y=y[:-forecast_preds]
#split the data
#split to training and testing
x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.2)#20% for testing
#train the model
svr_regressor=SVR(kernel='rbf',C=1e3,gamma=.1)#radio-basis kernel
svr_regressor.fit(x_train,y_train)
#model evaluation can begin
#return the coefficent of determination of the R**2 for the prediction
svr_confidence=svr_regressor.score(x_test,y_test)
print('SVR :svr_confidence',svr_confidence)
#Test the linear regressor
linear_clf=LinearRegression()
linear_clf.fit(x_train,y_train)

#model evaluation of the Linear Regressor
linear_confidence=linear_clf.score(x_test,y_test)
print('Linear Regression :linear_confidence',linear_confidence)
#Get the values of the forecast of the last n rows of the Adj Close price
x_forecast=np.array(data.drop(['Prediction'],1))[-forecast_preds:]
##Get the predictions for the next 'n ' days
linear_predictions=linear_clf.predict(x_forecast)
print(linear_predictions)
svr_predictions=svr_regressor.predict(x_forecast)
print(svr_predictions)
#Predict the future prices
actual=pd.DataFrame()
actual=data[X.shape[0]:]
actual['Prediction']=linear_predictions
plt.title('Nasdaq Stock')
plt.xlabel("Date")
plt.ylabel('Close Prices')
plt.plot(data['Adj Close'])
plt.plot(actual[['Adj Close','Prediction']])
plt.legend(['Original','Price Validation','Predictions'])
plt.show()




