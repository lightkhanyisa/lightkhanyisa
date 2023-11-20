import pandas as pd 
import numpy as np 
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt 
import seaborn as sns



file='../TestData/^NDX.csv'
data=pd.read_csv(file)
data_close=data['Close']

data_returns=round(np.log(data_close).diff().dropna()*100,2)#returns the price data as a series/you can change to a dataframe

print(data_returns)
#data_returns.plot()
print(data_returns.describe())
n,minmaxi,mean,var,skew,kurt=stats.describe(data_returns)
mini,maxi=minmaxi
std=var**.5
#plt.hist(data_returns,bins=40)
#plot a normal distribution from the sample of datapoints-1200
X=norm.rvs(mean,std,n)
#plt.hist(X,bins=40)
#Price hypothesis is it Normally distributed
#Use the kurtosis test to see if the underlying kurtosis is that of a normally distributed 
#--variable

X_test=stats.kurtosistest(X)
data_test=stats.kurtosistest(data_returns)

print(f"{'Test Statistics ':20}{'p-value':>15}")
print(f"{'  '*5}{'-'*30}")
print(f"x:{X_test[0]:>17.2f}{X_test[1]:16.4f}")
print(f"NDX:{data_test[0]:13.2f}{data_test[1]:16.4f}")

plt.hist(data_returns,bins=25,edgecolor='w',density=True)
overlay=np.linspace(mini,maxi,100)
plt.plot(overlay,norm.pdf(overlay,mean,std))
#conduct a hypothesis test
print(stats.ttest_1samp(data_returns,0,alternative='two-sided'))
plt.show()