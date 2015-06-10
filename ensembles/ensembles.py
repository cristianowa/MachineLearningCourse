import numpy as np
import matplotlib.pyplot as plt
from pylab import savefig
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import KFold
import statistics
#configs
n_classes = 3
plot_colors = "bry"
plot_step = 0.02

def plot(clf, X,y, name):
    # Plot the decision boundary
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, plot_step),
                         np.arange(y_min, y_max, plot_step))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    cs = plt.contourf(xx, yy, Z, cmap=plt.cm.Paired)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axis("tight")

    # Plot the training points
    for i, color in zip(range(n_classes), plot_colors):
        idx = np.where(y == i)
        plt.scatter(X[idx, 0], X[idx, 1], c=color, 
                    label=iris.target_names[i],
                    cmap=plt.cm.Paired)

    plt.axis("tight")
    plt.suptitle(name)
    plt.legend()
#    plt.show()
    savefig(name.replace(" ","_") , bbox_inches='tight')
    plt.close()
    return Z

clf_svm = svm.SVC(gamma=0.001, C=100.)
clf_nb = GaussianNB()
clf_dt = DecisionTreeClassifier()

class Voter:
    def __init__(self, predictors):
        self.predictors = predictors
    def fit(self, x, y):
        for p in self.predictors:
            p.fit(x,y)
    def predict(self, value):
        ans = []
        for p in self.predictors:
            ans.append(p.predict(value))
        final_ans = []
        for i in range(len(ans[0])):
            final = []
            for p in range(len(self.predictors)):
                final.append(ans[p][i])
            try:
                final_ans.append(statistics.mode(final))
            except:
                final_ans.append( ans[0][i])
        return np.array(final_ans)
cmatrix = {
"Naive Bayes" :[[0,0,0],[0,0,0],[0,0,0]], 
"Decision Tree" :[[0,0,0],[0,0,0],[0,0,0]],
"SVM" :[[0,0,0],[0,0,0],[0,0,0]],
"Voter" :[[0,0,0],[0,0,0],[0,0,0]],
}
def confusion_matrix(predicted, target,pred):
    matrix = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(len(target)):
        t = target[i]
        p = predicted[i]
        matrix[t][p] += 1
        cmatrix[pred][t][p] += 1
    return matrix
def print_cmatrix(matrix):
    print "       | 0     |     1 |     2 |" 
    for i in range(3):
            print "       | " + str(matrix[i][0]).rjust(5),
            print "| "        + str(matrix[i][1]).rjust(5),
            print "| "        + str(matrix[i][2]).rjust(5) + " |" 

voter = Voter([clf_svm, clf_dt, clf_nb])
predictors =  { 
    "Naive Bayes" :clf_nb,
    "Decision Tree": clf_dt,
    "SVM":clf_svm,
    "Voter":voter
    }

iris = datasets.load_iris()
X = iris.data[:, :2]
y = iris.target

def fold_validation(x,y,tx,ty,sufix):
    print " ======= " + sufix  + " =========== "
    for p in predictors:
        print p
        predictors[p].fit(x, y)
        z = plot(predictors[p], tx, ty, p  + "_" + sufix)
        m = confusion_matrix(predictors[p].predict(tx),ty, p)
        print_cmatrix(m)
def fold(X,Y,train, test):
    xx = []
    yy = []
    tx = []
    ty = []
    for i in train:
        xx.append(X[i].tolist())
        yy.append(Y[i].tolist())
    for i in test:
        tx.append(X[i].tolist())
        ty.append(Y[i].tolist())
    xx = np.array(xx)
    yy = np.array(yy)
    tx = np.array(tx)
    ty = np.array(ty)
    return xx, yy, tx, ty

kf =KFold(len(iris.data),10)
f = 0
for train, test in kf:
    xx, yy, tx, ty = fold(X,y, train, test)
    fold_validation(xx, yy, tx, ty, "fold_" + str(f))
    f += 1
print "========================"
for p in cmatrix:
    print p
    print_cmatrix(cmatrix[p])
#fold_validation(X,y, "all")
#fold_validation(xx,yy, "fold" + str(i))

