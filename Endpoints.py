from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
import boto3
import os
from io import *
from multiprocessing.pool import ThreadPool



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/usuarios'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

from Usuarios import Usuario

#Regla general: En todos los strings que sean parte de una direccion web, los espacios se representan como  -

@app.route('/')
def carga():
    s3 = boto3.resource('s3')
    data = open('base.pl', 'rb')
    s3.Bucket('progralenguajes').put_object(Key='base.pl', Body=data)
    return 'cargado!'

@app.route('/agregarReceta',methods=['GET','POST'])
def agregarReceta():
    receta = str(request.args.get('nombre').replace('-',' '))       #pendiente
    s3 = boto3.resource('s3')
    file = s3.Object('progralenguajes','base.pl').get()['Body'].read()
    string = 'String de pruebas'
    string = string.encode('utf-8')
    str2 = file+string
    io = BytesIO()
    io.write(str2)
    s3.Bucket('progralenguajes').put_object(Key='base.pl',Body=io.getvalue())
    return 'Modified'

@app.route('/buscar',methods=['GET','POST'])
def buscar():
    nombre= str(request.args.get('nombre').replace('-',' '))            #obtiene el string nombre de la direccion HTTP
    pool = ThreadPool(processes=5)                                      #inicializa el pool de hilos
    async_result = pool.apply_async(consulta_aux,("'"+nombre+"'",))         #inicia el hilo
    x = str(async_result.get())                                         #obtiene el resultado de la consulta prolog
    return x

def consulta_aux(nombre):
    from pyswip import Prolog
    prolog = Prolog()
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
    x = list(prolog.query('comida('+nombre+',X,Y,Z,A)'))
    return x

@app.route('/agregarUsuario',methods=['GET','POST'])
def agregarUsuario():
    nombre1 = str(request.args.get('nombre'))
    correo1 = str(request.args.get('correo'))
    password1 = str(request.args.get('password'))
    try:
        usuario = Usuario(              #crea el usuario
            nombre = nombre1,
            correo = correo1,
            password = password1
        )
        db.session.add(usuario)         #lo agrega a la BD
        db.session.commit()
        return 'Registrado!'
    except Exception as e:
        return str(e)




if __name__ == '__main__':

    app.run()







