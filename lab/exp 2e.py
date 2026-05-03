import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder


data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Overcast'],
    'Humidity': ['High', 'High', 'High', 'Normal', 'Normal', 'Normal'],
    'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Strong', 'Strong'],
    'PlayTennis': ['No', 'No', 'Yes', 'Yes', 'No', 'Yes']
}

df = pd.DataFrame(data)

le = LabelEncoder()
for col in df.columns:
    df[col] = le.fit_transform(df[col])

X = df[['Outlook', 'Humidity', 'Wind']]
y = df['PlayTennis']

model = DecisionTreeClassifier(criterion='entropy')
model.fit(X, y)

test = pd.DataFrame([[2, 1, 1]], columns=['Outlook', 'Humidity', 'Wind'])
result = model.predict(test)

if result[0] == 1:
    print("Yes You can go for Tennis")
else:
    print("No You cannot go for Tennis")
