from flask import Flask, request, render_template, Response, url_for, redirect, session, jsonify
from io import open
from datetime import datetime
import os
import json
from flask_wtf.csrf import CSRFProtect
from flask import g
from config import DevelomentConfig
from models import Profesores
from models_pizza import registro_pizza
from pizza import ordenes
import forms
import form_pizza
from flask import flash
from models import db
from models_pizza import db_pizza
from diccionarios_dias_mes import meses, dias
app = Flask(__name__)
app.config.from_object(DevelomentConfig)
csrf = CSRFProtect()
app.config['variable_universal'] = None

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
def before_request():
    g.variable_universal = None

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
    venta_s = 0
    valor = 0
    ingresos = 0
    subtotal = 0
    lista_o = []
    lista_f= []
    lista_p = []
    pedido = ""
    archivo_texto= ""
    t=""
    ig=""
    c=""
    s=""
    b=""
    i = registro_pizza.query.all()
    r = registro_pizza.query.limit(1)
    v = registro_pizza.query.limit(3)
    for p_costo in i:
        ingresos += p_costo.costo
    
    if request.method == 'POST':
        pizza1 = registro_pizza(nombre=pizza_forms.nombre.data,
                                telefono=pizza_forms.telefono.data,
                                direccion=pizza_forms.direccion.data,
                                tam_pizza=pizza_forms.t_pizza.data,
                                ingredientes=pizza_forms.ingredientes.data,
                                cantidad=pizza_forms.cantidad.data,
                                estatus="proceso",
                                create_date = pizza_forms.fecha.data)
        total = len(pizza1.ingredientes)
        if 'Chica' == pizza1.tam_pizza:
            total = (total * 10)
            subtotal = (total + 40)
        if 'Mediana' == pizza1.tam_pizza:
            total = (total * 10)
            subtotal = (total + 80)
        if 'Grande' == pizza1.tam_pizza:
            total = (total * 10)
            subtotal = (total + 120)
        if not pizza1.ingredientes:
          
          pizza1.ingredientes.append("Queso")
        
        t_ingredientes = ', '.join(pizza1.ingredientes)
        pizza1.ingredientes = t_ingredientes
        pizza1.costo = int(subtotal) * pizza1.cantidad
        print(subtotal)
        if "agregar" == request.form.get("agregar"):
          archivo_texto = open("ordenes_pedidos.txt", 'a')
          archivo_texto.write(pizza1.nombre+" "+pizza1.telefono+" "+pizza1.direccion+" "+pizza1.tam_pizza+" "+pizza1.ingredientes+" "+ str(pizza1.cantidad)+" "+str(pizza1.costo)+'\n')
          archivo_texto.close()
          archivo_texto = open("ordenes_pedidos.txt", 'r')
        for lineas in archivo_texto.readlines():
            valor += 1
            lista_o.append(lineas.rstrip().split())
            lista_f.append(lineas.rstrip().split())
        print(valor)
        if "Queso" == lista_f[0][5]:
          ig=lista_f[0][5]
          c = lista_f[0][6]
          s = int(lista_f[0][7])
          print(ig)
        if "Jamon" == lista_f[0][5]:
          ig=lista_f[0][5]
          c = lista_f[0][6]
          s = int(lista_f[0][7])
          print("cuando es queso",ig)
        if 'Piña' == lista_f[0][6]:
          ig = lista_f[0][5] +" "+ lista_f[0][6]
            
          c = lista_f[0][7]
          s = int(lista_f[0][8])
          print("cuando es pina",ig)
        if 'Champiñones' == lista_f[0][6]:
          ig = lista_f[0][5] +" "+ lista_f[0][6]
          c = lista_f[0][7]
          s = int(lista_f[0][8])
          print("cuando es champi",ig)
        t=lista_f[0][4]
        print(t)
        print(ig)
        print(c)
        print(s)
        print("valor",int(valor))
        #for item in range(len(lista_f)):
         #   pedido = ordenes(nombre=lista_f[item][0], telefono=lista_f[item][1], direccion=lista_f[item][2] + " " + lista_f[item][3], tam_pizza=lista_f[item][4].replace("(", ""), ingredientes=lista_f[item][5],cantidad=lista_f[item][6], costo=lista_f[item][7])
       
        if "agregar" == request.form.get("agregar"):
          print("agregar otro producto")
          
        
          lista_p.append(pizza1)
         
        
        db_pizza.session.add(pizza1)
        db_pizza.session.commit()       
       
        b = registro_pizza.query.filter(registro_pizza.estatus == 'proceso').all() 
        print(b)
        
        for p_costo in b:
            venta_s += p_costo.costo
        # Insert
        session["subt"] = venta_s
        session["total"] = ingresos
       
    return render_template("registro_pizza.html", form=pizza_forms, pizzas=r, total=ingresos, ventas=v, lista_pedidos= lista_p, t=t, i=ig, c=c, s=s, lista_pedido= lista_p, pedido_proceso=b , sub= venta_s)



@app.route('/pizzass', methods=("GET", "POST"))
def pizza():
    pizza_forms = form_pizza.UserForm(request.form)
    p = registro_pizza.query.all()
    print(p)
    return render_template('ABC_Pizzas.html', ventas=p, form=pizza_forms)

@app.route("/pizzas",methods=["GET","POST"])

