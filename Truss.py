import re
import numpy as np
import pylab as plt

class Truss:
    def __init__(self,filename):
        fo = open(filename,'r')

        line = fo.readline()
        line = fo.readline()

        self.nodes = []
        while not re.match("BAR",line):
            a = [float(x) for x in line[0:-1].split(',')]
            self.nodes.append(a)
            line = fo.readline()
        self.nodes = np.array(self.nodes)
        print(self.nodes)    


        line = fo.readline()

        self.bars = []
        while not re.match("REAC",line):
            a = [int(x) for x in line[0:-1].split(',')]
            self.bars.append(a)
            line = fo.readline()

        self.bars = np.array(self.bars)
        print(self.bars)   


        line = fo.readline()

        self.reac = []
        while not re.match("FORC",line):
            a = [int(x) for x in line[0:-1].split(',')]
            self.reac.append(a)
            line = fo.readline()

        self.reac = np.array(self.reac)
        print(self.reac)   

        line = fo.readline()

        self.force = []
        while not re.match("END",line):
            a = [float(x) for x in line[0:-1].split(',')]
            self.force.append(a)
            line = fo.readline()

        self.force = np.array(self.force)
        print(self.force)

        fo.close()
    def plot(self):
        
        dplotx = (max(self.nodes[:,0])-min(self.nodes[:,0]))*0.1
        dploty = (max(self.nodes[:,1])-min(self.nodes[:,1]))*0.1
        plt.scatter(self.nodes[:,0],self.nodes[:,1])
        for i in range(len(self.bars)):
            plotx=[self.nodes[self.bars[i,0],0],self.nodes[self.bars[i,1],0]]    
            ploty=[self.nodes[self.bars[i,0],1],self.nodes[self.bars[i,1],1]]
            plt.plot(plotx,ploty,'-b')
        
        for i in range(len(self.reac)):
            plotx=[self.nodes[self.reac[i,0],0],self.nodes[self.reac[i,0],0]-self.reac[i,1]*dplotx]
            ploty=[self.nodes[self.reac[i,0],1],self.nodes[self.reac[i,0],1]-self.reac[i,2]*dplotx]
            plt.plot(plotx,ploty,'-k')
        for i in range(len(self.force)):
            print(self.force[i,1:2])
            lfuer = np.linalg.norm(self.force[i,1:])
            idx_f = int(self.force[i,0])
            plotx=[self.nodes[idx_f,0],self.nodes[idx_f,0]-self.force[i,1]*dplotx/lfuer]
            ploty=[self.nodes[idx_f,1],self.nodes[idx_f,1]-self.force[i,2]*dploty/lfuer]
            plt.plot(plotx,ploty,'-r')
        plt.axis('equal')
        plt.show()    

    def plot_deformed(self,DX,factor):
        nodes_def = np.zeros((len(self.nodes),2))
        nodes_def[:,0]=DX[0::2]*factor+self.nodes[:,0]
        nodes_def[:,1]=DX[1::2]*factor+self.nodes[:,1]        
        dplotx = (max(nodes_def[:,0])-min(nodes_def[:,0]))*0.1
        dploty = (max(nodes_def[:,1])-min(nodes_def[:,1]))*0.1
        plt.scatter(nodes_def[:,0],nodes_def[:,1])
        for i in range(len(self.bars)):
            plotx=[nodes_def[self.bars[i,0],0],nodes_def[self.bars[i,1],0]]    
            ploty=[nodes_def[self.bars[i,0],1],nodes_def[self.bars[i,1],1]]
            plt.plot(plotx,ploty,'-g')
        
        for i in range(len(self.reac)):
            plotx=[nodes_def[self.reac[i,0],0],nodes_def[self.reac[i,0],0]-self.reac[i,1]*dplotx]
            ploty=[nodes_def[self.reac[i,0],1],nodes_def[self.reac[i,0],1]-self.reac[i,2]*dplotx]
            plt.plot(plotx,ploty,'-k')
        for i in range(len(self.force)):
            print(self.force[i,1:2])
            lfuer = np.linalg.norm(self.force[i,1:])
            idx_f = int(self.force[i,0])
            plotx=[nodes_def[idx_f,0],nodes_def[idx_f,0]-self.force[i,1]*dplotx/lfuer]
            ploty=[nodes_def[idx_f,1],nodes_def[idx_f,1]-self.force[i,2]*dploty/lfuer]
            plt.plot(plotx,ploty,'-r')
        plt.axis('equal')
        plt.show()    

    def write_results(self,DX,R,F,filename):
        fo = open(filename,'w')
        fo.write("Results, Force\n")
        for i in range(len(self.bars)):
            fo.write("Force Bar %i: %.2f\n" % (i,F[i]))
        for i in range(len(self.reac)):
            fo.write("Reaction in node %i, components [%i,%i]: %.2f\n" % (self.reac[i,0],self.reac[i,1],self.reac[i,2],R[i]))
            
        for i in range(len(self.nodes)):
            fo.write("Displacement in node %i: [%f,%f]\n" % (i,DX[2*i],DX[2*i+1]) )
            
        fo.close()
    def print_results(self,DX,R,F):
        print("Results, Force")
        for i in range(len(self.bars)):
            print("Force Bar %i: %.2f" % (i,F[i]))
        for i in range(len(self.reac)):
            print("Reaction in node %i, components [%i,%i]: %.2f" % (self.reac[i,0],self.reac[i,1],self.reac[i,2],R[i]))
            
        for i in range(len(self.nodes)):    
            print("Displacement in node %i: [%e,%e]" % (i,DX[2*i],DX[2*i+1]) ) 
    def X(self,i,j):
        x = (self.nodes[i,0]-self.nodes[j,0])/(np.sqrt((self.nodes[i,0]-self.nodes[j,0])**2+(self.nodes[i,1]-self.nodes[j,1])**2))
        return x
    def Y(self,i,j):
        y = (self.nodes[i,1]-self.nodes[j,1])/(np.sqrt((self.nodes[i,0]-self.nodes[j,0])**2+(self.nodes[i,1]-self.nodes[j,1])**2))
        return y
