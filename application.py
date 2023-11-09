from flask import Flask, url_for, redirect, render_template, request, session, jsonify, send_file, make_response
from config import DevConfig

#Encriptar la pass
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
import os

#SQL
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="diocesis"
)

application = app = Flask(__name__)

app.config.from_object(DevConfig)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        mycursor = mydb.cursor()
        usuario = request.form.get('usuario')
        contrasena = request.form.get('contrasena')
        print(f'Usuario: {usuario}, Contraseña: {contrasena}')
        aux = comprobarcuenta(usuario, contrasena)
        if aux:
          #print(aux)
          #comprobar si es admin o alguien de una escuela
          if int(aux[3]) == 2: #admin
            query = "SELECT id_admin, nmb_admin, admin.id_user, id_tipo_user FROM admin, usuarios WHERE admin.id_user = %s and admin.id_user = usuarios.id_user"
            mycursor.execute(query, (int(aux[0]),)) 
            data = mycursor.fetchall()
          else: #colegio
            query = "SELECT escuela_id, nmb_esc, escuelas.id_user, id_tipo_user FROM escuelas, usuarios WHERE escuelas.id_user = %s and escuelas.id_user = usuarios.id_user"
            mycursor.execute(query, (int(aux[0]),)) 
            data = mycursor.fetchall()
          print(data)
          session['user_data'] = data[0]
          return redirect(url_for('home'))
    return render_template('login.html')
  
def comprobarcuenta(user, pasw):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM usuarios WHERE user = %(username)s', {'username': user})
    data = mycursor.fetchall()
    if data:
      userdata = data[0]
      if userdata:
        passcheck = userdata[2]
      if userdata and check_password_hash(passcheck, pasw):
        #print("Acceso concedido...")
        return userdata
    else:
      #print("Malos credenciales...")
      return userdata

@app.route('/home')
def home():
  usuario = session.get('user_data')
  #print(usuario)
  if usuario[3] == 2:
    usuario = session.get('user_data')
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM actividades')
    actividades = mycursor.fetchall()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM escuelas')
    colegios = mycursor.fetchall()   
    return render_template('./admin_views/home.html', user = usuario, actividades = actividades, colegios = colegios)
  else:
     return render_template('./colegios_views/home.html', user = usuario)


#Mis actividades
#Actividades
@app.route('/mis_actividades')
def mis_actividades():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  query = "SELECT actividadxcolegio.id_actividad, titulo, fecha FROM actividadxcolegio, actividades WHERE escuela_id = %s and actividadxcolegio.id_actividad = actividades.id_actividad"
  mycursor.execute(query, (usuario[3],))
  actividades = mycursor.fetchall()
  print(actividades)
  return render_template('./colegios_views/mis_actividades.html', user = usuario, actividades = actividades)

#Actividades
@app.route('/actividades')
def actividades():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  mycursor.execute('SELECT * FROM actividades')
  actividades = mycursor.fetchall()
  return render_template('actividades.html', user = usuario, actividades = actividades)

#Ver actividad
@app.route('/ver_actividad/<int:id>')
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

@app.route('/borrar_actividad/<int:id>', methods=['DELETE'])
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


#Adherirse a la actividad COLEGIO
@app.route('/participar_actividad/<int:id>', methods=['POST'])
def participar_actividad(id):
  import datetime
  # Obtén la fecha y hora actual
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

#Crear actividad Admin
@app.route('/crear_actividad', methods=['GET', 'POST'])
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
      return redirect(url_for('actividades'))
  return render_template('./admin_views/crear_actividades.html', user = usuario)

#Resoluciones
@app.route('/resoluciones')
def resoluciones():
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  mycursor.execute('SELECT * FROM resoluciones')
  resoluciones = mycursor.fetchall()
  return render_template('resoluciones.html', user = usuario, resoluciones = resoluciones)

@app.route('/cargar_resolucion', methods=['GET', 'POST'])
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
      return redirect(url_for('actividades'))
  return render_template('./admin_views/crear_resolucion.html', user = usuario)
# Ruta para cargar el archivo
#Subir resoluciones #ADMIN
@app.route('/upload', methods=['POST'])
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

@app.route('/open_pdf/<filename>')
def open_pdf(filename):
    ruta_al_archivo = f"resoluciones/{filename}" 
    # Abre el archivo en una nueva pestaña
    response = make_response(send_file(ruta_al_archivo, as_attachment=False))
    response.headers['Content-Disposition'] = 'inline'
    return response
  
#Colegios
#Listar Colegios
@app.route('/colegios')
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

#Crear colegio Admin
@app.route('/crear_colegio', methods=['GET', 'POST'])
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
      sql_insert = f"INSERT INTO escuelas (nmb_esc, tel_escu, celu_esc, email_esc, direc_esc, id_user) VALUES ('{nombre}',{telefono},{celular},'{email}','{direccion}',{usuario[0]})"
      # Ejecuta la sentencia SQL
      mycursor.execute(sql_insert)
      mydb.commit()
      return redirect(url_for('colegios'))
  mycursor.execute('SELECT id_user,user FROM usuarios')
  users = mycursor.fetchall()
  return render_template('./admin_views/crear_colegio.html', user = usuario, users = users)

#Ver Colegio
@app.route('/ver_colegio/<int:id>')
def ver_coelgio(id):
  usuario = session.get('user_data')
  mycursor = mydb.cursor()
  #query de info de actividad
  query = f"SELECT nmb_esc, tel_escu, celu_esc, email_esc, direc_esc, user FROM escuelas, usuarios WHERE escuela_id = {id} and escuelas.id_user=usuarios.id_user"
  mycursor.execute(query)
  colegio = mycursor.fetchone()
  return render_template('ver_colegio.html', user = usuario, colegio = colegio, personal = "")


#Este no se va a ver, ya que van a tener cuentas creadas por defecto ya..
#@app.route('/cargar_accs', methods=['POST', 'GET'])
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

if __name__=='__main__':
    app.run(debug = True, port= 8000)