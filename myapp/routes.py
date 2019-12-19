from myapp import app
from flask import render_template, request
import csv

#leer el fichero csv
fSales = open('./data/sales.csv', 'r')

csvreader = csv.reader(fSales, delimiter=',')
registros = []
for linea in csvreader:
    registros.append(linea)
    
cabecera = registros[0]
ventas = []
for datos in registros[1:]:
    d = {}
    for ix, nombre_campo in enumerate(cabecera):
        d[nombre_campo] = datos[ix]
    ventas.append(d)

@app.route('/')
def index():

    datos = {}
    for linea in ventas:
        if linea['region'] in datos:
            regAct = datos[linea['region']]
            regAct['ingresos_totales'] += float(linea['ingresos_totales'])
            regAct['beneficios_totales'] += float(linea['beneficio'])
        else:
            datos[linea['region']] = {'ingresos_totales': float(linea['ingresos_totales']), 'beneficios_totales': float(linea['beneficio'])}
    

    resultado = []
    for clave in datos:
        resultado.append((clave, datos[clave]))

    return render_template('index.html', registros=resultado)

@app.route('/detail/')
def detail():

    datos = {}
    region_name = request.values['region']
    for linea in ventas:
        if linea['region'] == region_name:
            if linea['pais'] in datos:
                regAct = datos[linea['pais']]
                regAct['ingresos_totales'] += float(linea['ingresos_totales'])
                regAct['beneficios_totales'] += float(linea['beneficio'])
            else:
                datos[linea['pais']] = {'ingresos_totales': float(linea['ingresos_totales']), 'beneficios_totales': float(linea['beneficio'])}


    return render_template('detail.html', region=region_name, registros=datos)