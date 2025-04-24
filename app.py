from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

DB_PATH = 'Data/usuarios.db'

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
        app.run(debug=True)
