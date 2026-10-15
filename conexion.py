import psycopg
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()
# Conectar con PostgreSQL
conexion = psycopg.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT")
)

print("Conexion exitosa")

cursor = conexion.cursor()


# Función para agregar productos
def agregar_producto():
    nombre = input("Nombre del producto: ")
    precio = float(input("Precio: "))
    stock = int(input("Stock: "))
    categoria_id = int(input("ID de categoria: "))

    cursor.execute(
        """
        INSERT INTO productos (nombre, precio, stock, categoria_id)
        VALUES (%s, %s, %s, %s)
        """,
        (nombre, precio, stock, categoria_id)
    )

    conexion.commit()
    print("Producto agregado correctamente")

def ver_productos():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    for producto in productos:
        print(f"ID: {producto[0]} | {producto[1]} | Precio: ${producto[2]} | Stock: {producto[3]}")

    print(f"Total de productos registrados: {len(productos)}")

    total = 0

    for producto in productos:
        total += producto[2] * producto[3]

    print(f"Valor total del inventario: ${total}")

def buscar_producto():
    nombre = input("¿Qué producto deseas buscar? ")

    cursor.execute(
        "SELECT * FROM productos WHERE nombre = %s",
        (nombre,)
    )

    producto = cursor.fetchone()

    if producto is not None:
        print(f"Producto: {producto[1]}")
        print(f"Precio: {producto[2]}")
        print(f"Stock: {producto[3]}")
    else:
        print("Producto no encontrado")

def actualizar_producto():
    nombre = input("Nombre del producto a actualizar: ")
    nuevo_precio = float(input("Nuevo precio: "))

    cursor.execute(
        """
        UPDATE productos
        SET precio = %s
        WHERE nombre = %s
        """,
        (nuevo_precio, nombre)
    )

    conexion.commit()
    print("Producto actualizado correctamente")

def eliminar_producto():
    nombre = input("Nombre del producto a eliminar: ")
    confirmacion = input("Seguro que deseas eliminarlo? s/n: ")

    if confirmacion == "s":

        cursor.execute(
            "DELETE FROM productos WHERE nombre = %s",
            (nombre,)
        )

        conexion.commit()
        print("Producto eliminado correctamente")
    else:
        print("Eliminacion cancelada")

def mostrar_estadisticas():
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()

    print("\n===== ESTADÍSTICAS =====")
    print(f"Productos registrados: {len(productos)}")

    total = 0

    for producto in productos:
        total += producto[3] * producto[2]

    print(f"Valor total del inventario: ${total}")

while True:
    print("\n==== SISTEMA DE INVENTARIO ====")
    print("1. Agregar producto")
    print("2. Ver productos")
    print("3. Buscar producto")
    print("4. Actualizar producto")
    print("5. Eliminar producto")
    print("6. Mostrar estadísticas")
    print("7. Salir")

    opcion = input("Selecciona una opcion: ")

    if opcion == "1":
        agregar_producto()
    elif opcion == "2":
        print("Iniciando consulta...")
        ver_productos()
        print("Consulta finalizada")
    elif opcion == "3":
        buscar_producto()
    elif opcion == "4":
        actualizar_producto()
    elif opcion == "5":
        eliminar_producto()
    elif opcion == "6":
        mostrar_estadisticas()
    elif opcion == "7":
        print("Saliendo del sistema...")
        break
    else:
        print("Opcion no válida. Intenta nuevamente.")

#agregar_producto()
#buscar_producto()
#ver_productos()
#actualizar_producto()
#eliminar_producto()
cursor.close()
conexion.close()