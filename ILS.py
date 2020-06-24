import pandas as pd
import numpy as np
from itertools import combinations
import math as mt
import random

if __name__ == "__main__":

    InputData = "InputDataHubSmallInstance.xlsx"

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
                        data_dict[i + 1] = values[1][i]
                else:
                    for i in range(values.shape[0]):
                        data_dict[i + 1] = values[i][1]

            else:  # For two-dimension (matrix) parameters in Excel
                for i in range(values.shape[0]):
                    for j in range(values.shape[1]):
                        data_dict[(i + 1, j + 1)] = values[i][j]
            return data_dict


    nodeNum = read_excel_data(InputData, "NodeNum")

    flow_wij = read_excel_data(InputData, "flow(wij)")

    Cost_cij = read_excel_data(InputData, "varCost(cij)")

    fixCost_fk = read_excel_data(InputData, "fixCost(fk)")

    alpha = read_excel_data(InputData, "alpha")

    cap = read_excel_data(InputData, "Cap(ckmax)")


    def getVoisin(solution,noeud): 
        voisins = []
        for (i,j) in solution :
            if (i == noeud) :
                voisins.append(j)
            if (j == noeud) : 
                voisins.append(i)
        return voisins

    def getAllPathFromi_bis(solution,current,shortest,visited,path) :
        voisins = getVoisin(solution,current)
        visited.append(current)

        path[current] = shortest 
        for voisin in voisins :
            if (voisin not in visited) :
                getAllPathFromi_bis(solution,voisin, shortest + [voisin],visited,path)
    
    def getAllPathFromi(solution,i) :
        path = {}
        getAllPathFromi_bis(solution,i,[i],[],path)
        return path

    def verify(solution,hub) : 
        hub_flow = {}
        for i in hub :
            hub_flow[i] = 0
    
        for i in range(1,nodeNum[0]+1) :
            path_i = getAllPathFromi(solution,i)
            for j in range(1,nodeNum[0]+1) :
                if (i != j and j in path_i.keys()):
                    chemin = path_i[j]
                    for value in hub : 
                        if (value in chemin) :
                            hub_flow[value] += flow_wij[i,j]

        for value in hub :
            if hub_flow[value] > cap[value - 1] :
                return False
        return True


    def findSolution2(N) :
        cap_copy = cap.copy()
        
        hub = []
        node = [i + 1 for i in range(nodeNum[0])]
        for i in range(N) :
            hub_max = cap.index(max(cap_copy)) + 1
            hub.append(hub_max)
            node.remove(hub_max)
            cap_copy.remove(max(cap_copy))

        solution = []
        arbred = [hub[0]]

        for i in range(len(hub) - 1) : 
            arbred_cop = arbred.copy()
            while arbred_cop != [] :
                choice = random.choice(arbred_cop) 
                new_sol = solution.copy()
                new_sol.append((choice,hub[i+1]))
                if (verify(new_sol,hub)) :
                    arbred.append(hub[i+1])
                    solution.append((choice,hub[i+1]))
                    break
                arbred_cop.remove(choice)
                

        for i in node : 
            hub_copy = hub.copy()
            while hub_copy != [] :
                choice = random.choice(hub_copy) 
                new_sol = solution.copy()
                new_sol.append((choice,i))
                if (verify(new_sol,hub) == True) :
                    solution.append((choice,i)) 
                    break
                hub_copy.remove(choice)

        return hub,solution

    #Nombre de hub
    def findSolution(N):
        hub = []
        node = [i + 1 for i in range(nodeNum[0])]
        for i in range(N) :
            hub.append(random.choice(node))
            node.remove(hub[i])

        solution = []
        arbred = [hub[0]]
        for i in range(len(hub) - 1) : 
            solution.append((random.choice(arbred),hub[i+1]))
            arbred.append(hub[i+1])

        for i in node :
            solution.append((random.choice(hub),i))
            #min = Cost_cij[(hub[0],i)]
            #value = hub[0]
            #for j in hub :
            #    if (min > Cost_cij[(j,i)]) :
            #        min = Cost_cij[(j,i)]
            #        value = j
            #solution.append((value,i))

        return hub,solution

    #def 
    def objectiveValue(hub,solution): 
        fk = 0
        for i in hub : 
            fk += fixCost_fk[i - 1]

        var_cost = 0
        for i in range(1,nodeNum[0]+1) :
            path_i = getAllPathFromi(solution,i)
            for j in range(1,nodeNum[0]+1) :
                if (i != j):
                    chemin = path_i[j]
                    for m in range(len(chemin) - 1) :
                        k = chemin[m]
                        l = chemin[m+1]
                        if (k in hub and l in hub):
                            var_cost +=  alpha[0] * Cost_cij[(k,l)] * flow_wij[(i,j)]
                        else : 
                            var_cost += Cost_cij[(k,l)] * flow_wij[(i,j)]
        return var_cost + fk

    def local1(hub,solution) : 
        old_spokes = []
        for (i,j) in solution :
            if j not in hub :
                old_spokes.append(j)

        i = random.randint(0,len(old_spokes))
        start = old_spokes[0:i]
        start.reverse() 
        new_spokes = start + old_spokes[i:]
        new_sol = []
        for (i,j) in solution :
            if j not in hub :
                new_sol.append((i,new_spokes.pop(0)))
            else :
                new_sol.append((i,j))
        return hub, new_sol

    def getNewSol(solution,spoke,hub) : 
        new_sol = []
        for (h,s) in solution :
            if s == spoke :
                new_sol.append((hub,spoke))
            else : 
                new_sol.append((h,s))
        return new_sol

    def local2(hub,solution) : 
        # Select one spoke
        node = [i + 1 for i in range(nodeNum[0]) if i + 1 not in hub]
        selected = random.choice(node)

        # search hub that lead to minimum cost with that spoke
        min_h = hub[0]
        sol_0 = getNewSol(solution,selected,min_h)
        value = objectiveValue(hub,sol_0)
        for j in hub :
            sol_j = getNewSol(solution,selected,j)
            value_j = objectiveValue(hub,sol_j)
            if (value_j < value) : 
                min_h = j
                value = value_j

        return hub,getNewSol(solution,selected,min_h)


    def shaking(hub, solution) :
        index =  random.randrange(len(hub))
        first = hub[index]
        second = hub[(index + 1) % len(hub)]

        new_sol = []
        for (h,s) in solution : 
            if (h == second and s == first) or (h == first and s == second):
                new_sol.append((s,h))
            elif (h == first) :
                new_sol.append((second,s))
            elif (h == second) :
                new_sol.append((first,s))
            elif (s == first) :
                new_sol.append((h,second))
            elif (s == second):
                new_sol.append((h,first))
            else :
                new_sol.append((h,s))
        return hub,new_sol




N = 7
hub, solut = findSolution(N)
acc = 0
while(verify(solut,hub) == False) :
    hub, solut = findSolution(N)
print("Première solution trouvé :")
min_o = objectiveValue(hub,solut)
print("coût : ",min_o)

while(True) :
    hub1 = []
    solut1 = []
    i = random.randint(1,3)
    if i == 1 :
        hub1,solut1 = local1(hub,solut)
    elif i == 2 :
        hub1,solut1 = local2(hub,solut)
    else : 
        hub1,solut1 = shaking(hub,solut)

    verified = verify(solut1,hub1) 
    min1 = objectiveValue(hub1,solut1)
    if (verified == True and min_o > min1 ):
        min_o = min1
        hub,solut = hub1,solut1
        print("coût : ",min_o)
            
