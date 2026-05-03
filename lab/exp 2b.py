import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import seaborn as sn
from matplotlib import pyplot as plt

data = pd.read_csv("abcd.csv")

X = data.iloc[:, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]].values
y = data.iloc[:, 13].values


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=1
)

gnb = GaussianNB()
gnb.fit(X_train, y_train)

y_pred = gnb.predict(X_test)

accuracy = metrics.accuracy_score(y_test, y_pred) * 100
print("Classification Accuracy:", accuracy)

cm = metrics.confusion_matrix(y_test, y_pred)
print(cm)

plt.figure(figsize=(5, 4))
sn.heatmap(cm, annot=True)
plt.xlabel('Predicted Value')
plt.ylabel('Truth or Actual Value')
plt.show()
