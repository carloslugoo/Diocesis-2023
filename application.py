from flask import Flask, url_for, redirect, render_template, request, session, jsonify
from config import DevConfig

#Encriptar la pass
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

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
    return render_template('./admin_views/home.html', user = usuario)
  else:
     return render_template('./colegios_views/home.html', user = usuario)
  
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
  query = "SELECT id_actividad, titulo, descripcion, objetivos, fecha, nmb_admin FROM actividades, admin WHERE id_actividad = %s and admin.id_user = actividades.id_user"
  mycursor.execute(query, (id,))
  actividad = mycursor.fetchall()
  print(actividad)
  return render_template('ver_actividad.html', user = usuario, actividad = actividad[0])

@app.route('/borrar_actividad/<int:id>', methods=['DELETE'])
def borrar_actividad(id):
  print("Borrar actividad", id)
  mycursor = mydb.cursor()
  query = "DELETE FROM actividades WHERE id_actividad = %s"
  mycursor.execute(query, (id,))
  mydb.commit()
  return jsonify({"message": "Actividad borrada exitosamente"})

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