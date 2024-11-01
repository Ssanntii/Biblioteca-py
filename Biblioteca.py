import mysql.connector as mysql
import os
from datetime import datetime, timedelta

def clear():
    os.system('cls' if os.name== 'nt' else 'clear')

def columnas_usuarios():
    # Conectar a la base de datos
    con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")
    cursor = con.cursor()

    # Obtener los nombres de las columnas de la tabla
    cursor.execute("SHOW COLUMNS FROM USUARIOS")
    columns = cursor.fetchall()

    for column in columns:
        column_name = column[0]  # Nombre de la columna
        
        # Consultar la longitud máxima de la columna
        cursor.execute(f"SELECT MAX(LENGTH({column_name})) FROM USUARIOS")
        max_length = cursor.fetchone()[0]

        if max_length:  # Verifica que max_length no sea None
            
            # Actualizar registros para igualar la longitud
            update_query = f"""
                UPDATE USUARIOS
                SET {column_name} = CONCAT({column_name}, SPACE(%s - LENGTH({column_name})))
                WHERE LENGTH({column_name}) < %s
            """
            cursor.execute(update_query, (max_length, max_length))

            # Confirmar cambios
            con.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    con.close()

def columnas_inventario():
    # Conectar a la base de datos
    con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")
    cursor = con.cursor()

    # Obtener los nombres de las columnas de la tabla
    cursor.execute("SHOW COLUMNS FROM INVENTARIO")
    columns = cursor.fetchall()

    for column in columns:
        column_name = column[0]  # Nombre de la columna
        
        # Consultar la longitud máxima de la columna
        cursor.execute(f"SELECT MAX(LENGTH({column_name})) FROM INVENTARIO")
        max_length = cursor.fetchone()[0]

        if max_length:  # Verifica que max_length no sea None
            
            # Actualizar registros para igualar la longitud
            update_query = f"""
                UPDATE INVENTARIO
                SET {column_name} = CONCAT({column_name}, SPACE(%s - LENGTH({column_name})))
                WHERE LENGTH({column_name}) < %s
            """
            cursor.execute(update_query, (max_length, max_length))

            # Confirmar cambios
            con.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    con.close()

def columnas_generos():
    # Conectar a la base de datos
    con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")
    cursor = con.cursor()

    # Obtener los nombres de las columnas de la tabla
    cursor.execute("SHOW COLUMNS FROM GENEROS")
    columns = cursor.fetchall()

    for column in columns:
        column_name = column[0]  # Nombre de la columna
        
        # Consultar la longitud máxima de la columna
        cursor.execute(f"SELECT MAX(LENGTH({column_name})) FROM GENEROS")
        max_length = cursor.fetchone()[0]

        if max_length:  # Verifica que max_length no sea None
            
            # Actualizar registros para igualar la longitud
            update_query = f"""
                UPDATE GENEROS
                SET {column_name} = CONCAT({column_name}, SPACE(%s - LENGTH({column_name})))
                WHERE LENGTH({column_name}) < %s
            """
            cursor.execute(update_query, (max_length, max_length))

            # Confirmar cambios
            con.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    con.close()

def columnas_prestamos():
    # Conectar a la base de datos
    con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")
    cursor = con.cursor()

    # Obtener los nombres de las columnas de la tabla
    cursor.execute("SHOW COLUMNS FROM PRESTAMOS")
    columns = cursor.fetchall()

    for column in columns:
        column_name = column[0]  # Nombre de la columna
        
        # Consultar la longitud máxima de la columna
        cursor.execute(f"SELECT MAX(LENGTH({column_name})) FROM PRESTAMOS")
        max_length = cursor.fetchone()[0]

        if max_length:  # Verifica que max_length no sea None
            
            # Actualizar registros para igualar la longitud
            update_query = f"""
                UPDATE PRESTAMOS
                SET {column_name} = CONCAT({column_name}, SPACE(%s - LENGTH({column_name})))
                WHERE LENGTH({column_name}) < %s
            """
            cursor.execute(update_query, (max_length, max_length))

            # Confirmar cambios
            con.commit()

    # Cerrar la conexión a la base de datos
    cursor.close()
    con.close()

