import pandas as pd
import yfinance as yf
from sqlalchemy import create_engine
from datetime import timedelta

def create_db(stock: str,):
    df = yf.download(stock, start= pd.to_datetime('today') - timedelta(7), interval= '1m')
    df.to_sql(f'{stock}', engine)
    return pd.read_sql(f'{stock}', engine)

def SQL_importer(stock, engine):
    try:    
        #updating a table already in DB
        max_date = pd.read_sql(f'Select max(Datetime) from {stock}', engine).values[0][0]
        df = yf.download(stock, start= pd.to_datetime('today') - timedelta(7), interval= '1m')
        new_values = df[df.index > max_date]
        new_values.to_sql(f'{stock}', if_exists = 'append')
        return print(f'{len(new_values)} new rows have been added since the last update at {max_date} in the database') 
    except:
        #create the table in DB if it doesn't exist
        create_db(stock)
        print(f'{stock} data was imported')

stock = input('Provide stock: ')
engine = create_engine(f'sqlite:///Intraday_DB.db')

