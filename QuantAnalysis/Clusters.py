import pandas as pd 
import datetime as dt
import numpy as np  
import yfinance as yf 

from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.cluster import KMeans
 


comp_30=['AAPL','MSFT','NVDA','TSLA','FB']

start=dt.datetime.now()-dt.timedelta(days=365*2)
end=dt.datetime.now()

data=yf.download(comp_30,start,end)[['Open','Close']]

open_price=np.array(data['Open'].T)#must Transpose the data
close_price=np.array(data['Close'].T)

daily_mov=close_price-open_price

normalizer=Normalizer()
cluster_model=KMeans(n_clusters=5,max_iter=1000)
pipeline=make_pipeline(normalizer,cluster_model)
pipeline.fit(daily_mov)
clusters=pipeline.predict(daily_mov)


result_data=pd.DataFrame({
		'n_clusters':5,
		'Clusters':clusters,
		'instruments':list(comp_30)
	}).sort_values(by=['clusters'],axis=0)


print(result_data)


