import customtkinter as ctk
import productos as pr
import clientes as cl
import pedidos as pd
from PIL import Image

ctk.set_appearance_mode("dark")
ventana = ctk.CTk()
ventana.geometry("445x340")
ventana.title("Inicio")

titulo = ctk.CTkLabel(ventana, text="SUPERMERCADO", font=("Eras Demi ITC", 30))
titulo.grid(row=0, column=0, columnspan=2, padx=10, pady=20)

imgProductos = ctk.CTkImage(light_image=Image.open("imgs/productos.png"),
                            dark_image=Image.open("imgs/productos.png"), size=(80, 80))
btnProductos = ctk.CTkButton(ventana, text="PRODUCTOS", command=pr.productos, image=imgProductos, text_color="black", font=("Eras Demi ITC", 15))
btnProductos.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

imgClientes = ctk.CTkImage(light_image=Image.open("imgs/clientes.png"),
                            dark_image=Image.open("imgs/clientes.png"), size=(80, 80))
btnClientes = ctk.CTkButton(ventana, text="CLIENTES", command=cl.clientes, image=imgClientes, text_color="black", font=("Eras Demi ITC", 15))
btnClientes.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

imgPedidos = ctk.CTkImage(light_image=Image.open("imgs/pedidos.png"),
                            dark_image=Image.open("imgs/pedidos.png"), size=(80, 80))
btnPedidos = ctk.CTkButton(ventana, text="PEDIDOS", command=pd.pedidos, image=imgPedidos, text_color="black", font=("Eras Demi ITC", 15))
btnPedidos.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

ventana.mainloop()