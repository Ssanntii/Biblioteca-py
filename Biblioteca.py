import mysql.connector as mysql
import os
from datetime import datetime, timedelta
from mysql.connector import Error

host='localhost'
port=3306
user='root'
database='biblioteca'
password=''

def con(query, values=[]):
    try:
        con = mysql.connect(
                host=host,
                port=port,
                user=user,
                database=database,
                password=password)
        cur = con.cursor()
        cur.execute(query,values)
        res=cur.fetchall()
       
        con.commit()
        if len(res)>0:
            return res
        return None
    except Error as e:
        input(f"Error al insertar datos: {e}")
    finally:
        cur.close()
        con.close()

def crear_tablas():
    query="""
CREATE TABLE IF NOT EXISTS GENEROS(
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
GENERO VARCHAR(40) NOT NULL,
DESCRIPCION TEXT)

CREATE TABLE IF NOT EXISTS USUARIOS(
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
NOMBRE VARCHAR(40) NOT NULL,
APELLIDO VARCHAR(40) NOT NULL,
DNI VARCHAR(8) NOT NULL UNIQUE,
TELEFONO VARCHAR(20),
EMAIL VARCHAR(100),
CREADO_EL TIMESTAMP DEFAULT NOW(),
ACTUALIZADO_EL TIMESTAMP DEFAULT NOW(),
ESTADO TINYINT DEFAULT 1)

CREATE TABLE IF NOT EXISTS INVENTARIO(
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
TITULO VARCHAR(80) NOT NULL,
AUTOR VARCHAR(80) NOT NULL,
GENERO_ID INT NOT NULL,
AÑO_PUBLICACION VARCHAR(4),
CREADO_EL TIMESTAMP DEFAULT NOW(),
ACTUALIZADO_EL TIMESTAMP DEFAULT NOW(),
ESTADO TINYINT DEFAULT 1,
CONSTRAINT FK_INVENTARIO_GENEROS FOREIGN KEY(GENERO_ID) REFERENCES GENEROS(ID))

CREATE TABLE IF NOT EXISTS PRESTAMOS(
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
FECHA_PRESTAMO TIMESTAMP DEFAULT NOW() NOT NULL,
FECHA_ESTIPULADA TIMESTAMP NOT NULL,
FECHA_REAL TIMESTAMP,
LIBRO_ID INT NOT NULL,
USUARIO_ID INT NOT NULL,
CONSTRAINT FK_PRESTAMOS_INVENTARIO FOREIGN KEY(LIBRO_ID) REFERENCES INVENTARIO(ID),
CONSTRAINT FK_PRESTAMOS_USUARIOS FOREIGN KEY(USUARIO_ID) REFERENCES USUARIOS(ID));
"""
    con(query)

 
""" ancho_col=[0,0]
 
for hola in res:
    id=str(hola[0])
    hi=hola[1]
    if len(id) > ancho_col[0]:
        ancho_col[0]=len(id)
    if len(hi) > ancho_col[1]:  
        ancho_col[1]=len(hi)
 
# print("1"*8)
#
 
for i,r in enumerate(res):
   
    id =str(r[0])
    hi=r[1]
    diff_id= abs(len(id) - ancho_col[0])
    diff_hi=abs(len(hi) - ancho_col[1])
    if i == 0:
        print("+"+("-"*ancho_col[1])+"-+-"+"-"*ancho_col[0]+"+")
        print(("| HOLA"+" "*diff_hi)+"| "+("ID"+" "*diff_id+"|"))
        print("+"+("-"*ancho_col[1])+"-+-"+"-"*ancho_col[0]+"+")
 
    print("|"+(hi+(" "*diff_hi))+" | "+(id+(" "*diff_id)+"|"))
   
    if i == len(res)-1:
        print("+"+("-"*ancho_col[1])+"-+-"+"-"*ancho_col[0]+"+") """

def clear():
    os.system('cls' if os.name== 'nt' else 'clear')

def genre():
    select='SELECT * FROM GENEROS'

    res=con(select)

    ancho_col=[0,0]
 
    for hola in res:
        id=str(hola[0])
        hi=hola[1]
        if len(id) > ancho_col[0]:
            ancho_col[0]=len(id)
        if len(hi) > ancho_col[1]:  
            ancho_col[1]=len(hi)
    

    for i,r in enumerate(res):
    
        id =str(r[0])
        hi=r[1]
        diff_id= abs(len(id) - ancho_col[0])
        diff_hi=abs(len(hi) - ancho_col[1])
        if len(id)>1:
            diff_encabezado_id=abs(len("ID") - ancho_col[0])
        else:
            diff_encabezado_id=0
        diff_encabezado_genero=abs(len("GÉNEROS") - ancho_col[1])
        if i == 0:
            print("+"+("-"*ancho_col[0])+"-+-"+"-"*ancho_col[1]+"+")
            print(("|ID"+" "*diff_encabezado_id)+"| "+("GÉNEROS"+" "*diff_encabezado_genero+"|"))
            print("+"+("-"*ancho_col[0])+"-+-"+"-"*ancho_col[1]+"+")
    
        print("|"+(id+(" "*diff_id))+" | "+(hi+(" "*diff_hi)+"|"))
    
        if i == len(res)-1:
            print("+"+("-"*ancho_col[0])+"-+-"+"-"*ancho_col[1]+"+") 

    genero=input("Ingrese el ID del genero: ")
    if not genero.strip():
        input("Género inválido, por favor ingrese de nuevo.")
    else:
        return genero
        
