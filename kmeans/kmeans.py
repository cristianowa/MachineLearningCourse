from math import sqrt
import time
import matplotlib.pyplot as plt
from pylab import savefig
import numpy as np
def load_dist(filename):
    lines =  open(filename).read().split("\n")
    values = []
    for l in lines:
        v = l.split(" ")
        try:
            while "" in v:
                v.remove("")
        except:
            pass
        if (len(v)) == 2:
            values.append([float(v[0]), float(v[1])])
        else:
            print "ERROR in line[" + l + "]"
    return values
    
def distance(p1, p2):
    a = pow(p1[0] - p2[0], 2)
    b = pow(p1[1] - p2[1], 2)
    return sqrt(a + b)



class Kmean:
    """ this assumes values in two dimensions"""
    def __init__(self, values, classes = ["c1","c2"]):
        self.values = values
        self.groups = dict.fromkeys(classes,None)
        for k in self.groups: 
            self.groups[k] = { "points" :[], "mean": None , "centroid": None }
        self.centroids = False
        self.colors = ["red", "blue", "green"]
        self.minx = 9999
        self.maxx = -9999
        self.miny = 9999
        self.maxx = -9999
        for v in self.values:
            self.minx = min( self.minx , v[0])
            self.maxx = max( self.maxx , v[0])
            self.miny = min( self.miny , v[1])
            self.maxx = max( self.maxx , v[1])
    def plot(self, display = False, name = "plot.png"):
        c = 0
        for k in self.groups:
            x = []
            y = []
            for v in self.groups[k]["points"]:
                x.append(v[0])
                y.append(v[1])
            c += 1
            plt.scatter(x,y,c=self.colors[c])
        if display:
            plt.show()
        savefig(name, bbox_inches='tight')
        plt.close()
    def update_centroids(self):
        if not self.centroids:
            x = 0
            for k in self.groups:
                #This can be a liability if first values are the same
                self.groups[k]["centroid"] = self.values[x]
                x += 1
            self.centroids = True
            return True
        else:
            new_centroids = dict.fromkeys(self.groups.keys(),None)
            for k in self.groups:
                for v in self.values:
                    if distance(v, self.groups[k]["mean"]) < distance(self.groups[k]["centroid"], self.groups[k]["mean"]):
                        new_centroids[k] = v
            change = False
            for k in new_centroids:
                if  new_centroids[k] != None:
                    self.groups[k]["centroid"] = new_centroids[k]
                    change = True
            return change

    def assign_to_groups(self):
        for k in self.groups:
            self.groups[k]["points"] = []
        for v in self.values:
            group = self.groups.keys()[0]
            for k in self.groups:
                if distance(v, self.groups[k]["centroid"]) < distance(v, self.groups[group]["centroid"]):
                    group = k
            self.groups[group]["points"].append(v)
    def update_group_mean(self):
        for k in self.groups:
            acc = [0,0]
            count = 0
            for v in self.groups[k]["points"]:
                count += 1
                acc[0] += v[0]
                acc[1] += v[1]
            self.groups[k]["mean"] = [acc[0]/count, acc[1]/count]
    def run(self, plot = False, show = False):
        step = 0
        while self.update_centroids():
            self.assign_to_groups()
            self.update_group_mean()
            for k in self.groups:
                print "======================= STEP : " + str(step)
                step += 1
                print k
                print self.groups[k]["mean"]
                print self.groups[k]["centroid"]
                if plot:
                    self.plot(show, "kmean-step"+str(step).zfill(2)+".png")

if __name__ == "__main__":
    kmean = Kmean(load_dist("dist2.txt"))
    kmean.run(True) 
