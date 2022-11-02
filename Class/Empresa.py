import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import random
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from datetime import datetime
import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class Empresa:
    models = [] #[Clustering model, predictive model]
    metricas = [] #[Inertia,Exactitud]
    data = pd.DataFrame()
    clusteringData = None #clusteringData tiene los resultados del modelo de CLustering (registro con su respectivo cluster)
    min_max_scaler = MinMaxScaler()
    def __init__(self, nombreEmpresa, sectorEmpresa):
        '''Constructor de la clase empresa'''
        self.idEmpresa = random.randrange(0000,9999)
        self.nombreEmpresa = nombreEmpresa
        self.sectorEmpresa = sectorEmpresa
        self.fechaCreacionUsuario = datetime.utcnow()
    
    #def clusterDescription(self):
        #if len(self.models) >= 1:
            #tmp = self.data.drop('Clusters', axis=1)
            #centroides = pd.DataFrame(self.models[0].cluster_centers_, tmp.columns.values)
            #centroides = centroides.round(0)
            #return centroides
    
    def dataStatistics(self):
        '''Si el campo data de la empresa, NO está vacío, imprime la información del dataframe y la descripción estadistica'''
        if not self.data.empty:
            data_return = self.data.describe()
            return data_return
        
    def preparacionData(self,dataframe):
        '''Preparación de los datos'''
        data = dataframe
        self.min_max_scaler.fit(data[['Sueldo',  'Hijos',  'Incapacidades',  'Antiguedad']]) #Ajuste de parámetro
        data[['Sueldo', 'Hijos',  'Incapacidades',  'Antiguedad']]= self.min_max_scaler.transform(data[['Sueldo',  'Hijos',  'Incapacidades',  'Antiguedad']])
        data['Casado']=data['Casado'].astype('category')
        data['Carro']=data['Carro'].astype('category')
        data['Alq_Prop']=data['Alq_Prop'].astype('category')
        data['Sindicato']=data['Sindicato'].astype('category')
        data['Sexo']=data['Sexo'].astype('category')
        self.data = pd.get_dummies(data,columns=['Casado','Carro','Alq_Prop','Sindicato','Sexo'],drop_first=True)
        
         
    def clusteringModel(self):
        '''Genera el modelo de clustering y lo añade al array models de la empresa, hace lo mismo con las metricas del modelo'''
        toClient = []
        model = KMeans(n_clusters=5,max_iter=500)
        model.fit(self.data)
        centroides=pd.DataFrame(model.cluster_centers_, columns=self.data.columns.values)
        tmp = self.data
        tmp["Clusters"] = model.labels_
        self.clusteringData = tmp
        self.models.append(model)
        self.metricas.append(model.inertia_)
        self.data[['Sueldo', 'Hijos',  'Incapacidades',  'Antiguedad']]=self.min_max_scaler.inverse_transform(self.data[['Sueldo', 'Hijos',  'Incapacidades',  'Antiguedad']])
        
    
    def exportModels(self):
        '''Función para descargar el modelo como un pickle'''
        with open("Models.obj", "wb") as filehandler:
            pickle.dump(self.models,filehandler)
        
    
    def predictiveModel(self):
        '''Genera el modelo predictivo y lo añade al array models de la empresa, hace lo mismo con las metricas del modelo'''
        features = self.clusteringData.drop("Clusters", axis = 1)
        predictions = self.clusteringData["Clusters"]
        X_train, X_test, Y_train, Y_test = train_test_split(features, predictions, test_size=0.3, stratify=predictions)
        model_Knn = neighbors.KNeighborsClassifier(n_neighbors = 1, metric='euclidean')
        model_Knn.fit(X_train, Y_train)
        Y_pred_knn = model_Knn.predict(X_test)      
        exactitud = accuracy_score(Y_test, Y_pred_knn)
        self.metricas.append(exactitud)
        self.models.append(model_Knn)
    
    def toString(self):
        return "Empresa ("+str(self.idEmpresa)+") "+self.nombreEmpresa+", enfocada a: "+self.sectorEmpresa+". Registrada en Calamita en la fecha: " + str(self.fechaCreacionUsuario)
        
    def exportData(self):
        '''Exportar data con clusters, debe tener el nombre y ruta deseada del archivo'''
        self.clusteringData.to_excel("clustersEmpleados.xlsx")
        
if __name__ == "__main__": #TODO: Remove when merging with GUI
    #Ejemplo de logica
    empresaEjemplo = Empresa("Calamita INC", "Analitica de datos")  #datafile = 
    print(empresaEjemplo.toString())
    empresaEjemplo.preparacionData(pd.read_excel("Empleados.xlsx",sheet_name=0))
    #empresaEjemplo.dataStatistics() Descripción estadistica de la data
    empresaEjemplo.clusteringModel() 
    empresaEjemplo.predictiveModel()
    print(empresaEjemplo.clusteringData) 
    print(empresaEjemplo.models) #Resultado esperado: [KMeans(max_iter=500, n_clusters=5), KNeighborsClassifier(metric='euclidean', n_neighbors=1)]
    print(empresaEjemplo.metricas)
    empresaEjemplo.exportModels()
    