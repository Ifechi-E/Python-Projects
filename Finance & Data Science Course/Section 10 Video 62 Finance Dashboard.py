import pandas as pd
from pandas.tseries.offsets import DateOffset 
import numpy as np 
import streamlit as st 
import yfinance as yf 

st.title('Finance Dashboard')

tickers = ('TSLA','AAPL','INTC','MSFT','AMD')
start = st.date_input('Start', value = pd.to_datetime('2000-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))

dropdown = st.multiselect('Select Assets',tickers)

#Price plotting (not as relevant or comparable but good to have)
if len(dropdown)>0:
    pricedf = yf.download(dropdown,start,end)['Adj Close']
    st.header('Cumilative Returns: {}'.format(dropdown))
    st.line_chart(pricedf)

#Cumulative Returns function 
def cumreturns(df):
    r = df.pct_change()
    c = (r+1).cumprod()-1 #-1 just centers the plot around 0
    c = c.fillna(0)
    return c

# Cumulative Returns Plotting from Dropdown selection 
if len(dropdown) > 0:
    retdf = cumreturns(yf.download(dropdown,start,end,)['Adj Close'])
    st.header('Cumilative Returns: {}'.format(dropdown))
    st.line_chart(retdf)



