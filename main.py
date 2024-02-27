from flask import Flask, request, render_template, Response
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelomentConfig
from models import Profesores

import forms
from flask import flash
from models import db
app = Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf = CSRFProtect()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/index", methods=["GET", "POST"])
def index():
    profe_form = forms.UserForm(request.form)

    if request.method == 'POST' :
        profe = Profesores(nombre=profe_form.nombre.data,
                       telefono=profe_form.telefono.data,
                       sueldo=profe_form.sueldo.data,
                       tiempo = profe_form.tiempo.data,
                       materia = profe_form.materia.data)
        # Insert
        db.session.add(profe)
        db.session.commit()
    return render_template("index.html", form=profe_form)

@app.route("/ABC_profesores",  methods=("GET", "POST"))
def ABCProfe():
    profe_form = forms.UserForm(request.form)
    profesor= Profesores.query.all()
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


if __name__ == "__main__":
    csrf.init_app(app)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    app.run()
