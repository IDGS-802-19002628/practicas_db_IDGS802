from flask_sqlalchemy import SQLAlchemy
import datetime

db=SQLAlchemy()

class Profesores(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(50))
    telefono=db.Column(db.String(50))
    sueldo=db.Column(db.Integer)
    tiempo=db.Column(db.String(50))
    materia = db.Column(db.String(50))
    create_date=db.Column(db.DateTime, default=datetime.datetime.now)