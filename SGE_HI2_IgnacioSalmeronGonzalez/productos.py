import os
import tkinter as tk
import customtkinter as ctk
import pandas as pd
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

# Declaración de variables globales
entryId = None
entryNom = None
entryCat = None
entryPr = None
entrySt = None
conexion = None
cursor = None
tablaProductos = None
ventana = None

def mostrarDatos(cursor, tablaProductos):
    # Limpiamos la tabla antes de cargar nuevos datos
    tablaProductos.delete(*tablaProductos.get_children())

    # Ejecutamos la consulta y obtenemos los resultados
    cursor.execute('''
        SELECT productos.id_producto, productos.nombre, categorias.categoria, productos.precio, productos.stock
        FROM productos
        JOIN categorias ON productos.id_categoria = categorias.id_categoria
        ''')
    filas = cursor.fetchall()

    # Insertamos los datos en el Treeview
    for fila in filas:
        tablaProductos.insert("", "end", values=fila)

def insert():
    # Obtenemos los valores de los Entry
    nombre = entryNom.get()
    categoria = entryCat.get()
    precio = entryPr.get()
    stock = entrySt.get()

    # Comprobamos si los campos están completos
    if not nombre or not categoria or not precio or not stock:
        messagebox.showinfo(
            message="No todos los campos están completos. Rellene todos a excepción del id.",
            title="Error en sentencia INSERT")
    else:
        try:
            # Convertimos a enteros o floats según corresponda
            precio = float(precio)
            stock = int(stock)
            categoria = int(categoria)

            # Insertamos los datos en la tabla
            cursor.execute("INSERT INTO productos (nombre, id_categoria, precio, stock) VALUES (?, ?, ?, ?)",
                           (nombre, categoria, precio, stock))

            # Confirmamos la sentencia insert
            conexion.commit()

            # Limpiamos los Entry después de la inserción
            entryNom.delete(0, "end")
            entryCat.delete(0, "end")
            entryPr.delete(0, "end")
            entrySt.delete(0, "end")

            # Actualizamos la tabla
            mostrarDatos(cursor, tablaProductos)

        except ValueError as e:
            mensajeError = f"Error en la entrada de datos. Compruebe que el tipo de dato introducido sea correcto. Cod. error: {str(e)}"
            messagebox.showinfo(
                message=mensajeError, title="Error en sentencia INSERT")

def update():
    # Obtenemos los valores de los Entry
    id = entryId.get()
    nombre = entryNom.get()
    categoria = entryCat.get()
    precio = entryPr.get()
    stock = entrySt.get()

    # Comprobamos si los campos están completos
    if (not id or not nombre or not categoria or not precio or not stock):
        messagebox.showinfo(message="No todos los campos están completos. Debe rellenar todos para actualizar una entrada de la tabla.",
                            title="Error en sentencia UPDATE")

    else:
        # Actualizamos los datos en la tabla
        cursor.execute("UPDATE productos SET nombre = ?, id_categoria = ?, precio = ?, stock = ? WHERE id_producto = ?",
                       (nombre, categoria, precio, stock, id))

        # Confirmamos la sentencia update
        conexion.commit()

        # Limpiamos los Entry después de la inserción
        entryNom.delete(0, "end")
        entryCat.delete(0, "end")
        entryPr.delete(0, "end")
        entrySt.delete(0, "end")

        # Actualizamos la tabla
        mostrarDatos(cursor, tablaProductos)


def delete():
    #Obtenemos el id
    id = entryId.get()

    #Comprobamos
    if (not id):
        messagebox.showinfo(message="Introduzca el id de la entrada que desee eliminar.",
                            title="Error en sentencia DELETE")

    else:
        # Eliminamos la sentencia que coincida con ese id
        cursor.execute("DELETE FROM productos WHERE id_producto = ?", (id,))
        conexion.commit()

        entryId.delete(0, "end")

        mostrarDatos(cursor, tablaProductos)

def convertCSV():
    #Creamos un dataframe con los datos de nuestra tabla
    sql = pd.read_sql_query ('''SELECT productos.id_producto, productos.nombre, categorias.categoria, productos.precio, productos.stock
        FROM productos
        JOIN categorias ON productos.id_categoria = categorias.id_categoria''', conexion)
    df = pd.DataFrame(sql, columns = ['id', 'nombre', 'categoria', 'precio', 'stock'])

    #Creamos el nombre del documento con la fecha actual
    time = datetime.datetime.now()
    fecha = time.strftime('%d_%m_%Y-%H_%M_%S')
    nombre="tabla_productos-" + fecha + ".csv"

    # Combinamos la ruta de la carpeta con el nombre del archivo y lo guardamos
    carpeta = os.path.join(os.getcwd(), 'CSVs')
    ruta = os.path.join(carpeta, nombre)
    df.to_csv(ruta)

