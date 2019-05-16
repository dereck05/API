from flask import Flask
import boto3

from io import *




app = Flask(__name__)



@app.route('/')
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



if __name__ == '__main__':
    app.run()







