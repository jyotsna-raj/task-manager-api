import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier

X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([0,1,1,0])

model = MLPClassifier(hidden_layer_sizes=(2,), max_iter=1000)
model.fit(X, y)

print(model.predict(X))

xx, yy = np.meshgrid(np.linspace(-0.5,1.5,200), np.linspace(-0.5,1.5,200))
Z = model.predict(np.c_[xx.ravel(), yy.ravel()]).reshape(xx.shape)

plt.contourf(xx, yy, Z, alpha=0.5)
plt.scatter(X[:,0], X[:,1], c=y)
plt.show()
