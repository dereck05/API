from flask import Flask
import boto3
from io import *
from multiprocessing.pool import ThreadPool

import time


app = Flask(__name__)



@app.route('/a')
def carga():
    s3 = boto3.resource('s3')
    data = open('base.pl', 'rb')
    print(type(data))
    s3.Bucket('progralenguajes').put_object(Key='base.pl', Body=data)
    return 'cargado!'

@app.route('/modifica')
def modifica():
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes','base.pl').get()['Body'].read()

    string = 'String de pruebas'
    string = string.encode('utf-8')
    str2 = file+string
    io = BytesIO()
    io.write(str2)

    s3.Bucket('progralenguajes').put_object(Key='base.pl',Body=io.getvalue())

    return 'Modified'

@app.route('/')
def buscar():
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(consulta)
    #x= threading.Thread(target=consu()).start()
    x = async_result.get()
    print(x)
    return 'Consultado!'

def consulta():
    from pyswip import Prolog
    prolog = Prolog()
    #prolog.assertz('comida(a,b)')
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes', 'base.pl').get()['Body'].read().decode().replace('\n', '')
    cont = 0
    rule = ""
    lis = []
    while (cont < len(file)):
        while (file[cont] != '.'):
            rule += file[cont]
            cont += 1
        lis.append(rule)
        cont += 1
        rule = ""

    cont = 0
    while (cont < len(lis)):
        prolog.assertz(lis[cont])
        cont += 1
    x = list(prolog.query('comida(arroz,X,Y,Z,A)'))
    return x


if __name__ == '__main__':
    app.run()







