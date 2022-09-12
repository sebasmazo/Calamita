import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import sys
from sklearn.cluster import KMeans

def preparacionData(filename):
    data = pd.read_excel(filename, sheet_name=0)
    data['Casado']=data['Casado'].astype('category')
    data['Coche']=data['Coche'].astype('category')
    data['Alq/Prop']=data['Alq/Prop'].astype('category')
    data['Sindic.']=data['Sindic.'].astype('category')
    data['Sexo']=data['Sexo'].astype('category')
    # print("------------------------- Información --------------------------------")
    # print(data.info)
    #Dummies
    data = pd.get_dummies(data,columns=['Casado','Coche','Alq/Prop','Sindic.','Sexo'])
    # print("------------------------- Dummies --------------------------------")
    # print(data.head())
    data.to_excel("Data/DataLimpio.xlsx")
    return data

def dataStatistics(data):
    print(data.info())
    dfStatistics = data.describe() #Media, Desviación, Minimo, Cuartiles
    print(dfStatistics)
    # Metodo del codo
    # ks = range(1, 7) 
    # inertias = []

    # for k in ks:
    #    Crear  modelo
    #    model = KMeans(n_clusters=k)
    #    model.fit(data)
    #    inertias.append(model.inertia_)

    # Graficar cantidad de clusters vs inertias
    # plt.plot(ks, inertias, '-o')
    # plt.xlabel('Numero de clusters, k')
    # plt.ylabel('inertia')
    # plt.xticks(ks)
    # plt.title('Metodo del codo')
    # plt.show()
    
def modelo(path_data, l): #Kmeans model
    model = KMeans(n_clusters=5, max_iter=200)
    if l == "0":
        dfData = pd.read_excel(path_data) #Comentar si se debe hacer limpieza de datos primero
        model.fit(dfData)
        
    else:
        model.fit(path_data)
        dfData = path_data
    
    print(model.inertia_)
    centroides = pd.DataFrame(model.cluster_centers_, columns=dfData.columns.values)
    print(centroides)
    



if len(sys.argv)-1 != 0 and sys.argv[2] == "0" or sys.argv[2] == "1":
    if sys.argv[2] == "1": 
        data = preparacionData(sys.argv[1]) 
        dataStatistics(data) 
        modelo(data,"1")
    elif sys.argv[2] ==  "0" :
        modelo(sys.argv[1],"0")
    
else:
    print("Usage: python3 clustering.py [File path] [Option: 1 = Limpieza primero 0 = Sin limpieza]")