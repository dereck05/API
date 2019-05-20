from Endpoints import db


class Usuario(db.Model):
    __tablename__ = 'Usuario'

    nombre = db.Column(db.String(),primary_key=True)
    correo = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, nombre, correo, password):
        self.nombre = nombre
        self.correo = correo
        self.password = password

    def __repr__(self):
        return '<nombre {}>'.format(self.nombre)

    def serialize(self):
        return {
            'nombre': self.nombre,
            'correo': self.correo,
            'password': self.password
        }