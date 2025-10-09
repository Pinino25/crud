from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambiar si tienes contraseña
app.config['MYSQL_DB'] = 'datos_esc'

mysql = MySQL(app)

# Ruta principal - Listar datos
@app.route('/')
def index():
    """
    Muestra la lista de estudiantes desde la base de datos.
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM estudiantes")  # Asegúrate de que la tabla se llame 'estudiantes'
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', estudiantes=data)

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

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO estudiantes (matricula, nombre, grupo, edad, direccion) VALUES (%s, %s, %s, %s, %s)",
                    (matricula, nombre, grupo, edad, direccion))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

# Ruta para obtener un estudiante por su ID y mostrar el formulario de edición
@app.route('/get_student/<string:id>')
def get_student(id):
    """
    Obtiene los datos de un estudiante por su ID para mostrar en el formulario de edición.
    """
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM estudiantes WHERE matricula = %s", (id,))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', estudiante=data[0])

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

        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE estudiantes
            SET nombre = %s,
                grupo = %s,
                edad = %s,
                direccion = %s
            WHERE matricula = %s
        """, (nombre, grupo, edad, direccion, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

# Ruta para eliminar un estudiante
@app.route('/delete_student/<string:id>')
def delete_student(id):
    """
    Elimina un estudiante de la base de datos.
    """
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM estudiantes WHERE matricula = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)