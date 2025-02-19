import pandas as pd
from pandas.tseries.offsets import DateOffset 
import matplotlib.pyplot as plt
import numpy as np 
import streamlit as st 
from sympy import Symbol
import yfinance as yf 

def cumreturns(df):
    r = df.pct_change()
    c = (r+1).cumprod()-1 
    c = c.fillna(0)
    return c

def get_ret(df, n):
    prevprice = df[:df.index[-1]-DateOffset(months= n)].tail(1).squeeze()
    recentprice = df.loc[df.index[-1]]
    retdf = (recentprice / prevprice) -1
    return retdf, prevprice.name

@st.cache_data
def get_data(dropdown):
    df = yf.download(dropdown, start = "2020-01-01")['Close']
    return df

st.title('Winner & Losers Dashboard')

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']
tickers = tickers.to_list()

dropdown = st.multiselect('Please Select Tickers: ', tickers)
n = st.number_input('Please Provide the Performance Horizon in Months: ',min_value= 1,max_value= 24)

################################################################################
if len(dropdown) > 0:
    df = get_data(dropdown)
    df.index = pd.to_datetime(df.index)

#Price plotting (not as relevant or comparable but good to have)
    st.header('Price Plot: {}'.format(dropdown))
    st.line_chart(df)

# Cumulative Returns Plotting from Dropdown selection 
    st.header('Cumilative Returns: {}'.format(dropdown))
    st.line_chart(cumreturns(df))


    retdf, date = get_ret(df,n)

    winners, losers = retdf.nlargest(5), retdf.nsmallest(5)
    winners.name, losers.name = 'Winners','Losers'
    w = winners.index.to_list()
    l = losers.index.to_list() 
    w.extend(l)

    st.table(winners)
    st.table(losers)

    st.header('Visulaise Key Performers')
    selection = st.multiselect("Select Performers to Visulaised",w)
    st.line_chart(cumreturns(df[w][date:]))