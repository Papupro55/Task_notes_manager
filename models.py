#importamos SQL alchemy
from flask_sqlalchemy import SQLAlchemy


#db sera nuestro objeto que tenga los metodos de sql alchemy y nos ayude a manipular  la base de datos
db = SQLAlchemy()

#Tabla de tareas
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    descripcion = db.Column(db.String(500), nullable=False)
    fecha = db.Column(db.String(500), nullable=False)
    estado = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Task {self.task}>'
#tabla de notas
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(500), nullable=False)
    contenido = db.Column(db.String(10000), nullable=False)
    fecha = db.Column(db.String(500), nullable=False)
    estado = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Note {self.Note}>'
#clase de notas que usamos en el app.py para manejar y manipular datos
class Notes:
    def __init__(self):
        self.notes = []#inicializamos un arreglo para guardar las notas, sera usado para mandar los datos a la base de datos y tambien como 
                        #algo parecido a una memoria RAM
#ruta para añadir notas
    def add_notes(self,  titulo, contenido, fecha, estado):
        self.notes = []#inicializamos la lista vacia para no agregar notas repetidas cada que usemos este metodo
        task = { # le damos la estructua que queremos al arreglo donde se guardaran los valores obtenidos del front end
            'titulo': titulo,#variable titulo
            'contenido': contenido,
            'fecha': fecha,
            'estado': estado
        }
        self.notes.append(task)#finalmente agregamos los valores obtenidos a la lista
    
    def save_note_db(self):#metodo para guardar valores en la base de datos
        for note in self.notes:#iteramos sobre nuestro arreglo con las notas agregadas
            new_note = Note(titulo=note['titulo'], contenido=note['contenido'], fecha=note['fecha'], estado=note['estado'])#creamos una instancia de nuestro modelo de base de datos para guardar los datos del arreglo
            db.session.add(new_note)# agregamos los datos a la base de datos
            db.session.commit()#lo comiteamos
        self.note = []#volvemos a vaciar el arreglo para evitar guardar valores repetidos
    
    def load_notes(self):#metodo para cargar las notas en el index
        self.notes = []#inicializamos el arreglo
        all_notes = Note.query.all()#creamos un objeto con todos los datos que tengamos en la base de datos
        for note in all_notes:
            note_dict = {         #con note_dict le damos a los datos el formato de diccionario
                'id': note.id,
                'titulo': note.titulo,
                'contenido': note.contenido,
                'fecha': note.fecha,
                'estado': note.estado
            }                               
            self.notes.append(note_dict)# los guardamos en nuestro arreglo

    def delete_notes(self, note_id):#metodo para eliminar notas
        # Buscar la tarea en la lista de tareas pendientes
        note_to_delete = None # creamos el espacio para la nota 
        for note in self.notes:#iteramos sobre nuestro arreglo
            if note['id'] == int(note_id):#si la id obtenida es igual a una del arreglo
                note_to_delete = note# guardamos el campo en el objeto creado anteriormente
                break

        if note_to_delete:# si hay datos en el objeto
            # Actualizar en la base de datos
            note_in_db = Note.query.get(note_id)#obtenemos el id del objeto en la base de datos
            if note_in_db:#si se encuentra
                db.session.delete(note_in_db)#lo borramos de la base de datos
                db.session.commit()

              
                self.notes.remove(note_to_delete)#lo borramos tambien del arreglo para mantener la coherencia en los datos
                

    def edit_note(self, note_id, new_titulo, new_contenido, new_fecha):#meotod para editar notas
    #obtenemos el id y lo buscamos en el arreglo
        for note in self.notes:
            if note['id'] == int(note_id):#si se encuentra  el dato en el arreglo
               note['titulo'] = new_titulo # cambiamos todos los valores a los que obtengamos del front
               note['contenido'] = new_contenido
               note['fecha'] = new_fecha
               break
        
        # Y actualizamos los datos en la base de datos
        note_in_db = Note.query.get(note_id)
        if note_in_db:
            note_in_db.titulo = new_titulo
            note_in_db.contenido = new_contenido
            note_in_db.fecha = new_fecha
            db.session.commit()
                        


    
################################################################# clase tasks  #################################################################
# aqui esta clase y la de notes son muy parecidas ya que al hacer la primera ya teniamos todo lo necesatio para hacer la otra    
#clase tasks, nos ayuda a manejar todo lo relacionado con las tasks
class Tasks:
    def __init__(self):
        self.tasks = []
        self.completedTasks = []
#metemos todo en un arreglo con la forma de un diccionario manejando asi todo en memoria temporal
    def add_task(self, titulo, descripcion, fecha, estado):
        self.tasks = []
        task = {
            'titulo': titulo,
            'descripcion': descripcion,
            'fecha': fecha,
            'estado': estado
        }
        self.tasks.append(task)
#cargamos todas las tareas pendientes y no pendientes desde la base de datos   
    def load_tasks(self):
        self.tasks = []
        self.completedTasks = []
        all_tasks = Task.query.all()
        for task in all_tasks:
            task_dict = {
                'id': task.id,
                'titulo': task.titulo,
                'descripcion': task.descripcion,
                'fecha': task.fecha,
                'estado': task.estado
            }
            if task.estado:
                self.completedTasks.append(task_dict)
            else:
                self.tasks.append(task_dict)

#el arrelglo anterior lo usamos para guardar lo que se guarde en cada espacio en la base de datos
    def save_db(self):
        for task in self.tasks:
            new_task = Task(titulo=task['titulo'], descripcion=task['descripcion'], fecha=task['fecha'], estado=task['estado'])
            db.session.add(new_task)
            db.session.commit()
        self.tasks = []   #Vaciamos el arreglo para no guardar datos repetidos
# el eliminaddo de tareas funciona como un dequeue eliminando FIFO, agarramos la ultima tarea de la base de datos
# Y la eliminamos tanto de la base de datos como del arreglo

    def dequeue(self):#simulamos un dequeue obteniendo con sqlalchemy el ultimo dato ingresado
        last_task = Task.query.order_by(Task.id.desc()).first()
        
        if last_task:
        # Eliminar el registro de la base de datos
            db.session.delete(last_task)
            db.session.commit()
        #hacemos lo mimo con nuesto arreglo para mantener la coherencia en la estructura
        self.tasks = [t for t in self.tasks if t['id'] != last_task.id]

#Funcion que usaremos para manejar las tareas completadas
    def complete_task(self, task_id):
        # Buscar la tarea en la lista de tareas pendientes
        task_to_complete = None
        for task in self.tasks:
            if task['id'] == int(task_id):
                task_to_complete = task
                break

        if task_to_complete:
            # Actualizar en la base de datos
            task_in_db = Task.query.get(task_id)
            if task_in_db:
                task_in_db.estado = True
                db.session.commit()

                # Mover de "tasks" a "completedTasks"
                self.tasks.remove(task_to_complete)
                self.completedTasks.append(task_to_complete)

    def delete_completed_task(self, task_id):
        # Primero buscamos y eliminamos de la lista completedTasks
        task_to_delete = None
        for task in self.completedTasks:
            if task['id'] == int(task_id):
                task_to_delete = task
                break
        
        if task_to_delete:
            self.completedTasks.remove(task_to_delete)
            
            # Luego obtenemos y eliminamos el objeto real de la base de datos
            task_in_db = Task.query.get(task_id)  # Esto devuelve el objeto SQLAlchemy
            if task_in_db:
                db.session.delete(task_in_db)
                db.session.commit()