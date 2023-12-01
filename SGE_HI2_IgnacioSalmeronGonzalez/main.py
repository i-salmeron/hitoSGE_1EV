import customtkinter as ctk
import productos as pr
import clientes as cl
import pedidos as pd
from PIL import Image

ctk.set_appearance_mode("dark")
ventana = ctk.CTk()
ventana.geometry("400x350")
ventana.title("Inicio")

btnProductos = ctk.CTkButton(ventana, text="PRODUCTOS", command=pr.productos)
btnProductos.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

btnClientes = ctk.CTkButton(ventana, text="CLIENTES", command=cl.clientes)
btnClientes.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

btnPedidos = ctk.CTkButton(ventana, text="PEDIDOS", command=pd.pedidos)
btnPedidos.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

#cat = ctk.CTkImage(light_image=Image.open("G://Mi unidad//2ºDAM//Sistemas de Gestión Empresarial//HITOS//H2_SistemasGestionEmpresarial_1T_Aitor_BarriosGarcia//img//categoria.png"),
                    #dark_image=Image.open("G://Mi unidad//2ºDAM//Sistemas de Gestión Empresarial//HITOS//H2_SistemasGestionEmpresarial_1T_Aitor_BarriosGarcia//img//categoria.png"),size=(70,70))
                    #,image=cat
ventana.mainloop()