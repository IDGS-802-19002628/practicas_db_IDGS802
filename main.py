from flask import Flask, request, render_template, Response, url_for, redirect
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelomentConfig
from models import Profesores
from models_pizza import registro_pizza

import forms
import form_pizza
from flask import flash
from models import db
from models_pizza import db_pizza
app = Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/index", methods=["GET", "POST"])
def index():
    profe_form = forms.UserForm(request.form)

    if request.method == 'POST':
        profe = Profesores(nombre=profe_form.nombre.data,
                           telefono=profe_form.telefono.data,
                           sueldo=profe_form.sueldo.data,
                           tiempo=profe_form.tiempo.data,
                           materia=profe_form.materia.data)
        # Insert
        db.session.add(profe)
        db.session.commit()
        return redirect(url_for('ABCProfe'))
    return render_template("index.html", form=profe_form)


@app.route("/eliminar", methods=("GET", "POST"))
def eliminar():

    profe_form = forms.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get('id')
        profe1 = db.session.query(Profesores).filter(
            Profesores.id == id).first()
        profe_form.id.data = request.args.get('id')
        profe_form.nombre.data = profe1.nombre
        profe_form.telefono.data = profe1.telefono
        profe_form.sueldo.data = profe1.sueldo
        profe_form.tiempo.data = profe1.tiempo
        profe_form.materia.data = profe1.materia
    if request.method == "POST":
        id = profe_form.id.data
        profe = Profesores.query.get(id)
        db.session.delete(profe)
        db.session.commit()
        return redirect(url_for('ABCProfe'))
    return render_template('eliminar.html', form=profe_form)


@app.route("/ABC_profesores",  methods=("GET", "POST"))
def ABCProfe():
    profe_form = forms.UserForm(request.form)
    profesor = Profesores.query.all()
    return render_template('ABC_Profesores.html', profesor=profesor)


@app.route("/alumnos", methods=("GET", "POST"))
def alumnos():
    print('dentro de ruta 2')
    nom = ''
    apaterno = ''
    correo = ''
    alum_forms = forms.UserForm(request.form)
    if request.method == 'POST':
        nom = alum_forms.nombre.data
        apaterno = alum_forms.apaterno.data
        correo = alum_forms.email.data
        messages = 'Bienvenido {}'.format(nom)
        flash(messages)
        print("Nombre: {}".format(nom))
        print("apaterno: {}".format(apaterno))
        print("correo: {}".format(correo))
        print(alum_forms.validate())
    return render_template("alumnos.html", form=alum_forms, nom=nom, apa=apaterno, c=correo)


@app.route("/pizza", methods=["GET", "POST"])
def pz():
    pizza_forms = form_pizza.UserForm(request.form)
    total = 0
    ingresos = 0
    subtotal = 0
    p = registro_pizza.query.order_by(registro_pizza.create_date).all()
    r = registro_pizza.query.limit(1)
    v = registro_pizza.query.limit(3)
    for p_costo in p:
        ingresos += p_costo.costo
        print(p_costo.costo)
    print(ingresos)
    if request.method == 'POST':
        pizza1 = registro_pizza(nombre=pizza_forms.nombre.data,
                                telefono=pizza_forms.telefono.data,
                                tam_pizza=pizza_forms.t_pizza.data,
                                ingredientes=pizza_forms.ingredientes.data,
                                cantidad=pizza_forms.cantidad.data)

        total = len(pizza1.ingredientes)
        if 'Chica' == pizza1.tam_pizza:
            total = (total * 10)
            subtotal = (total + 40)
        t_ingredientes = ', '.join(pizza1.ingredientes)
        pizza1.ingredientes = t_ingredientes
        pizza1.costo = int(subtotal) * pizza1.cantidad
        print(subtotal)
        # Insert
        db_pizza.session.add(pizza1)
        db_pizza.session.commit()
        return redirect(url_for('pizza'))
    return render_template("registro_pizza.html", form=pizza_forms, pizzas=r, total=ingresos, ventas=v)


@app.route('/pizzas', methods=("GET", "POST"))
def pizza():

    p = registro_pizza.query.all()

    return render_template('ABC_Pizzas.html', ventas=p)

@app.route("/eliminar_pizza", methods=("GET", "POST"))
def eliminar_pizza():

    pizza_forms = form_pizza.UserForm(request.form)
    if request.method == "GET":
        id = request.args.get('id')
        pizza1 = db.session.query(registro_pizza).filter(
            registro_pizza.id == id).first()
        pizza_forms.id.data = request.args.get('id')
        pizza_forms.nombre.data = pizza1.nombre
        pizza_forms.telefono.data = pizza1.telefono
        pizza_forms.tam_pizza.data = pizza1.tam_pizza
        pizza_forms.ingredientes.data = pizza1.ingredientes
        pizza_forms.cantidad.data = pizza1.cantidad
        pizza_forms.costo.data = pizza1.costo
    if request.method == "POST":
        id = pizza_forms.id.data
        pza = registro_pizza.query.get(id)
        db.session.delete(pza)
        db.session.commit()
        return redirect(url_for('pizza'))
    return render_template('eliminar_pedido.html', form=pizza_forms)

if __name__ == "__main__":
    csrf.init_app(app)
    db_pizza.init_app(app)
    with app.app_context():
        db_pizza.create_all()
    app.run()
