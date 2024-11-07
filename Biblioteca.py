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
    query1="""
CREATE TABLE IF NOT EXISTS GENEROS(
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
GENERO VARCHAR(40) NOT NULL,
DESCRIPCION TEXT)
"""
    con(query1)
    
    query2="""
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
"""
    con(query2)
    
    query3=""" CREATE TABLE IF NOT EXISTS INVENTARIO(
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
TITULO VARCHAR(80) NOT NULL,
AUTOR VARCHAR(80) NOT NULL,
GENERO_ID INT NOT NULL,
AÑO_PUBLICACION VARCHAR(4),
CREADO_EL TIMESTAMP DEFAULT NOW(),
ACTUALIZADO_EL TIMESTAMP DEFAULT NOW(),
ESTADO TINYINT DEFAULT 1,
CONSTRAINT FK_INVENTARIO_GENEROS FOREIGN KEY(GENERO_ID) REFERENCES GENEROS(ID)) """
    con(query3)
    
    query4=""" CREATE TABLE IF NOT EXISTS PRESTAMOS(
ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
FECHA_PRESTAMO TIMESTAMP DEFAULT NOW() NOT NULL,
FECHA_ESTIPULADA TIMESTAMP NOT NULL,
FECHA_REAL TIMESTAMP,
LIBRO_ID INT NOT NULL,
USUARIO_ID INT NOT NULL,
ESTADO TINYINT DEFAULT 1,
CONSTRAINT FK_PRESTAMOS_INVENTARIO FOREIGN KEY(LIBRO_ID) REFERENCES INVENTARIO(ID),
CONSTRAINT FK_PRESTAMOS_USUARIOS FOREIGN KEY(USUARIO_ID) REFERENCES USUARIOS(ID)) """
    con(query4)
    
def clear():
    os.system('cls' if os.name== 'nt' else 'clear')

def genre():
    while True:
        clear()
        select='SELECT * FROM GENEROS'
        res, columnas=con(select)

        ids=[]

        for elemento in res:
            ids.append(str(elemento[0]).strip())
                
        if res:
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            genero=input(' Ingrese el ID del género: ')

            if genero.strip() in ids:
                return genero
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')

def loan():
    while True:
        clear()
        select="""SELECT P.ID, P.FECHA_PRESTAMO, P.FECHA_ESTIPULADA, I.TITULO, U.DNI FROM PRESTAMOS P JOIN INVENTARIO I ON P.LIBRO_ID=I.ID JOIN USUARIOS U ON P.USUARIO_ID=U.ID WHERE P.ESTADO=1"""
        res, columnas=con(select)

        ids=[]

        for elemento in res:
            ids.append(str(elemento[0]).strip())
            
        if res:
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            prestamos=input(' Ingrese el ID del préstamo: ')
                
            if prestamos.strip() in ids:
                return prestamos
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')
       
def bring_some_books():
    try:
        while True:
            clear()
            select="""SELECT INVENTARIO.ID,INVENTARIO.TITULO,INVENTARIO.AUTOR,GENEROS.GENERO FROM INVENTARIO JOIN GENEROS ON GENEROS.ID=INVENTARIO.GENERO_ID WHERE INVENTARIO.ESTADO=1"""
            res, columnas=con(select)

            ids=[]

            for elemento in res:
                ids.append(str(elemento[0]).strip())

            if res:
                print(tabulate(res, headers=columnas, tablefmt='grid'))

                libro=input(' Ingrese el ID del libro: ')
                if libro.strip() in ids:
                    return libro
                else:
                    input(' ID no encontrado, por favor ingrese de nuevo.')
    except:
        input('Debe tener al menos un libro en stock.')

def bring_some_users():
    try:
        while True:
            clear()
            select="""SELECT ID,NOMBRE,APELLIDO,DNI FROM USUARIOS WHERE ESTADO=1"""
            res, columnas=con(select)

            ids=[]

            for elemento in res:
                ids.append(str(elemento[0]).strip())

            if res:
                print(tabulate(res, headers=columnas, tablefmt='grid'))

            usuario=input(' Ingrese el ID del usuario: ')
            if usuario.strip() in ids:
                return usuario
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')
    except:
        input('Debe tener al menos un usuario activo.')

