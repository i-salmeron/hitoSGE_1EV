import os
import customtkinter as ctk
import pandas as pd
from tkinter import ttk, messagebox
import sqlite3
import datetime
from tkcalendar import DateEntry

# Declaración de variables globales
entryId = None
entryProd = None
entryNum = None
entryCli = None
entryFecha = None
conexion = None
cursor = None
tablaPedidos = None
ventana = None

def mostrarDatos(cursor, tablaPedidos):
    # Limpiamos la tabla antes de cargar nuevos datos
    tablaPedidos.delete(*tablaPedidos.get_children())

    # Ejecutamos la consulta y obtenemos los resultados
    cursor.execute('''
            SELECT pedidos.id_pedido, clientes.nombre, productos.nombre, 
            detalle.unidades, pedidos.fechapedido, detalle.total
            FROM pedidos
            JOIN clientes ON pedidos.id = clientes.id
            JOIN detalle ON pedidos.id_pedido = detalle.id_pedido
            JOIN productos ON detalle.id_producto = productos.id_producto
            ''')
    filas = cursor.fetchall()

    # Insertamos los datos en el Treeview
    for fila in filas:
        tablaPedidos.insert("", "end", values=fila)

def insert():
    # Obtenemos los valores de los Entry
    producto = entryProd.get()
    unidades = entryNum.get()
    cliente = entryCli.get()
    fecha = entryFecha.get()

    #Comprobamos si los campos están completos
    if(not producto or not unidades or not cliente or not fecha):
        messagebox.showinfo(message="No todos los campos están completos. Rellene todos a excepción del id.",
                            title="Error en sentencia INSERT")

    else:
        # Insertamos los datos en las tablas
        cursor.execute("INSERT INTO pedidos (id, fechapedido) VALUES (?, ?)",
                       (cliente, fecha))

        # Confirmamos la sentencia insert
        conexion.commit()

        #Obtenemos el id del pedido
        cursor.execute("SELECT id_pedido FROM pedidos ORDER BY id_pedido DESC LIMIT 1")
        numPedido = cursor.fetchone()
        numPedido = int(numPedido[0])

        #Obtenemos el total del pedido
        cursor.execute("SELECT precio FROM productos WHERE id_producto = ?", (producto,))
        precioProducto = cursor.fetchone()
        precioProducto = float(precioProducto[0])

        unidades = int(unidades)

        total = round(precioProducto * unidades, 2)

        #Insertamos los detalles del pedido
        cursor.execute("INSERT INTO detalle (id_pedido, id_producto, unidades, total) VALUES (?, ?, ?, ?)",
                       (numPedido, producto, unidades, total))

        # Confirmamos la sentencia insert
        conexion.commit()

        # Limpiamos los Entry después de la inserción
        entryProd.delete(0, "end")
        entryNum.delete(0, "end")
        entryCli.delete(0, "end")
        entryFecha.delete(0, "end")

        # Actualizamos la tabla
        mostrarDatos(cursor, tablaPedidos)

def update():
    # Obtenemos los valores de los Entry
    id = entryId.get()
    producto = entryProd.get()
    unidades = entryNum.get()
    fecha = entryFecha.get()
    cliente = entryCli.get()

    # Comprobamos si los campos están completos
    if (not id or not producto or not unidades or not fecha or not cliente):
        messagebox.showinfo(message="No todos los campos están completos. Debe rellenar todos para actualizar una entrada de la tabla.",
                            title="Error en sentencia UPDATE")

    else:
        # Actualizamos los datos en la tabla
        cursor.execute("UPDATE pedidos SET id = ?, fechapedido = ? WHERE id_pedido = ?",
                       (cliente, fecha, id))

        # Confirmamos la sentencia update
        conexion.commit()

        # Obtenemos el total del pedido
        cursor.execute("SELECT precio FROM productos WHERE id_producto = ?", (producto,))
        precioProducto = cursor.fetchone()
        precioProducto = float(precioProducto[0])

        unidades = int(unidades)

        total = round(precioProducto * unidades, 2)

        # Actualizamos los datos en la tabla
        cursor.execute("UPDATE detalle SET id_pedido = ?, id_producto = ?, unidades = ?, total = ? WHERE id_pedido = ?",
                       (id, producto, unidades, total, id))

        # Confirmamos la sentencia update
        conexion.commit()

        # Limpiamos los Entry después de la inserción
        entryId.delete(0, "end")
        entryProd.delete(0, "end")
        entryNum.delete(0, "end")
        entryFecha.delete(0, "end")
        entryCli.delete(0, "end")

        # Actualizamos la tabla
        mostrarDatos(cursor, tablaPedidos)


def delete():
    #Obtenemos el id
    id = entryId.get()

    #Comprobamos
    if (not id):
        messagebox.showinfo(message="Introduzca el id de la entrada que desee eliminar.",
                            title="Error en sentencia DELETE")

    else:
        # Eliminamos la sentencia que coincida con ese id
        cursor.execute('''DELETE FROM pedidos WHERE id_pedido = ?''', (id,))
        conexion.commit()

        cursor.execute('''DELETE FROM detalle WHERE id_pedido = ?''', (id,))
        conexion.commit()

        entryId.delete(0, "end")

        mostrarDatos(cursor, tablaPedidos)

