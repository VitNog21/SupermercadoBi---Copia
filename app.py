from flask import Flask, render_template, request, redirect, url_for, session
import pyodbc

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  


def conectar_bd():
    return pyodbc.connect(
      'DRIVER={ODBC Driver 18 for SQL Server};'
        'SERVER=VICTOR;'
        'DATABASE=API;'
        'UID=admin;'
        'PWD=admin;'
        'Encrypt=yes;'
        'TrustServerCertificate=yes;'  
    )

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
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
