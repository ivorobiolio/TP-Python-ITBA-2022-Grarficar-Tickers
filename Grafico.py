from sqlite3 import connect
import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt
from Fechas import ordenar_fecha


plt.style.use('ggplot')

def graficar(database,ticker,date_from,date_to,complete_name):
        con = connect(database)
        data = pd.read_sql(
                f"SELECT * FROM '{ticker}' WHERE Date BETWEEN '{date_from}' AND '{date_to}' ORDER BY Date ASC", con)
        data.Date = pd.to_datetime(data.Date)
        data = data.set_index('Date')



        titulo = ticker + ': ' + complete_name +' \n '  ' De ' + ordenar_fecha(date_from) + ' a ' + ordenar_fecha(date_to) +' \n ' "MACD - Cruce de Medías Móviles (4, 18 y 40 días)"


        #  MACD:


        exp12 = data['Close'].ewm(span=12, adjust=False).mean()
        exp26 = data['Close'].ewm(span=26, adjust=False).mean()
        macd = exp12 - exp26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal

        fb_green = dict(y1=macd.values, y2=signal.values, where=signal < macd, color="green", alpha=0.6,
                        interpolate=True)
        fb_red = dict(y1=macd.values, y2=signal.values, where=signal > macd, color="red", alpha=0.6,
                      interpolate=True)
        fb_green['panel'] = 1
        fb_red['panel'] = 1
        fb = [fb_green, fb_red]

        apds = [#mpf.make_addplot(exp12, color='yellow'),
                #mpf.make_addplot(exp26, color='white'),
                mpf.make_addplot(histogram, type='bar', width=0.7, panel=1,
                                 color='dimgray', alpha=1, secondary_y=True),
                mpf.make_addplot(macd, panel=1, color='green', secondary_y=False),
                mpf.make_addplot(signal, panel=1, color='red', secondary_y=False )]

        mc = mpf.make_marketcolors(up='tab:green', down='tab:red',
                                   edge='inherit',
                                   wick={'up': 'green', 'down': 'red'},
                                   volume='in',
                                   ohlc='i')
        s = mpf.make_mpf_style(base_mpf_style='nightclouds', marketcolors=mc)

        mpf.plot(data[date_from:date_to], type='candle', addplot=apds, figscale=1.4, figratio=(6, 8), title=titulo,
                 style=s, volume=True, volume_panel=2, panel_ratios=(6, 1, 1), mav=(4,18,40),
                 fill_between=fb, show_nontrading=False, ylabel='Precio en US$',
                 ylabel_lower = 'Volumen',
                 xrotation=90,
                 datetime_format='%d-%m-%y',
                 tight_layout=True,
                 fontscale=1,)







