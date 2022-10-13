from email import message
from os import stat
from tkinter import *
from tkinter import ttk
from Class.Empresa import Empresa
from tkinter import messagebox
from tkinter.filedialog import askopenfile 
import pandas as pd
try: 
    empresas = []  
    file_path = None    
    GUI = Tk()
    GUI.title("Calamita")
    GUI.geometry("1280x720")
    frm = ttk.Frame(GUI, padding=10)
    frm.grid()
    ttk.Label(frm, text="Bienvenido a nuestro software de perfilamiento, Calamita").grid(column=0,row=0)
    ttk.Label(frm, text="Registrarse").grid(column=0,row=1)
   #region normal WorkFlow
    def createEmpresa(nombre_empresa,sector_empresa):
        '''Función para manejar los datos que deja el registro realizado por el usuario'''
        name_obj = nombre_empresa.get()
        sector_obj = sector_empresa.get()
        if name_obj != "" and sector_obj!= "":      
            nombre_empresa.config(state=DISABLED)
            sector_empresa.config(state=DISABLED)
            empresas.append(Empresa(name_obj, sector_obj)) 
            messagebox.showinfo(message="Registro exitoso", title="Update")
            upload_data.config(state="normal")
            #Habilitar botón en el GUI principal para upload data manejar un flujo permisivo con estados de botones
        else:
            messagebox.showerror(message="Por favor llenar los datos necesarios", title="Warning")
        
    def openNewWindow() -> None:
        '''Función para manejar botón de registro'''
        # Toplevel object which will
        # be treated as a new window
        newWindow = Toplevel(GUI)
        # sets the title of the
        # Toplevel widget
        newWindow.title("Registro empresa")
        # sets the geometry of toplevel
        newWindow.geometry("1024x768")
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
    #endregion
    
    #region data handling
    def openFileExplorer():
        '''Metodo para manejo de archivos con Tkinter'''
        filetypes = (
            ('Excel','*.xlsx'),
            ('CSV','*.csv')
        )
        file_path = askopenfile(mode='r', filetypes=filetypes)
        if file_path is not None:
            if file_path.name.endswith(".csv"):
                empresas[0].preparacionData(pd.read_csv(file_path.name))
                messagebox.showinfo(message="Subida exitosa, archivo: "+file_path.name, title="Update")
                upload_data.config(state=DISABLED)
                clustering.config(state="normal")
            elif file_path.name.endswith(".xlsx"):
                empresas[0].preparacionData(pd.read_excel(file_path.name,sheet_name=0))
                messagebox.showinfo(message="Subida exitosa, archivo: "+file_path.name, title="Update")
                upload_data.config(state=DISABLED)
                clustering.config(state="normal")
            else:
                messagebox.showerror(message="Solo son validos formatos xlsx o csv", title="Warning")
                
    def exportModels():
        empresas[0].exportModels()
                
    #endregion
    
    #region ML Models
    def clusteringModel():
        empresas[0].clusteringModel()
        predictive.config(state="normal")
    def predictiveModel():
        empresas[0].predictiveModel()
        exportButton.config(state="normal")
    #endregion
    
    ttk.Button(frm,command=openNewWindow, text="Registro").grid(column=0,row=2)
    upload_data = ttk.Button(frm, command=openFileExplorer,text="Subir datos",state=DISABLED)
    upload_data.grid(column=0,row=3)
    clustering = ttk.Button(frm, command=clusteringModel, text= "Perfilar base de datos",state=DISABLED)
    clustering.grid(column=0,row=4)
    predictive = ttk.Button(frm, command=predictiveModel, text= "Modelo predictivo",state=DISABLED)
    predictive.grid(column=1,row=4)
    exportButton = ttk.Button(frm, command=exportModels, text= "Descargar bundle de modelos",state=DISABLED)
    exportButton.grid(column=0,row=5)
    
    
    GUI.mainloop()
    
    
except Exception:
    print("Error")
