import numpy as np
from pulp import *
import pandas as pd
import networkx as nx
import random

#Lecture du tableau Excel
if __name__ == "__main__":

   InputData = "InputDataHubSmallInstance.xlsx"

  # Input Data Preparation #
   def read_excel_data(filename, sheet_name):
      data = pd.read_excel(filename, sheet_name=sheet_name, header=None)
      values = data.values
      if min(values.shape) == 1:  # This If is to make the code insensitive to column-wise or row-wise expression #
          if values.shape[0] == 1:
              values = values.tolist()
          else:
              values = values.transpose()
              values = values.tolist()
          return values[0]
      else:
          data_dict = {}
          if min(values.shape) == 2:  # For single-dimension parameters in Excel
              if values.shape[0] == 2:
                  for i in range(values.shape[1]):
                      data_dict[i+1] = values[1][i]
              else:
                  for i in range(values.shape[0]):
                      data_dict[i+1] = values[i][1]

          else:  # For two-dimension (matrix) parameters in Excel
              for i in range(values.shape[0]):
                  for j in range(values.shape[1]):
                      data_dict[(i+1, j+1)] = values[i][j]
          return data_dict
 
#This section reads the data from Excel#

#Read a set (set is the name of the worksheet)
   
   NodeNum = read_excel_data(InputData, "NodeNum")
   NodeNum = NodeNum[0]
   print("NodeNum: ", NodeNum)

   set = [i for i in range(NodeNum+1)]

   alpha = read_excel_data(InputData, "alpha")
   alpha = alpha[0]
   print("alpha: ", alpha)

   flow_wij = read_excel_data(InputData, "flow(wij)")
   print("flow(wij): ", flow_wij)

   varCost_cij = read_excel_data(InputData, "varCost(cij)")
   print("varCost(cij): ", varCost_cij)

   fixCost_fk = read_excel_data(InputData, "fixCost(fk)")
   print("fixCost(fk): ", fixCost_fk)

   Cap_ckmax = read_excel_data(InputData, "Cap(ckmax)")
   print("Cap(ckmax): ", Cap_ckmax)

#Solution initiale

def network():
    M = [] #matrice des couples 
    L = [1,2,3,4,5,6,7,8] #liste des spokes
    H = [] #liste des hubs
    for k in range(3):
        h = random.choice(L) #on récupère un chiffre au hasard dans la liste L
        L.remove(h)
        H.append(h)
    
    for s in L: #on parcourt la liste des spokes non choisis comme hubs
        h = random.choice(H) #on sélectionne un hub au hasard pour le relier au spoke k
        M.append([h,s]) #on ajoute le couple hub/spoke
        
    #on relie les hubs entre eux aléatoirement 
    h = random.choice(H) 
    H.remove(h)
    M.append([h, H[0]])
    M.append([h, H[1]])
    H.append(h)
    
    return getGraph(M)

def getGroup (M, p):
    H = []
    for m in M :
        node = m[p]
        H.append(node)
    return H 

def getGraph(M):
    M = []
    H = getGroup(M,0) #hubs
    M.append(H)
    S = getGroup(M,1) #spokes
    M.append(S) 
    return M

print(network())


def Hub_Spoke(M): #renvoie la liste des hubs et des spokes d'une matrice
    H = []
    S =[]
    for i in M[0]:
        H += [i]
    for j in M[1]:
        if j not in H :
            S += [j]
    return(H,S)

def Local_Search(M): #Algorithme du Local Search
    H,S = Hub_Spoke(M)
    for i in S : #on parcourt la liste des spokes pour leur appliquer le Local Search
        for j in range (len(M[0])):
            if M[j][1] == i:
                index_hub = M[j][0] #on cherche l'index de l'hub qui correspond à ce spoke
        S_final = cout_tot(M) #variable qui définit le coût du modèle qui sera retenu
        S_current = 0 #variable qui définit le coût du modèle en cours
        for k in H : #on parcourt la liste de hubs
            M_current = [k for k in M] #on copie la matrice de notre modèle
            for l in range (len(M[0])): #on parcourt la première colonne du tableau 
                if M[l][0] != m[index_hub][0]: #on vérifie que l'index est le bon
                    if M[l][0] == k:
                        M_current[l][0] = k
                        M_current[index_hub][0] = M[k][0] #on remplace tous les hubs
            S_current = cout_tot(M_current) #on calcule le prix du modèle en cours
            if S_current < S_final: 
                S_final = S_current 
                M = M_current 
    return M

def Local_Search2(M): #Algorithme du Local Search 2
    H,S = Hub_Spoke(M)
    for i in S : #on parcourt la liste des spokes pour leur appliquer le Local Search 2
        for j in range (len(M[0])):
            if M[j][1] == i:
                index_hub = M[j][1] #on cherche l'index de l'hub qui correspond à ce spoke
        S_final = cout_tot(M) 
        S_current = 0 
        for k in spokes : #on parcourt la liste des spokes
            M_current =[k for k in M]
            for l in range (len(M[1])): #on parcourt la deuxième colonne du tableau
                if M[l][1] != i: #on vérifie que l'index est le bon
                    if M[l][1] == k:
                        M_current[l][1] = i
                        M_current[index_hub][1] = M[k][0] #on remplace tous les spokes
            S_current = cout_tot(M_current) #on calcule le prix du modèle en cours
            if S_current > S_final: 
                S_final = S_current 
                M = M_current 
    return M

            
def cout_tot(M): #calcul du coût d'un modèle
    H, S = Hub_Spoke(M)
    Graph = nx.Graph(M)
    All_Path = dict(nx.all_pairs_shortest_path(Graph)) #création des chemins les plus courts
    cost = 0
    for i in range (1,9):
        cost+= fixCost_fk[i] #ajout des coûts fixes
        for j in range (1,9):
            for k in All_Path[(i, j)] :
                if k!= i:
                    cost+= flow_wij[(i,j)]*varCost_cij[(i, k)] #ajout des coûts variables en suivant le plus court chemin
    return cost
            
            
