import pandas as pd
import numpy as np
from sqlite3 import connect
import mplfinance as mpf

def graficar(database,ticker,date_from,date_to,complete_name):
        con = connect(database)
        data = pd.read_sql(
                f"SELECT * FROM '{ticker}' WHERE Date BETWEEN '{date_from}' AND '{date_to}' ORDER BY Date ASC", con)
        data.Date = pd.to_datetime(data.Date)
        data = data.set_index('Date')
        mc = mpf.make_marketcolors(up='tab:green', down='tab:red',
                                   wick={'up': 'green', 'down': 'red'},
                                   volume='gray', )
        titulo = ticker + ': ' + complete_name + ' De ' + date_from + ' a ' + date_to
        s = mpf.make_mpf_style(base_mpf_style="nightclouds", marketcolors=mc)
        mpf.plot(data[date_from:date_to],
                 type='candle',
                 style=s,
                 title=titulo,
                 ylabel='Precio en US$',
                 xrotation=0,
                 datetime_format='%d-%m-%y',
                 mav=(7),
                 figratio=(12, 8),
                 volume=True,
                 ylabel_lower='Volumen',)

def promedio_movil(lista,dias):
        promedio = [0.0 for i in range(len(lista))]
        for i in range(dias):
                promedio[i] = round(np.average(lista[0:dias]), 2)
        for i in range(dias, len(lista)):
                promedio[i] = round(np.average(lista[i - dias + 1: i +1]),2)
        return promedio
