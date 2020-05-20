# Import PuLP modeler functions
from pulp import *
import pandas as pd
import numpy as np
from itertools import combinations
import math as mt


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
 
   # This section reads the data from Excel #

   
   NodeNum = read_excel_data(InputData, "NodeNum")
   NodeNum = NodeNum[0]
   print("NodeNum: ", NodeNum)
   
   set = [i+1 for i in range(NodeNum)]

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
   
   Y = LpVariable.dicts('y',(set,set),0,1,'Binary')
   Z = LpVariable.dicts('z',(set,set),0,1,'Binary') 
   X = LpVariable.dicts('x',(set,(set,set)),0)
   
   O = []
   for i in set:
      O.append(sum([flow_wij[i][j] for j in set ]))
      
   D = []
   for i in set:
      D.append(sum([flow_wij[j][i] for j in set ]))
      

   Hub=LpProblem("Hub",LpMinimize)
   
   #fixed costs
   list_fc = [fixCost_fk[k-1] * Z[k][k] for k in set]
   fixed_cost = LpSum(list_fc)
   
   #variable costs
   list_vc1 = [ varCost_cij [key] * O[key[0]-1] * Z[key[0]][key[1]] for key in varCost_cij]
   list_vc2 = [ varCost_cij [key] * D[key[1]-1] * Z[key[1]][key[0]] for key in varCost_cij]
   variable_cost1 = lpSum([lpSum(list_vc1),lpSum(list_vc2)])
   
   list_vc3 = []
   for k in set:
      for m in set:
         if 
         
   
   # contrainte1
   for i in set:
      Hub+= (lpSum(Z[i][k] for k in set) = 1) 
   
   #contrainte2
   for k in set:
      for m in set:
         if m>k:
            Hub += Z[k][m]+Y[k][m]<=Z[m][m]
            Hub += Z[m][k]+Y[k][m]<=Z[k][k]
   
   #contrainte3
    for k in set:
      for m in set:
         if m>k:
            Hub += X[i,(k,m)] + X[i,(m,k)] <= O[i]*Y[k][m]
            
       #contrainte4:
    for i in set:
        for k in set:
            if k!=i:
                Hub+= (O[i]*Z[i][k] + lpSum(X[i,(m,k)] for m  in set and m!=k) = lpSum(X[i,(k,m)] for m in set and m!=k) + lpSum(flow_wim*Z[m][k] for m in set))
   #contrainte5:
   for k in set:
      if i=!K:
         if m=!k:
            Hub += lpSum((O[i]*Z[i][k] + lpSum(X[i,(m,k)] for m in set) for i in set) <= Cap_ckmax
            
    #contrainte6
   Hub += (lpSum(lpSum(Y[k][m] for m in set)for k in set)=lpSum(Z[k][k] for k in set)- 1)          
   
   