def convertCSV():
    #Creamos un dataframe con los datos de nuestra tabla
    sql = pd.read_sql_query ('''SELECT pedidos.id_pedido, clientes.nombre as cnombre, productos.nombre as pnombre, 
            detalle.unidades, pedidos.fechapedido, detalle.total
            FROM pedidos
            JOIN clientes ON pedidos.id = clientes.id
            JOIN detalle ON pedidos.id_pedido = detalle.id_pedido
            JOIN productos ON detalle.id_producto = productos.id_producto''', conexion)
    df = pd.DataFrame(sql, columns = ['id', 'cliente', 'producto', 'unidades', 'fecha', 'total'])

    #Creamos el nombre del documento con la fecha actual
    time = datetime.datetime.now()
    fecha = time.strftime('%d_%m_%Y-%H_%M_%S')
    nombre="tabla_pedidos-" + fecha + ".csv"

    # Combinamos la ruta de la carpeta con el nombre del archivo y lo guardamos
    carpeta = os.path.join(os.getcwd(), 'CSVs')
    ruta = os.path.join(carpeta, nombre)
    df.to_csv(ruta)


def ordenarPorColumna(treeview, col, reverse):
    data = [ (treeview.set(child, col), child) for child in treeview.get_children('')]
    data.sort(reverse=reverse)

    for i, item in enumerate(data):
        treeview.move(item[1], '', i)
    treeview.heading(col, command=lambda: ordenarPorColumna(treeview, col, not reverse))
def pedidos():
    global entryId, entryProd, entryNum, entryCli, entryFecha, conexion, cursor, tablaPedidos, ventana

    #Config. general de la ventana
    ctk.set_appearance_mode("dark")
    ventana = ctk.CTk()
    ventana.geometry("970x485")
    ventana.title("Clientes")

    #Conexión con la BBDD. Se crea si no existe
    conexion = sqlite3.connect("supermercado.db")
    cursor = conexion.cursor()

    #Si no existen las tablas se crean
    cursor.execute('''CREATE TABLE IF NOT EXISTS detalle (
                                    id_pedido INTEGER,
                                    id_producto TEXT,
                                    unidades INTEGER,
                                    total FLOAT,
                                    foreign key (id_pedido) references pedidos (id_pedido),
                                    foreign key (id_producto) references productos (id_producto)
                                )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS pedidos (
                        id_pedido INTEGER PRIMARY KEY,
                        id INTEGER,
                        fechapedido DATETIME,
                        foreign key (id) references clientes (id)
                    )''')

    #Botones y elementos visuales
    ctk.CTkLabel(ventana, text="Id:").grid(row=0, column=0, sticky="e", padx=10, pady=10)
    entryId = ctk.CTkEntry(ventana)
    entryId.grid(row=0, column=1, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Cliente (id):").grid(row=1, column=0, sticky="e", padx=10, pady=10)
    entryCli = ctk.CTkEntry(ventana)
    entryCli.grid(row=1, column=1, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Producto (id):").grid(row=0, column=2, sticky="e", padx=10, pady=10)
    entryProd = ctk.CTkEntry(ventana)
    entryProd.grid(row=0, column=3, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Nº unidades:").grid(row=0, column=4, sticky="e", padx=10, pady=10)
    entryNum = ctk.CTkEntry(ventana)
    entryNum.grid(row=0, column=5, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Fecha del pedido:").grid(row=1, column=2, sticky="e", padx=10, pady=10)
    entryFecha = DateEntry(ventana, selectmode='day')
    entryFecha.grid(row=1, column=3, padx=15, pady=15)


    #Botones CRUD
    btnInsert = (ctk.CTkButton(ventana, text="AÑADIR", command=insert))
    btnInsert.grid(row=2, column=2, pady=10)

    btnUpdate = (ctk.CTkButton(ventana, text="ACTUALIZAR", command=update))
    btnUpdate.grid(row=2, column=3, pady= 10)

    btnDelete = (ctk.CTkButton(ventana, text="ELIMINAR", command=delete))
    btnDelete.grid(row=2, column=4, pady=10)

    btnCSV = (ctk.CTkButton(ventana, text="EXPORTAR A CSV", command=convertCSV))
    btnCSV.grid(row=4, column=3, pady=10)

    #Creamos el treeview
    tablaPedidos = ttk.Treeview(ventana, columns=("id", "cliente", "producto", "unidades", "fecha", "total"),
                               show="headings", selectmode="browse",)
    #Añadimos sus encabezados (headings)
    tablaPedidos.heading("id", text="ID", command=lambda: mostrarDatos(cursor, tablaPedidos))
    tablaPedidos.heading("cliente", text="Cliente", command=lambda: ordenarPorColumna(tablaPedidos, "cliente", False))
    tablaPedidos.heading("producto", text="Producto", command=lambda: ordenarPorColumna(tablaPedidos, "producto", False))
    tablaPedidos.heading("unidades", text="Nº unidades")
    tablaPedidos.heading("fecha", text="Fecha", command=lambda: ordenarPorColumna(tablaPedidos, "fecha", False))
    tablaPedidos.heading("total", text="Total")

    #Rellenamos el treeview con los datos de nuestra tabla, y lo mostramos
    mostrarDatos(cursor, tablaPedidos)
    tablaPedidos.grid(row=3, column=1, padx=20, pady=20, rowspan=1, columnspan=5, sticky="nsew")
    for col in ("id", "cliente", "producto", "unidades", "fecha", "total"):
        tablaPedidos.column(col, width=130)



    ventana.mainloop()
