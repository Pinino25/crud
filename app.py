from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/datos_esc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Modelo ORM para la tabla 'estudiantes'
class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    matricula = db.Column(db.String(50), primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    grupo = db.Column(db.String(50))
    edad = db.Column(db.Integer)
    direccion = db.Column(db.String(200))

# Ruta principal - Listar datos
@app.route('/')  # Define la ruta principal de la aplicación (página de inicio)
def index():
    """
    Muestra la lista de estudiantes desde la base de datos.
    """
    estudiantes = Estudiante.query.all()  # Obtiene todos los registros como objetos Estudiante
    return render_template('index.html', estudiantes=estudiantes)  # Renderiza la plantilla 'index.html' pasando los estudiantes

# Ruta para añadir un nuevo estudiante
@app.route('/add_student', methods=['POST'])  # Define la ruta para agregar estudiantes, solo acepta POST
def add_student():
    """
    Añade un nuevo estudiante a la base de datos.
    """
    if request.method == 'POST':  # Verifica que la solicitud sea POST
        nombre = request.form.get('nombre')  # Obtiene el nombre del formulario
        matricula = request.form.get('matricula')  # Obtiene la matrícula del formulario
        grupo = request.form.get('grupo')  # Obtiene el grupo del formulario
        edad = request.form.get('edad') or None  # Obtiene la edad del formulario, o None si no se proporciona
        direccion = request.form.get('direccion')  # Obtiene la dirección del formulario

        nuevo = Estudiante(
            matricula=matricula,
            nombre=nombre,
            grupo=grupo,
            edad=int(edad) if edad else None,  # Convierte la edad a entero si se proporciona
            direccion=direccion
        )
        db.session.add(nuevo)  # Inserta un nuevo estudiante en la base de datos
        db.session.commit()  # Confirma los cambios en la base de datos
        return redirect(url_for('index'))  # Redirige a la página principal

# Ruta para obtener un estudiante por su ID y mostrar el formulario de edición
@app.route('/get_student/<string:id>')  # Define la ruta para obtener un estudiante por su matrícula
def get_student(id):
    """
    Obtiene los datos de un estudiante por su ID para mostrar en el formulario de edición.
    """
    estudiante = Estudiante.query.get(id)  # Consulta el estudiante por matrícula
    if not estudiante:
        return redirect(url_for('index'))  # Redirige si no se encuentra el estudiante
    return render_template('edit.html', estudiante=estudiante)  # Renderiza la plantilla de edición con los datos del estudiante

# Ruta para actualizar un estudiante
@app.route('/update_student/<string:id>', methods=['POST'])  # Define la ruta para actualizar un estudiante, solo acepta POST
def update_student(id):
    """
    Actualiza los datos de un estudiante en la base de datos.
    """
    estudiante = Estudiante.query.get(id)  # Consulta el estudiante por matrícula
    if not estudiante:
        return redirect(url_for('index'))  # Redirige si no se encuentra el estudiante

    estudiante.nombre = request.form.get('nombre')  # Obtiene el nombre actualizado del formulario
    estudiante.grupo = request.form.get('grupo')  # Obtiene el grupo actualizado del formulario
    edad = request.form.get('edad')  # Obtiene la edad actualizada del formulario
    estudiante.edad = int(edad) if edad else None  # Convierte la edad a entero si se proporciona
    estudiante.direccion = request.form.get('direccion')  # Obtiene la dirección actualizada del formulario

    db.session.commit()  # Confirma los cambios en la base de datos
    return redirect(url_for('index'))  # Redirige a la página principal

# Ruta para eliminar un estudiante
@app.route('/delete_student/<string:id>')  # Define la ruta para eliminar un estudiante por matrícula
def delete_student(id):
    """
    Elimina un estudiante de la base de datos.
    """
    estudiante = Estudiante.query.get(id)  # Consulta el estudiante por matrícula
    if estudiante:
        db.session.delete(estudiante)  # Elimina el estudiante de la sesión
        db.session.commit()  # Confirma los cambios en la base de datos
    return redirect(url_for('index'))  # Redirige a la página principal

if __name__ == '__main__':
    app.run(debug=True)  # Solo para desarrollo local
