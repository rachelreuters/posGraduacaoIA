
import numpy
import pandas
import seaborn
from matplotlib import pyplot


iris = pandas.read_csv('datasets/iris.data', sep=',', decimal='.')

class Perceptron:
    a : float
    b : float

    def __init__(self, v1, v2):
        self.a = (v2[1] - v1[1])/(v2[0] - v1[0])
        self.b = v2[1] - self.a*v2[0]

    def score(self, x):
        return self.a*x+self.b
    
    def predict(self, x):
        return self.a*x[0]+self.b - x[1]
    

my_iris = 'Iris-versicolor'  #escolhida o tipo de flor
my_step = 0.1
perceptron_attributes = ['petallength', 'petalwidth']
v1 = (5.5, 1.5)
v2 = (4.0,2.0)

X = iris[perceptron_attributes].to_numpy()
Y = (iris['flower'] == my_iris).astype(float).to_numpy()

model = Perceptron(v1, v2)

x_n = numpy.arange(start=X[:, 0].min(), stop=X[:, 0].max(), step=my_step)
y_n = model.score(x_n)
my_flower = (4.0, 1.5) #flor que quero testar
y_p = model.predict(my_flower)

if y_p > 0:
    my_flower_color = 'green'
else:
    my_flower_color = 'red'


fig = pyplot.figure(figsize=(6, 6))
ax = fig.add_subplot(111)
_ = ax.scatter(X[Y == 1, 0], X[Y == 1, 1], s=250, label=my_iris, color='green', marker='*')
_ = ax.scatter(X[Y == 0, 0], X[Y == 0, 1], s=100, label='outras', color = 'red', marker='s')
_ = ax.plot(x_n, y_n, color='green', ls='--')
_ = ax.scatter([v1[0], v2[0]], [v1[1], v2[1]], s=250, label='suporte', color = 'green', marker='P')
_ = ax.scatter(my_flower[0], my_flower[1], s=250, label='minha flor', color = my_flower_color, marker = 'X')
_ = ax.set_xlim([0, 7])
_ = ax.set_ylim([0, 3])
_ = ax.legend()
_ = ax.grid(which='both', ls=':', alpha=0.5)
_ = ax.set_title('SCORE MINHA FLOR:{:.2f} LINHA: a:{:.2f} b:{:.2f}'.format(y_p, model.a, model.b), size=16)

pyplot.show()
print()