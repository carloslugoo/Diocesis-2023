from flask import Blueprint
from flask import url_for, redirect, render_template, request, session,jsonify
#Encriptar la pass
from werkzeug.security import generate_password_hash
import mysql.connector
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="diocesis"
)

admin_views = Blueprint('admin', __name__, template_folder='templates')

@admin_views.route('/home')
def home():
    usuario = session.get('user_data')
    #print(usuario)
    #Query Todas las Actividades (Admin)
    usuario = session.get('user_data')
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM actividades ORDER BY fecha DESC LIMIT 5')
    actividades = mycursor.fetchall()
    #Query Todas las Instituciones (Admin)
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM escuelas')
    colegios = mycursor.fetchall()
    mycursor = mydb.cursor()
    #Query Todas las Resoluciones (Admin)
    mycursor.execute('SELECT * FROM resoluciones ORDER BY date DESC LIMIT 3')
    resoluciones = mycursor.fetchall()   
    return render_template('home.html', user = usuario, actividades = actividades, colegios = colegios,resoluciones = resoluciones)

#Ver actividad
@admin_views.route('/ver_actividad/<int:id>')
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

@admin_views.route('/borrar_actividad/<int:id>', methods=['DELETE'])
def borrar_actividad(id):
  print("Borrar actividad", id)
  mycursor = mydb.cursor()
  query = "DELETE FROM actividades WHERE id_actividad = %s"
  mycursor.execute(query, (id,))
  mydb.commit()
  query = "DELETE FROM actividadxcolegio WHERE id_actividad = %s"
  mycursor.execute(query, (id,))
  mydb.commit
  return jsonify({"message": "Actividad borrada exitosamente"})


#Crear actividad Admin
@admin_views.route('/crear_actividad', methods=['GET', 'POST'])
def crear_actividad():
  usuario = session.get('user_data')
  print(usuario)
  if request.method == 'POST':
      # Obtener los datos del formulario
      titulo = request.form['title']
      descripcion = request.form['description']
      objetivos = request.form['objectives']
      fecha_realizacion = request.form['date']
      mycursor = mydb.cursor()
      sql_insert = "INSERT INTO actividades (titulo, descripcion, objetivos, fecha, id_user) VALUES (%s, %s, %s, %s, %s)"
      valores = (titulo, descripcion, objetivos, fecha_realizacion, usuario[3])
      # Ejecuta la sentencia SQL
      mycursor.execute(sql_insert, valores)
      mydb.commit()
      return redirect(url_for('admin.actividades'))
  return render_template('crear_actividades.html', user = usuario)

#Resoluciones
@admin_views.route('/resoluciones')
def resoluciones():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  mycursor.execute('SELECT * FROM resoluciones')
  resoluciones = mycursor.fetchall()
  return render_template('resoluciones.html', user = usuario, resoluciones = resoluciones)


@admin_views.route('/cargar_resolucion', methods=['GET', 'POST'])
def cargar_resolucion():
  usuario = session.get('user_data')
  print(usuario)
  if request.method == 'POST':
      # Obtener los datos del formulario
      titulo = request.form['title']
      descripcion = request.form['description']
      objetivos = request.form['objectives']
      fecha_realizacion = request.form['date']
      mycursor = mydb.cursor()
      sql_insert = "INSERT INTO actividades (titulo, descripcion, objetivos, fecha, id_user) VALUES (%s, %s, %s, %s, %s)"
      valores = (titulo, descripcion, objetivos, fecha_realizacion, usuario[3])
      # Ejecuta la sentencia SQL
      mycursor.execute(sql_insert, valores)
      mydb.commit()
      return redirect(url_for('admin.actividades'))
  return render_template('crear_resolucion.html', user = usuario)

#Borrar resolucion ADMIN
@admin_views.route('/borrar_resolucion/<int:id>', methods=['DELETE'])
def borrar_resolucion(id):
  print("Borrar resolucion", id)
  mycursor = mydb.cursor()
  query = "DELETE FROM resoluciones WHERE id_res = %s"
  mycursor.execute(query, (id,))
  mydb.commit()
  return jsonify({"message": "Resolucion borrada exitosamente"})

# Ruta para cargar el archivo
#Subir resoluciones #ADMIN
@admin_views.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
      import datetime
      # Obtener los datos del formulario
      titulo = request.form['title']
      descripcion = request.form['description']
      usuario = session.get('user_data')
      # Obtén la fecha y hora actual
      fecha_actual = datetime.datetime.now()
      # Formatea la fecha en el formato adecuado para SQL (YYYY-MM-DD HH:MM:SS)
      fecha_formateada = fecha_actual.strftime('%Y-%m-%d')
      if 'archivo' not in request.files:
          return jsonify({"error": "Error de archivo"}), 400  # 400: Bad Request
      archivo = request.files['archivo']
      if archivo.filename == '':
          return jsonify({"error": "Nombre de archivo vacío"}), 400  # 400: Bad Request
      if archivo and archivo.filename.endswith('.pdf'):
          archivo.save(os.path.join('resoluciones', archivo.filename))
          mycursor = mydb.cursor()
          mycursor.execute('INSERT INTO resoluciones (id_user, filename, titulo, des, date) VALUES (%s, %s, %s, %s, %s)',
                          (usuario[3], archivo.filename, titulo, descripcion, fecha_formateada))
          mydb.commit()
          return jsonify({"message": "Archivo cargado exitosamente"}), 200  # 200: OK
      else:
          return jsonify({"error": "Formato de archivo inválido"}), 415  # 415: Unsupported Media Type
      
