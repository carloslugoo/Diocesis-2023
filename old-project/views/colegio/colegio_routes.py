from flask import Blueprint
from flask import render_template, session, jsonify, request, redirect, url_for
import mysql.connector
import datetime
import os
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="diocesis"
)

colegios_views = Blueprint('colegio', __name__, template_folder='templates')

@colegios_views.route('/home')
def home():
    usuario = session.get('user_data')
    #Query Actividades Que Participa (User)
    mycursor = mydb.cursor()
    query = "SELECT actividadxcolegio.id_actividad, titulo, fecha FROM actividadxcolegio, actividades WHERE escuela_id = %s and actividadxcolegio.id_actividad = actividades.id_actividad ORDER BY fecha DESC LIMIT 3"
    mycursor.execute(query, (usuario[3],))
    actividades = mycursor.fetchall()
    #Query Todas las Resoluciones (User)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM resoluciones ORDER BY date DESC LIMIT 3')
    resoluciones = mycursor.fetchall()
    #Query Todas las Actividades Disponibles / Por Participar (User)
    mycursor = mydb.cursor()
    query = "SELECT actividades.id_actividad, titulo, fecha FROM actividadxcolegio, actividades WHERE escuela_id = %s and actividadxcolegio.id_actividad != actividades.id_actividad ORDER BY fecha DESC LIMIT 3"
    mycursor.execute(query, (usuario[3],))
    disponibles = mycursor.fetchall()
    #print(disponibles)
    return render_template('home.html', user = usuario,actividades=actividades,resoluciones = resoluciones,disponibles= disponibles)

#Mis actividades
#Actividades
@colegios_views.route('/mis_actividades')
def mis_actividades():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  query = "SELECT actividadxcolegio.id_actividad, titulo, fecha FROM actividadxcolegio, actividades WHERE escuela_id = %s and actividadxcolegio.id_actividad = actividades.id_actividad"
  mycursor.execute(query, (usuario[3],))
  actividades = mycursor.fetchall()
  print(actividades)
  return render_template('mis_actividades.html', user = usuario, actividades = actividades)

#Actividades
@colegios_views.route('/actividades')
def actividades():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  mycursor.execute('SELECT * FROM actividades')
  actividades = mycursor.fetchall()
  return render_template('actividades.html', user = usuario, actividades = actividades)

#Ver actividad
@colegios_views.route('/ver_actividad/<int:id>')
def ver_actividad(id):
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  #query de info de actividad
  query = "SELECT id_actividad, titulo, descripcion, objetivos, fecha, nmb_admin FROM actividades, admin WHERE id_actividad = %s and admin.id_user = actividades.id_user"
  mycursor.execute(query, (id,))
  actividad = mycursor.fetchall()
  #print(actividad)
  #query de colegios adheridos
  query = "SELECT id_axc, actividadxcolegio.escuela_id, nmb_esc FROM actividadxcolegio, escuelas WHERE id_actividad = %s and actividadxcolegio.escuela_id = escuelas.escuela_id"
  mycursor.execute(query, (id,))
  colegios = mycursor.fetchall()
  print(colegios)
  #query para comprobar si ya adherio
  query = "SELECT id_axc, escuela_id FROM actividadxcolegio WHERE id_actividad = %s and escuela_id = %s"
  mycursor.execute(query, (id, usuario[3]))
  comp = mycursor.fetchall()
  return render_template('ver_actividad.html', user = usuario, actividad = actividad[0], colegios = colegios, comp = comp)

    
#Adherirse a la actividad COLEGIO
@colegios_views.route('/participar_actividad/<int:id>', methods=['POST'])
def participar_actividad(id):
  fecha_actual = datetime.datetime.now()
  # Formatea la fecha en el formato adecuado para SQL (YYYY-MM-DD HH:MM:SS)
  fecha_formateada = fecha_actual.strftime('%Y-%m-%d')
  usuario = session.get('user_data')
  print("actividad", id)
  mycursor = mydb.cursor()
  mycursor.execute('INSERT INTO actividadxcolegio (escuela_id, id_actividad, fecha_adherido) VALUES (%s, %s, %s)',
                        (usuario[3], id, fecha_formateada))
  mydb.commit()
  return jsonify({"message": "Exito"})


#Culminar actividad COLEGIO
@colegios_views.route('/culminar_actividad/<int:id>', methods=['GET', 'POST'])
def culminar_actividad(id):
  usuario = session.get('user_data')
  print(usuario)
  mycursor = mydb.cursor()
  #query para obtener los datos
  query = "SELECT * FROM actividades WHERE id_actividad = %s"
  mycursor.execute(query, (id,))
  datos = mycursor.fetchall()
  print(datos)
  if request.method == "POST":
    print(request.form['description'], request.files.getlist('archivo[]'))
    archivos = request.files.getlist('archivo[]')
    cant = 0 #cantidad de archivos
    for archivo in archivos:
      nombre, extension = os.path.splitext(archivo.filename)
      nombre = f"{datos[0][1]}_{usuario[1]}"
      archivo.filename = nombre + extension
      cant+= 1
      #print(archivo.filename)
      archivo.save('data/actividades_fotos/' + archivo.filename)
    fecha_actual = datetime.datetime.now()
    # Formatea la fecha en el formato adecuado para SQL (YYYY-MM-DD HH:MM:SS)
    fecha_formateada = fecha_actual.strftime('%Y-%m-%d')
    #guarda el registro de la actividad culminada
    mycursor.execute('INSERT INTO culminadoxcolegio (escuela_id, id_actividad,desc_f, fecha_f, cant_arch) VALUES (%s, %s, %s, %s, %s)',
                        (usuario[3], id,request.form['description'],fecha_formateada,cant))
    mydb.commit()
    #coloca el estado de la actividad en culminado
    query = "UPDATE actividadxcolegio SET estado = %s WHERE escuela_id = %s and id_actividad = %s"
    mycursor.execute(query, (1,usuario[3], id))
    mydb.commit()
    return redirect(url_for('colegios.culminar_activdad')) 
  return render_template('culminar_actividad.html', user = usuario, datos = datos[0])

#Resoluciones
@colegios_views.route('/resoluciones')
def resoluciones():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  mycursor.execute('SELECT * FROM resoluciones')
  resoluciones = mycursor.fetchall()
  return render_template('resoluciones.html', user = usuario, resoluciones = resoluciones)