def insert_user(nombre,apellido,dni,telefono,email):
        query="""INSERT INTO USUARIOS(nombre,apellido,dni,telefono,email) VALUES (%s,%s,%s,%s,%s)"""
        values=[nombre,apellido,dni,telefono,email]

        con(query,values)

        input("Datos cargados correctamente.")

def insert_book(titulo,autor,genero,año_publicacion):
    query="""INSERT INTO INVENTARIO(titulo,autor,genero_id,año_publicacion) VALUES (%s,%s,%s,%s)"""
    values=(titulo,autor,genero,año_publicacion)

    con(query,values)

    print("Datos cargados correctamente.")

def insert_genre(genero,descripcion):
    query="""INSERT INTO GENEROS(genero,descripcion) VALUES (%s,%s)"""
    values=(genero,descripcion)

    con(query,values)

    print("Datos cargados correctamente.")


def traer_libros():  
    select="""SELECT INVENTARIO.ID,INVENTARIO.TITULO,INVENTARIO.AUTOR,GENEROS.GENERO FROM INVENTARIO JOIN GENEROS ON GENEROS.ID=INVENTARIO.GENERO_ID WHERE INVENTARIO.ESTADO=1"""

    res=con(select)

    while True:
        clear()
        print("                                 ====== LIBROS ======")
        ids=[]

        ancho_col=[0,0,0,0]
 
        for hola in res:
            id=str(hola[0])
            hi=hola[1]
            autor=hola[2]
            genero=hola[3]
            if len(id) > ancho_col[0]:
                ancho_col[0]=len(id)
            if len(hi) > ancho_col[1]:  
                ancho_col[1]=len(hi)
            if len(autor) > ancho_col[2]:
                ancho_col[2]=len(autor)
            if len(genero) > ancho_col[3]:
                ancho_col[3]=len(genero)
            ids.append(str(hola[0]).strip())
        
        for i,r in enumerate(res):
        
            id =str(r[0])
            hi=r[1]
            autor=r[2]
            genero=r[3]
            diff_id= abs(len(id) - ancho_col[0])
            diff_hi=abs(len(hi) - ancho_col[1])
            diff_autor=abs(len(autor) - ancho_col[2])
            diff_genero=abs(len(genero)- ancho_col[3])
            if len(id)>1:
                diff_encabezado_id=abs(len("ID") - ancho_col[0])
            else:
                diff_encabezado_id=0
            diff_encabezado_titulo=abs(len("TÍTULO") - ancho_col[1])
            diff_encabezado_autor=abs(len("AUTOR") - ancho_col[2])
            diff_encabezado_genero=abs(len("GÉNERO") - ancho_col[3])
            lineas=""""+"+("-"*ancho_col[0])+"-+-"+("-"*ancho_col[1])+'-+-'+('-'*ancho_col[2])'-+-'+('-'*ancho_col[3])+'+'"""
            if i == 0:
                print ("+",("-"*ancho_col[0]),"-+-",("-"*ancho_col[1]),"-+-",("-"*ancho_col[2])+"-+-",("-"*ancho_col[3]),"+")
                print(("|ID"+" "*diff_encabezado_id)+"| "+("TÍTULO"+" "*diff_encabezado_titulo)+"| "+("AUTOR"+" "*diff_encabezado_autor)+"| "+("GÉNERO"+" "*diff_encabezado_genero+"|"))
                print("+"+("-"*ancho_col[0])+"-+-"+("-"*ancho_col[1])+"-+-"+("-"*ancho_col[2])+"-+-"+("-"*ancho_col[3])+"+")
        
            print("|"+(id+(" "*diff_id))+" | "+(hi+(" "*diff_hi))+" | "+(autor+(" "*diff_autor))+" | "+(genero+(" "*diff_genero)+"|"))
        
            if i == len(res)-1:
                print ("+",("-"*ancho_col[0]),"-+-",("-"*ancho_col[1]),"-+-",("-"*ancho_col[2])+"-+-",("-"*ancho_col[3]),"+")

        print("===============================")
        id=input("Ingrese el ID del libro: ")
        if id.strip() in ids:
            return id
        else:
            clear()
            print("                                 ====== LIBROS ======")
            input(f"El libro {id} no se encuentra disponible")

