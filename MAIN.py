from Fechas import cambiar_fecha
from Fechas import ordenar_fecha
from Fechas import today
from Com_servidor import pedido_servidor
from Com_servidor import check_ticker_servidor
from Tablas import crear_tabla
from Tablas import insertar_lista_datos
from Tablas import convertir_datos
from Tablas import lista_de_tablas
from Tablas import fech_operador
from Tablas import nombre_accion
from Tablas import agregar_nombre_ticker
from Grafico import graficar
import time

database = 'polygon_proyecto.db'
nueva_accion = False
# SELECCIÓN DE OPCIÓN
opcion = 0
opcion2 = 0
while True:
    opcion = input('Seleccione una opción:\n1. Actualización de datos\n2. Visualización de datos\n')
    if opcion == '1' or opcion == '2': break
    else:
        time.sleep(1)
        print('Opción inválida')

# INGRESO DE TICKER
ticker = ''
if opcion == '1': opcion_palabra = 'actualizar'
else: opcion_palabra = 'visualizar'
while True:
    ticker = input('Ingrese Acción a '+ opcion_palabra +':\n').upper()

# Chequeo de Ticker en base de datos
# ------------------------------------------------------------------------- FORMULA
    ticker_list = lista_de_tablas(database)
    if ticker in ticker_list:
# ------------------------------------------------------------------------- FORMULA
        print(nombre_accion(database,ticker))
        time.sleep(1)
        print('En base de datos')
        nueva_accion = False
# ------------------------------------------------------------------------- FORMULA
        complete_name = nombre_accion(database,ticker)
        break
    else:
        print('Acción no econtrada en base de datos')
        time.sleep(1)
        print('Solicitado al servidor...')

# Chequeo de Ticker en servidor
# ------------------------------------------------------------------------------ FORMULA
        x = check_ticker_servidor(ticker)
        nueva_accion = True
        if len(x) > 0:
            complete_name = x[0]['name']
            print(complete_name)
            break
        else:
            print('Acción no encontrada en Servidor')
            time.sleep(1)

# INGRESO DE FECHAS CON VALIDACIÓN
if opcion == '1':
    date_from, date_to = '', ''
    ts_from, ts_to = 0, 0
    while True:
        try:
            date_from = input('Ingrese fecha inicial:\n')
            date_to = input('Ingrese fecha final:\n')
            # ------------------------------------------------------------------------------ FORMULA
            ts_from, date_from = cambiar_fecha(date_from)
            ts_to, date_to = cambiar_fecha(date_to)
        except:
            print('Formato de fecha inválido')
            continue
        if ts_to < ts_from:
            print('Rango de fecha inválido')
        else: break

    # CHEQUEO DE FECHAS EN BASE DE DATOS
    date_from1 = ''
    date_to1 = ''
    datos_ya_existentes = False
    if nueva_accion == False:
        # ------------------------------------------------------------------------------ FORMULA
        ts_min = fech_operador(database, ticker, 'min','Timestamp')
        ts_max = fech_operador(database, ticker, 'max','Timestamp')
        if ts_from >= ts_min and ts_to <= ts_max:
            print('Datos ya existentes en base de datos')
            time.sleep(1)
        else:
            if ts_from < ts_min:
                date_to1 = fech_operador(database, ticker, 'min','date')
                print('Actualizando base de datos',ticker,date_from,'-',date_to1)
                # PEDIDO AL SERVIDOR en fechas corregidas inserción en tabla
                #------------------------------------------------------------------------------ FORMULA
                result = pedido_servidor(ticker, date_from, date_to1)
                list_res = convertir_datos(result)
                insertar_lista_datos(ticker, list_res, database)
            if ts_to > ts_max:
                date_from1 = fech_operador(database, ticker, 'max','date')
                print('Actualizando base de datos', ticker, date_from1, '-', date_to)
                # PEDIDO AL SERVIDOR en fechas corregidas e inserción en tabla
                # ------------------------------------------------------------------------------ FORMULA
                result = pedido_servidor(ticker, date_from1, date_to)
                list_res = convertir_datos(result)
                insertar_lista_datos(ticker, list_res, database)
            time.sleep(1)
            print('Base de datos actualizada')

    else:
        agregar_nombre_ticker(database, ticker, complete_name)
        print('Solicitando Datos al servidor...')
        # PEDIDO AL SERVIDOR
        #------------------------------------------------------------------------------ FORMULA
        result = pedido_servidor(ticker,date_from,date_to)
        list_res = convertir_datos(result)

        # CREAR TABLA (si no existe) e IMPORTAR DATOS A LA BASE (si no están)
        #------------------------------------------------------------------------------ FORMULA
        crear_tabla(ticker,database)
        insertar_lista_datos(ticker,list_res,database)
        time.sleep(1)
        print('Base de datos actualizada')

# OPCIÓN VISUALIZACIÓN DE DATOS
else:
    while True:
        opcionV = input('Seleccione la opción de visualización:\n1. Resumen\n2. Gráfico\n')
        if opcionV == '1' or opcionV == '2': break
        else: print('Opción inválida')
    if opcionV == '2':
        # INGRESO NUEVO A GRAFICAR (si no está en la base de datos)
        if nueva_accion == True:
            agregar_nombre_ticker(database, ticker, complete_name)
            print('Solicitando datos al servidor...')
            lista = pedido_servidor(ticker, '2000-01-01', today())
            list_res = convertir_datos(lista)
            print('Actualizando base de datos...')
            crear_tabla(ticker, database)
            insertar_lista_datos(ticker, list_res, database)
            print('Base de datos actualizados correctamente')

    # GRAFICO DEL RANGO DE FECHAS
        #------------------------------------------------------------------------------ FORMULA
        date_from = fech_operador(database, ticker, 'min','date')
        date_to = fech_operador(database, ticker, 'max','date')
        graficar(database,ticker,date_from,date_to,complete_name)

# RESUMEN DE TICKER EN BASE D EDATOS
    else:
        time.sleep(1)
        tablas = sorted(lista_de_tablas(database))
        print('Acción'.ljust(8)+'Rango de fechas')
        for i in tablas:
            if i == 'Tickers': pass
            else:
                try:
                    min = ordenar_fecha(fech_operador(database, i, 'min','date'))
                    max = ordenar_fecha(fech_operador(database, i, 'max','date'))
                    print((i + ':').ljust(8) + min + ' <==> ' + max)
                except:
                    print((i + ':').ljust(8) + 'Sin valores')