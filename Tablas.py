import sqlite3 as sq
from datetime import datetime

def crear_tabla(name,base_de_datos):
    coneccion = sq.connect(base_de_datos)
    cursor = coneccion.cursor()
    cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {name} (
        Date TEXT PRIMARY KEY NOT NULL,
        Volume INTEGER,
        Val_W REAL NOT NULL,
        Open REAL NOT NULL,
        Close REAL NOT NULL,
        High REAL NOT NULL,
        Low REAL NOT NULL,
        Timestamp INTEGER NOT NULL,
        N INTEGER);
    ''')
    coneccion.commit()
    coneccion.close()

# Ingreso de datos a base y ordenamiento por fecha ascendiente
def insertar_lista_datos(name,lista_de_tuplas,base_de_datos):
    coneccion = sq.connect(base_de_datos)
    cursor = coneccion.cursor()
    cursor.executemany(
        f"INSERT OR IGNORE INTO {name} (Date, Volume, Val_W, Open, Close, High, Low, Timestamp, N) "
        f"VALUES (?,?,?,?,?,?,?,?,?)", lista_de_tuplas)
    coneccion.commit()
    coneccion.close()

def agregar_nombre_ticker(base_de_datos,name,complete_name):
    coneccion = sq.connect(base_de_datos)
    cursor = coneccion.cursor()
    cursor.execute(
        f"INSERT OR IGNORE INTO Tickers (Ticker, Complete_name) VALUES ('{name}','{complete_name}')")
    coneccion.commit()
    coneccion.close()

# Convertir datos pedidos en lista de tuplas
def convertir_datos(lista):
    lista_final = []
    if len(lista) > 0:
        for i in range(len(lista)):
            a = (str(datetime.fromtimestamp(float(lista[i]['t']) / 1000).strftime('%Y-%m-%d')), int(lista[i]['v']),
                 float(lista[i]['vw']), float(lista[i]['o']), float(lista[i]['c']), float(lista[i]['h']), float(lista[i]['l']),
                 int(lista[i]['t'])//1000, int(lista[i]['n']))
            lista_final += [tuple(a)]
    return lista_final

def lista_de_tablas(base_de_datos):
    con = sq.connect(base_de_datos)
    c = con.cursor()
    lista = c.execute(f"SELECT name FROM sqlite_master WHERE type='table';")
    data = []
    for i in lista:
        data += i
    con.close()
    return data

def fech_operador(base_de_datos,name,operador,col):
    con = sq.connect(base_de_datos)
    c = con.cursor()
    operador.upper()
    c.execute(f"SELECT {operador}({col}) FROM {name};")
    data_raw = c.fetchall()
    data = data_raw[0][0]
    con.close()
    return data

def nombre_accion(base_de_datos,name):
    coneccion = sq.connect(base_de_datos)
    cursor = coneccion.cursor()
    cursor.execute(f"SELECT Complete_name FROM Tickers WHERE Ticker='{name}'")
    data = cursor.fetchall()[0][0]
    return data




