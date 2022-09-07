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
    print("------------------------- Información --------------------------------")
    print(data.info)
    #Dummies
    data = pd.get_dummies(data,columns=['Casado','Coche','Alq/Prop','Sindic.','Sexo'])
    print("------------------------- Dummies --------------------------------")
    print(data.head())
    data.to_excel("Data/DataLimpio.xlsx")
    return data

#def modelo(data):
    #Metodo del codo
    #ks = range(1, 7) 
    #inertias = []

    #for k in ks:
    #    # Crear  modelo
    #    model = KMeans(n_clusters=k)
    #    model.fit(data)
    #    inertias.append(model.inertia_)

    ## Graficar cantidad de clusters vs inertias
    #plt.plot(ks, inertias, '-o')
    #plt.xlabel('Numero de clusters, k')
    #plt.ylabel('inertia')
    #plt.xticks(ks)
    #plt.title('Metodo del codo')
    #plt.show()



if len(sys.argv)-1 != 0:
    data = preparacionData(sys.argv[1])
    #modelo(data)
else:
    print("Usage: python3 clustering.py [File path]")