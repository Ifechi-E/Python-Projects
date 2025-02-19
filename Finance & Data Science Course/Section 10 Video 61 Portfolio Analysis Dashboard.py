import pandas as pd
from pandas.tseries.offsets import DateOffset 
import matplotlib.pyplot as plt
import numpy as np 
import streamlit as st 
import yfinance as yf 

st.title('Portfolio Analysis Dashboard')

assets = st.text_input('Provide Ticker Symbols Seperated by comas','TSLA, AAPL, INTC, MSFT, AMD')
start = st.date_input('Provide Analysis Start Date', value= pd.to_datetime('2020-01-01'))
df = yf.download(assets,start = start)['Adj Close']
benchmark = yf.download('^GSPC',start=start)['Adj Close']

#calculate portfolio cumulative returns
relret = df.pct_change()
cumret = (relret + 1).cumprod()-1
pcumret = cumret.mean(axis =1)

#setting up comparison to the SNP 500 as a benchmark
SNPcret = (benchmark.pct_change()+1).cumprod()-1
SNPstd =  benchmark.pct_change().std()

#weights vector as equaal weights portfolio & risk comparison 
w = np.ones(len(relret.cov())) / len(relret.cov())
pf_std = (w.dot(relret.cov()).dot(w))**(1/2)

#combining benchmark and portfolio df
tog = pd.concat([pcumret,SNPcret], axis = 1)
tog.columns = ['Portfolio Returns','SNP 500 Returns']

# Back end done, Streamlit setup 
st.line_chart(data = tog)
st.header('Portfolio vs Benchmark')

st.subheader('Portfolio Risk:')
pf_std # type: ignore

st.subheader('Benchmark Risk:')
SNPstd # type: ignore

st.subheader('Portfolio Composition:')
fig, ax = plt.subplots(facecolor = '#121212')
ax.pie(w, labels = relret.columns, autopct='%1.1f%%', textprops= {'color':'white'})

st.pyplot(fig)
