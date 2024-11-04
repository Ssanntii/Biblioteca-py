import mysql.connector as mysql
import os
from datetime import datetime, timedelta
from mysql.connector import Error
from tabulate import tabulate

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
            columnas = [i[0] for i in cur.description] if cur.description else []
            return res, columnas
        return None
    
    except Error as e:
        input(f"Error {e} encontrado.")

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

def clear():
    os.system('cls' if os.name== 'nt' else 'clear')

def genre():
    select='SELECT * FROM GENEROS'
    res, columnas=con(select)

    ids=[]

    for elemento in res:
        ids.append(str(elemento[0]).strip())
        
    while True:
        clear()
        if res:
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            genero=input(' Ingrese el ID del género: ')

            if genero.strip() in ids:
                return genero
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')

def bring_some_books():  
    select="""SELECT INVENTARIO.ID,INVENTARIO.TITULO,INVENTARIO.AUTOR,GENEROS.GENERO FROM INVENTARIO JOIN GENEROS ON GENEROS.ID=INVENTARIO.GENERO_ID WHERE INVENTARIO.ESTADO=1"""
    res, columnas=con(select)

    ids=[]

    for elemento in res:
        ids.append(str(elemento[0]).strip())

    while True:
        clear()
        if res:
            print('                          +----------------+                          ')
            print('                          | NUEVO PRÉSTAMO |                          ')
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            libro=input(' Ingrese el ID del libro: ')
            if libro.strip() in ids:
                return libro
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')

def bring_some_users():
    select="""SELECT ID,NOMBRE,APELLIDO,DNI FROM USUARIOS WHERE ESTADO=1"""
    res, columnas=con(select)

    ids=[]

    for elemento in res:
        ids.append(str(elemento[0]).strip())

    while True:
        clear()
        if res:
            print('            +----------------+               ')
            print('            | NUEVO PRÉSTAMO |               ')
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            usuario=input(' Ingrese el ID del usuario: ')
            if usuario.strip() in ids:
                return usuario
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')

def bring_all_books():
    select="""SELECT INVENTARIO.ID,INVENTARIO.TITULO,INVENTARIO.AUTOR,GENEROS.GENERO,INVENTARIO.ESTADO FROM INVENTARIO JOIN GENEROS ON GENEROS.ID=INVENTARIO.GENERO_ID"""
    res, columnas=con(select)

    ids=[]

    for elemento in res:
        ids.append(str(elemento[0]).strip())

    while True:
        clear()
        if res:
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            libro=input(' Ingrese el ID del libro que desea actualizar: ')
            if libro.strip() in ids:
                return libro
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')

def bring_all_users():
    select="""
            SELECT ID,NOMBRE,APELLIDO,DNI,
                CASE 
                    WHEN ESTADO = 1 THEN 'ACTIVO' 
                    WHEN ESTADO = 0 THEN 'INACTIVO'  
                END AS ESTADO
            FROM USUARIOS;"""
    res, columnas=con(select)

    ids=[]

    for elemento in res:
        ids.append(str(elemento[0]).strip())

    while True:
        clear()
        if res:
            print('                 +--------------------+                 ')
            print("                 | ACTUALIZAR USUARIO |                 ")
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            usuario=input(' Ingrese el ID del usuario que desea actualizar: ')
            if usuario.strip() in ids:
                return usuario
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')

def insert_user():
    while True:
            clear()
            print('                   +---------------+                   ')
            print("                   | NUEVO USUARIO |                   ")
            print("+-----------------------------------------------------+")

            nombre=input(" Ingrese el nombre del usuario: ").capitalize()
            apellido=input(" Ingrese el apellido del usuario: ").capitalize()
            dni=input(" Ingrese el DNI del usuario: ")
            telefono=input(" Ingrese el teléfono del usuario: ")
            email=input(" Ingrese el email del usuario: ").lower()
            
            if not nombre.strip() or not apellido.strip() or not dni.strip:
                print("+-----------------------------------------------------+")
                input("Datos inválidos, por favor ingrese de nuevo.")
            else:
                query="""INSERT INTO USUARIOS(nombre,apellido,dni,telefono,email) VALUES (%s,%s,%s,%s,%s)"""
                values=[nombre,apellido,dni,telefono,email]
                con(query,values)
                print("+-----------------------------------------------------+")
                input(" Usuario cargado correctamente.")

                clear()
                print('                   +---------------+                   ')
                print("                   | NUEVO USUARIO |                   ")
                print("+-----------------------------------------------------+")

                eleccion=input(" Desea agregar otro usuario? (S/N): ").upper()
                if eleccion=="S":
                    continue
                else:
                    break

