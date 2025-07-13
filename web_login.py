import sqlite3
import hashlib
from flask import Flask, request, render_template_string

# --- Configuración de la app Flask ---
app = Flask(__name__)
PORT = 5800

# --- Base de datos SQLite ---
def crear_bd():
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            hash_clave TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# --- Guardar usuarios con hash ---
def agregar_usuarios():
    usuarios = {
        'Camilo Mora': 'camilo123',
        'Javier Muñoz': 'javier456',
        'Benjamin Lopez': 'benjamin789'
    }
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    for nombre, clave in usuarios.items():
        hash_clave = hashlib.sha256(clave.encode()).hexdigest()
        cursor.execute('INSERT INTO usuarios (nombre, hash_clave) VALUES (?, ?)', (nombre, hash_clave))
    conn.commit()
    conn.close()

# --- Validación de usuario desde el formulario web ---
def validar_usuario(nombre, clave):
    hash_input = hashlib.sha256(clave.encode()).hexdigest()
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE nombre = ? AND hash_clave = ?', (nombre, hash_input))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

# --- Interfaz web simple con Flask ---
HTML = '''
<!DOCTYPE html>
<html>
<head><title>Login Grupo</title></head>
<body>
    <h2>Iniciar Sesión</h2>
    <form method="POST">
        Nombre: <input type="text" name="nombre"><br><br>
        Contraseña: <input type="password" name="clave"><br><br>
        <input type="submit" value="Ingresar">
    </form>
    {% if mensaje %}
        <p><strong>{{ mensaje }}</strong></p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ''
    if request.method == 'POST':
        nombre = request.form['nombre']
        clave = request.form['clave']
        if validar_usuario(nombre, clave):
            mensaje = f'✅ Bienvenido, {nombre}'
        else:
            mensaje = '❌ Usuario o contraseña incorrecta'
    return render_template_string(HTML, mensaje=mensaje)

# --- Crear BD y agregar usuarios al ejecutar por primera vez ---
crear_bd()
agregar_usuarios()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