def bring_all_books():
    while True:
        clear()
        select="""SELECT INVENTARIO.ID,INVENTARIO.TITULO,INVENTARIO.AUTOR,GENEROS.GENERO,INVENTARIO.ESTADO FROM INVENTARIO JOIN GENEROS ON GENEROS.ID=INVENTARIO.GENERO_ID"""
        res, columnas=con(select)

        ids=[]

        for elemento in res:
            ids.append(str(elemento[0]).strip())

        if res:
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            libro=input(' Ingrese el ID del libro que desea actualizar: ')
            if libro.strip() in ids:
                return libro
            else:
                input(' ID no encontrado, por favor ingrese de nuevo.')

def bring_all_users():
    while True:
        clear()
        select="""
                SELECT ID,NOMBRE,APELLIDO,DNI,
                    CASE 
                        WHEN ESTADO = 1 THEN 'ACTIVO' 
                        WHEN ESTADO = 0 THEN 'INACTIVO'  
                    END AS ESTADO
                FROM USUARIOS"""
        res, columnas=con(select)

        ids=[]

        for elemento in res:
            ids.append(str(elemento[0]).strip())
        
        if res:
            print(tabulate(res, headers=columnas, tablefmt='grid'))

        usuario=input(' Ingrese el ID del usuario que desea actualizar: ')
        if usuario.strip() in ids:
            return usuario
        else:
            input(' ID no encontrado, por favor ingrese de nuevo.')

def insert_user():
    while True:
            clear()
            print('            +---------------+             ')
            print("            | NUEVO USUARIO |             ")
            print("+----------------------------------------+")

            nombre=input(" Ingrese el nombre del usuario: ").capitalize()
            apellido=input(" Ingrese el apellido del usuario: ").capitalize()
            dni=input(" Ingrese el DNI del usuario: ")
            telefono=input(" Ingrese el teléfono del usuario: ")
            email=input(" Ingrese el email del usuario: ").lower()
            
            if not nombre.strip() or not apellido.strip() or not dni.strip:
                print("+----------------------------------------+")
                input("Datos inválidos, por favor ingrese de nuevo.")
            else:
                query="""INSERT INTO USUARIOS(nombre,apellido,dni,telefono,email) VALUES (%s,%s,%s,%s,%s)"""
                values=[nombre,apellido,dni,telefono,email]
                con(query,values)
                print("+----------------------------------------+")
                input(" Usuario cargado correctamente.")

                clear()
                print('            +---------------+             ')
                print("            | NUEVO USUARIO |             ")
                print("+----------------------------------------+")

                eleccion=input(" Desea agregar otro usuario? (S/N): ").upper()
                if eleccion=="S":
                    continue
                else:
                    return

def insert_book():
    try:
        while True:
            clear()
            print('             +-------------+              ')
            print("             | NUEVO LIBRO |              ")
            print("+----------------------------------------+")

            titulo=input(" Ingrese el título del libro: ").capitalize()
            autor=input(" Ingrese el autor del libro: ").capitalize()
            genero=genre()
            año_publicacion=input(" Ingrese el año de publicación: ")

            if not titulo.strip() or not autor.strip() or not genero.strip():
                print("+----------------------------------------+")
                input(" Datos inválidos, por favor ingrese de nuevo.")
            else:
                query="""INSERT INTO INVENTARIO(titulo,autor,genero_id,año_publicacion) VALUES (%s,%s,%s,%s)"""
                values=[titulo,autor,genero,año_publicacion]
                con(query,values)
                print("+----------------------------------------+")
                input(" Libro cargado correctamente.")
                
                clear()
                print('             +-------------+              ')
                print("             | NUEVO LIBRO |              ")
                print("+----------------------------------------+")

                eleccion=input(" Desea agregar otro libro? (S/N): ").upper()
                if eleccion=="S":
                    continue
                else:
                    return
    except:
        input("No existen géneros aún, por favor ingrese al menos un género antes de agregar un libro.")
        return

