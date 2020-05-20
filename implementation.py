# Import PuLP modeler functions
from pulp import *
import pandas as pd
import numpy as np
from itertools import combinations
import math as mt


if __name__ == "__main__":

   InputData = "InputDataSmallHubSmallInstance.xlsx"

  # Input Data Preparation #
   def read_excel(filename, sheet_name):
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

   # Read a set (set is the name of the worksheet)
   # The set has eight elements
   NodeNum = read_excel_data(InputData, "NodeNum")
   NodeNum = NodeNum[0]
   print("NodeNum: ", NodeNum)

   alpha = read_excel_data(InputData, "alpha")
   alpha = alpha[0]
   print("alpha: ", alpha)

   # Read an array 4x4 (array2 is the name of the worksheet)
   flow_wij = read_excel_data(InputData, "flow(wij)")
   print("flow(wij): ", flow_wij)

   varCost_cij = read_excel_data(InputData, "varCost(cij)")
   print("varCost(cij): ", varCost_cij)

   fixCost_fk = read_excel_data(InputData, "fixCost(fk)")
   print("fixCost(fk): ", fixCost_fk)

   Cap_ckmax = read_excel_data(InputData, "Cap(ckmax)")
   print("Cap(ckmax): ", Cap_ckmax)
