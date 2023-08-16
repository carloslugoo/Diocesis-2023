from flask import Flask, url_for, redirect, render_template
from config import DevConfig


application = app = Flask(__name__)

app.config.from_object(DevConfig)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

if __name__=='__main__':
    app.run(debug = True, port= 8000)