def traer_usuarios():
    clear()
    try:
        con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")
        
        if con.is_connected():
            cur=con.cursor()
            query="""SELECT ID,NOMBRE,APELLIDO FROM USUARIOS WHERE ESTADO=1"""
            cur.execute(query)
            
            lista=cur.fetchall()
            while True:
                clear()
                print("                                 ====== USUARIOS ======")
                ids=[]
                for elemento in lista:
                    print(elemento)
                    ids.append(str(elemento[0]))
                print("===============================")
                id=input("Ingrese el ID del usuario: ")
                if not id in ids:
                    clear()
                    print("                                 ====== USUARIOS ======")
                    print(f"El usuario {id} no se encuentra disponible")
                    input("Presione ENTER para continuar...")
                else:
                    break

        return id
                
    except Exception as e:
        print(f"Error en la conexión: {e}")

def insert_loan(libro,usuario):
    try:
        con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")

        if con.is_connected():
            fecha_estipulada=(datetime.now()+timedelta(days=7))
            print(type(fecha_estipulada))
            cur=con.cursor()
            query="""INSERT INTO PRESTAMOS(FECHA_ESTIPULADA,LIBRO_ID,USUARIO_ID) VALUES (%s,%s,%s)"""
            values=(fecha_estipulada,libro,usuario)
            cur.execute(query,values)
            con.commit()
            cur.execute("UPDATE INVENTARIO SET ESTADO=0 WHERE ID=%s",[libro])
            con.commit()
            input("Préstamo realizado con éxito.")

    except Exception as e:
        input(f"Error al insertar datos: {e}")

    finally:
        if con.is_connected():
            cur.close()
            con.close()
            
def main_menu():
    clear()
    print("             ====== MENÚ ======")
    print("1. Agregar")
    print("2. Actualizar")
    print("3. Estado")
    print("4. Salir")
    print("===========================================")

def menu_agregar():
    while True:
        clear()
        print("             ====== AGREGAR ======")
        print("1. Agregar Usuario")
        print("2. Agregar Libro")
        print("3. Agregar Género")
        print("4. Agregar Préstamo")
        print("5. Volver")
        print("===========================================")
        opcion = input("Seleccione una opción: ")

        if opcion=='1':
            while True:
                clear()
                print("             ====== AGREGAR USUARIO ======")
                nombre=input("Ingrese el nombre del usuario: ")
                nombre=nombre.capitalize()
                apellido=input("Ingrese el apellido del usuario: ")
                apellido=apellido.capitalize()
                dni=input("Ingrese el dni del usuario: ")
                telefono=input("Ingrese el telefono del usuario: ")
                email=input("Ingrese el email del usuario: ")
                if dni is "" or apellido is "" or  nombre is "":
                    input("Datos inválidos, por favor ingrese de nuevo.")
                else:
                    insert_user(nombre,apellido,dni,telefono,email)
                    eleccion=input("Desea cargar otro usuario? (S/N): ")
                    eleccion=eleccion.upper()
                    if eleccion=="S":
                        continue
                    else:
                        break
        elif opcion == '2':
            while True:
                clear()
                print("             ====== AGREGAR LIBRO ======")
                titulo=input("Ingrese el titulo del libro: ")
                titulo=titulo.capitalize()
                autor=input("Ingrese el autor del libro: ")
                autor=autor.capitalize()
                genero=genre()
                año_publicacion=input("Ingrese el año de publicacion: ")
                if titulo is "" or autor is "" or genero is "":
                    input("Datos invalidos, por favor ingrese de nuevo.")
                else:
                    insert_book(titulo,autor,genero,año_publicacion)
                    eleccion=input("Desea cargar otro libro? (S/N): ")
                    eleccion=eleccion.upper()
                    if eleccion=="S":
                        continue
                    else:
                        break
        elif opcion == '3':
            print("             ====== AGREGAR GÉNERO ======")
            genero=input("Ingrese el genero: ")
            genero=genero.capitalize()
            descripcion=input("Ingrese una descripcion: ")
            descripcion=descripcion.capitalize()
            if genero is "" :
                input("Datos invalidos, por favor ingrese de nuevo")
            else:
                insert_genre(genero, descripcion)
                break
        elif opcion == '4':
            while True:
                print("             ====== AGREGAR PRÉSTAMO ======")
                libro=traer_libros()
                print(libro)
                input("")
                usuario=traer_usuarios()
                insert_loan(libro,usuario)
                break
        elif opcion == '5':
            return
        else:
            input(f"Opcion {opcion} invalida, por favor ingrese de nuevo. ")

def menu_actualizar():
    clear()
    print("             ====== ACTUALIZAR ======")
    print("1. Actualizar Usuario")
    print("2. Actualizar Libro")
    print("3. Actualizar Género")
    print("4. Actualizar Préstamo")
    print("5. Volver")
    print("===========================================")
    opcion = input("Seleccione una opción: ")

def main():
    while True:
        main_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            menu_agregar()
        elif opcion == '2':
            menu_actualizar()    
        elif opcion == '3':
            clear()
            print("====== ESTADO ======")
            print("1. Estado Usuario")
            print("2. Estado Libro")
            print("3. Volver")
            print("===============================")
        elif opcion == '4':
            clear()
            input("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, intenta de nuevo.")

main()
