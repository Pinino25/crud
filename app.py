import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'mysql+pymysql://root:@127.0.0.1:3306/datos_esc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ruta principal - Listar datos
@app.route('/')
def index():
    """
    Muestra la lista de estudiantes desde la base de datos.
    """
    estudiantes = db.session.execute("SELECT * FROM estudiantes").fetchall()
    return render_template('index.html', estudiantes=estudiantes)

# Ruta para añadir un nuevo estudiante
@app.route('/add_student', methods=['POST'])
def add_student():
    """
    Añade un nuevo estudiante a la base de datos.
    """
    if request.method == 'POST':
        nombre = request.form['nombre']
        matricula = request.form['matricula']
        grupo = request.form['grupo']
        edad = request.form['edad']
        direccion = request.form['direccion']

        db.session.execute("""
            INSERT INTO estudiantes (matricula, nombre, grupo, edad, direccion) VALUES (%s, %s, %s, %s, %s)
        """, (matricula, nombre, grupo, edad, direccion))
        db.session.commit()
        return redirect(url_for('index'))

# Ruta para obtener un estudiante por su ID y mostrar el formulario de edición
@app.route('/get_student/<string:id>')
def get_student(id):
    """
    Obtiene los datos de un estudiante por su ID para mostrar en el formulario de edición.
    """
    estudiante = db.session.execute("SELECT * FROM estudiantes WHERE matricula = %s", (id,)).fetchone()
    return render_template('edit.html', estudiante=estudiante)

# Ruta para actualizar un estudiante
@app.route('/update_student/<string:id>', methods=['POST'])
def update_student(id):
    """
    Actualiza los datos de un estudiante en la base de datos.
    """
    if request.method == 'POST':
        nombre = request.form['nombre']
        matricula = request.form['matricula']
        grupo = request.form['grupo']
        edad = request.form['edad']
        direccion = request.form['direccion']

        db.session.execute("""
            UPDATE estudiantes
            SET nombre = %s,
                grupo = %s,
                edad = %s,
                direccion = %s
            WHERE matricula = %s
        """, (nombre, grupo, edad, direccion, id))
        db.session.commit()
        return redirect(url_for('index'))

# Ruta para eliminar un estudiante
@app.route('/delete_student/<string:id>')
def delete_student(id):
    """
    Elimina un estudiante de la base de datos.
    """
    db.session.execute("DELETE FROM estudiantes WHERE matricula = %s", (id,))
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)