def insert_book():
    while True:
        clear()
        print('                   +-------------+                   ')
        print("                   | NUEVO LIBRO |                   ")
        print("+---------------------------------------------------+")

        titulo=input(" Ingrese el título del libro: ").capitalize()
        autor=input(" Ingrese el autor del libro: ").capitalize()
        genero=genre()
        año_publicacion=input(" Ingrese el año de publicación: ")

        if not titulo.strip() or not autor.strip() or not genero.strip():
            print("+---------------------------------------------------+")
            input(" Datos inválidos, por favor ingrese de nuevo.")
        else:
            query="""INSERT INTO INVENTARIO(titulo,autor,genero_id,año_publicacion) VALUES (%s,%s,%s,%s)"""
            values=[titulo,autor,genero,año_publicacion]
            con(query,values)
            print("+---------------------------------------------------+")
            input(" Libro cargado correctamente.")
            
            clear()
            print('                   +-------------+                   ')
            print("                   | NUEVO LIBRO |                   ")
            print("+---------------------------------------------------+")

            eleccion=input(" Desea agregar otro libro? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                break

def insert_genre():
    while True:
        clear()
        print('                   +--------------+                   ')
        print("                   | NUEVO GÉNERO |                   ")
        print("+----------------------------------------------------+")

        genero=input(" Ingrese el género: ").capitalize()
        descripcion=input(" Ingrese una descripción: ").capitalize()

        if not genero.strip():
            print("+----------------------------------------------------+")
            input(" Datos inválidos, por favor ingrese de nuevo")
        else:
            query="""INSERT INTO GENEROS(genero,descripcion) VALUES (%s,%s)"""
            values=[genero,descripcion]
            con(query,values)
            print("+----------------------------------------------------+")
            input(" Género cargado correctamente.")

            clear()
            print('                   +--------------+                   ')
            print("                   | NUEVO GÉNERO |                   ")
            print("+----------------------------------------------------+")

            eleccion=input(" Desea agregar otro género? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                break

def insert_loan():
    while True:
        clear()


        libro=bring_some_books()
        usuario=bring_some_users()

        query="""INSERT INTO PRESTAMOS(FECHA_ESTIPULADA,LIBRO_ID,USUARIO_ID) VALUES (%s,%s,%s)"""
        values=[(datetime.now()+timedelta(days=7)),libro,usuario]
        con(query,values)

        update="UPDATE INVENTARIO SET ESTADO=0, ACTUALIZADO_EL=%s WHERE ID=%s"
        values=[datetime.now(),libro]
        con(update,values)

        print("+-------------------------------------------+")
        input(" Préstamo realizado con éxito.")

        clear()
        print('                   +----------------+                   ')
        print('                   | NUEVO PRÉSTAMO |                   ')
        print("+------------------------------------------------------+")

        eleccion=input(" Desea agregar otro préstamo? (S/N): ").upper()
        if eleccion=="S":
            continue
        else:
            break

def update_user():
    while True:
        clear()

        select="""
        SELECT ID,NOMBRE,APELLIDO,DNI,TELEFONO,EMAIL
        FROM USUARIOS WHERE ID=%s;"""
        id=[bring_all_users()]
        res, columnas=con(select,id)

        while True:
            clear()
            if res:
                print(tabulate(res, headers=columnas, tablefmt='grid'))

            nombre=input(" Ingrese el nombre del usuario: ").capitalize()
            apellido=input(" Ingrese el apellido del usuario: ").capitalize()
            dni=input(" Ingrese el dni del usuario: ")
            telefono=input(" Ingrese el teléfono del usuario: ")
            email=input(" Ingrese el email del usuario: ").lower()
                
            if not nombre.strip() or not apellido.strip() or not dni.strip:
                print("+-----------------------------------------------------+")
                input("Datos inválidos, por favor ingrese de nuevo.")
            else:
                update="""
                UPDATE USUARIOS SET NOMBRE=%s, APELLIDO=%s, DNI=%s, TELEFONO=%s, EMAIL=%s, ACTUALIZADO_EL=%s
                WHERE ID=%s"""
                values=[nombre,apellido,dni,telefono,email,datetime.now(),id[0]]
                con(update,values)
                print("+-----------------------------------------------------+")
                input(" Usuario actualizado correctamente.")

            clear()
            print('                   +--------------------+                   ')
            print("                   | ACTUALIZAR USUARIO |                   ")
            print("+----------------------------------------------------------+")

            eleccion=input(" Desea actualizar otro usuario? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                return

def update_book():
    while True:
        clear()

        select="""
        SELECT ID,NOMBRE,APELLIDO,DNI,TELEFONO,EMAIL
        FROM USUARIOS WHERE ID=%s;"""
        id=[bring_all_users()]
        res, columnas=con(select,id)

        while True:
            clear()
            if res:
                print(tabulate(res, headers=columnas, tablefmt='grid'))

            nombre=input(" Ingrese el nombre del usuario: ").capitalize()
            apellido=input(" Ingrese el apellido del usuario: ").capitalize()
            dni=input(" Ingrese el dni del usuario: ")
            telefono=input(" Ingrese el teléfono del usuario: ")
            email=input(" Ingrese el email del usuario: ").lower()
                
            if not nombre.strip() or not apellido.strip() or not dni.strip:
                print("+-----------------------------------------------------+")
                input("Datos inválidos, por favor ingrese de nuevo.")
            else:
                update="""
                UPDATE USUARIOS SET NOMBRE=%s, APELLIDO=%s, DNI=%s, TELEFONO=%s, EMAIL=%s, ACTUALIZADO_EL=%s
                WHERE ID=%s"""
                values=[nombre,apellido,dni,telefono,email,datetime.now(),id[0]]
                con(update,values)
                print("+-----------------------------------------------------+")
                input(" Usuario actualizado correctamente.")

            clear()
            print('                   +--------------------+                   ')
            print("                   | ACTUALIZAR USUARIO |                   ")
            print("+----------------------------------------------------------+")

            eleccion=input(" Desea actualizar otro usuario? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                return

def main_menu():
    clear()
    print('                   +----------------+                   ')
    print("                   | MENÚ PRINCIPAL |                   ")
    print("+------------------------------------------------------+")
    print("|1. Agregar                                            |")
    print("|2. Actualizar                                         |")
    print("|3. Devoluciones                                       |")
    print("|4. Estado                                             |")
    print("|5. Salir                                              |")
    print("+------------------------------------------------------+")

def menu_agregar():
    while True:
        clear()
        print('                   +---------+                   ')
        print("                   | AGREGAR |                   ")
        print("+-----------------------------------------------+")
        print("|1. Nuevo Usuario                               |")
        print("|2. Nuevo Libro                                 |")
        print("|3. Nuevo Género                                |")
        print("|4. Nuevo Préstamo                              |")
        print("|5. Volver                                      |")
        print("+-----------------------------------------------+")

        opcion = input(" Seleccione una opción: ")

        if opcion=='1':
            insert_user()
        elif opcion == '2':
            insert_book()
        elif opcion == '3':
            insert_genre()
        elif opcion == '4':
            insert_loan()
        elif opcion == '5':
            return
        else:
            input(f"Opcion {opcion} invalida, por favor ingrese de nuevo. ")

def menu_actualizar():
    while True:
        clear()
        print('                    +------------+                   ')
        print("                    | ACTUALIZAR |                   ")
        print("+---------------------------------------------------+")
        print("|1. Actualizar Usuario                              |")
        print("|2. Actualizar Libro                                |")
        print("|3. Actualizar Género                               |")
        print("|4. Actualizar Préstamo                             |")
        print("|5. Volver                                          |")
        print("+---------------------------------------------------+")

        opcion = input(" Seleccione una opción: ")

        if opcion == '1':
            update_user()
        if opcion == '2':
            update_book()
        elif opcion=='5':
            return
        else:
            input(f"Opcion {opcion} invalida, por favor ingrese de nuevo. ")

def main():
    while True:
        crear_tablas()
        main_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            menu_agregar()
        elif opcion == '2':
            menu_actualizar()    
        elif opcion == '3':
            clear()
            print("====== DEVOLUCIONES ======")
            print("1. Devolver libro")
            print("2. Volver")
            print("===============================")
        elif opcion == '4':
            clear()
            print("====== ESTADO ======")
            print("1. Estado Usuario")
            print("2. Estado Libro")
            print("3. Volver")
            print("===============================")
        elif opcion=='5':
            clear()
            input("Saliendo del programa...")
            break 
        else:
            input("Opción inválida. Por favor, intenta de nuevo.")

main()
