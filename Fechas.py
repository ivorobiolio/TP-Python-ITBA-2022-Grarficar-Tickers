from datetime import datetime
import time

def cambiar_fecha(fech):
    s = ' '
    if '/' in fech: s = '/'
    elif '-' in fech: s = '-'
    elif '_' in fech: s = '_'
    fech = fech.split(s)
    for i in range(3):
        if len(fech[i]) == 1: fech[i] = '0' + fech[i]
    y1 = int(fech[0])
    m1 = int(fech[1])
    d1 = int(fech[2])
    if len(fech[2]) == 4:
        y1 = int(fech[2])
        d1 = int(fech[0])
    elif len(fech[2]) == 2 and len(fech[0]) == 2:
        y1 = int(fech[2]) + 2000
        d1 = int(fech[0])
        fech[2] = str(y1)
    ts = int(time.mktime(datetime(year=y1, month=m1, day=d1).timetuple()))
    if len(fech[0])==4: fech = '-'.join(fech)
    else: fech = fech[2] + '-' + fech[1] + '-' + fech[0]
    return ts,fech

def ordenar_fecha(date_yyyy_mm_dd_format):
    x = date_yyyy_mm_dd_format.split('-')
    x.reverse()
    date = '-'.join(x)
    return date

def today():
    hoy = str(datetime.today().strftime('%Y-%m-%d'))
    return hoy

