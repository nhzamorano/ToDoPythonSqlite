import textwrap
import os
import csv 
from database import Create_db



class Tarea:
    def __init__(self, descripcion, categoria, detalles):
        self._descripcion = descripcion
        self._categoria = categoria 
        self._detalles = detalles 
        self._estado = 'Pendiente'

    #Getters
    @property
    def descripcion(self):
        '''
        Regresa la descripcion de la tarea
        '''
        return self._descripcion
    
    @property
    def categoria(self):
        '''
        Regresa la categoria de la tarea
        '''
        return self._categoria 
    
    @property
    def detalles(self):
        '''
        Regresa el detalle de la tarea
        '''
        return self._detalles
    
    @property
    def estado(self):
        '''
        Regresa el estado de la tarea
        '''
        return self._estado 
    
    #Setter
    @estado.setter
    def estado(self,nuevo_estado):
        '''
        Modificar el estado de la tarea
        '''
        self._estado = nuevo_estado

    #Mostrar tarea
    def mostrar(self):
        '''
        Mostrar informacion de la tarea
        '''
        ancho = 80
        str_detalles = f'Detalles: {self._detalles}'
        if len(str_detalles) > ancho:
            detalles = textwrap.fill(str_detalles, width=ancho)
        else:
            detalles = str_detalles 

        print('='*ancho)
        print(f'Tarea: {self._descripcion}')
        print('='*ancho)
        print(f'Categoria: {self._categoria}')
        print('.'*ancho)
        print(f'Estado: {self._estado}')
        print('.'*ancho)
        print(detalles)
        print('='*ancho)


class Administrador:
    def __init__(self):
        self._tareas = []
    
    @property
    def tareas(self):
        return self._tareas
    
    def mostrar(self,categoria=None):
        '''
        Mostrar la tarea en una tabla
        '''
        if len(self._tareas) != 0:
            ancho_col = 80
            
            #Encabezado
            formato_cols = '{0:<6} {1:<35} {2:<25} {3:<11}'
            print('='*ancho_col)
            print(formato_cols.format('ID', 'Tarea', 'Categoria', 'Estado'))
            print('='*ancho_col)

            #Imprimir tarea segun su categoria, si es none imprime todas
            if categoria == None:
                for ID, tarea in enumerate(self._tareas):
                    print(formato_cols.format(str(ID+1), tarea.descripcion,tarea.categoria, tarea.estado))
                    print('.'*ancho_col)
            else:
                for ID, tarea in enumerate(self.tareas):
                    if tarea.categoria == categoria:
                        print(formato_cols.format(str(ID+1), tarea.descripcion, tarea.categoria, tarea.estado))
                        print('.'*ancho_col)
        else:
            print('*** NO HAY TAREAS DISPONIBLES ***')
    
    def agregar_tarea(self, tarea):
        '''
        Agregar una tarea a la lista
        '''
        self._tareas.append(tarea)
    
    def actualizar_tarea(self, ID):
        '''
        Modificar una tarea segun su id
        '''
        if len(self._tareas) != 0:
            try:
                if self._tareas[ID-1].estado == 'Pendiente':
                    self._tareas[ID-1].estado = 'Completada'
                else:
                    self._tareas[ID-1].estado = 'Pendiente'
            except:
                print('*** NO EXISTE EL ID ESPECIFICADO ***')
        else:
            print('*** NO HAY TAREAS DISPONIBLES ***')

    def eliminar_tarea(self, ID):
        '''
        Eliminar una taerea segun su id
        '''
        if len(self._tareas) !=0:
            try:
                self._tareas.pop(ID-1)
            except:
                print(f'*** NO EXISTE EL ID {ID} ESPECIFICADO ***')
        else:
            print('*** NO HAY TAREAS DISPONIBLES ***')

    def detalle_tarea(self, ID):
        if len(self._tareas) != 0:
            try:
                self._tareas[ID-1].mostrar()
            except:
                print('*** NOEXISTE EL ID ESPECIFICADO ***')
        else: 
            print('*** NO HAY TAREAS DISPONIBLES ***')


