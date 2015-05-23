from math import sqrt,pi,e
from scipy.stats import multivariate_normal
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
            values.append((float(v[0]), float(v[1])))
        else:
            print "ERROR in line[" + l + "]"
    return values
    
def distance(p1, p2):
    a = pow(p1[0] - p2[0], 2)
    b = pow(p1[1] - p2[1], 2)
    return sqrt(a + b)

def pdf_multivariate_gauss(x, mu, cov):
    assert(mu.shape[0] > mu.shape[1]), 'mu must be a row vector'
    assert(x.shape[0] > x.shape[1]), 'x must be a row vector'
    assert(cov.shape[0] == cov.shape[1]), 'covariance matrix must be square'
    assert(mu.shape[0] == cov.shape[0]), 'cov_mat and mu_vec must have the same dimensions'
    assert(mu.shape[0] == x.shape[0]), 'mu and x must have the same dimensions'

    part1 = 1 / ( ((2* np.pi)**(len(mu)/2)) * (np.linalg.det(cov)**(1/2)) )
    part2 = (-1/2) * ((x-mu).T.dot(np.linalg.inv(cov))).dot((x-mu))
    return float(part1 * np.exp(part2))

classes = ["c1","c2"]

class Kmean:
    """ this assumes values in two dimensions"""
    def __init__(self, values, classes = classes):
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
            plt.scatter(self.groups[k]["mean"][0], self.groups[k]["mean"][1],  marker='x', c= self.colors[c])
            plt.scatter(self.groups[k]["centroid"][0], self.groups[k]["centroid"][1],  marker='v', c= self.colors[c])
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
    def getCentroids(self):
        centroids = dict.fromkeys(self.groups.keys(), None)
        for k in self.groups: 
            centroids[k] = self.groups[k]["centroid"] 
        return centroids
    def getValues(self):
        data = {}
        for k in self.groups:
            for v in self.groups[k]["points"]:
                data[v] = k
        return data


class EM:
    """designed for work with only two classes"""
    def __init__(self, values, means):
        #uma media para cada classe
       self.means = means
       self.covar = {"c1":[[1,0],[0,1]], "c2":[[1,0],[0,1 ]]}
       self.mixture = { "c1": 0.5, "c2":0.5 }
       self.values = dict.fromkeys(values.keys(), None)
       for v in self.values:
            self.values[v] = {"gamma":{"c1":0, "c2":0 }, "class":"none"}
            self.values[v]["gamma"][values[v]] = 1
    def plot(self, display = False, name = "plot.png"):
       c = 0
       for v in self.values:
           x = []
           y = []
           for k in classes:
                 
               x.append(v[0])
               y.append(v[1])
               c += 1
               plt.scatter(x,y,c=self.colors[c])
       if display:
           plt.show()
       savefig(name, bbox_inches='tight')
       plt.close()
    def N(self, x, u, z ):
        xx = np.array([[x[0]],[x[1]]])
        uu = np.array([[u[0]],[u[1]]])
        zz = np.array(z)
        return pdf_multivariate_gauss(xx, uu, zz) 
    def gamma(self, n):
        partGamma = {}
        accGamma = 0.0
        for k in classes:
            partGamma[k] = self.mixture[k]*self.N(n, self.means[k], self.covar[k])
            accGamma += partGamma[k]
        for k in classes:
            partGamma[k] /= accGamma
        return partGamma
    def E(self):
        for v in self.values:
            self.values[v]["gamma"] = self.gamma(v)
            if self.values[v]["gamma"]["c1"] > self.values[v]["gamma"]["c2"]:
                self.values[v]["class"] = "c1"
            else:
                self.values[v]["class"] = "c2"
    def new_covar(self, k, u_n_k, cnt_k):
        summ = np.zeros([2,2])
        for v in self.values:
            x = np.array([[v[0]],[v[1]]])
            u = np.array([[u_n_k[0]],[u_n_k[1]]])
            tmp = x -u
            tmp = np.multiply(tmp, tmp.transpose())
            tmp *= self.values[v]["gamma"][k]
            summ += tmp
        return summ / cnt_k
    def M(self):
        count = dict.fromkeys(classes, 0.0)
        accGamma = dict.fromkeys(classes, (0.0,0.0))
        for v in self.values:
            for k in classes:
                if self.values[v]["class"]:
                    count[k] += self.values[v]["gamma"][k]
                    new_gamma = (accGamma[k][0] + self.values[v]["gamma"][k]*v[0], accGamma[k][1] + self.values[v]["gamma"][k]*v[1])
                    accGamma[k] = new_gamma
        for k in classes:
            self.means[k] = (accGamma[k][0]/count[k], accGamma[k][0]/count[k])
            self.covar[k] = self.new_covar(k,  self.means[k],  count[k])
            self.mixture[k] = float(count[k])/len(self.values)
            
    def convergence(self):
        pass
    def run(self):
#        while not self.convergence():
         self.E()
         self.M()

if __name__ == "__main__":
    values = load_dist("dist2.txt")
    kmean = Kmean(values)
    kmean.run(True) 
    kcentre = kmean.getCentroids()
    kvalues = kmean.getValues()
    em = EM(kvalues, kcentre)
    print kcentre
    em.run()
