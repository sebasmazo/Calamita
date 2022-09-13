from statistics import mode
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.cluster import KMeans
import random
import pickle


class Empresa:
    idEmpresa = random.randrange(0000,9999)
    def __init__(self, datafile):
        self.data = self.preparacionData(datafile)
        self.clusteringData = self.model(self.data) #clusteringData has [model, model inertia, data with clusters]
        #self.predictiveModel = self.predictiveModel(self.clusteringData[2])
        
    
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
      
    def model(self,data):
        toClient = []
        model = KMeans(n_clusters=5,max_iter=500)
        model.fit(data)
        centroides=pd.DataFrame(model.cluster_centers_, columns=data.columns.values)
        print(centroides.round(0)) 
        data["Clusters"] = model.labels_
        toClient.append([model,model.inertia_,data])
        
        return toClient
    
    

        

if __name__ == "__main__":
    empresaEjemplo = Empresa("Data/Empleados.xlsx")