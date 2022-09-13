from copyreg import pickle
from statistics import mode
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.cluster import KMeans
import random
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.metrics import accuracy_score

class Empresa:
    idEmpresa = random.randrange(0000,9999)
    def __init__(self, datafile):
        self.data = self.preparacionData(datafile)
        self.modelsData = self.clusteringModel(self.data) #modelsData has [model, model inertia, data with clusters]
        self.predictiveModel = self.predictiveModel()
        
    
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
        data = pd.get_dummies(data,columns=['Casado','Carro','Alq_Prop','Sindicato','Sexo'])
       
        return data  
      
    def clusteringModel(self,data):
        toClient = []
        model = KMeans(n_clusters=5,max_iter=500)
        model.fit(data)
        centroides=pd.DataFrame(model.cluster_centers_, columns=data.columns.values)
        print(centroides.round(0)) 
        data["Clusters"] = model.labels_
        
        toClient.append(data)
        toClient.append(model)
        return toClient
    
    #def exportClusteringModel(self): Understand how Pickle works
        #filename = 'Calamita-'+self.idEmpresa+'.pkl'
        #pickle.dump(self.modelsData, open(filename,'wb'))
    
    def predictiveModel(self):
        features = self.modelsData[1].drop("Clusters", axis = 1)
        predictions = self.modelsData[1]["Clusters"]
        X_train, X_test, Y_train, Y_test = train_test_split(features, predictions, test_size=0.3, stratify=predictions)
        model_Knn = neighbors.KNeighborsClassifier(n_neighbors = 1, metric='euclidean')
        model_Knn.fit(X_train, Y_train)
        Y_pred_knn = model_Knn.predict(X_test)      
        exactitud = accuracy_score(Y_test, Y_pred_knn)
        #print(exactitud) 1.0
        
        
          
if __name__ == "__main__":
    empresaEjemplo = Empresa("Data/Empleados.xlsx")