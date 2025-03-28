
from flask import Flask, request, render_template 
from models import db, Tasks, Notes 


app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#inicializadosr de la base de datos
db.init_app(app)
#crea el archivo para la base de datos
with app.app_context():
    db.create_all() 

PapuTasks = Tasks() #Instacia del objeto tasks con las funciones necesarias para las rutas

@app.route("/") # ruta index donde se mostrara todas las notas y tareas
def index():
    PapuTasks.load_tasks()  # Cargar datos antes de mostrar
    PapuNotes.load_notes() # tambien mandamos los datos para poder usarlos con jinja
    return render_template('index.html', tasks=PapuTasks.tasks, completedTasks=PapuTasks.completedTasks, notes=PapuNotes.notes)
 
#ruta para añadir tareas
@app.route("/add", methods=["POST"])
def agregar():
    titulo = request.form['titulo']             #creamos un objeto de cada parametro obtenido del front End mediante los forms
    descripcion = request.form['descripcion']
    fecha = request.form['fecha']
    estado = False                              #inicializamos el estado en false para despues poder cambiarlo a true si es necesario

    PapuTasks.add_task(titulo, descripcion, fecha, estado)#añadimos la informacion a un arreglo
    PapuTasks.save_db()# guardamos los datos en la base de datos para tener persistencia de datos

    return index()  # devolvemos a ruta index para mostrar todos los datos

@app.route("/delete", methods=["POST"])# ruta para eliminar una tarea
def eliminar():
    PapuTasks.dequeue()# metodo de la clase tasks para hacer un dequeue de las tareas
    return index()

@app.route("/delete_complete", methods=["POST"])#ruta para elminar por id las tareas completadas
def eliminar_completa():
    task_id = request.form.get('completed_task_id')# obtenemos la id mediante un input en el front
    if task_id:#si obtenemos el dato, o sea si se pulsa el boton de borrar
        PapuTasks.delete_completed_task(task_id)#borramos la tarea con el id obtenido
    return index()


@app.route("/complete", methods=["POST"])# ruta para completar una tarea y mandarla al arreglo de tareas completadas
def completar():
    task_id = request.form.get('task_id')# parecido a eliminar solo que aqui en vez de eliminar la guardamos en un arreglo llamado completed_tasks
    if task_id:
        PapuTasks.complete_task(task_id)
    return index()

###################################################### rutas de las notas ######################################################
PapuNotes = Notes()#intanciamos la clase Notes en el objeto papunotas

@app.route("/add_notes", methods=["POST"])# ruta para agregar nota, similar a la de tareas
def agregar_nota():
    titulo = request.form['titulo']
    contenido = request.form['contenido']
    fecha = request.form['fecha']
    estado = False                # aqui el estado no se utiliza

    PapuNotes.add_notes(titulo, contenido, fecha, estado)
    PapuNotes.save_note_db()

    return index()

@app.route("/delete_notes", methods=["POST"])#ruta para borrar notas
def eliminar_nota():#aqui lo hacemos igual que en la ruta de tareas, aqui no implementamos un dequeue sino que se eliminan por id
    note_id = request.form.get('note_id')
    if note_id:
        PapuNotes.delete_notes(note_id)
        return index()
    
@app.route("/edit_note", methods=["POST"])#ruta para editar notas
def editar_nota():
    note_id = request.form.get('note_id')  #con este campo que viene desde el from y esta en el for que muestra las notas podemos obtener el id de cada nota
    titulo = request.form.get('titulo') # y tambien los datos de cada nota, se obtienen mediante los inputs que aqui obtenemos los editados
    contenido = request.form.get('contenido')
    fecha = request.form.get('edit_fecha')
    
    if note_id and titulo and contenido and fecha:#Si se obtienen todos los datos se guardan los cambios
        PapuNotes.edit_note(note_id, titulo, contenido, fecha)
    
    return index()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
        
