import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 


file='../Datasets/^NDX.csv'
data=pd.read_csv(file)


#Apply the fft to the price data

data['Sample']=data['Close'].values


fft_result=np.fft.fft(data['Sample'])
power_spec=np.abs(fft_result)**2


#Extract the frequencies within the data

sampling_frequency=1
num_samples=len(data['Sample'])
frequencies=np.fft.fftfreq(num_samples,1/sampling_frequency)


dominant_freq=np.abs(frequencies[np.argmax(power_spec)])
trend_cycle=(1/dominant_freq)

fig,(ax1,ax2)=plt.subplots(2,1,figsize=(8,4))
ax1.plot(data['Sample'])
ax1.set_xlabel('Time')
ax1.set_ylabel('Close-Price')

ax2.plot(frequencies,power_spec)
ax2.set_xlabel('Power_Spectrum')
ax2.set_ylabel('frequency-domain')
'''
ax3.axvline(x=dominant_freq,color='r',linestyle='--',label=f'dominant_freq:{dominant_freq:4f}Hz')
ax3.set_xlabel('frequency')
ax3.set_ylabel('Trend-Cycle')

ax3.legend()
'''
plt.tight_layout()
plt.show()
print(f'The estimated trend cycle is approximately{trend_cycle:2f}...  .....  days.')




