import os
import sys
import sqlite3
import webbrowser
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, session

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

template_dir = resource_path('templates')
data_dir = resource_path('Data')
DB_PATH = os.path.join(data_dir, 'usuarios.db')

app = Flask(__name__, template_folder=template_dir)
app.secret_key = 'sua_chave_secreta'

def conectar_bd():
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    return sqlite3.connect(DB_PATH)

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']

        conn = conectar_bd()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuarios WHERE usuario = ? AND senha = ?", (usuario, senha))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            error = 'Usuário ou senha inválidos.'

    return render_template('login.html', error=error)

@app.route('/home')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('home.html', usuario=session['usuario'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    def run_app():
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_app)
    flask_thread.daemon = True
    flask_thread.start()

    time.sleep(1.5)
    webbrowser.open("http://127.0.0.1:5000/")

    while True:
        time.sleep(1)
   