def genre():
    try:
        con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")

        if con.is_connected():
            cur=con.cursor()
            cur.execute("SELECT * FROM GENEROS")
            row=cur.fetchall()
            print("==========================")           
            print("|| ID ||    GENERO      ||")
            print("==========================")
            for elemento in row:
                print(f"|| {elemento[0]}  || {elemento[1]}||")
                print("==========================")

            genero=input("Ingrese el id del genero: ")
            
            return genero

    except Exception as e:
        print(f"Error al insertar datos: {e}")

    finally:
        if con.is_connected():
            cur.close()
            con.close()
        
def insert_user(nombre,apellido,dni,telefono,email):
    try:
        con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")

        if con.is_connected():
            cur=con.cursor()
            query="""INSERT INTO USUARIOS(nombre,apellido,dni,telefono,email) VALUES (%s,%s,%s,%s,%s)"""
            values=(nombre,apellido,dni,telefono,email)
            cur.execute(query,values)
            con.commit()
            input("Datos cargados correctamente.")

    except Exception as e:
        print(f"Error al insertar datos: {e}")

    finally:
        if con.is_connected():
            cur.close()
            con.close()

def insert_book(titulo,autor,genero,año_publicacion):
    try:
        con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")

        if con.is_connected():
            cur=con.cursor()
            query="""INSERT INTO INVENTARIO(titulo,autor,genero_id,año_publicacion) VALUES (%s,%s,%s,%s)"""
            values=(titulo,autor,genero,año_publicacion)
            cur.execute(query,values)
            con.commit()
            print("Datos cargados correctamente.")

    except Exception as e:
        print(f"Error al insertar datos: {e}")

    finally:
        if con.is_connected():
            cur.close()
            con.close()

def insert_genre(genero,descripcion):
    try:
        con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")

        if con.is_connected():
            cur=con.cursor()
            query="""INSERT INTO GENEROS(genero,descripcion) VALUES (%s,%s)"""
            values=(genero,descripcion)
            cur.execute(query,values)
            con.commit()
            print("Datos cargados correctamente.")
    except Exception as e:
        print(f"Error al insertar datos: {e}")

    finally:
        if con.is_connected():
            cur.close()
            con.close()

def traer_libros():
    clear()
    try:
        con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")
        
        if con.is_connected():
            cur=con.cursor()
            query="""SELECT INVENTARIO.ID,INVENTARIO.TITULO,INVENTARIO.AUTOR,GENEROS.GENERO FROM INVENTARIO JOIN GENEROS ON GENEROS.ID=INVENTARIO.GENERO_ID; WHERE INVENTARIO.ESTADO=1"""
            cur.execute(query)
            
            lista=cur.fetchall()
            while True:
                clear()
                print("                                 ====== LIBROS ======")
                ids=[]
                for elemento in lista:
                    print(elemento)
                    ids.append(str(elemento[0]))
                print("===============================")
                id=input("Ingrese el ID del libro: ")
                if not id in ids:
                    clear()
                    print("                                 ====== LIBROS ======")
                    print(f"El libro {id} no se encuentra disponible")
                    input("Presione ENTER para continuar...")
                else:
                    break

            return id
        
    except Exception as e:
        print(f"Error en la conexión: {e}")

    finally:
        return None

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

    finally:
        return None  

def insert_loan(libro,usuario):
    try:
        con=mysql.connect(
        host="localhost",
        port=3306,
        user="root",
        database="biblioteca")

        if con.is_connected():
            fecha_estipulada=(datetime.now()+timedelta(days=7)).timestamp()
            cur=con.cursor()
            query="""INSERT INTO PRESTAMOS(FECHA_ESTIPULADA,LIBRO_ID,USUARIO_ID) VALUES (%s,%s,%s)"""
            values=(fecha_estipulada,libro,usuario)
            cur.execute(query,values)
            cur.execute("UPDATE INVENTARIO SET ESTADO=0 WHERE ID=LIBRO_ID")
            con.commit()
            print("Préstamo realizado con éxito.")

    except Exception as e:
        print(f"Error al insertar datos: {e}")

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
            libro=traer_libros()
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
        columnas_usuarios()
        columnas_inventario()
        columnas_prestamos()
        columnas_generos()
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
