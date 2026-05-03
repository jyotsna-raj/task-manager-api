import numpy as np
import matplotlib.pyplot as plt

X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([0,1,1,1])

w = np.array([1,1])
b = -0.5

def step(x): return 1 if x>=0 else 0

out = [step(np.dot(x,w)+b) for x in X]
print(out)

plt.scatter(X[:,0], X[:,1], c=y)

x = np.linspace(-0.5,1.5,100)
y_line = -(w[0]*x + b)/w[1]
plt.plot(x,y_line)

plt.show()
