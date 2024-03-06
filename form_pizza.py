from wtforms import Form
from wtforms import StringField, TextAreaField, SelectField, RadioField, EmailField, IntegerField, SelectMultipleField
from wtforms import validators

class UserForm(Form):
    id = IntegerField('', [validators.number_range(min=1, max=20, message='valor no valido')])
    nombre = StringField("Nombre",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message="Ingresa nombre valido")
    ])
    telefono = StringField("Telefono",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message="Ingresa nombre valido")])
    direccion = StringField("Direccion",[
        validators.DataRequired(message='El campo es requerido'),
        validators.length(min=4, max=10, message="Ingresa nombre valido")
    ])
    t_pizza = RadioField('T Pizza', choices=[('Chica', 'Chica $40'), ('Mediana', 'Mediana $80'), ('Grande', 'Grande $120')])
    
    ingredientes = SelectMultipleField('Checkboxes', choices=[('Jamon', 'Jamon $10'), ('Piña', 'Piña $10'), ('Champiñones', 'Champiñones $10')])
    cantidad = IntegerField('Cantidad pizzas', [validators.DataRequired(message='El campo es requerido')])


    