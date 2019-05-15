from flask import Flask
from pyswip import Prolog

prolog = Prolog()
prolog.consult("base.pl")
app = Flask(__name__)


@app.route('/')
def hello_world():
  
    x = list(prolog.query("comida(arroz,B)."))
    print(x)
    return 'hola'

if __name__ == '__main__':
    app.run()







