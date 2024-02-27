from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField, RadioField, EmailField, IntegerField
from wtforms import validators

class UserForm(Form):
    id = IntegerField('id', [validators.number_range(min=1, max=20, message='valor no valido')])
    nombre = StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message="Ingresa nombre valido")
    ])
    telefono = StringField("Telefono",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message="Ingresa nombre valido")])
    tiempo = StringField("Tiempo",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message="Ingresa nombre valido")
    ])
    materia = StringField("Materia",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message="Ingresa nombre valido")
    ])
    
    sueldo = IntegerField('Sueldo', [
        validators.number_range(min=1, max=28, message="Valor no valido")
    ])

    radios = RadioField('Curso', choices=[('1', '1'), ('2','2'), ('3','3')])

    