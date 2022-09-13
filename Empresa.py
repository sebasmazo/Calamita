from copyreg import pickle
from statistics import mode
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from pytz import timezone
from sklearn import metrics
from sklearn.cluster import KMeans
import random
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.metrics import accuracy_score
from datetime import datetime

class Empresa:
    models = []
    metricas = [] #[,Exactitud]
    data = None
    clusteringData = None
    
    def __init__(self, nombreEmpresa, sectorEmpresa):
        self.idEmpresa = random.randrange(0000,9999)
        self.nombreEmpresa = nombreEmpresa
        self.sectorEmpresa = sectorEmpresa
        self.fechaCreacionUsuario = datetime.utcnow()
        
        #self.data = self.preparacionData(datafile)     Logica programa
        #self.clusteringData = self.clusteringModel(self.data) #modelsData has [model, model inertia, data with clusters]
        #self.predictiveModel()
        
    
    def dataStatistics(self,dfdata):
        print(dfdata.info())
        print(dfdata.describe())
    
    def preparacionData(self,filename):
        data = pd.read_excel(filename, sheet_name=0)
        data['Casado']=data['Casado'].astype('category')
        data['Carro']=data['Carro'].astype('category')
        data['Alq_Prop']=data['Alq_Prop'].astype('category')
        data['Sindicato']=data['Sindicato'].astype('category')
        data['Sexo']=data['Sexo'].astype('category')
        self.data = pd.get_dummies(data,columns=['Casado','Carro','Alq_Prop','Sindicato','Sexo'])
         
      
    def clusteringModel(self):
        toClient = []
        model = KMeans(n_clusters=5,max_iter=500)
        model.fit(self.data)
        centroides=pd.DataFrame(model.cluster_centers_, columns=self.data.columns.values)
        print(centroides.round(0)) 
        tmp = self.data
        tmp["Clusters"] = model.labels_
        self.clusteringData = tmp
        self.models.append(model)
        self.metricas.append(model.inertia_)
        
    
    #def exportClusteringModel(self): Understand how Pickle works
        #filename = 'Calamita-'+self.idEmpresa+'.pkl'
        #pickle.dump(self.modelsData, open(filename,'wb'))
    
    def predictiveModel(self):
        features = self.clusteringData.drop("Clusters", axis = 1)
        predictions = self.clusteringData["Clusters"]
        X_train, X_test, Y_train, Y_test = train_test_split(features, predictions, test_size=0.3, stratify=predictions)
        model_Knn = neighbors.KNeighborsClassifier(n_neighbors = 1, metric='euclidean')
        model_Knn.fit(X_train, Y_train)
        Y_pred_knn = model_Knn.predict(X_test)      
        exactitud = accuracy_score(Y_test, Y_pred_knn)
        self.metricas.append(exactitud)
        #print(exactitud) 1.0
        self.models.append(model_Knn)
    
    def toString(self):
        return "Empresa ("+str(self.idEmpresa)+") "+self.nombreEmpresa+", enfocada a: "+self.sectorEmpresa+". Registrada en Calamita en la fecha: " + str(self.fechaCreacionUsuario)
        
          
if __name__ == "__main__": #TODO: Remove when merging with GUI
    #Ejemplo de logica
    empresaEjemplo = Empresa("Calamita INC", "Analitica de datos")  #datafile = 
    print(empresaEjemplo.toString())
    empresaEjemplo.preparacionData("Data/Empleados.xlsx")
    empresaEjemplo.clusteringModel() 
    empresaEjemplo.predictiveModel()
    print(empresaEjemplo.models) #Resultado esperado: [KMeans(max_iter=500, n_clusters=5), KNeighborsClassifier(metric='euclidean', n_neighbors=1)]
    print(empresaEjemplo.metricas)