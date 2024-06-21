from flask import Flask, url_for, redirect, render_template, request, session, send_file, make_response
from config import DevConfig

#Encriptar la pass
from werkzeug.security import generate_password_hash


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

#Vistas
from views.invitado.invitado_routes import invitados_views
from views.admin.admin_routes import admin_views
from views.colegio.colegio_routes import colegios_views
#rutas
app.register_blueprint(invitados_views, url_prefix='/', template_folder='views/invitado/templates') #usuario sin registrarse
app.register_blueprint(admin_views, url_prefix='/', template_folder='views/admin/templates') #admin
app.register_blueprint(colegios_views, url_prefix='/', template_folder='views/colegio/templates') #colegio

@app.route('/open_pdf/<filename>')
def open_pdf(filename):
    ruta_al_archivo = f"data/resoluciones/{filename}" 
    # Abre el archivo en una nueva pestaña
    response = make_response(send_file(ruta_al_archivo, as_attachment=False))
    response.headers['Content-Disposition'] = 'inline'
    return response
  

#Logout
@app.route('/logout')
def logout():
    session.pop('user_data', None)
    return redirect(url_for('invitados.login'))

def createpassword(password):
  return generate_password_hash(password)

if __name__=='__main__':
    app.run(debug = True, port= 8000)