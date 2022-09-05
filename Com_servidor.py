import requests as r

def pedido_servidor(ticker,date_from,date_to):
    results = []
    url = 'https://api.polygon.io/v2/aggs/ticker/'
    stocksT = ticker
    mult = '1'
    timestamp = 'day'
    adjusted = 'adjusted=true'
    sort = 'sort=desc'
    limit = '1000'
    apiKey = 'apiKey=LKm4RpgA9fMWn8ZD7vmz1D5WDyNJTiyv'
    x = r.get(url+stocksT+'/range/'+ mult+'/'+ timestamp+'/'+ date_from+'/'+date_to+'/?'+adjusted+'&'+sort+'&'+limit+'&'+apiKey)
    y = x.json()
    date = 0
    if str(x.status_code)[0] == '4':
        print('Hubo un Error')
    else:
        if y['queryCount'] == 0: print('Sin valores econtrados')
        else: results = y['results']
    return results

def check_ticker_servidor(name):
    pars = r.get('https://api.polygon.io/v3/reference/tickers?ticker='+name+'&active=true&sort=ticker&order=desc&limit=1000&apiKey=LKm4RpgA9fMWn8ZD7vmz1D5WDyNJTiyv')
    complete_name = pars.json()['results']
    return complete_name