def grafico():
    # Creamos un dataframe con los datos que mostraremos en nuestro gráfico
    sql = pd.read_sql_query('''SELECT categorias.categoria FROM productos
        JOIN categorias ON productos.id_categoria = categorias.id_categoria''', conexion)
    df = pd.DataFrame(sql, columns=['categoria'])

    # Calcular la frecuencia de cada código postal
    frecuencia_cp = df['categoria'].value_counts()

    # Crear el gráfico tipo "pie"
    fig, ax = plt.subplots()
    ax.pie(frecuencia_cp, labels=frecuencia_cp.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Crear una ventana para el pop-up
    popup = tk.Toplevel(ventana)
    popup.title("Porcentaje de productos por categoría")

    # Incorporar el gráfico en la interfaz de Tkinter
    canvas = FigureCanvasTkAgg(fig, master=popup)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()

    # Botón para cerrar el pop-up
    btnCerrar = ttk.Button(popup, text="OK", command=popup.destroy)
    btnCerrar.pack(pady=10)

def ordenarPorColumna(treeview, col, reverse):
    data = [ (treeview.set(child, col), child) for child in treeview.get_children('')]
    data.sort(reverse=reverse)

    for i, item in enumerate(data):
        treeview.move(item[1], '', i)
    treeview.heading(col, command=lambda: ordenarPorColumna(treeview, col, not reverse))
def productos():
    global entryId, entryNom, entryCat, entryPr, entrySt, conexion, cursor, tablaProductos, ventana

    #Config. general de la ventana
    ctk.set_appearance_mode("dark")
    ventana = ctk.CTk()
    ventana.geometry("925x600")
    ventana.title("Productos")

    #Conexión con la BBDD. Se crea si no existe
    conexion = sqlite3.connect("supermercado.db")
    cursor = conexion.cursor()

    #Si no existe las tablas se crean
    cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (
                                id_categoria INTEGER PRIMARY KEY,
                                categoria TEXT
                            )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS productos (
                        id_producto INTEGER PRIMARY KEY,
                        nombre TEXT,
                        id_categoria INTEGER,
                        precio FLOAT, 
                        stock INTEGER, 
                        foreign key (id_categoria) references categorias (id_categoria)
                    )''')


    #Botones y elementos visuales
    titulo = ctk.CTkLabel(ventana, text="PRODUCTOS", font=("Eras Demi ITC", 30))
    titulo.grid(row=0, column=0, columnspan=6, padx=10, pady=20)

    ctk.CTkLabel(ventana, text="Id:", font=("Eras Demi ITC", 15)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
    entryId = ctk.CTkEntry(ventana)
    entryId.grid(row=1, column=1, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Nombre:", font=("Eras Demi ITC", 15)).grid(row=1, column=2, sticky="e", padx=10, pady=10)
    entryNom = ctk.CTkEntry(ventana)
    entryNom.grid(row=1, column=3, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Categoría (id):", font=("Eras Demi ITC", 15)).grid(row=1, column=4, sticky="e", padx=10, pady=10)
    entryCat = ctk.CTkEntry(ventana)
    entryCat.grid(row=1, column=5, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Precio:", font=("Eras Demi ITC", 15)).grid(row=2, column=0, sticky="e", padx=10, pady=10)
    entryPr = ctk.CTkEntry(ventana)
    entryPr.grid(row=2, column=1, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Stock:", font=("Eras Demi ITC", 15)).grid(row=2, column=2, sticky="e", padx=10, pady=10)
    entrySt = ctk.CTkEntry(ventana)
    entrySt.grid(row=2, column=3, padx=15, pady=15)

    #Botones CRUD
    btnInsert = (ctk.CTkButton(ventana, text="AÑADIR", command=insert, font=("Eras Demi ITC", 12)))
    btnInsert.grid(row=3, column=2, pady=10)

    btnUpdate = (ctk.CTkButton(ventana, text="ACTUALIZAR", command=update, font=("Eras Demi ITC", 12)))
    btnUpdate.grid(row=3, column=3, pady= 10)

    btnDelete = (ctk.CTkButton(ventana, text="ELIMINAR", command=delete, font=("Eras Demi ITC", 12)))
    btnDelete.grid(row=3, column=4, pady=10)

    btnCSV = (ctk.CTkButton(ventana, text="EXPORTAR A CSV", command=convertCSV, font=("Eras Demi ITC", 12)))
    btnCSV.grid(row=5, column=3, pady=10)

    btnGrafico = (ctk.CTkButton(ventana, text="MOSTRAR GRÁFICO", command=grafico, font=("Eras Demi ITC", 12)))
    btnGrafico.grid(row=5, column=1, pady=10)

    #Creamos el treeview
    tablaProductos = ttk.Treeview(ventana, columns=("id", "nombre", "categoria", "precio", "stock"),
                               show="headings", selectmode="browse",)
    #Añadimos sus encabezados (headings)
    tablaProductos.heading("id", text="ID", command=lambda: mostrarDatos(cursor, tablaProductos))
    tablaProductos.heading("nombre", text="Nombre", command=lambda: ordenarPorColumna(tablaProductos, "nombre", False))
    tablaProductos.heading("categoria", text="Categoria", command=lambda: ordenarPorColumna(tablaProductos, "categoria", False))
    tablaProductos.heading("precio", text="Precio")
    tablaProductos.heading("stock", text="Stock")

    #Rellenamos el treeview con los datos de nuestra tabla, y lo mostramos
    mostrarDatos(cursor, tablaProductos)
    tablaProductos.grid(row=4, column=1, padx=20, pady=20, rowspan=1, columnspan=5, sticky="nsew")
    for col in ("id", "nombre", "categoria", "precio", "stock"):
        tablaProductos.column(col, width=130)



    ventana.mainloop()
