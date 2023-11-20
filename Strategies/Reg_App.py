import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go

file='../Datasets/^NDX.csv'

##ml libs

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


##get the data
data=pd.read_csv(file)
data=data.set_index(pd.DatetimeIndex(data['Date'].values))

new_data=data.copy()
new_data['Numbers']=list(range(0,len(data)))

##generate our X test and Y test variables

X=np.array(new_data[['Numbers']])
y=new_data['Close'].values

##generate our linear model

linear_mod=LinearRegression()

linear_mod.fit(X,y)

st.subheader(
    '''
    Application for the forecast of Price Data
    '''
    )
st.subheader('**Raw Data**')
st.write(data.head(100)
         )

st.subheader('**Plot the data**')

def intercept():
    y_pred=linear_mod.coef_*X+linear_mod.intercept_
    return y_pred

new_data['Predictions']=intercept()

def plot_data():
    fig= go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'],
                             y=data['Close'],
                             name='Close Prices'))
    fig.layout.update(title_text='Time Series',xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


def plot_intercept():
    st.subheader('**The model params**')
    st.write('linear model coefficent :',linear_mod.coef_)
    st.write('linear model intercept :',linear_mod.intercept_)
    fig= go.Figure()
    fig.add_trace(go.Scatter(x=new_data['Date'],
                             y=new_data['Predictions'],
                             name='Regressor'))
    fig.add_trace(go.Scatter(x=data['Date'],
                            y=data['Close'],
                            name='Closing Prices'))
    fig.layout.update(title_text='Predicted Price Series',xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)


plot_intercept()
plot_data()
                  

                  
                             

