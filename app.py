import os
import sys
import sqlite3
import webbrowser
import threading
import time
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

base_path = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(base_path, 'Data', 'usuarios.db')

def conectar_bd():
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
    data_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if not os.path.exists(DB_PATH):
        print(f"AVISO: Banco de dados não encontrado em '{DB_PATH}'. Se for o primeiro uso, um será criado se necessário.")

    def run_app():
        app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False)

    flask_thread = threading.Thread(target=run_app)
    flask_thread.daemon = True
    flask_thread.start()

    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000/")

    try:
        input("Servidor rodando. Pressione Enter para sair...\n")
    except KeyboardInterrupt:
        print("Servidor finalizado.")
        