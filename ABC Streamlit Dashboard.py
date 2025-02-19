import pandas as pd
from pandas.tseries.offsets import DateOffset 
import numpy as np 
from matplotlib import pyplot as plt
import yfinance as yf 
import streamlit as st 
import statsmodels.api as sm
import statsmodels.formula.api as smf

#[theme]
#primaryColor="#7c4e1c"
#backgroundColor="#fffcf7"
#secondaryBackgroundColor="#c3b5a7"
#textColor="#7c4e1c"

st.title('ABC Companion Dashboard')

#Creating Functions to make my life easier
def cumreturns(df):
    r = df.pct_change()
    c = (r+1).cumprod()-1 
    c = c.fillna(0)
    return c

def plotprice(ticker):
    str(ticker)
    placeholder= yf.download(ticker)['Adj Close']
    return placeholder.plot(figsize = (16,9))

#Define some important variables
complist = ['SNY','PFE','AZN','VRTX','REGN','^DRG','ROG.SW','NVS','GSK','BAYRY','NVO','JNJ','ABT','ABBV','MRK','LLY','BMY','^GSPC']
Metrics  = ['sector','country','website','industry','grossMargins','ebitdaMargins','operatingMargins','ebitda','totalDebt','debtToEquity','beta','marketCap','payoutRatio','dividendYield','fiveYearAvgDividendYield','lastDividendValue','lastDividendDate','revenuePerShare','returnOnAssets','returnOnEquity','revenueGrowth','bookValue','priceToBook',]
start = st.date_input('Start', value = pd.to_datetime('2014-01-01'))
end = st.date_input('End', value = pd.to_datetime('today'))

#Setting up Data Table     
HH = pd.DataFrame()

for ticker in complist:
   HH[str(ticker)] = yf.Ticker(str(ticker)).info

HH = HH[HH.index.isin(Metrics)]

#Streamlit Set Up
dropdown = st.multiselect('Select Assets',complist)
OLSreg = st.selectbox('Select Explanatory Asset',complist)

#Cumulative returns Line Chart
if len(dropdown)>0:
    pricedf = yf.download(dropdown,start= start, end= end)['Adj Close']
    comprets = cumreturns(pricedf)
    st.header('Cumulative Returns: {}'.format(dropdown))
    st.line_chart(comprets)

#Period Cumulative return 
if len(dropdown) > 0:
    st.subheader('End of Period Cumulative Returns')
    st.write(comprets.tail(1))

#Sharpe Ratios
if len(dropdown) > 0:
    st.subheader('Sharpe Ratios')
    (pricedf.pct_change().mean())/(np.std(pricedf.pct_change()))

#Data Table
HH = pd.DataFrame()

for ticker in dropdown:
   HH[str(ticker)] = yf.Ticker(str(ticker)).info

HH = HH[HH.index.isin(Metrics)]

st.table(HH)

#Log Price Line Chart
if len(dropdown)>0:
    pricedf = np.log10(yf.download(dropdown,start= start, end= end)['Adj Close'])
    st.header('Log Prices: {}'.format(dropdown))
    st.line_chart(pricedf)

#Flat Price Line Chart
if len(dropdown)>0:
    pricedf = yf.download(dropdown,start= start, end= end)['Adj Close']
    st.header('Flat Prices: {}'.format(dropdown))
    st.line_chart(pricedf)

#Benchmark Volatility (normalised around 0) 
if len(dropdown) > 0:
    st.subheader(f'{OLSreg} As Benchmark Volatility (normalised around 0):')
    BenchmarkNormstd = np.std(yf.download(OLSreg,start= start, end= end)['Adj Close'].pct_change())
    st.write(BenchmarkNormstd)

#Period Volatility 
if len(dropdown) > 0:
    st.subheader('Period Volatility')
    normstd = np.std(pricedf.pct_change())
    st.write((normstd)/(BenchmarkNormstd))

#Finding ideal benchmakr with regression 
regression = pd.DataFrame()

regression['y'] = yf.download('SNY')['Adj Close'].pct_change().fillna(0)
regression['x'] = yf.download(OLSreg)['Adj Close'].pct_change().fillna(0)

if len(OLSreg) > 0 and len(dropdown) >0:
   st.subheader(f'Sanofi Regression against {OLSreg}')
   model = sm.OLS(regression['y'],regression['x']).fit()
   st.write(model.summary()) 
