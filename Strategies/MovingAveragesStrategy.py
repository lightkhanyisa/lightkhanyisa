
import pandas as pd
import matplotlib.pyplot as plt


data=pd.read_csv("../Datasets/NSDQ.csv")
data_frame=pd.DataFrame(data)
##calculate the moving averages

data_frame["SMA_20"]=data_frame["Close"].rolling(window=20).mean()
data_frame["SMA_50"]=data_frame["Close"].rolling(window=50).mean()

data_frame=data_frame.dropna()

##clean up data_set to access the values we actually need
data_frame=data_frame[["Close","SMA_20","SMA_50"]]
##print(data_frame)

##define the strategy

Buys =[]
Sells=[]

for i in range(len(data_frame)):
    if data_frame.SMA_20.iloc[i] > data_frame.SMA_50.iloc[i] and data_frame.SMA_20.iloc[i-1] < data_frame.SMA_50.iloc[i-1]:
        Buys.append(i)
    elif data_frame.SMA_20.iloc[i] < data_frame.SMA_50.iloc[i]  and data_frame.SMA_20.iloc[i-1]> data_frame.SMA_50.iloc[i-1]:
        Sells.append(i)
        
print(Buys)
print(Sells)

## show case the data

plt.figure(figsize=(12.5,4.5))
plt.plot(data_frame["Close"],label="Closing Prices",c="blue")
plt.plot(data_frame["SMA_20"],label=" 20 day Moving Average Prices",c="red")
plt.plot(data_frame["SMA_50"],label="50 day Moving Average Prices",c="green")
plt.legend(loc="upper left")
##showcase the buy signals

plt.scatter(data_frame.iloc[Buys].index,data_frame.iloc[Buys]["Close"],marker='^',color='green')
plt.scatter(data_frame.iloc[Sells].index,data_frame.iloc[Sells]["Close"],marker='*',color='red')

plt.show()
        
