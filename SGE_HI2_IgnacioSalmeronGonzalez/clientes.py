import tkinter as tk
import customtkinter as ctk
import pandas as pd
from tkinter import ttk
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Declaración de variables globales
entryId = None
entryNom = None
entryApe = None
entryDir = None
entryCp = None
entryTlf = None
conexion = None
cursor = None
tablaClientes = None
ventana = None

def mostrarDatos(cursor, tablaClientes):
    # Limpiamos la tabla antes de cargar nuevos datos
    tablaClientes.delete(*tablaClientes.get_children())

    # Ejecutamos la consulta y obtenemos los resultados
    cursor.execute("SELECT * FROM clientes")
    filas = cursor.fetchall()

    # Insertamos los datos en el Treeview
    for fila in filas:
        tablaClientes.insert("", "end", values=fila)

def insert():
    # Obtenemos los valores de los Entry
    nombre = entryNom.get()
    apellido = entryApe.get()
    direccion = entryDir.get()
    cp = entryCp.get()
    tlf = entryTlf.get()

    # Insertamos los datos en la tabla
    cursor.execute("INSERT INTO clientes (nombre, apellido, direccion, cp, tlf) VALUES (?, ?, ?, ?, ?)",
                   (nombre, apellido, direccion, cp, tlf))

    # Confirmamos la sentencia insert
    conexion.commit()

    # Limpiamos los Entry después de la inserción
    entryNom.delete(0, "end")
    entryApe.delete(0, "end")
    entryDir.delete(0, "end")
    entryCp.delete(0, "end")
    entryTlf.delete(0, "end")

    # Actualizamos la tabla
    mostrarDatos(cursor, tablaClientes)

def update():
    # Obtenemos los valores de los Entry
    id = entryId.get()
    nombre = entryNom.get()
    apellido = entryApe.get()
    direccion = entryDir.get()
    cp = entryCp.get()
    tlf = entryTlf.get()

    # Actualizamos los datos en la tabla
    cursor.execute("UPDATE clientes SET nombre = ?, apellido = ?, direccion = ?, cp = ?, tlf = ? WHERE id = ?",
                   (nombre, apellido, direccion, cp, tlf, id))

    # Confirmamos la sentencia update
    conexion.commit()

    # Limpiamos los Entry después de la inserción
    entryNom.delete(0, "end")
    entryApe.delete(0, "end")
    entryDir.delete(0, "end")
    entryCp.delete(0, "end")
    entryTlf.delete(0, "end")

    # Actualizamos la tabla
    mostrarDatos(cursor, tablaClientes)

def delete():
    #Obtenemos el id
    id = entryId.get()

    #Eliminamos la sentencia que coincida con ese id
    cursor.execute("DELETE FROM clientes WHERE id=?", id)
    conexion.commit()

    entryId.delete(0, "end")

    mostrarDatos(cursor, tablaClientes)

def convertCSV():
    #Creamos un dataframe con los datos de nuestra tabla
    sql = pd.read_sql_query ('''SELECT * FROM clientes''', conexion)
    df = pd.DataFrame(sql, columns = ['id', 'nombre', 'apellido', 'direccion', 'cp', 'tlf'])

    #Y los exportamos a un archivo .csv
    df.to_csv('tabla_clientes.csv')

