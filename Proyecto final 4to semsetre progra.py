
import psycopg2  

# conexion a la base de datos
connection = psycopg2.connect(
    host="localhost",  
    port="5432",  
    database="bd-ltd",  
    user="STRYKER",  
    password="STRYKER237",  
)

connection.autocommit = True
cursor = connection.cursor()

# ==============================================================================
class GestionEstudiantes:
    @staticmethod
    def crear_Estudiante():
        carnet = input("Ingrese el carnet: ")
        nombre = input("Ingrese el nombre: ")
        carrera = input("Ingrese la carrera: ")
        query = """INSERT INTO tabla_gestion (carnet, nombre, carrera) VALUES (%s, %s, %s)"""
        cursor.execute(query, (carnet, nombre, carrera))
        connection.commit()
        print("Estudiante agregado exitosamente.")

    @staticmethod
    def eliminar_estudiante():
        carnet = input("Ingrese el carnet del estudiante que desea eliminar: ")
        query = """DELETE FROM tabla_gestion WHERE carnet = %s"""
        cursor.execute(query, (carnet,))
        connection.commit()
        print("Estudiante eliminado exitosamente.")

    @staticmethod
    def modificar_estudiante():
        carnet = input("Ingrese el carnet del estudiante que desea modificar: ")
        nueva_carrera = input("Ingrese la nueva carrera: ")
        query = """UPDATE tabla_gestion SET carrera = %s WHERE carnet = %s"""
        cursor.execute(query, (nueva_carrera, carnet))
        connection.commit()
        print("Carrera modificada exitosamente.")

    @staticmethod
    def mostrar_menu1():
        while True:
            print("\n--- Menu de Estudiantes ---")
            print("1. Crear estudiante")
            print("2. Eliminar estudiante")
            print("3. Modificar estudiante")
            print("4. Salir")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                GestionEstudiantes.crear_Estudiante()
            elif opcion == "2":
                GestionEstudiantes.eliminar_estudiante()
            elif opcion == "3":
                GestionEstudiantes.modificar_estudiante()
            elif opcion == "4":
                print("Saliendo del menú de gestión de estudiantes...")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")


class RegistroNotas:
    @staticmethod
    def registrar_notas():
        carnet = input("Ingrese el carnet del estudiante: ")
        query = "SELECT * FROM tabla_gestion WHERE carnet = %s"
        cursor.execute(query, (carnet,))
        estudiante = cursor.fetchone()
        if estudiante:
            primer_parcial = int(input("Ingrese la nota del primer parcial: "))
            segundo_parcial = int(input("Ingrese la nota del segundo parcial: "))
            tercer_parcial = int(input("Ingrese la nota del tercer parcial: "))
            update_query = """UPDATE tabla_gestion 
                            SET primer_parcial = %s, segundo_parcial = %s, tercer_parcial = %s 
                            WHERE carnet = %s"""
            cursor.execute(update_query, (primer_parcial, segundo_parcial, tercer_parcial, carnet))
            connection.commit()
            print("Notas registradas exitosamente.")
        else:
            print("Estudiante no encontrado.")

    @staticmethod
    def mostrar_notas():
        query = "SELECT carnet, nombre, primer_parcial, segundo_parcial, tercer_parcial FROM tabla_gestion"
        cursor.execute(query)
        notas = cursor.fetchall()
        if notas:
            print("\n--- Notas de los Estudiantes ---")
            print("Carnet\t\tNombre\t\tPrimer Parcial\tSegundo Parcial\tTercer Parcial")
            for nota in notas:
                carnet, nombre, primer_parcial, segundo_parcial, tercer_parcial = nota
                print(f"{carnet}\t{nombre}\t{primer_parcial}\t{segundo_parcial}\t{tercer_parcial}")
        else:
            print("No hay notas registradas en la base de datos.")

    @staticmethod
    def notas_faltantes():
        query = """
            SELECT carnet, nombre, primer_parcial, segundo_parcial, tercer_parcial 
            FROM tabla_gestion 
            WHERE primer_parcial IS NULL OR segundo_parcial IS NULL OR tercer_parcial IS NULL"""
        cursor.execute(query)
        estudiantes_con_notas_faltantes = cursor.fetchall()
        if estudiantes_con_notas_faltantes:
            print("\n--- Estudiantes con Notas Faltantes ---")
            print("Carnet\t\tNombre\t\tPrimer Parcial\tSegundo Parcial\tTercer Parcial")
            for estudiante in estudiantes_con_notas_faltantes:
                carnet, nombre, primer_parcial, segundo_parcial, tercer_parcial = estudiante
                primer_parcial = primer_parcial if primer_parcial is not None else "Faltante"
                segundo_parcial = segundo_parcial if segundo_parcial is not None else "Faltante"
                tercer_parcial = tercer_parcial if tercer_parcial is not None else "Faltante"
                print(f"{carnet}\t{nombre}\t{primer_parcial}\t{segundo_parcial}\t{tercer_parcial}")
        else:
            print("No hay estudiantes con notas faltantes.")

    @staticmethod
    def agregar_curso():
        carnet = input("Ingrese el carnet del estudiante al que desea asignar el curso: ")
        curso = input("Ingrese el nombre del curso: ")
        
        cursor.execute("SELECT * FROM tabla_gestion WHERE carnet = %s", (carnet,))
        estudiante = cursor.fetchone()
        
        if estudiante:
            query = "UPDATE tabla_gestion SET curso = %s WHERE carnet = %s"
            cursor.execute(query, (curso, carnet))
            connection.commit()
            print("Curso agregado exitosamente al estudiante.")
        else:
            print("No se encontró un estudiante con ese carnet.")

    @staticmethod
    def mostrar_menu2():
        while True:
            print("\n--- Menu de Registro de Notas ---")
            print("1. Registrar Notas")
            print("2. Mostrar Notas")
            print("3. Notas Faltantes")
            print("4. Agregar curso")
            print("5. Salir")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                RegistroNotas.registrar_notas()
            elif opcion == "2":
                RegistroNotas.mostrar_notas()
            elif opcion == "3":
                RegistroNotas.notas_faltantes()
            elif opcion == "4":
                RegistroNotas.agregar_curso()
            elif opcion == "5":
                print("Saliendo del menú de registro de notas...")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")

