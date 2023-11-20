import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



filepath='../Datasets/^NDX.csv'

def load_data(loc:str):
    data=pd.read_csv(loc)
    data_frame=pd.DataFrame(data)
    return data_frame

data_set=load_data(filepath)

##generate the moving averages needed for this implementation

data_set["50d"]=data_set["Close"].rolling(window=50).mean()
data_set["150d"]=data_set["Close"].rolling(window=150).mean()

print(data_set[['Close','50d','150d']].tail(10))

data_set['50d-150d']=data_set['50d']-data_set['150d']

SD=50

##calculations for the regime
data_set['regime']=np.where(data_set['50d-150d']>SD,1,0)
data_set['sell_regime']=np.where(data_set['50d-150d']<-SD,-1,data_set['regime'])

##market response to the regime strategy

data_set['Market']=np.log(data_set['Close']/data_set['Close'].shift(1))
data_set['Strategy']=data_set['regime'].shift(1)*data_set['Market']
plt.plot(data_set['Market'].cumsum().apply(np.exp),lw=2,label='Market',color='blue')
plt.plot(data_set['Strategy'].cumsum().apply(np.exp),lw=2,label='Strategy',color='red')
plt.legend(loc='upper left')
print(data_set['regime'].value_counts())
print(data_set['sell_regime'].value_counts())

plt.show()



      
