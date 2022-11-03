from tkinter import *
from tkinter import ttk
from Class.Empresa import Empresa
from tkinter import messagebox
from tkinter.filedialog import askopenfile 
import pandas as pd
from pandastable import Table
import matplotlib.pyplot as plt
import matplotlib
import customtkinter
# https://github.com/TomSchimansky/CustomTkinter/wiki
customtkinter.set_appearance_mode("light")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

try: 
    matplotlib.use('TkAgg')
    empresas = []  
    file_path = None    
    GUI = customtkinter.CTk()
    GUI.title("Calamita")
    fotosapo = PhotoImage(file='images/Saposilueta.png')
    GUI.iconphoto(False,fotosapo)
    GUI.geometry(f"{515}x{190}")
    frm = customtkinter.CTkFrame(GUI,width=1080,height=1080)

    frm.grid()
    customtkinter.CTkLabel(frm, text="Bienvenido a nuestro software de perfilamiento de clientes, Calamita").grid(column=0,row=0)
   #region normal WorkFlow
    def helpWindow():
        messagebox.showinfo("Ayuda funcionamiento", "1. Registrarse \n 2. Subir los datos de la empresa \n 3. Puedes analizar los datos ingresados con un CRUD integrado de excel \n 4. Realizar el entrenamiento de los modelos de clustering y luego el modelo predictivo \n 5. Se habilita la opción de descargar un bundle (Pickle) de los modelos \n 6.Descargar la data con los clusters calculados")
    def createEmpresa(nombre_empresa,sector_empresa):
        '''Función para manejar los datos que deja el registro realizado por el usuario'''
        name_obj = nombre_empresa.get()
        sector_obj = sector_empresa.get()
        if name_obj != "" and sector_obj!= "":      
            nombre_empresa.config(state=DISABLED)
            sector_empresa.config(state=DISABLED)
            empresas.append(Empresa(name_obj, sector_obj)) 
            messagebox.showinfo(message="Registro exitoso", title="Update")
            upload_data.configure(state="normal")
            #Habilitar botón en el GUI principal para upload data manejar un flujo permisivo con estados de botones
            registrobutton.configure(state="disabled")
            
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
        newWindow.iconphoto(False,fotosapo)
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
        customtkinter.CTkButton(newWindow,width=120,height=32,border_width=0,corner_radius=8,command=lambda: createEmpresa(nombre_empresa,sector_empresa),text="Enviar datos").pack()
        

    #endregion
    
    #region file handling
    
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
                analisisButton.config(state="normal")
                clustering.config(state="normal")
            elif file_path.name.endswith(".xlsx"):
                empresas[0].preparacionData(pd.read_excel(file_path.name,sheet_name=0))
                messagebox.showinfo(message="Subida exitosa, archivo: "+file_path.name, title="Update")
                upload_data.configure(state=DISABLED)
                analisisButton.configure(state="normal")
                clustering.configure(state="normal")
            else:
                messagebox.showerror(message="Solo son validos formatos xlsx o csv", title="Warning")
                
    def exportModels():
        empresas[0].exportModels()
        messagebox.showinfo(message="Pickle descargado", title="Update")
    
    def exportData():
        empresas[0].exportData()
   
    def dataAnalysis():
        data = empresas[0].dataStatistics() #data.describe() #Buscar como mostrar el describe
        f = Toplevel(GUI)
        table = pt = Table(f, dataframe=empresas[0].data,
                                    showtoolbar=True, showstatusbar=True)
        pt.show()
        if "Clusters" in empresas[0].data:
            data_tmp = empresas[0].data
            #centroids_dataframe = empresas[0].clusterDescription()
            #clusters_profiling = Toplevel(GUI)
            #table = pc = Table(clusters_profiling, dataframe=centroids_dataframe)
            #pc.show()
            plt.figure("Clusters en pie chart")
            labels = ["C1","C2","C3","C4","C5"]
            values=empresas[0].data['Clusters'].value_counts() 
            plt.pie(empresas[0].data['Clusters'].value_counts(),labels=["C1","C2","C3","C4","C5"],autopct=lambda p : '{:.2f}%  ({:,.0f})'.format(p,p * sum(values)/100))
            #plt.xlabel("Clusters")
            #plt.ylabel("# de clusters")
            plt.title("Distribución de clusters")
            plt.show()
            
            #centroids_dataframe = empresas[0].clusterDescription()
            #clusters_profiling = Toplevel(GUI)
            #table = pc = Table(clusters_profiling, dataframe=centroids_dataframe)
            #pc.show()
            bar_chart = plt.figure(figsize=(10,5))
            plt.bar(["C1","C2","C3","C4","C5"], [data_tmp[data_tmp.Clusters == 0].shape[0],data_tmp[data_tmp.Clusters == 1].shape[0],data_tmp[data_tmp.Clusters == 2].shape[0],data_tmp[data_tmp.Clusters == 3].shape[0],data_tmp[data_tmp.Clusters == 4].shape[0]])
            plt.xlabel("Clusters")
            plt.ylabel("# de empleados por cluster")
            plt.title("Distribución de clusters")
            plt.show()
        
        
    #endregion
    
    #region ML Models
    def clusteringModel():
        empresas[0].clusteringModel()
        predictive.configure(state="normal")
        exportDataButton.configure(state="normal")
        
    def predictiveModel():
        empresas[0].predictiveModel()
        exportButton.configure(state="normal")
    #endregion
    
    
    registrobutton=customtkinter.CTkButton(frm,width=120,height=32,border_width=0,corner_radius=8,command=openNewWindow, text="Registro")
    registrobutton.grid(column=0,row=1)
    customtkinter.CTkButton(frm,width=120,height=32,border_width=0,corner_radius=8,command=helpWindow, text="Ayuda").grid(column=1,row=5)
    upload_data = customtkinter.CTkButton(frm,width=120,height=32,border_width=0,corner_radius=8, command=openFileExplorer,text="Subir datos",state=DISABLED)
    upload_data.grid(column=0,row=2)
    clustering = customtkinter.CTkButton(frm,width=120,height=32,border_width=0,corner_radius=8, command=clusteringModel, text= "Perfilar base de datos",state=DISABLED)
    clustering.grid(column=0,row=3)
    predictive = customtkinter.CTkButton(frm,width=120,height=32,border_width=0,corner_radius=8, command=predictiveModel, text= "Modelo predictivo",state=DISABLED)
    predictive.grid(column=1,row=2)
    exportButton = customtkinter.CTkButton(frm,width=120,height=32,border_width=0,corner_radius=8, command=exportModels, text= "Descargar bundle de modelos",state=DISABLED)
    exportButton.grid(column=0,row=4)
    exportDataButton = customtkinter.CTkButton(frm,width=120,height=32,border_width=0,corner_radius=8, command=exportData, text= "Exportar el perfilado a excel",state=DISABLED)
    exportDataButton.grid(column=0,row=5)
    analisisButton = customtkinter.CTkButton(frm,width=120,height=32,border_width=0,corner_radius=8, command=dataAnalysis,text="Analizar datos",state=DISABLED)
    analisisButton.grid(column=1,row=3)

    
    
    
    GUI.mainloop()
    
except Exception as e:
    print(e)
