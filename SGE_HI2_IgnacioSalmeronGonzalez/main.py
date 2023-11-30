import customtkinter as ctk
import productos as pr
import clientes as cl
import pedidos as pd

ctk.set_appearance_mode("dark")
ventana = ctk.CTk()
ventana.geometry("400x350")
ventana.title("Inicio")

btnProductos = ctk.CTkButton(ventana, text="PRODUCTOS", command = pr.productos)
btnProductos.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

btnClientes = ctk.CTkButton(ventana, text="CLIENTES", command = cl.clientes)
btnClientes.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

btnPedidos = ctk.CTkButton(ventana, text="PEDIDOS", command = pd.pedidos)
btnPedidos.grid(row=1, column=0, padx=20, pady=20, sticky="ew")


ventana.mainloop()