def grafico():
    # Creamos un dataframe con los datos que mostraremos en nuestro gráfico
    sql = pd.read_sql_query('''SELECT cp FROM clientes''', conexion)
    df = pd.DataFrame(sql, columns=['cp'])

    # Calcular la frecuencia de cada código postal
    frecuencia_cp = df['cp'].value_counts()

    # Crear el gráfico tipo "pie"
    fig, ax = plt.subplots()
    ax.pie(frecuencia_cp, labels=frecuencia_cp.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')

    # Crear una ventana para el pop-up
    popup = tk.Toplevel(ventana)
    popup.title("Porcentaje de clientes por código postal")

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
def clientes():
    global entryId, entryNom, entryApe, entryDir, entryCp, entryTlf, conexion, cursor, tablaClientes, ventana

    #Config. general de la ventana
    ctk.set_appearance_mode("dark")
    ventana = ctk.CTk()
    ventana.geometry("970x485")
    ventana.title("Clientes")

    #Conexión con la BBDD. Se crea si no existe
    conexion = sqlite3.connect("supermercado.db")
    cursor = conexion.cursor()

    #Si no existe la tabla se crea
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY,
                        nombre TEXT,
                        apellido TEXT,
                        direccion TEXT, 
                        cp INTEGER, 
                        tlf INTEGER
                    )''')

    #Botones y elementos visuales
    ctk.CTkLabel(ventana, text="Id:").grid(row=0, column=0, sticky="e", padx=10, pady=10)
    entryId = ctk.CTkEntry(ventana)
    entryId.grid(row=0, column=1, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Nombre:").grid(row=0, column=2, sticky="e", padx=10, pady=10)
    entryNom = ctk.CTkEntry(ventana)
    entryNom.grid(row=0, column=3, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Apellido:").grid(row=0, column=4, sticky="e", padx=10, pady=10)
    entryApe = ctk.CTkEntry(ventana)
    entryApe.grid(row=0, column=5, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Dirección:").grid(row=1, column=0, sticky="e", padx=10, pady=10)
    entryDir = ctk.CTkEntry(ventana)
    entryDir.grid(row=1, column=1, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="CP:").grid(row=1, column=2, sticky="e", padx=10, pady=10)
    entryCp = ctk.CTkEntry(ventana)
    entryCp.grid(row=1, column=3, padx=15, pady=15)

    ctk.CTkLabel(ventana, text="Teléfono:").grid(row=1, column=4, sticky="e", padx=10, pady=10)
    entryTlf = ctk.CTkEntry(ventana)
    entryTlf.grid(row=1, column=5, padx=15, pady=15)

    #Botones CRUD
    btnInsert = (ctk.CTkButton(ventana, text="AÑADIR", command=insert))
    btnInsert.grid(row=2, column=2, pady=10)

    btnUpdate = (ctk.CTkButton(ventana, text="ACTUALIZAR", command=update))
    btnUpdate.grid(row=2, column=3, pady= 10)

    btnDelete = (ctk.CTkButton(ventana, text="ELIMINAR", command=delete))
    btnDelete.grid(row=2, column=4, pady=10)

    btnCSV = (ctk.CTkButton(ventana, text="EXPORTAR A CSV", command=convertCSV))
    btnCSV.grid(row=4, column=3, pady=10)

    btnGrafico = (ctk.CTkButton(ventana, text="GRÁFICO", command=grafico))
    btnGrafico.grid(row=4, column=1, pady=10)

    #Creamos el treeview
    tablaClientes = ttk.Treeview(ventana, columns=("id", "nombre", "apellido", "direccion", "cp", "tlf"),
                               show="headings", selectmode="browse",)
    #Añadimos sus encabezados (headings)
    tablaClientes.heading("id", text="ID", command=lambda: mostrarDatos(cursor, tablaClientes))
    tablaClientes.heading("nombre", text="Nombre", command=lambda: ordenarPorColumna(tablaClientes, "nombre", False))
    tablaClientes.heading("apellido", text="Apellido", command=lambda: ordenarPorColumna(tablaClientes, "apellido", False))
    tablaClientes.heading("direccion", text="Dirección")
    tablaClientes.heading("cp", text="Código postal", command=lambda: ordenarPorColumna(tablaClientes, "cp", False))
    tablaClientes.heading("tlf", text="Teléfono")

    #Aplicamos estilo al encabezado
    #estiloTreeview = tk.style()
    #estiloTreeview.configure("Treeview", background="blue", foreground="white")

    #Rellenamos el treeview con los datos de nuestra tabla, y lo mostramos
    mostrarDatos(cursor, tablaClientes)
    tablaClientes.grid(row=3, column=1, padx=20, pady=20, rowspan=1, columnspan=5, sticky="nsew")
    for col in ("id", "nombre", "apellido", "direccion", "cp", "tlf"):
        tablaClientes.column(col, width=130)



    ventana.mainloop()

