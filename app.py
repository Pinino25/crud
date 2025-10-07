from flask import Flask, render_template, request, redirect, url_for  # Importa las funciones principales de Flask
from flask_mysqldb import MySQL  # Importa la extensión para conectar Flask con MySQL

app = Flask(__name__)  # Crea una instancia de la aplicación Flask usando el nombre del módulo actual

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'  # Define el host donde está la base de datos MySQL
app.config['MYSQL_USER'] = 'root'  # Define el usuario de la base de datos
app.config['MYSQL_PASSWORD'] = ''  # Define la contraseña del usuario (vacía por defecto)
app.config['MYSQL_DB'] = 'datos_esc'  # Define el nombre de la base de datos a utilizar

mysql = MySQL(app)  # Inicializa la extensión MySQL con la aplicación Flask

# Ruta principal - Listar datos
@app.route('/')  # Define la ruta principal de la aplicación (página de inicio)
def index():
    """
    Muestra la lista de estudiantes desde la base de datos.
    """
    cur = mysql.connection.cursor()  # Crea un cursor para ejecutar consultas SQL
    cur.execute("SELECT * FROM estudiantes")  # Ejecuta una consulta para obtener todos los estudiantes
    data = cur.fetchall()  # Recupera todos los resultados de la consulta
    cur.close()  # Cierra el cursor
    return render_template('index.html', estudiantes=data)  # Renderiza la plantilla 'index.html' pasando los estudiantes

# Ruta para añadir un nuevo estudiante
@app.route('/add_student', methods=['POST'])  # Define la ruta para agregar estudiantes, solo acepta POST
def add_student():
    """
    Añade un nuevo estudiante a la base de datos.
    """
    if request.method == 'POST':  # Verifica que la solicitud sea POST
        nombre = request.form['nombre']  # Obtiene el nombre del formulario
        matricula = request.form['matricula']  # Obtiene la matrícula del formulario
        grupo = request.form['grupo']  # Obtiene el grupo del formulario
        edad = request.form['edad']  # Obtiene la edad del formulario
        direccion = request.form['direccion']  # Obtiene la dirección del formulario

        cur = mysql.connection.cursor()  # Crea un cursor para ejecutar consultas SQL
        cur.execute("INSERT INTO estudiantes (matricula, nombre, grupo, edad, direccion) VALUES (%s, %s, %s, %s, %s)",
                    (matricula, nombre, grupo, edad, direccion))  # Inserta un nuevo estudiante en la base de datos
        mysql.connection.commit()  # Confirma los cambios en la base de datos
        cur.close()  # Cierra el cursor
        return redirect(url_for('index'))  # Redirige a la página principal

# Ruta para obtener un estudiante por su ID y mostrar el formulario de edición
@app.route('/get_student/<string:id>')  # Define la ruta para obtener un estudiante por su matrícula
def get_student(id):
    """
    Obtiene los datos de un estudiante por su ID para mostrar en el formulario de edición.
    """
    cur = mysql.connection.cursor()  # Crea un cursor para ejecutar consultas SQL
    cur.execute("SELECT * FROM estudiantes WHERE matricula = %s", (id,))  # Consulta el estudiante por matrícula
    data = cur.fetchall()  # Recupera el resultado de la consulta
    cur.close()  # Cierra el cursor
    print(data[0])  # Imprime los datos del estudiante en consola (opcional)
    return render_template('edit.html', estudiante=data[0])  # Renderiza la plantilla de edición con los datos del estudiante

# Ruta para actualizar un estudiante
@app.route('/update_student/<string:id>', methods=['POST'])  # Define la ruta para actualizar un estudiante, solo acepta POST
def update_student(id):
    """
    Actualiza los datos de un estudiante en la base de datos.
    """
    if request.method == 'POST':  # Verifica que la solicitud sea POST
        nombre = request.form['nombre']  # Obtiene el nombre actualizado del formulario
        matricula = request.form['matricula']  # Obtiene la matrícula (no se usa en la consulta)
        grupo = request.form['grupo']  # Obtiene el grupo actualizado del formulario
        edad = request.form['edad']  # Obtiene la edad actualizada del formulario
        direccion = request.form['direccion']  # Obtiene la dirección actualizada del formulario

        cur = mysql.connection.cursor()  # Crea un cursor para ejecutar consultas SQL
        cur.execute("""
            UPDATE estudiantes
            SET nombre = %s,
                grupo = %s,
                edad = %s,
                direccion = %s
            WHERE matricula = %s
        """, (nombre, grupo, edad, direccion, id))  # Actualiza los datos del estudiante en la base de datos
        mysql.connection.commit()  # Confirma los cambios en la base de datos
        cur.close()  # Cierra el cursor
        return redirect(url_for('index'))  # Redirige a la página principal

# Ruta para eliminar un estudiante
@app.route('/delete_student/<string:id>')  # Define la ruta para eliminar un estudiante por matrícula
def delete_student(id):
    """
    Elimina un estudiante de la base de datos.
    """
    cur = mysql.connection.cursor()  # Crea un cursor para ejecutar consultas SQL
    cur.execute("DELETE FROM estudiantes WHERE matricula = %s", (id,))  # Elimina el estudiante por matrícula
    mysql.connection.commit()  # Confirma los cambios en la base de datos
    cur.close()  # Cierra el cursor
    return redirect(url_for('index'))  # Redirige a la página principal

if __name__ == '__main__':
    app.run(debug=True)  # Solo para desarrollo local