#Crear colegio Admin
@admin_views.route('/crear_colegio', methods=['GET', 'POST'])
def crear_colegio():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  if request.method == 'POST':
      # Obtener los datos del formulario
      nombre = request.form['name']
      telefono = request.form['tel']
      celular = request.form['phone']
      email = request.form['email']
      direccion = request.form['address']
      encargado = request.form['user_asig']
      sql_insert = f"INSERT INTO escuelas (nmb_esc, tel_escu, celu_esc, email_esc, direc_esc, id_user) VALUES ('{nombre}',{telefono},{celular},'{email}','{direccion}',{encargado})"
      # Ejecuta la sentencia SQL
      mycursor.execute(sql_insert)
      mydb.commit()
      return redirect(url_for('admin.colegios'))
  mycursor.execute('SELECT id_user,user FROM usuarios WHERE id_tipo_user !=2 and id_user not in (SELECT DISTINCT id_user FROM escuelas)')
  usuarios = mycursor.fetchall()
  print(usuarios)
  return render_template('crear_colegio.html', user = usuario, usuarios = usuarios)

#Colegios
#Listar Colegios
@admin_views.route('/colegios')
def colegios():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  mycursor.execute('SELECT * FROM escuelas')
  res = mycursor.fetchall()
  i = 0
  colegios = []
  for col in res:
    i += 1
    col = (*col, i)
    colegios.append(col)
  print(colegios)
  return render_template('colegios.html', user = usuario, colegios = colegios)

#Ver Colegio
@admin_views.route('/ver_colegio/<int:id>')
def ver_colegio(id):
  #Query para Obtener Colegio (id)
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  query = "SELECT nmb_esc, tel_escu, celu_esc, email_esc, direc_esc, user FROM escuelas, usuarios WHERE escuela_id = %s and escuelas.id_user=usuarios.id_user"
  mycursor.execute(query, (id,))
  colegio = mycursor.fetchone()
  print(colegio)
  return render_template('ver_colegio.html', user = usuario, colegio = colegio, personal = "")

#Cuentas (Configuracion de Colegios y Usuarios)
@admin_views.route('/panelcuentas')
def cuentas():
  usuario = session.get('user_data')
  #Usuarios No Asignados a Ninguna Escuela
  mycursor = mydb.cursor()
  mycursor.execute("SELECT usuarios.id_user, usuarios.user, usuarios.id_tipo_user FROM usuarios WHERE usuarios.id_user NOT IN ( SELECT escuelas.id_user FROM escuelas WHERE escuelas.id_user IS NOT NULL);")
  usuarios = mycursor.fetchall()
  #Escuelas con sus Usuarios Asignados
  mycursor = mydb.cursor()
  mycursor.execute('SELECT escuelas.nmb_esc, usuarios.user FROM usuarios INNER JOIN escuelas ON usuarios.id_user = escuelas.id_user;')
  colegios = mycursor.fetchall()
  return render_template('panel_cuentas.html',user = usuario, usuarios = usuarios, colegios = colegios)

@admin_views.route('/add_user', methods=['POST', 'GET'])
def add_user():
  usuario = session.get('user_data')
  if request.method == 'POST':
        user_save = request.form.get('Nombre_Usuario')
        contrasena = request.form.get('Contrasena_Usuario')
        tipo_usuario = request.form.get('Tipo_Usuario')
        contrasena_hash = createpassword(contrasena)
        print(user_save, contrasena, tipo_usuario,contrasena_hash)
        mycursor = mydb.cursor()
        query = "INSERT INTO usuarios (user, password, id_tipo_user) VALUES (%s, %s, %s)"
        user_datos = (user_save, contrasena_hash,tipo_usuario)
        # Ejecuta la sentencia SQL
        mycursor.execute(query, user_datos)
        mydb.commit()
  return redirect(url_for('admin.cuentas'))

#Este no se va a ver, ya que van a tener cuentas creadas por defecto ya..
#@admin_views.route('/cargar_accs', methods=['POST', 'GET'])
def cargar_accs():
    usuario = request.form.get('usuario')
    contrasena = request.form.get('contrasena')
    if contrasena:
        encriptada = createpassword(contrasena)
        print(f'Usuario: {usuario}, Contraseña: {contrasena}, Encriptado {encriptada}')
        mycursor = mydb.cursor()
        mycursor.execute('INSERT INTO usuarios (user, password, id_tipo_user) VALUES (%s, %s, %s)',
                        (usuario,
                        encriptada, 1))
        mydb.commit()
        #Tipo usuario = 1 / Colegio
        print("Creado...")
    return render_template('./admin_views/cargar_accs.html')



def createpassword(password):
  return generate_password_hash(password)