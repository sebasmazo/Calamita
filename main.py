from email import message
from tkinter import *
from tkinter import ttk

from matplotlib.pyplot import title
from Class.Empresa import Empresa
from tkinter import messagebox

try: 
    empresa_usuario = None       
    GUI = Tk()
    GUI.title("Calamita")
    GUI.geometry("1280x720")
    frm = ttk.Frame(GUI, padding=10)
    frm.grid()
    ttk.Label(frm, text="Bienvenido a nuestro software de perfilamiento, Calamita").grid(column=0,row=0)
    ttk.Label(frm, text="Registrarse").grid(column=0,row=1)
   
    def createEmpresa(nombre_empresa,sector_empresa):
        name_obj = nombre_empresa.get()
        sector_obj = sector_empresa.get()
        if name_obj != "" and sector_obj!= "":      
            nombre_empresa.config(state=DISABLED)
            sector_empresa.config(state=DISABLED)
            empresa_usuario = Empresa(name_obj, sector_obj)
            messagebox.showinfo(message="Registro exitoso", title="Update")
            #Habilitar botón en el GUI principal para upload data manejar un flujo permisivo con estados de botones
        else:
            messagebox.showerror(message="Por favor llenar los datos necesarios", title="Warning")
        
    def openNewWindow() -> None:
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(GUI)
        # sets the title of the
        # Toplevel widget
        newWindow.title("Registro empresa")
        # sets the geometry of toplevel
        newWindow.geometry("1280x720")
        # A Label widget to show in toplevel
        Label(newWindow,
            text ="Datos de la empresa").pack()
        Label(newWindow,text="Nombre empresa").pack()
        nombre_empresa = ttk.Entry(newWindow)
        nombre_empresa.pack()
        Label(newWindow,text="Sector empresa").pack()
        sector_empresa = ttk.Entry(newWindow)
        sector_empresa.pack()
        ttk.Button(newWindow,command=lambda: createEmpresa(nombre_empresa,sector_empresa),text="Enviar datos").pack()
    
    ttk.Button(frm,command=openNewWindow, text="Registro").grid(column=0,row=2)
    upload_data = ttk.Button(frm, command=openDataWindow,text="Subir datos")
    GUI.mainloop()
except Exception:
    print("Error")
    