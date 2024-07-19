import sqlite3

class Create_db:
    def __init__(self):
        self.conexion = sqlite3.connect('DB.sqlite3',check_same_thread=False)
        self.cursor = self.conexion.cursor()
    
    def crear_tablas(self):
        self.cursor.execute("""
                DROP TABLE IF EXISTS tareas;
            """)
        self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS tareas(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            tarea TEXT NOT NULL,
                            categoria TEXT NOT NULL,
                            detalles TEXT,
                            estado TEXT NOT NULL
                            );
""" )

    def listar_tareas(self):
        #self.conexion.row_factory = sqlite3.Row #Modo diccionario
        #self.cursor = self.conexion.cursor()
        self.cursor.execute("SELECT * FROM tareas;")
        tareas = list(self.cursor.fetchall())
        return tareas