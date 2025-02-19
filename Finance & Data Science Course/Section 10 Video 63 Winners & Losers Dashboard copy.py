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

def winners():
    highestret = df.nlargest(5, axis =1)
    return highestret.index()

def losers():
    lowestret = df.nsmallest(5, axis =1)
    return lowestret.index()


st.title('Winner & Losers Dashboard')

tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]['Symbol']
tickers = tickers.to_list()

dropdown = st.multiselect('Please Select Tickers: ', tickers)
begin = st.date_input('Start', value = pd.to_datetime('2000-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))
n = st.number_input("Please Provide Performance Horizon in Months:", min_value= 1, max_value= 24)

@st.cache_data
def get_data(dropdown, begin, end):
    df = yf.download(dropdown, start = begin, end = end)['Close']
    return df

df = get_data(dropdown, begin, end)

#Price plotting (not as relevant or comparable but good to have)
st.header('Price Plot: {}'.format(dropdown))
if len(dropdown)>0:
    st.line_chart(df)

# Cumulative Returns Plotting from Dropdown selection 
st.header('Cumilative Returns: {}'.format(dropdown))
if len(dropdown) > 0:
    st.line_chart(cumreturns(df))

