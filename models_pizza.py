from flask_sqlalchemy import SQLAlchemy
import datetime

db_pizza=SQLAlchemy()

class registro_pizza(db_pizza.Model):
    id=db_pizza.Column(db_pizza.Integer, primary_key=True)
    nombre=db_pizza.Column(db_pizza.String(50))
    telefono=db_pizza.Column(db_pizza.String(50))
    direccion=db_pizza.Column(db_pizza.String(50))
    tam_pizza=db_pizza.Column(db_pizza.String(50))
    ingredientes=db_pizza.Column(db_pizza.String(50))
    cantidad = db_pizza.Column(db_pizza.Integer)
    estatus = db_pizza.Column(db_pizza.String(20))
    costo = db_pizza.Column(db_pizza.Integer)
    create_date=db_pizza.Column(db_pizza.DateTime)