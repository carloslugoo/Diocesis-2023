from flask import Flask, url_for, redirect, render_template, request, session
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
          print(aux)
          #comprobar si es admin o alguien de una escuela
          if int(aux[3]) == 2: #admin
            query = "SELECT * FROM admin WHERE id_user = %s"
            mycursor.execute(query, (int(aux[0]),)) 
            data = mycursor.fetchall()
          else: #colegio
            query = "SELECT * FROM escuelas WHERE id_user = %s"
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
        print("Acceso concedido...")
        return userdata
    else:
      print("Malos credenciales...")
      return userdata

@app.route('/home')
def home():
  usuario = session.get('user_data')
  print(usuario)
  return render_template('home.html', user = usuario)
#Este no se va a ver, ya que van a tener cuentas creadas por defecto ya..
@app.route('/cargar_accs', methods=['POST', 'GET'])
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
    return render_template('cargar_accs.html')

def createpassword(password):
  return generate_password_hash(password)

if __name__=='__main__':
    app.run(debug = True, port= 8000)