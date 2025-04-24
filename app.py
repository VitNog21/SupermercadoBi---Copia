import os
import sys
import sqlite3
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'


if getattr(sys, 'frozen', False):
    
    base_path = os.path.dirname(sys.executable)
else:
   
    base_path = os.path.dirname(__file__)

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
    if not os.path.exists(DB_PATH):
        print(f"❌ Banco de dados '{DB_PATH}' não encontrado.")
    else:
        import threading
        
        def run():
            app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False) 
        t = threading.Thread(target=run)
        t.start()

        webbrowser.open("http://127.0.0.1:5000/")
