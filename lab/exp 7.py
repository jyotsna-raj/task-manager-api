import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from hmmlearn import hmm

data = pd.read_csv("HistoricalQuotes.csv")
data.columns = data.columns.str.strip()

data['Close/Last'] = data['Close/Last'].replace(r'[\$,]', '', regex=True).astype(float)

data['Date'] = pd.to_datetime(data['Date'])
data = data.sort_values('Date')

data['Returns'] = data['Close/Last'].pct_change().dropna()
data = data.dropna()

X = data['Returns'].values.reshape(-1, 1)

model = hmm.GaussianHMM(n_components=2, n_iter=1000)
model.fit(X)

states = model.predict(X)
data['State'] = states

print(model.transmat_)

plt.scatter(data['Date'], data['Close/Last'], c=states)
plt.plot(data['Date'], data['Close/Last'], color='black', alpha=0.3)
plt.title("HMM States")
plt.show()
         
