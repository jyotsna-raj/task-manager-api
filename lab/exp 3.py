import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
from scipy.optimize import linear_sum_assignment

df = pd.read_csv("iris.csv")
X = StandardScaler().fit_transform(df.iloc[:, :-1])
y = LabelEncoder().fit_transform(df.iloc[:, -1])

kmeans = KMeans(n_clusters=len(np.unique(y)), random_state=42)
clusters = kmeans.fit_predict(X)

cm = confusion_matrix(y, clusters)
row, col = linear_sum_assignment(-cm)
mapping = dict(zip(col, row))
y_pred = np.vectorize(mapping.get)(clusters)

print("Accuracy:", accuracy_score(y, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y, y_pred))
print("\nCluster Centroids:\n", kmeans.cluster_centers_)

plt.scatter(X[:, 0], X[:, 1], c=clusters)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], marker='X', s=200)
plt.title("K-Means Clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()