def pedio():
    pedido = ""
    busqueda_pedido = ""
    lista_de_busqueda = []
    pizza_forms = form_pizza.UserForm(request.form)

    if request.method == 'POST':
        busqueda = pizza_forms.dia.data
        busqueda_lower = busqueda.lower()
        print(busqueda_lower)

        if busqueda_lower in meses:
            busqueda_pedido = meses.get(busqueda_lower)
            print(busqueda_pedido)
            pedido = registro_pizza.query.all()

            for item in pedido:
                print(item)
                if isinstance(item.create_date, str):
                    fecha_objeto = datetime.strptime(item.create_date, "%Y-%m-%d %H:%M:%S")
                else:
                    fecha_objeto = item.create_date

                mes = fecha_objeto.strftime("%B")
                print(mes)

                if mes == busqueda_pedido:
                    lista_de_busqueda.append(item)

        elif busqueda_lower in dias:
            busqueda_pedido = dias.get(busqueda_lower)
            print(busqueda_pedido)
            pedido = registro_pizza.query.all()

            for item in pedido:
                print(item)
                if isinstance(item.create_date, str):
                    fecha_objeto = datetime.strptime(item.create_date, "%Y-%m-%d %H:%M:%S")
                else:
                    fecha_objeto = item.create_date

                dia_semana = fecha_objeto.strftime("%A")
                print(dia_semana)

                if dia_semana == busqueda_pedido:
                    lista_de_busqueda.append(item)

        else:
            pedido = registro_pizza.query.filter(
                (registro_pizza.nombre.like(f"%{busqueda}%")) |
                (registro_pizza.telefono.like(f"%{busqueda}%")) |
                (registro_pizza.tam_pizza.like(f"%{busqueda}%")) |
                (registro_pizza.ingredientes.like(f"%{busqueda}%")) |
                (registro_pizza.cantidad.like(f"%{busqueda}%")) |
                (registro_pizza.costo.like(f"%{busqueda}%")) |
                (registro_pizza.create_date.like(f"%{busqueda}%"))
            )

            for item in pedido:
                lista_de_busqueda.append(item)

    return render_template("ABC_Pizzas.html", form=pizza_forms, busqueda=lista_de_busqueda)

@app.route('/proceso', methods=("GET", "POST"))
def proceso():

      pizza_forms = form_pizza.UserForm(request.form)
      v = registro_pizza.query.limit(3)
      m = registro_pizza.query.order_by(registro_pizza.id.desc()).first()
      print("prueba proceso",m)
      print("id", m.id)
      session["id"] = m.id
      pizza.estatus = "terminado" 
      b = registro_pizza.query.filter(registro_pizza.estatus == 'proceso').all()
      for pedidos in b:
        pedidos.estatus = "terminado"
        db_pizza.session.add(pedidos)
        db_pizza.session.commit()
        print("cambio de estatus a terminado")
      i = registro_pizza.query.all()
      ingresos = 0
      for p_costo in i:
            ingresos += p_costo.costo
      try:
        # Intenta eliminar el archivo
        os.remove('ordenes_pedidos.txt')
        print(f"El archivo  ha sido eliminado correctamente.")
      except OSError as e:
        # Maneja posibles errores al intentar eliminar el archivo
        print(f"No se pudo eliminar el archivo. Error: {e}")
        
      b = registro_pizza.query.filter(registro_pizza.estatus == 'proceso').all()
      return render_template('registro_pizza.html', form=pizza_forms, ventas=v,  pedido_proceso= b, total=ingresos)

@app.route("/eliminar_pizza", methods=("GET", "POST"))
def eliminar_pizza():
    u =0
    n=0
    pizza_forms = form_pizza.UserForm(request.form)
    print(request.method)
    if request.method == "GET":
        id = request.args.get('id')
        print("eliminar",id)
        pizza1 = db_pizza.session.query(registro_pizza).filter(
            registro_pizza.id == id).first()
        pizza_forms.id.data = request.args.get('id')
        pizza_forms.nombre.data = pizza1.nombre
        pizza_forms.telefono.data = pizza1.telefono
        pizza_forms.direccion.data = pizza1.direccion
        pizza_forms.t_pizza.data = pizza1.tam_pizza
        pizza_forms.ingredientes.data = pizza1.ingredientes
        pizza_forms.cantidad.data = pizza1.cantidad
        pizza_forms.fecha.data = pizza1.create_date
        numero = pizza_forms.telefono.data
        
        print(numero)
        va = request.args.get('eliminar')
        
        print(va)
        request.method = "POST"
        print(request.method)
    if request.method == "POST":
        id = pizza_forms.id.data
        pza = registro_pizza.query.filter(registro_pizza.id == id).first()
        print("prueba de nuemro",numero)
        db_pizza.session.delete(pza)
        db_pizza.session.commit()

    b = registro_pizza.query.filter(registro_pizza.estatus ==  "proceso").all()
    c = registro_pizza.query.all()
    v = registro_pizza.query.limit(3)
    for v_costo in c:
        u +=v_costo.costo
    for v_costo in b:
        n +=v_costo.costo
     
        
    return render_template('registro_pizza.html', form=pizza_forms, pedido_proceso=b, ventas=v, total=u, sub=n)

@app.route("/modificar_pizza", methods=("GET", "POST"))
def modificar_pizza():

    pizza_forms = form_pizza.UserForm(request.form)
    
    id = session("id", 0)
    pizza = db_pizza.session.query(registro_pizza).filter(registro_pizza.id == id).first()
    pizza.estatus = "terminado"
    print("paso por aqui")
    db_pizza.session.add(pizza)
    db_pizza.session.commit()
    
    return render_template('registros_pizza.html', form=pizza_forms)

if __name__ == "__main__":
    csrf.init_app(app)
    db_pizza.init_app(app)
    with app.app_context():
        db_pizza.create_all()
    app.run()