def insert_genre():
    while True:
        clear()
        print('             +--------------+             ')
        print("             | NUEVO GÉNERO |             ")
        print("+----------------------------------------+")

        genero=input(" Ingrese el género: ").capitalize()
        descripcion=input(" Ingrese una descripción: ").capitalize()

        if not genero.strip():
            print("+----------------------------------------+")
            input(" Datos inválidos, por favor ingrese de nuevo")
        else:
            query="""INSERT INTO GENEROS(genero,descripcion) VALUES (%s,%s)"""
            values=[genero,descripcion]
            con(query,values)
            print("+----------------------------------------+")
            input(" Género cargado correctamente.")

            clear()
            print('             +--------------+             ')
            print("             | NUEVO GÉNERO |             ")
            print("+----------------------------------------+")

            eleccion=input(" Desea agregar otro género? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                return

def insert_loan():
    try:
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

            print("+----------------------------------------+")
            input(" Préstamo realizado con éxito.")

            clear()
            print('            +----------------+            ')
            print('            | NUEVO PRÉSTAMO |            ')
            print("+----------------------------------------+")

            eleccion=input(" Desea agregar otro préstamo? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                return
    except:
        input('Antes de realizar un préstamo debe tener al menos un libro y un usuario cargado.')
        return

def update_user():
    try:
        while True:
            clear()

            select="""
            SELECT ID,NOMBRE,APELLIDO,DNI,TELEFONO,EMAIL
            FROM USUARIOS WHERE ID=%s"""
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
                    print("+----------------------------------------+")
                    input(" Datos inválidos, por favor ingrese de nuevo.")
                else:
                    update="""
                    UPDATE USUARIOS SET NOMBRE=%s, APELLIDO=%s, DNI=%s, TELEFONO=%s, EMAIL=%s, ACTUALIZADO_EL=%s
                    WHERE ID=%s"""
                    values=[nombre,apellido,dni,telefono,email,datetime.now(),id[0]]
                    con(update,values)
                    print("+----------------------------------------+")
                    input(" Usuario actualizado correctamente.")
                    break

            clear()
            print('          +--------------------+          ')
            print("          | ACTUALIZAR USUARIO |          ")
            print("+----------------------------------------+")

            eleccion=input(" Desea actualizar otro usuario? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                return
    except:
        input('Debe tener al menos un usuario cargado antes de poder actualizar datos.')
        return

def update_book():
    try:
        while True:
            clear()
            select="""SELECT INVENTARIO.ID,INVENTARIO.TITULO,INVENTARIO.AUTOR,GENEROS.GENERO,INVENTARIO.ESTADO FROM INVENTARIO JOIN GENEROS ON GENEROS.ID=INVENTARIO.GENERO_ID WHERE INVENTARIO.ID=%s"""
            id=[bring_all_books()]
            res, columnas=con(select,id)

            while True:
                clear()
                if res:
                    print(tabulate(res, headers=columnas, tablefmt='grid'))

                titulo=input(" Ingrese el título del libro: ").capitalize()
                autor=input(" Ingrese el autor del libro: ").capitalize()
                genero=genre()
                año_publicacion=input(" Ingrese el año de publicación: ")

                if not titulo.strip() or not autor.strip() or not genero.strip():
                    print("+----------------------------------------+")
                    input(" Datos inválidos, por favor ingrese de nuevo.")
                else:
                    update="""UPDATE INVENTARIO SET titulo=%s ,autor=%s ,genero_id=%s,año_publicacion=%s, ACTUALIZADO_EL=%s WHERE ID=%s"""
                    values=[titulo,autor,genero,año_publicacion,datetime.now(),id[0]]
                    con(update,values)
                    print("+----------------------------------------+")
                    input(" Libro actualizado correctamente.")
                    break
                    
                clear()
                print('           +------------------+           ')
                print("           | ACTUALIZAR LIBRO |           ")
                print("+----------------------------------------+")

                eleccion=input(" Desea actualizar otro libro? (S/N): ").upper()
                if eleccion=="S":
                    continue
                else:
                    return
    except:
        input('Debe tener al menos un libro cargado antes de poder actualizar datos.')
        return

def update_genre():
    try:
        while True:
            clear()
            select="""SELECT * FROM GENEROS WHERE ID=%s"""
            id=[genre()]
            res,columnas=con(select,id)
            

            if res:
                print(tabulate(res, headers=columnas, tablefmt='grid'))
                
            genero=input(" Ingrese el género: ").capitalize()
            descripcion=input(" Ingrese una descripción: ").capitalize()

            if not genero.strip():
                print("+----------------------------------------+")
                input(" Datos inválidos, por favor ingrese de nuevo.")
            else:
                update="""UPDATE GENEROS SET genero=%s, descripcion=%s """
                values=[genero,descripcion]
                con(update,values)
                print("+----------------------------------------+")
                input(" Género actualizado correctamente.")
                break

            clear()
            print('          +-------------------+           ')
            print("          | ACTUALIZAR GÉNERO |           ")
            print("+----------------------------------------+")

            eleccion=input(" Desea actualizar otro género? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                return
    except:
        input("No existen géneros aún, por favor ingrese al menos un género antes de actualizar.")
        return

def update_loan():
    try:
        while True:
            clear()
            select="""SELECT P.ID, P.FECHA_PRESTAMO, P.FECHA_ESTIPULADA,P.LIBRO_ID, I.TITULO,P.USUARIO_ID, U.NOMBRE,U.APELLIDO,U.DNI FROM PRESTAMOS P JOIN INVENTARIO I ON P.LIBRO_ID=I.ID JOIN USUARIOS U ON P.USUARIO_ID=U.ID WHERE P.ID=%s"""
            id=[loan()]
            res,columnas=con(select,id)

            libro_id=[]

            for elemento in res:
                libro_id.append(str(elemento[3]).strip())
            
            while True:
                clear() 
                eleccion=input('Desea cambiar de libro prestado? (S/N)').upper()
                if eleccion == 'S':
                    libro=bring_some_books()
                else:
                    libro=None
                usuario=bring_some_users()

                if res:
                    print(tabulate(res, headers=columnas, tablefmt='grid'))

                if libro:
                    update="""UPDATE INVENTARIO SET ESTADO=1 WHERE ID=%s"""
                    values=[libro_id[0]]
                    con(update,values)

                    update="""UPDATE PRESTAMOS SET LIBRO_ID=%s,USUARIO_ID=%s WHERE ID=%s """
                    values=[libro,usuario,id[0]]
                    con(update,values)
                else:
                    update="""UPDATE PRESTAMOS SET USUARIO_ID=%s WHERE ID=%s """
                    values=[usuario,id[0]]
                    con(update,values)

                update="UPDATE INVENTARIO SET ESTADO=0, ACTUALIZADO_EL=%s WHERE ID=%s"
                values=[datetime.now(),libro]
                con(update,values)

                print("+----------------------------------------+")
                input(" Préstamo actualizado con éxito.")
                break

            clear()
            print('         +---------------------+          ')
            print('         | ACTUALIZAR PRÉSTAMO |          ')
            print("+----------------------------------------+")

            eleccion=input(" Desea actualizar otro préstamo? (S/N): ").upper()
            if eleccion=="S":
                continue
            else:
                return  
    except:
        input('No existen préstamos disponibles para actualizar.')                 

def devolver_libro():
    try:
        while True:
            clear()
            select="""SELECT P.ID,P.FECHA_PRESTAMO,P.FECHA_ESTIPULADA,P.LIBRO_ID,I.TITULO,P.USUARIO_ID,U.NOMBRE,U.APELLIDO,U.DNI FROM PRESTAMOS P JOIN INVENTARIO I ON P.LIBRO_ID=I.ID JOIN USUARIOS U ON P.USUARIO_ID=U.ID WHERE P.ID=%s"""
            id=[loan()]
            res, columnas=con(select,id)

            libro_id=[]
            usuario_id=[]
            fecha_estipulada=[]
            fecha_real=[]
            fecha_real.append(datetime.now())
        
            for e in res:
                libro_id.append(e[3])
                usuario_id.append(e[5])
                fecha_estipulada.append(e[2])

            if res:
                print(tabulate(res, headers=columnas, tablefmt='grid'))

            eleccion=input('Desea finalizar este préstamo? (S/N): ').upper()
            if eleccion == 'S':     
                update="""UPDATE PRESTAMOS SET FECHA_REAL=%s WHERE ID=%s """
                values=[fecha_real[0],id[0]]
                con(update,values)

                update="UPDATE INVENTARIO SET ESTADO=1, ACTUALIZADO_EL=%s WHERE ID=%s"
                values=[fecha_real[0],libro_id[0]]
                con(update,values)

                if fecha_real>fecha_estipulada:
                    update="UPDATE USUARIOS SET ESTADO=0, ACTUALIZADO_EL=%s WHERE ID=%s"
                    values=[fecha_real[0],usuario_id[0]]
                    con(update,values) 

                print("+----------------------------------------+")
                input(" Devolución realizada con éxito.")

                clear()
                print('             +--------------+             ')
                print('             | DEVOLUCIONES |             ')
                print("+----------------------------------------+")

                eleccion=input(" Desea realizar otra devolución? (S/N): ").upper()
                if eleccion=="S":
                    continue
                else:
                    return
            else:
                return
    except:
        input('No existen préstamos disponibles para devolver.')    
            
def status_books():
    try:
        while True:
            clear()
            select="""SELECT I.ID,I.TITULO,I.AUTOR,G.GENERO,
                        CASE 
                            WHEN I.ESTADO = 1 THEN 'EN STOCK' 
                            WHEN I.ESTADO = 0 THEN 'FUERA DE STOCK'  
                        END AS ESTADO FROM INVENTARIO I JOIN GENEROS G ON G.ID=I.GENERO_ID"""
            res, columnas=con(select)

            ids=[]
            status=[]

            for elemento in res:
                ids.append(str(elemento[0]).strip())
                status.append(str(elemento[4]).strip())

            if res:
                print(tabulate(res, headers=columnas, tablefmt='grid'))
                            
            eleccion=input(" Desea actualizar el estado de un libro? (S/N): ").upper()
            if eleccion=="S":
                libro=input(' Ingrese el ID del libro que desea actualizar: ')
                libro_id=int(ids[0])
                if libro.strip() in ids:
                    if status[libro_id]== 'FUERA DE STOCK':
                        update="""UPDATE INVENTARIO SET ESTADO=1, ACTUALIZADO_EL=%s WHERE ID=%s"""
                        values=[datetime.now(),libro]
                        con(update,values)
                    else:
                        update="""UPDATE INVENTARIO SET ESTADO=0, ACTUALIZADO_EL=%s WHERE ID=%s"""
                        values=[datetime.now(),libro]
                        con(update,values)

                    input(" Actualización realizada con éxito.")

                    clear()
                    print('         +----------------------+         ')
                    print("         | ESTADO DE LOS LIBROS |         ")
                    print("+----------------------------------------+")

                    eleccion=input(" Desea actualizar otro libro? (S/N): ").upper()
                    if eleccion=="S":
                        continue
                    else:
                        return
                else:
                    input(' ID no encontrado, por favor ingrese de nuevo.')
            else:
                return
    except:
        input("Debe tener al menos agregado un libro para poder cambiar su estado, por favor ingrese uno.")
        return
  
def status_users():
    try:
        while True:
            clear()
            select="""
                    SELECT ID,NOMBRE,APELLIDO,DNI,
                        CASE 
                            WHEN ESTADO = 1 THEN 'ACTIVO' 
                            WHEN ESTADO = 0 THEN 'INACTIVO'  
                        END AS ESTADO
                    FROM USUARIOS"""
            res, columnas=con(select)

            ids=[]
            status=[]

            for elemento in res:
                ids.append(str(elemento[0]).strip())
                status.append(str(elemento[4]).strip())

            if res:
                print(tabulate(res, headers=columnas, tablefmt='grid'))
                    
            eleccion=input(" Desea actualizar el estado de un usuario? (S/N): ").upper()
            if eleccion=="S":
                usuario=input(' Ingrese el ID del usuario que desea actualizar: ')
                usuario_id=int(ids[0])
                if usuario.strip() in ids:
                    if status[usuario_id]== 'INACTIVO':
                        update="""UPDATE USUARIOS SET ESTADO=1, ACTUALIZADO_EL=%s WHERE ID=%s"""
                        values=[datetime.now(),usuario]
                        con(update,values)
                    else:
                        update="""UPDATE USUARIOS SET ESTADO=0, ACTUALIZADO_EL=%s WHERE ID=%s"""
                        values=[datetime.now(),usuario]
                        con(update,values)

                    input(" Actualización realizada con éxito.")

                    clear()
                    print('        +------------------------+        ')
                    print("        | ESTADO DE LOS USUARIOS |        ")
                    print("+----------------------------------------+")

                    eleccion=input(" Desea actualizar otro libro? (S/N): ").upper()
                    if eleccion=="S":
                        continue
                    else:
                        return
                else:
                    input(' ID no encontrado, por favor ingrese de nuevo.')
            else:
                return
    except:
        input("Debe tener al menos agregado un usuario para poder cambiar su estado, por favor ingrese uno.")
        return

def loan_list():
    while True:
        clear()
        select="""SELECT P.ID, P.FECHA_PRESTAMO, P.FECHA_ESTIPULADA,P.FECHA_REAL, I.TITULO, U.DNI,
                    CASE
                        WHEN P.ESTADO=1 THEN 'ACTIVO'
                        WHEN P.ESTADO=0 THEN 'DEVUELTO'
                    END AS ESTADO FROM PRESTAMOS P JOIN INVENTARIO I ON P.LIBRO_ID=I.ID JOIN USUARIOS U ON P.USUARIO_ID=U.ID"""
        res, columnas=con(select)
            
        if res:
            print(tabulate(res, headers=columnas, tablefmt='grid'))

            eleccion=input(""" Ingrese "Q" para volver: """).upper()
                
            if eleccion == 'Q':
                return
            else:
                continue

def main_menu():
    clear()
    print('            +----------------+            ')
    print("            | MENÚ PRINCIPAL |            ")
    print("+----------------------------------------+")
    print("|1. Agregar                              |")
    print("|2. Actualizar                           |")
    print("|3. Devoluciones                         |")
    print("|4. Estados y listas                     |")
    print("|5. Salir                                |")
    print("+----------------------------------------+")

def menu_agregar():
    while True:
        clear()
        print('               +---------+                ')
        print("               | AGREGAR |                ")
        print("+----------------------------------------+")
        print("|1. Nuevo Usuario                        |")
        print("|2. Nuevo Libro                          |")
        print("|3. Nuevo Género                         |")
        print("|4. Nuevo Préstamo                       |")
        print("|5. Volver                               |")
        print("+----------------------------------------+")

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
        print('              +------------+              ')
        print("              | ACTUALIZAR |              ")
        print("+----------------------------------------+")
        print("|1. Actualizar Usuario                   |")
        print("|2. Actualizar Libro                     |")
        print("|3. Actualizar Género                    |")
        print("|4. Actualizar Préstamo                  |")
        print("|5. Volver                               |")
        print("+----------------------------------------+")

        opcion = input(" Seleccione una opción: ")

        if opcion == '1':
            update_user()
        elif opcion == '2':
            update_book()
        elif opcion =='3':
            update_genre()
        elif opcion =='4':
            update_loan()
        elif opcion=='5':
            return
        else:
            input(f"Opcion {opcion} invalida, por favor ingrese de nuevo. ")

def menu_devoluciones():
    while True:
        clear()
        print('             +--------------+             ')
        print("             | DEVOLUCIONES |             ")
        print("+----------------------------------------+")
        print("|1. Devolver libro                       |")
        print("|2. Volver                               |")
        print("+----------------------------------------+")

        opcion = input(" Seleccione una opción: ")

        if opcion == '1':
            devolver_libro()
        elif opcion == '2':
            return
        else:
            input(f"Opcion {opcion} invalida, por favor ingrese de nuevo. ")

def menu_estado():
    while True:
        clear()
        print('                +--------+                ')
        print("                | ESTADO |                ")
        print("+----------------------------------------+")
        print("|1. Estado de los libros                 |")
        print("|2. Estado de los usuarios               |")
        print("|3. Listado de préstamos                 |")
        print("|4. Volver                               |")
        print("+----------------------------------------+")

        opcion = input(" Seleccione una opción: ")

        if opcion == '1':
            status_books()
        elif opcion == '2':
            status_users()
        elif opcion == '3':
            loan_list()
        elif opcion == '4':
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
            menu_devoluciones()
        elif opcion == '4':
            menu_estado()
        elif opcion=='5':
            clear()
            input("Saliendo del programa...")
            break 
        else:
            input("Opción inválida. Por favor, intenta de nuevo.")

main()
