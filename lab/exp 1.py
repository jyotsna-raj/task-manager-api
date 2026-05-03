import pandas as pd
from sklearn.preprocessing import StandardScaler, Normalizer

df = pd.read_csv("Iris.csv")

X = df.drop("Species", axis=1)

mean_removed = X - X.mean()

scaled = StandardScaler().fit_transform(X)
normalized = Normalizer().fit_transform(X)

print(mean_removed.head())
print(pd.DataFrame(scaled).head())
print(pd.DataFrame(normalized).head())
