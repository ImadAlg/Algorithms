import numpy as np
import time

#read instance from .col files
def from_file(file_path:str):
        with open(file_path) as f:
            line = f.readline()
            while line[0] != "p":
                line = f.readline()
            n = int(line.split()[2])
            adj_mat = []
            for i in range(0,n):
                adj_mat.append([False]*n)
            for line in f:
                if line[0] == "e":
                    w, v = map(int, line.split()[1:])
                    adj_mat[w-1][v-1] = adj_mat[v-1][w-1] = True
        return np.array(adj_mat)


class DynamicProgramming:
    def __init__(self, g:np.ndarray):
        self.graphe = g    
        self.coloration = [None] * len(g)
        self.soluce  = None
        self.time_processing = None
    
    def solve(self) :
        t0 = time.time()
        #Nunber of vertices
        V = len(self.graphe)
        #Initial state
        state = ([],0)
        #All stage Ek
        Level = [np.array( [ ( [] , 0) ], dtype=object)]
        #for each nodes :
        for node in range(V):
            #Gets all states from the previous stage :E(k-1)
            States = Level.pop()
            #Get the cost of each state (sub-soluce)
            XG_list = States[:,1]
            indStates = np.where(XG_list== XG_list.min())[0]
            #Initialisation of new Stage Ek
            Solutions = []
            #for each sub-solution:
            for i in indStates :
                #Get a new State for the stage Ek
                Solutions.extend(self.colorNode(States[i],node) )
            #Add all states to Ek Ek
            Level.append(np.array(Solutions))
        #Get the best solution
        States = Level.pop()
        XG_list = States[:,1]
        t1 = time.time()
        self.coloration , self.soluce = States[np.argmin(XG_list)]
        self.time_processing = t1 - t0
        return self.coloration,self.soluce,self.time_processing
    
    #Color a node to transition for the state to another
    def colorNode(self,state:np.ndarray, node:int):
        if node == 0:
            #Color 0 for the first node
            NewStates = [ ([0] , 1) ]
        else : 
            #Get the sub-Optimal solution
            Soluce = state[0]
            #Number of colors for The last state
            XG = state[1]
            #Initialisation of the new states
            NewStates = []
            #Get the adjacents nodes to the node that we color
            Adjacents = np.where(self.graphe[node][:node] == True)[0]
            #Get the colors used for the adjacents node
            AdjColor = np.unique( np.array( [Soluce[V] for V in Adjacents] ) )
            #Use all color possible to color the node (Two Adjacents nodes mustn't have the same color)
            for color in range(XG): # For all color
                if color not in AdjColor:
                    #Add a color already used ,present in the previous state (XG(n) = XG(n-1))
                    NewSoluce = Soluce.copy()
                    NewSoluce.append(color)
                    NewState = [NewSoluce , XG]
                    NewStates.append(NewState)
            #Add a new color not present in the previous state (XG(n) = XG(n-1) + 1)
            NewSoluce = Soluce.copy()
            NewSoluce.append(XG)
            NewState = [NewSoluce , XG + 1]
            NewStates.append(NewState) 
        return np.array(NewStates,dtype=object)
    
    def save(self,file_path):
        f = open(file_path, "w")
        f.write( "# Solution for the instance "+file_path+"\n" )
        f.write( "Minimum number of colors used : %d \n"%self.soluce )
        f.write( "Execution time :: %f \n"%self.time_processing )
        f.write( "Color Affectation to the nodes : \n")
        [f.write( "Node "+ str(i)+ " :: "+str(self.coloration[i]) +"\n") for i in range(len(self.coloration))]
        f.close()
        return
    
  
file_name = "myciel3.col" 
file_path = "Instances/"+file_name
g = from_file(file_name)
dyP = DynamicProgramming(g)
dyP.solve()
dyP.save("Solutions/soluce_"+file_name)
