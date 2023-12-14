from flask import Blueprint
from flask import url_for, redirect, render_template, request, session
from werkzeug.security import check_password_hash
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="diocesis"
)

invitados_views = Blueprint('invitados', __name__, template_folder='templates')
#Aca debe ir el home sn login
@invitados_views.route('/')
def index():
    return redirect(url_for('invitados.login'))

@invitados_views.route('/login', methods=['POST', 'GET'])
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
          #print(data)
          aux = data[0]
          session['user_data'] = data[0]
          if aux[3] == 2: 
            return redirect(url_for('admin.home'))
          else:
            return redirect(url_for('colegio.home'))
          
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