class Busquedas:
    @staticmethod
    def buscar_por_nombre():
        nombre = input("Ingrese el nombre del estudiante: ")
        query = "SELECT carnet, nombre, carrera FROM tabla_gestion WHERE nombre ILIKE %s"
        cursor.execute(query, ('%' + nombre + '%',))
        estudiantes = cursor.fetchall()
        if estudiantes:
            print("\n--- Estudiantes encontrados ---")
            print("Carnet\t\tNombre\t\tCarrera")
            for estudiante in estudiantes:
                print(f"{estudiante[0]}\t{estudiante[1]}\t{estudiante[2]}")
        else:
            print("No se encontraron estudiantes con ese nombre.")

    @staticmethod
    def buscar_por_carrera():
        carrera = input("Ingrese la carrera del estudiante: ")
        query = "SELECT carnet, nombre, carrera FROM tabla_gestion WHERE carrera ILIKE %s"
        cursor.execute(query, ('%' + carrera + '%',))
        estudiantes = cursor.fetchall()
        if estudiantes:
            print("\n--- Estudiantes encontrados ---")
            print("Carnet\t\tNombre\t\tCarrera")
            for estudiante in estudiantes:
                print(f"{estudiante[0]}\t{estudiante[1]}\t{estudiante[2]}")
        else:
            print("No se encontraron estudiantes con esa carrera.")

    @staticmethod
    def buscar_por_curso():
        curso = input("Ingrese el curso del estudiante: ")
        query = "SELECT carnet, nombre, carrera FROM tabla_gestion WHERE curso ILIKE %s"
        cursor.execute(query, ('%' + curso + '%',))
        estudiantes = cursor.fetchall()
        if estudiantes:
            print("\n--- Estudiantes encontrados ---")
            print("Carnet\t\tNombre\t\tCarrera")
            for estudiante in estudiantes:
                print(f"{estudiante[0]}\t{estudiante[1]}\t{estudiante[2]}")
        else:
            print("No se encontraron estudiantes con ese curso.")

    @staticmethod
    def mostrar_menu3():
        while True:
            print("\n--- Menu de Búsquedas ---")
            print("1. Buscar por Nombre")
            print("2. Buscar por Carrera")
            print("3. Buscar por Curso")
            print("4. Salir")

            opcion = input("Seleccione una opcion: ")

            if opcion == "1":
                Busquedas.buscar_por_nombre()
            elif opcion == "2":
                Busquedas.buscar_por_carrera()
            elif opcion == "3":
                Busquedas.buscar_por_curso()
            elif opcion == "4":
                print("Saliendo del menú de búsquedas...")
                break
            else:
                print("Opción inválida. Por favor, seleccione una opción válida.")


def main():
    while True:
        print("\n<<<<< Menú de Gestiones Principal >>>>>")
        print(  "1. Gestionar Estudiantes")
        print(  "2. Gestionar Notas")
        print(  "3. Búsquedas")
        print(  "4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            GestionEstudiantes.mostrar_menu1()
        elif opcion == "2":
            RegistroNotas.mostrar_menu2()
        elif opcion == "3":
            Busquedas.mostrar_menu3()
        elif opcion == "4":
            print("saliendo del programa...")
            break    
        else:
            print("opcion invalida intente de nuevo")


if __name__ == "__main__":
    main()