class App:
    def __init__(self):
        self.db = Create_db()
        self._administrador = Administrador()
        self._abrir_base_datos()


    def _abrir_base_datos(self):
        #Verificar si el csv existe, si es asi crea la instancia administrador
        #y almacena el listado de tareas, de lo contrario crea el archivo vacio
        #db = Create_db()
        if os.path.isfile('./DB.sqlite3'):
            self._agregar_tareas()
            self._administrador.mostrar()
        
        #Ejecutar aplicativo despues de verificar existencia de archivo
        #self._ejecutar()


    def _agregar_tareas(self):
        tareas = self.db.listar_tareas()
        #print(tareas[0])
        #print(len(tareas))
        for t in tareas:
            #print(t[1])
            #print(t[2])
            #print(t[3])
            #print(t[4])
            #print('-----------------------------------------------------------------')
            tarea = Tarea(t[1],t[2],t[3])
            if t[4] == 'Completada':
                tarea.estado = 'Completada'
            self._administrador.agregar_tarea(tarea)
        """
        with open('./tareas.csv', 'r') as archivo:
            reader = csv.reader(archivo)
            
            for fila in reader:
                if len(fila) != 0:
                    tarea = Tarea(fila[0], fila[1], fila[2])
                    if fila[3] == 'Completada':
                        tarea.estado = 'Completada'
                    self._administrador.agregar_tarea(tarea)
        """    
    
    def _ejecutar(self):
        '''
        Interaccion co el usuario
        '''
        continuar = True 
        while continuar:
            print('\n\nSeleccione una opcion: ')
            print('   (1) Mostrar administrador de tareas')
            print('   (2) Agregar tarea')
            print('   (3) Actualizar tarea')
            print('   (4) Eliminar tarea')
            print('   (5) Ver detalle de una tarea')
            print('   (6) Salir')

            opcion = int(input('Opción: '))

            if opcion == 1:
                print('\n    Indique las categorias a mostrar: (a) todas, (b) filtrar')
                opcion_cat = input('    Opción:  ')
                if opcion_cat.lower() ==  'a':
                    self._administrador.mostrar()
                else:
                    print('\n   Especifique la categoria a mostrar: ')
                    cat = input('     Categoria: ')
                    self._administrador.mostrar(categoria=cat)
            elif opcion == 2:
                print('Informacion de la tarea a agregar: ')
                descripcion = input('Descripcion: ')
                categoria = input('Categoria: ')
                detalles = input('Detalles: ')
                tarea = Tarea(descripcion, categoria, detalles)
                self._administrador.agregar_tarea(tarea)
                self._administrador.mostrar()
            elif opcion == 3:
                self._administrador.mostrar()
                print('\nID de la tarea a actualizar: ')
                ID = int(input('ID: '))
                self._administrador.actualizar_tarea(ID)
                self._administrador.mostrar()
            elif opcion == 4:
                self._administrador.mostrar()
                print('\nID de la tarea a eliminar')
                ID = int(input('ID: '))
                respuesta = input('¡Seguro que desea eliminar la tarea? (S/N): ')
                if respuesta.lower() == 's':
                    self._administrador.eliminar_tarea(ID)
                self._administrador.mostrar()
            elif opcion == 5:
                self._administrador.mostrar()
                print('\nIntroduzca el ID de la tarea que quiere ver en detalle: ')
                ID = int(input('ID: '))
                self._administrador.detalle_tarea(ID)
            elif opcion == 6:
                continuar = False
                self._actualizar_base_datos()
                break
            else:
                print('Debe seleccionar una opecion entre 1 y 6')

            input('Presione una tecla para continuar...')
            os.system('cls')
    
    def _actualizar_base_datos(self):
        '''
        Actualiza el archivo csv con las tareas agregadas o modificadas durante la sesion
        '''
        #self.db.crear_tablas()
        with open('./tareas.csv', 'w') as archivo:
            writer = csv.writer(archivo)

            if len(self._administrador.tareas) != 0:
                for tarea in self._administrador.tareas:
                    #Mirar si es el salto de linea lo que genera en el csv una linea vacia
                    fila = [tarea.descripcion, tarea.categoria, tarea.detalles, tarea.estado]
                    writer.writerow(fila)
                    

if __name__ == "__main__":
    app = App()

